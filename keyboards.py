from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from config import DIRECTIONS


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Arizani boshlash", callback_data="start_application")],
    ])


def direction_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=direction, callback_data=f"direction:{direction}")]
        for direction in DIRECTIONS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_application"),
            InlineKeyboardButton(text="🔄 Qayta boshlash", callback_data="restart_application"),
        ]
    ])


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Barcha arizalar", callback_data="admin_list")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
    ])
