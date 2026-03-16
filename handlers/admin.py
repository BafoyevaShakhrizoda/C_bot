from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import ADMIN_IDS
from keyboards import admin_keyboard
from database import get_all_applications, get_application_count

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS



@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q.")
        return

    count = await get_application_count()
    await message.answer(
        f"🔐 <b>Admin panel</b>\n\n"
        f"📊 Jami arizalar: <b>{count}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard(),
    )



@router.callback_query(F.data == "admin_list")
async def admin_list(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return

    apps = await get_all_applications()
    if not apps:
        await callback.answer("Hozircha ariza yo'q.", show_alert=True)
        return

  
    for app in apps[:10]:
        username = f"@{app['username']}" if app['username'] else "—"
        text = (
            f"🆔 <b>Ariza #{app['id']}</b> | {app['created_at'][:16]}\n"
            f"👤 {app['full_name']}\n"
            f"📱 {app['phone']}\n"
            f"🎯 {app['direction']}\n"
            f"💻 {app['technologies']}\n"
            f"🔗 {app['portfolio']}\n"
            f"✈️ {username}"
        )
        await callback.message.answer(text, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q", show_alert=True)
        return

    apps = await get_all_applications()
    total = len(apps)

    if total == 0:
        await callback.answer("Hozircha ariza yo'q.", show_alert=True)
        return

    direction_counts: dict = {}
    for app in apps:
        d = app["direction"]
        direction_counts[d] = direction_counts.get(d, 0) + 1

    stats_text = f"📊 <b>Statistika</b>\n\nJami arizalar: <b>{total}</b>\n\n<b>Yo'nalishlar bo'yicha:</b>\n"
    for direction, count in sorted(direction_counts.items(), key=lambda x: -x[1]):
        bar = "▓" * count + "░" * (total - count)
        stats_text += f"• {direction}: <b>{count}</b>\n"

    await callback.message.answer(stats_text, parse_mode="HTML")
    await callback.answer()
