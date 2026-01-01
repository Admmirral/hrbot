import asyncio
from highrise import *
from highrise.models import *
from modules.setup_equip import setup_equip
from commands.setup_follow import setup_follow
from commands.setup_reaction import setup_reaction
from modules.setup_emote import setup_bot, emote_dict 
   # ✅ برای گرفتن duration ایموت‌ها


@setup_equip
@setup_follow
@setup_reaction
@setup_bot
class Bot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("[START] Bot started successfully!")
        self.highrise = self.highrise
        self.bot_id = "681331b082112207bfdea247"

        # 📍 مکان اولیه بات
        await self.highrise.walk_to(Position(17.5, 0.0, 11.5, facing="FrontRight"))

        # 📍 شروع ایموت لوپ روی خود بات (laidback)
        asyncio.create_task(self.loop_self_emote("laidback"))

    async def loop_self_emote(self, emote_name: str):
        """ایموت مشخص‌شده رو روی خود بات لوپ کنه"""
        if emote_name not in emote_dict:
            print(f"❌ ایموت '{emote_name}' پیدا نشد.")
            return

        emote_code, emote_duration = emote_dict[emote_name]
        while True:
            try:
                await self.highrise.send_emote(emote_code, self.bot_id)
                await asyncio.sleep(emote_duration)
            except Exception as e:
                print(f"⚠️ خطا در لوپ ایموت: {e}")
                await asyncio.sleep(2)  # جلوگیری از اسپم خطا

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            print(f"User object: {user}")
            print(f"User ID: {user.id}")

            # ✅ فقط خوشامد (بدون هیچ ایموتی روی کاربر)
            welcome_message = (
                f"سلام, {user.username} خوش اومدی 🌹 "
                f"فعلاً {len(emote_dict)} تا ایموت موجوده، امیدوارم خوش بگذره! 🔥"
            )
            await self.highrise.send_whisper(user.id, welcome_message)

        except Exception as e:
            print(f"Error sending welcome message: {e}")
