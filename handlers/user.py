from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from states import ApplicationForm
from keyboards import (
    start_keyboard, direction_keyboard,
    phone_keyboard, remove_keyboard, confirm_keyboard
)

router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Bu bot orqali <b>amaliyot arizasi</b> topshirishingiz mumkin.\n\n"
        "Ariza to'ldirish uchun quyidagi tugmani bosing 👇",
        parse_mode="HTML",
        reply_markup=start_keyboard(),
    )



@router.callback_query(F.data == "start_application")
async def begin_application(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 Ariza boshlandi!\n\n"
        "<b>1/5</b> — Ism va familiyangizni kiriting:\n"
        "<i>Masalan: Ali Valiyev</i>",
        parse_mode="HTML",
    )
    await state.set_state(ApplicationForm.full_name)
    await callback.answer()


@router.callback_query(F.data == "restart_application")
async def restart_application(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🔄 Ariza qayta boshlandi.\n\n"
        "<b>1/5</b> — Ism va familiyangizni kiriting:\n"
        "<i>Masalan: Ali Valiyev</i>",
        parse_mode="HTML",
    )
    await state.set_state(ApplicationForm.full_name)
    await callback.answer()



@router.message(ApplicationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 3:
        await message.answer("❌ Iltimos, to'liq ism va familiyangizni kiriting.")
        return

    await state.update_data(full_name=name)
    await message.answer(
        f"✅ Rahmat, <b>{name}</b>!\n\n"
        "<b>2/5</b> — Telefon raqamingizni yuboring:\n"
        "Tugmani bosing yoki qo'lda kiriting: <i>+998901234567</i>",
        parse_mode="HTML",
        reply_markup=phone_keyboard(),
    )
    await state.set_state(ApplicationForm.phone)



@router.message(ApplicationForm.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await _save_phone(message, state, phone)



@router.message(ApplicationForm.phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not (phone.startswith("+") and len(phone) >= 10):
        await message.answer(
            "❌ Noto'g'ri format. Iltimos raqamni to'g'ri kiriting.\n"
            "<i>Masalan: +998901234567</i>",
            parse_mode="HTML",
        )
        return
    await _save_phone(message, state, phone)


async def _save_phone(message: Message, state: FSMContext, phone: str):
    await state.update_data(phone=phone)
    await message.answer(
        "<b>3/5</b> — Qaysi yo'nalish bo'yicha amaliyot qilmoqchisiz?",
        parse_mode="HTML",
        reply_markup=remove_keyboard(),
    )
    await message.answer(
        "Yo'nalishni tanlang 👇",
        reply_markup=direction_keyboard(),
    )
    await state.set_state(ApplicationForm.direction)



@router.callback_query(ApplicationForm.direction, F.data.startswith("direction:"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.split(":")[1]
    await state.update_data(direction=direction)
    await callback.message.edit_text(
        f"✅ Yo'nalish: <b>{direction}</b>\n\n"
        "<b>4/5</b> — Qaysi texnologiyalarni bilasiz?\n"
        "<i>Masalan: Python, Django, PostgreSQL</i>",
        parse_mode="HTML",
    )
    await state.set_state(ApplicationForm.technologies)
    await callback.answer()



@router.message(ApplicationForm.technologies)
async def process_technologies(message: Message, state: FSMContext):
    tech = message.text.strip()
    if len(tech) < 2:
        await message.answer("❌ Iltimos, texnologiyalarni kiriting.")
        return

    await state.update_data(technologies=tech)
    await message.answer(
        "<b>5/5</b> — Portfolio yoki GitHub havolangizni yuboring:\n"
        "<i>Masalan: github.com/username</i>\n\n"
        "Agar yo'q bo'lsa: <b>yo'q</b> deb yozing",
        parse_mode="HTML",
    )
    await state.set_state(ApplicationForm.portfolio)


# ──────────────────────────────────────────────
# Step 5: Portfolio
# ──────────────────────────────────────────────
@router.message(ApplicationForm.portfolio)
async def process_portfolio(message: Message, state: FSMContext):
    portfolio = message.text.strip()
    await state.update_data(portfolio=portfolio)

    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    summary = (
        "📋 <b>Arizangiz ko'rinishi:</b>\n\n"
        f"👤 <b>Ism:</b> {data['full_name']}\n"
        f"📱 <b>Telefon:</b> {data['phone']}\n"
        f"🎯 <b>Yo'nalish:</b> {data['direction']}\n"
        f"💻 <b>Texnologiyalar:</b> {data['technologies']}\n"
        f"🔗 <b>Portfolio:</b> {data['portfolio']}\n"
        f"✈️ <b>Telegram:</b> {username}\n\n"
        "Arizani tasdiqlaysizmi?"
    )
    await message.answer(summary, parse_mode="HTML", reply_markup=confirm_keyboard())
    await state.set_state(ApplicationForm.confirm)


# ──────────────────────────────────────────────
# Step 6: Confirm & send
# ──────────────────────────────────────────────
@router.callback_query(ApplicationForm.confirm, F.data == "confirm_application")
async def confirm_application(callback: CallbackQuery, state: FSMContext):
    from config import CHANNEL_ID
    from database import save_application

    data = await state.get_data()
    user = callback.from_user
    username = f"@{user.username}" if user.username else f"id:{user.id}"

    # Save to DB
    app_id = await save_application(user.id, user.username or "", data)

    # Format channel message
    channel_text = (
        "🆕 <b>YANGI AMALIYOTCHI ARIZASI</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>Ariza №:</b> {app_id}\n"
        f"👤 <b>Ism:</b> {data['full_name']}\n"
        f"📱 <b>Telefon:</b> {data['phone']}\n"
        f"🎯 <b>Yo'nalish:</b> {data['direction']}\n"
        f"💻 <b>Texnologiyalar:</b> {data['technologies']}\n"
        f"🔗 <b>Portfolio:</b> {data['portfolio']}\n"
        f"✈️ <b>Telegram:</b> {username}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        await callback.bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_text,
            parse_mode="HTML",
        )
        await callback.message.edit_text(
            "🎉 <b>Arizangiz muvaffaqiyatli yuborildi!</b>\n\n"
            f"Ariza raqamingiz: <b>#{app_id}</b>\n\n"
            "Tez orada siz bilan bog'lanamiz. Rahmat! 🙏",
            parse_mode="HTML",
        )
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {e}\n"
            "Iltimos, adminga murojaat qiling."
        )

    await state.clear()
    await callback.answer("✅ Ariza yuborildi!")
