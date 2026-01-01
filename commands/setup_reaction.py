from highrise import BaseBot, User
import asyncio
from utils.chat_wrapper import wrap_on_chat  # ✅ برای جلوگیری از تداخل با دکوراتورهای دیگه

def setup_reaction(cls):
    async def on_chat(self: BaseBot, user: User, message: str):
        if message.startswith("/heart"):
            parts = message.split()
            
            # 🔹 اگر فقط /heart زده شده یا دستور ناقصه، راهنمایی بده
            if len(parts) < 2 or not parts[1].startswith("@"):
                await self.highrise.send_whisper(
                    user.id,
                    "/heart @id (number of send = deafult = 1) min 1 | 100 "
                )
                return

            username = parts[1][1:]  # حذف @ از ابتدای نام کاربری

            # تعیین تعداد ری‌اکشن‌ها
            heart_count = 1  # مقدار پیش‌فرض
            if len(parts) >= 3:
                try:
                    heart_count = int(parts[2])
                    if heart_count < 1:
                        heart_count = 1
                    elif heart_count > 100:
                        heart_count = 100
                except ValueError:
                    heart_count = 1  # اگر عدد نبود، پیش‌فرض 1

            try:
                room_users = (await self.highrise.get_room_users()).content
                target_user = next(
                    (u for u, _ in room_users if u.username == username),
                    None
                )

                if not target_user:
                    await self.highrise.send_whisper(user.id, f"❌ کاربری با نام @{username} در اتاق پیدا نشد.")
                    return

                # 🔹 فقط به فرستنده پیام وضعیت ارسال را نشان بده
                await self.highrise.send_whisper(user.id, f"💘 در حال ارسال {heart_count} ری‌اکشن قلب برای @{username} ...")

                for _ in range(heart_count):
                    await self.highrise.react("heart", target_user.id)
                    await asyncio.sleep(0.002)

                await self.highrise.send_whisper(user.id, "✅ ری‌اکشن‌ها با موفقیت ارسال شدند!")

            except Exception as e:
                await self.highrise.send_whisper(user.id, f"❌ خطا در ارسال ری‌اکشن: {e}")

    return wrap_on_chat(cls, on_chat)
