
def wrap_on_chat(cls, new_on_chat):
    old_on_chat = getattr(cls, "on_chat", None)

    if old_on_chat is None:
        cls.on_chat = new_on_chat
    else:
        async def combined_on_chat(self, user, message):
            await old_on_chat(self, user, message)
            await new_on_chat(self, user, message)
        cls.on_chat = combined_on_chat

    return cls
