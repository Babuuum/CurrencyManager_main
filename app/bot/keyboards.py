from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Actives"), KeyboardButton(text="💰 incomes")],
            [KeyboardButton(text="⚙️ Settings")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел"
    )

def actives_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Create", callback_data="active:create"),
                InlineKeyboardButton(text="✏️ Update", callback_data="active:update")
            ],
            [
                InlineKeyboardButton(text="❌ Delete", callback_data="active:delete"),
                InlineKeyboardButton(text="⬅️ Quit", callback_data="active:quit"),
            ]
        ]
    )