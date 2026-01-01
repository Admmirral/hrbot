from highrise import *
from highrise.models import *
from utils.chat_wrapper import wrap_on_chat

OWNER_ID = "689b031cbdb1f4d383a0ab8c"  # 👈 آیدی خودتو اینجا بذار

OWNER_ID = "689b031cbdb1f4d383a0ab8c"  # آیدی خودتو اینجا بذار

def setup_equip(cls):
    async def on_chat(self, user, message):
        if message.lower().startswith("/equip"):
            if user.id != OWNER_ID:
                await self.highrise.send_whisper(user.id, "شما اجازه استفاده از این فرمان را ندارید.")
                return

            body_color = 2
            hair_color = 0

            if "body_color" in message:
                try:
                    body_color = int(message.split("body_color:")[1].split()[0])
                except Exception:
                    pass

            if "hair_color" in message:
                try:
                    hair_color = int(message.split("hair_color:")[1].split()[0])
                except Exception:
                    pass

            await self.highrise.set_outfit(outfit=[
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=body_color),
                Item(type='clothing', amount=1, id='eye-n_basic2018femaleround', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows07', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='mouth-n_basic2018toothythinround', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shirt-n_2016fallblackkknottedtee', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='skirt-n_room22019skirtwithsocksplaid', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019hightopsblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_basic2020overshoulderstraightbangs', account_bound=False, active_palette=hair_color),
                Item(type='clothing', amount=1, id='hair_back-n_basic2020overshoulderstraightbangs', account_bound=False, active_palette=hair_color),
            ])
            await self.highrise.send_whisper(user.id, f"لباس‌ها تنظیم شدند با رنگ‌های جدید (بدن: {body_color}, مو: {hair_color}) ✅")

    # حالا از wrap_on_chat استفاده می‌کنیم که on_chat جدید رو به on_chat قبلی متصل کنه
    return wrap_on_chat(cls, on_chat)
