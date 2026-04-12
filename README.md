# PatchPyro

A fork of pyromod (renamed as patchpyro) providing conversation patches for Pyrogram-based clients.

## Requirements
```text
kurigram>=2.0.69
python>=3.9
```

## Installation
```bash
pip install patchpyro
```
 
## Usage
Import `patchpyro` at least once in your script so you can use the modified Pyrogram in all files of the same process. 

### Example
```python
# config.py
from patchpyro import listen # or import patchpyro.listen
from pyrogram import Client

listen.thank() # use this if your linter/IDE flags patchpyro as an unused import.

mybot = Client("mysession")
```

```python
# any other .py
from config import mybot
# no need to import patchpyro again; Pyrogram is already monkeypatched globally (in the same process)
```

## Available Methods
Just importing `patchpyro.listen` will automatically do the monkeypatch and you'll get these new methods:

### `Chat.listen`, `User.listen`
- `await mybot.listen(chat_id, filters=None, timeout=30)`
- Awaits a new message in the specified chat and returns it.
- Raises `asyncio.TimeoutError` if timeout (optional parameter) occurs.
- You can pass Update Filters to the filters parameter just like you do for the update handlers.
  - E.g. `filters=filters.photo & filters.bot`

### `Chat.ask`, `User.ask`
- `await mybot.ask(text, chat_id, filters=None, timeout=30)`
- Same as `.listen()` above, but sends a message before awaiting.
- You can pass custom parameters to its internal `send_message()` call. Check the example below.
    
### `Chat.asker`, `User.asker`
- `await mybot.asker(chat_id, filters=None, timeout=36)` 
- Same as `.listen()` but `.asker()` returns `None` instead of raising `asyncio.TimeoutError`.
- Useful for graceful timeout handling, `.asker()` has a default timeout of 2 minutes (adjustable via `timeout` argument).

## Examples

### `asker()`
```python
# ...
    sendx = await client.send_message(chat_id, "`Send me your name:`")
    answer = await client.asker(chat_id, filters=None, timeout=60)
    if not answer: # `None` if timeout reached with no reply.
        return await sendx.reply_text("How long should I wait? Bye!")
    await answer.reply_text(f"{answer.text}, That's a cool name!")
# ...
```

### `ask()`
```python
# ...
    answer = await client.ask(chat_id, '*Send me your name:*', parse_mode=enums.ParseMode.MARKDOWN)
    await client.send_message(chat_id, f'Your name is: {answer.text}')
# ...
```

## Copyright & License
This project includes code from:
- **[kurimod](https://github.com/ohmyarthur/kurimod)**: Monkeypatcher logic and modern async compatibility fixes.
- **Pyrogram**: Telegram MTProto API Client Library for Python. Copyright (C) 2017-2022 Dan <<https://github.com/delivrance>>
- **pyromod**: Original conversation patch logic.

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
