"""Composition and polling loop for the independent V2 development bot."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from threading import Event
from time import sleep
from typing import Iterable, Mapping

from rom_v2.infrastructure.telegram.bot_api import TelegramBotApi, TelegramTransportError
from rom_v2.presentation.development_shell import ShellView, route_shell_action
from rom_v2.presentation.registration_flow import TelegramRegistrationFlow
from rom_v2.presentation.profile_flow import TelegramProfileFlow
from rom_v2.presentation.character_reset_flow import TelegramCharacterResetFlow

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DevelopmentBotConfig:
    """Runtime-only configuration for the isolated Telegram shell."""

    token: str
    allowed_user_ids: frozenset[int]
    poll_timeout_seconds: int = 20
    transport_retry_seconds: float = 2.0

    def __post_init__(self) -> None:
        if not str(self.token or "").strip():
            raise ValueError("token must not be empty")
        if self.poll_timeout_seconds < 0:
            raise ValueError("poll_timeout_seconds must not be negative")


class IndependentDevelopmentBot:
    """Own the shell polling lifecycle without owning gameplay or durable state."""

    def __init__(self, config: DevelopmentBotConfig, api: TelegramBotApi | None = None, registration_flow: TelegramRegistrationFlow | None = None, profile_flow: TelegramProfileFlow | None = None, reset_flow: TelegramCharacterResetFlow | None = None) -> None:
        self._config = config
        self._api = api or TelegramBotApi(config.token)
        self._stop = Event()
        self._registration_flow = registration_flow
        self._profile_flow = profile_flow
        self._reset_flow = reset_flow

    def stop(self) -> None:
        """Request graceful termination after the current Telegram request."""
        self._stop.set()

    def _authorized(self, user_id: int) -> bool:
        return not self._config.allowed_user_ids or int(user_id) in self._config.allowed_user_ids

    def _send_view(self, chat_id: int, view: ShellView) -> None:
        self._api.send_message(chat_id, view.text, reply_markup=view.reply_markup)

    def handle_update(self, update: Mapping[str, object]) -> None:
        """Parse one update, authorize first, and render only shell actions."""
        message = update.get("message")
        callback = update.get("callback_query")
        if isinstance(message, Mapping):
            sender = message.get("from")
            chat = message.get("chat")
            if not isinstance(sender, Mapping) or not isinstance(chat, Mapping):
                return
            user_id = int(sender.get("id", 0) or 0)
            chat_id = int(chat.get("id", 0) or 0)
            if not user_id or not chat_id or not self._authorized(user_id):
                return
            text = str(message.get("text", "") or "").strip()
            if text.startswith("/start"):
                if self._profile_flow is not None and self._profile_flow.has_profile(user_id):
                    self._send_view(chat_id, route_shell_action("/start"))
                elif self._registration_flow is not None:
                    self._send_view(chat_id, self._registration_flow.start(user_id))
                else:
                    self._send_view(chat_id, route_shell_action("/start"))
            elif self._registration_flow is not None:
                view = self._registration_flow.message(user_id, text)
                if view is not None:
                    self._send_view(chat_id, view)
            elif text.startswith("/start"):
                self._send_view(chat_id, route_shell_action("/start"))
            return
        if isinstance(callback, Mapping):
            sender = callback.get("from")
            origin = callback.get("message")
            if not isinstance(sender, Mapping) or not isinstance(origin, Mapping):
                return
            chat = origin.get("chat")
            if not isinstance(chat, Mapping):
                return
            user_id = int(sender.get("id", 0) or 0)
            chat_id = int(chat.get("id", 0) or 0)
            if not user_id or not chat_id or not self._authorized(user_id):
                return
            callback_id = str(callback.get("id", "") or "").strip()
            if callback_id:
                self._api.answer_callback_query(callback_id)
            data = str(callback.get("data", "") or "")
            if self._reset_flow is not None:
                reset_view = self._reset_flow.callback(user_id, data)
                if reset_view is not None:
                    self._send_view(chat_id, reset_view)
                    return
            if self._profile_flow is not None:
                profile_view = self._profile_flow.callback(user_id, data)
                if profile_view is not None:
                    self._send_view(chat_id, profile_view)
                    return
            if self._registration_flow is not None and data.startswith("v2:register:"):
                view = self._registration_flow.callback(user_id, data)
                if view is not None:
                    self._send_view(chat_id, view)
            else:
                self._send_view(chat_id, route_shell_action(data))

    def run(self) -> None:
        """Run one stoppable long-polling loop owned only by the V2 process."""
        offset: int | None = None
        while not self._stop.is_set():
            try:
                response = self._api.get_updates(offset=offset, timeout=self._config.poll_timeout_seconds)
            except TelegramTransportError as error:
                LOGGER.warning("V2 Telegram transport retry: %s", error)
                if self._config.transport_retry_seconds:
                    sleep(self._config.transport_retry_seconds)
                continue
            updates = response.result if isinstance(response.result, list) else []
            for update in updates:
                if not isinstance(update, Mapping):
                    continue
                update_id = int(update.get("update_id", 0) or 0)
                if update_id:
                    offset = update_id + 1
                self.handle_update(update)


def build_development_bot(token: str, allowed_user_ids: Iterable[int] = ()) -> IndependentDevelopmentBot:
    """Compose the independent shell from transport and presentation owners."""
    config = DevelopmentBotConfig(
        token=str(token),
        allowed_user_ids=frozenset(int(value) for value in allowed_user_ids),
    )
    return IndependentDevelopmentBot(config)
