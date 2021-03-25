# PatchPyro
### This is a fork of pyromod (renamed as patchpyro) for personal usecases.

### Remember that this fork contains only conversation patch.

# Requirements:
 ~~~python
 pyrogram>=2.0.69
 python>=3.9
 ~~~

 # Installation:
```
python -m pip install patchpyro
```
 
# Usage:
Import `patchpyro` at least one time in your script, so you'll be able to use modified pyrogram in all files of the same proccess. 
Example:

```python
# config.py
from patchpyro import listen # or import patchpyro.listen
from pyrogram import Client

mybot = Client("mysession")
```

```python
# any other .py
from config import mybot
# no need to import patchpyro again pyrogram is already monkeypatched globally (at the same proccess)
```

## `patchpyro.listen`
Just import it, it will automatically do the monkeypatch and you'll get these new methods:

- Available bound methods::
  - `Chat.listen, User.listen`

    - `await mybot.listen(chat_id, filters=None, timeout=30)`
    - raises `asyncio.TimeoutError` if timeout (optional parameter)
    - Awaits for a new message in the specified chat and returns it.
    - You can pass Update Filters to the filters parameter just like you do for the update handlers.
    - E.g. `filters=filters.photo & filters.bot`
  - `Chat.ask, User.ask`

    - `await mybot.ask(text, chat_id, filters=None, timeout=30)`
    - Same of `.listen()` above, but sends a message before awaiting.
    - You can pass custom parameters to its send_message() call. Check the example below.
    
  - `Chat.asker, User.asker`
     - `await mybot.asker(chat_id, filters=None, timeout=36)` 
     - same as `.listen()` but `.asker()` returns `None` instead of raising `asyncio.TimeoutError`.
     - Found useful in some cases for me, `.asker()` has a default timeout of 2 minutes. 
     - You can adjust it by passing as a argument. Refer the example code given below.

# Examples:
### For .asker():
```python
...
    sendx = await client.send_message(chat_id, "`Send me your name:`")
    answer = await client.asker(chat_id, filters=None, timeout=60)
    if not answer: # `None` if timeout if no reply received.
        return await sendx.reply_text("How long should I wait?, Eh! Bye!")
    await answer.reply_text(f"{answer.text}, That's a cool name!")
...
```
### For .ask():
```python
...
    answer = await client.ask(chat_id, '*Send me your name:*', parse_mode='Markdown')
    await client.send_message(chat_id, f'Your name is: {answer.text}')
...
```


### Copyright & License
This project may include snippets of Pyrogram code
- Pyrogram - Telegram MTProto API Client Library for Python. Copyright (C) 2017-2022 Dan <<https://github.com/delivrance>>

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
