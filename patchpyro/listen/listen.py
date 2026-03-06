"""patchpyro - A monkeypatcher add-on for Pyrogram
Copyright (C) 2026 Aditya Prasad S <https://github.com/adityaprasad502>.

This file is part of patchpyro and was forked from usernein/pyromod.
Additional patching logic was adapted from kurimod (C) Dias Arthur.

patchpyro is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

patchpyro is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with patchpyro.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import functools
from contextlib import suppress
from inspect import iscoroutinefunction

import pyrogram
import pyrogram.client
import pyrogram.handlers.message_handler
import pyrogram.types.user_and_chats.chat
import pyrogram.types.user_and_chats.user

from patchpyro.utils import patch_into, should_patch


class ListenerCanceled(Exception):
    pass


pyrogram.errors.ListenerCanceled = ListenerCanceled


@patch_into(pyrogram.client.Client)
class Client:
    @should_patch()
    def __init__(self, *args, **kwargs) -> None:
        self.listening = {}
        self.using_mod = True

        self.old__init__(*args, **kwargs)

    @should_patch()
    async def listen(
        self,
        chat_id: int | str,
        filters: pyrogram.filters.Filter | None = None,
        timeout: int | None = None,
    ) -> pyrogram.types.Message:
        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        # Cancel existing listener in this chat if any
        self.cancel_listener(chat_id)

        loop = asyncio.get_running_loop()
        future = loop.create_future()
        future.add_done_callback(functools.partial(self.clear_listener, chat_id))
        self.listening[chat_id] = {"future": future, "filters": filters}

        return await asyncio.wait_for(future, timeout)

    @should_patch()
    async def ask(
        self,
        chat_id: int | str,
        text: str,
        filters: pyrogram.filters.Filter | None = None,
        timeout: int | None = None,
        *args,
        **kwargs,
    ) -> pyrogram.types.Message:
        request = await self.send_message(chat_id, text, *args, **kwargs)
        response = await self.listen(chat_id, filters, timeout)
        response.request = request
        return response

    @should_patch()
    async def asker(
        self,
        chat_id: int | str,
        filters: pyrogram.filters.Filter | None = None,
        timeout: int = 119,
    ) -> pyrogram.types.Message | None:
        try:
            return await self.listen(chat_id, filters, timeout)
        except asyncio.TimeoutError:
            return None

    @should_patch()
    def clear_listener(self, chat_id: int, future: asyncio.Future) -> None:
        with suppress(KeyError):
            if (
                chat_id in self.listening
                and future == self.listening[chat_id]["future"]
            ):
                self.listening.pop(chat_id, None)

    @should_patch()
    def cancel_listener(self, chat_id: int) -> None:
        listener = self.listening.get(chat_id)
        if not listener or listener["future"].done():
            return

        if not listener["future"].done():
            listener["future"].set_exception(ListenerCanceled())
        self.clear_listener(chat_id, listener["future"])


@patch_into(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler:
    @should_patch()
    def __init__(self, callback: callable, filters=None) -> None:
        self.user_callback = callback
        self.old__init__(self.resolve_listener, filters)

    @should_patch()
    async def resolve_listener(self, client: "pyrogram.Client", message: pyrogram.types.Message, *args) -> None:
        listener = client.listening.get(message.chat.id)
        if listener and not listener["future"].done():
            listener["future"].set_result(message)
            raise pyrogram.StopPropagation

        if listener and listener["future"].done():
            client.clear_listener(message.chat.id, listener["future"])

        await self.user_callback(client, message, *args)

    @should_patch()
    async def check(self, client: "pyrogram.Client", update: pyrogram.types.Message):
        listener = client.listening.get(update.chat.id)

        if listener and not listener["future"].done():
            filters = listener["filters"]
            if callable(filters):
                if iscoroutinefunction(filters.__call__):
                    return await filters(client, update)
                loop = asyncio.get_running_loop()
                return await loop.run_in_executor(None, filters, client, update)
            return True

        if callable(self.filters):
            if iscoroutinefunction(self.filters.__call__):
                return await self.filters(client, update)
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self.filters, client, update)
        return True


@patch_into(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.Chat):
    @should_patch()
    async def listen(self, *args, **kwargs) -> pyrogram.types.Message:
        return await self._client.listen(self.id, *args, **kwargs)

    @should_patch()
    async def ask(self, *args, **kwargs) -> pyrogram.types.Message:
        return await self._client.ask(self.id, *args, **kwargs)

    @should_patch()
    def cancel_listener(self) -> None:
        return self._client.cancel_listener(self.id)


@patch_into(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.User):
    @should_patch()
    async def listen(self, *args, **kwargs) -> pyrogram.types.Message:
        return await self._client.listen(self.id, *args, **kwargs)

    @should_patch()
    async def ask(self, *args, **kwargs) -> pyrogram.types.Message:
        return await self._client.ask(self.id, *args, **kwargs)

    @should_patch()
    def cancel_listener(self) -> None:
        return self._client.cancel_listener(self.id)
