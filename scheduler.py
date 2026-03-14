import random
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import get_all_users
from stickers import BLESSING_STICKERS

logger = logging.getLogger(__name__)

async def send_blessing(bot: Bot, chat_id: int):
    blessing_messages = [
        "✨ Вы получили благословение от свинки! 🐖💖\nПусть ваш день будет чудесным! 🌸☀️",
        "🐽 Свинка шлет вам свои лучи добра! 🌞\nУдачного и легкого дня! 🍀✨",
        "💖 Сегодня свинка особенно благосклонна к вам!\nЛовите порцию розового счастья! 🌸🐷",
        "☀️ Хрю-хрю! Ваше утреннее благословение доставлено! 🎁✨\nУлыбнитесь и покоряйте этот мир! 🐖👑",
        "🍀 Свинка помахала вам хвостиком на удачу! 🐾\nПусть всё задуманное сегодня сбудется! 🌟",
        "🐷 Доброе утро! Свинка дарит вам заряд позитива на весь день! 🔋💖\nВы справитесь со всем! 💪✨",
        "🎀 Розовое облачко счастья уже летит к вам! ☁️🐖\nПусть этот день принесет только радость! 🎈",
        "🌸 Свинка чихнула на удачу! 🤧💖\nГотовьтесь к чудесам и хорошим новостям сегодня! 💌✨",
        "💫 Свинка-волшебница посылает вам магию хорошего настроения! 🪄🐖\nСияйте ярче всех! ✨💖",
        "🐽 Хрю! Свинка просит передать, что вы сегодня выглядите великолепно! 🥰\nЧудесного вам дня! ☀️✨",
        "🌸 Утренняя свинка желает вам море улыбок! 🌊💖\nПусть этот день будет мягким, как розовое пузико! 🐖",
        "🐽 Свинка принесла вам букет хорошего настроения! 💐✨\nНаслаждайтесь каждой минутой сегодня! ☀️",
        "💖 Свинка-купидон зарядила этот день любовью и радостью! 💘🐖\nПусть все получается легко и играючи! 🎯",
        "🌟 Звездная свинка предсказывает вам грандиозный успех! 🌠🐷\nСмело идите вперед, вы супер! 🚀✨",
        "🎀 Эта маленькая свинка верит в вас! 🥺💖\nПусть сегодняшний день принесет только приятные сюрпризы! 🎁",
        "🧁 Сладкая свинка желает вам такого же вкусного и классного дня! 🍩🐖\nБольше радостей и меньше забот! 🎈",
        "🍀 Волшебный пятачок приносит удачу каждому, кто это читает! 🐽✨\nЛовите свой счастливый билет на сегодня! 🎫💖",
        "👑 Королевская свинка благословляет вас на великие дела! 🐖✨\nПусть день пройдет по самому лучшему сценарию! 📜🌟",
        "🎈 Свинка надула для вас шарик веселого настроения! 🐖🎈\nЛегкости, уюта и самых добрых новостей! ☁️✨",
        "💌 Вам письмо! ✉️ От кого? От самой милой свинки! 🐖💖\nВнутри сказано, что сегодня ваш день! Наслаждайтесь! 🌸☀️"
    ]
    try:
        sticker_id = random.choice(BLESSING_STICKERS)
        msg_text = random.choice(blessing_messages)
        await bot.send_message(chat_id, msg_text)
        await bot.send_sticker(chat_id, sticker_id)
    except Exception as e:
        logger.error(f"Failed to send blessing to {chat_id}: {e}")

async def schedule_daily_blessings(bot: Bot, scheduler: AsyncIOScheduler):
    users = await get_all_users()
    logger.info(f"Scheduling blessings for {len(users)} users.")
    
    now = datetime.now()
    # If we want to schedule for today morning (useful if ran at midnight)
    # We pick a time between 08:00 and 12:00
    for user in users:
        # Random hours between 8 and 11, random minutes between 0 and 59
        random_hour = random.randint(8, 11)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        
        run_time = now.replace(hour=random_hour, minute=random_minute, second=random_second, microsecond=0)
        
        # If the generated time is already in the past (e.g., bot started late in the day)
        # we skip scheduling for today or schedule it for tomorrow. For simplicity, we schedule it for tomorrow.
        if run_time < now:
            run_time = run_time + timedelta(days=1)
            
        scheduler.add_job(
            send_blessing,
            'date',
            run_date=run_time,
            kwargs={'bot': bot, 'chat_id': user['chat_id']},
            id=f"blessing_{user['user_id']}",
            replace_existing=True
        )
        logger.info(f"Scheduled blessing for chat {user['chat_id']} at {run_time}")

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    # Runs the planning logic every day at 00:00
    scheduler.add_job(
        schedule_daily_blessings,
        'cron',
        hour=0,
        minute=0,
        kwargs={'bot': bot, 'scheduler': scheduler}
    )
    return scheduler

