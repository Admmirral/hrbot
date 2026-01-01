from highrise import BaseBot, Position, AnchorPosition, User
from highrise.models import *
import asyncio
from utils.chat_wrapper import wrap_on_chat  # مهم

# ✅ لیست آیدی‌های مجاز برای استفاده از دستور follow و stop
ALLOWED_USERS = {
    "689b031cbdb1f4d383a0ab8c",  # آیدی خودت  # آیدی بات (مثال)  # آیدی دوستت (مثال)
    "6842d71152a75d44a4d1b952",  # هر چندتا بخوای اضافه کن
}

def setup_follow(cls):
    async def on_chat(self: BaseBot, user: User, message: str):
        # فقط اجازه استفاده به یوزرهای داخل لیست
        if message.startswith("/follow") or message.startswith("/stop"):
            if user.id not in ALLOWED_USERS:
                await self.highrise.send_whisper(user.id, "❌ شما اجازه استفاده از این دستور را ندارید.")
                return

        if message.startswith("/follow"):
            await follow(self, user)
        elif message.startswith("/stop"):
            await stop(self, user)

    return wrap_on_chat(cls, on_chat)  # ✅ ترکیب امن با سایر setupها

async def follow(self: BaseBot, user: User) -> None:
    async def following_loop():
        while True:
            room_users = (await self.highrise.get_room_users()).content
            user_position = next((pos for u, pos in room_users if u.id == user.id), None)

            if user_position and not isinstance(user_position, AnchorPosition):
                await self.highrise.walk_to(
                    Position(user_position.x + 1, user_position.y, user_position.z)
                )

            await asyncio.sleep(0.5)

    taskgroup = self.highrise.tg
    if any(t.get_name() == "following_loop" for t in taskgroup._tasks):
        await self.highrise.chat("❗ همین الان دارم دنبال یه نفر می‌رم.")
        return

    task = taskgroup.create_task(following_loop())
    task.set_name("following_loop")
    await self.highrise.chat(f"👣 دنبال {user.username} افتادم!")

async def stop(self: BaseBot, user: User) -> None:
    taskgroup = self.highrise.tg
    for task in list(taskgroup._tasks):
        if task.get_name() == "following_loop":
            task.cancel()
            await self.highrise.chat(f"🛑 دنبال کردن {user.username} رو قطع کردم.")
            return

    await self.highrise.chat("❌ کسی رو دنبال نمی‌کنم که بخوام متوقف کنم.")
