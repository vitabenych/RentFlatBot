import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)
from api.actions import parse_and_save_listing  

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Вітальний текст
WELCOME_MESSAGE = (
    "🏠 *Вітаємо у RentFlatBot!*\n\n"
    "Налаштуй параметри пошуку всього за один крок — і я надсилатиму тобі нові квартири з більшості телеграм-каналів щойно вони з'являться.\n\n"
    "Я тут, щоб зробити пошук квартири зручним. Спробуй! 😊"
)

# Меню: тип пошуку
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Обрати тип пошуку", callback_data="choose_search_type")],
        [InlineKeyboardButton("🛠 Почати пошук", callback_data="start_search")]
    ])

# Меню: кімнати
def rooms_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1 кімната", callback_data="rooms_1")],
        [InlineKeyboardButton("2 кімнати", callback_data="rooms_2")],
        [InlineKeyboardButton("3 кімнати", callback_data="rooms_3")],
        [InlineKeyboardButton("4+ кімнати", callback_data="rooms_4_plus")],
        [InlineKeyboardButton("↩ Назад до районів", callback_data="by_district")]
    ])

# Меню редагування параметрів
def edit_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📍 Змінити район", callback_data="edit_district")],
        [InlineKeyboardButton("🛏 Змінити кімнати", callback_data="edit_rooms")],
        [InlineKeyboardButton("💰 Змінити бюджет", callback_data="edit_budget")],
        [InlineKeyboardButton("🧹 Скинути все", callback_data="reset_all")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown", reply_markup=main_menu())

# Обробка натискань кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "choose_search_type":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏘 По районах", callback_data="by_district")],
            [InlineKeyboardButton("🏙 По ЖК", callback_data="by_complex")]
        ])
        await query.edit_message_text("Оберіть тип пошуку:", reply_markup=keyboard)

    elif query.data == "by_district":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Все місто", callback_data="district_all")],
            [InlineKeyboardButton("📍 Сихівський", callback_data="district_sykhiv")],
            [InlineKeyboardButton("📍 Брюховичі", callback_data="district_briukhovychi")],
            [InlineKeyboardButton("📍 Галицький", callback_data="district_halytskyi")],
            [InlineKeyboardButton("📍 Сокільники", callback_data="district_sokilnyky")],
            [InlineKeyboardButton("📍 Залізничний", callback_data="district_zaliznychnyi")],
            [InlineKeyboardButton("📍 Лисиничі", callback_data="district_lysychnychi")],
            [InlineKeyboardButton("📍 Личаківський", callback_data="district_lychakivskyi")],
            [InlineKeyboardButton("📍 Винники", callback_data="district_vynnyky")],
            [InlineKeyboardButton("📍 Шевченківський", callback_data="district_shevchenkivskyi")],
            [InlineKeyboardButton("📍 Франківський", callback_data="district_frankivskyi")],
            [InlineKeyboardButton("↩ Назад", callback_data="choose_search_type")]
        ])
        await query.edit_message_text("Оберіть район:", reply_markup=keyboard)

    elif query.data == "by_complex":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏢 ЖК Велика Британія", callback_data="complex_britania")],
            [InlineKeyboardButton("🏢 ЖК Софіївка", callback_data="complex_sofiivka")],
            [InlineKeyboardButton("🏢 ЖК Парус", callback_data="complex_parus")],
            [InlineKeyboardButton("🏢 ЖК Авалон", callback_data="complex_avalon")],
            [InlineKeyboardButton("🏢 ЖК Щасливий", callback_data="complex_shchaslyvyi")],
            [InlineKeyboardButton("↩ Назад", callback_data="choose_search_type")]
        ])
        await query.edit_message_text("Оберіть житловий комплекс:", reply_markup=keyboard)

    elif query.data.startswith("district_"):
        selected = query.data.replace("district_", "")
        if selected == "all":
            selected = "Все місто"
        else:
            selected = selected.capitalize()
        context.user_data["district"] = selected
        context.user_data.pop("complex", None)
        await query.edit_message_text(
            f"✅ Ви обрали район: *{selected}*\n\nТепер оберіть кількість кімнат:",
            parse_mode="Markdown",
            reply_markup=rooms_menu()
        )

    elif query.data.startswith("complex_"):
        selected = query.data.replace("complex_", "").capitalize()
        context.user_data["complex"] = selected
        context.user_data.pop("district", None)
        await query.edit_message_text(
            f"✅ Ви обрали ЖК: *{selected}*\n\nТепер оберіть кількість кімнат:",
            parse_mode="Markdown",
            reply_markup=rooms_menu()
        )

    elif query.data.startswith("rooms_"):
        rooms = query.data.replace("rooms_", "").replace("_plus", "+")
        context.user_data["rooms"] = rooms
        district = context.user_data.get('district') or context.user_data.get('complex') or "не обрано"
        await query.edit_message_text(
            f"🏡 Обрано: *{district}*, кімнат: *{rooms}*\n\n"
            "Тепер введіть бюджет:\n\n"
            "`від` і `до` через пробіл або новий рядок\n\n"
            "Наприклад: `8000 15000`",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_budget"] = True

    elif query.data == "start_search":
        await query.edit_message_text("🔎 Пошук розпочато!\n(Поки що в демо-режимі)")

    elif query.data == "edit_params":
        await query.edit_message_text("Що хочеш змінити?", reply_markup=edit_menu())

    elif query.data == "edit_district":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Все місто", callback_data="district_all")],
            [InlineKeyboardButton("📍 Сихівський", callback_data="district_sykhiv")],
            [InlineKeyboardButton("📍 Брюховичі", callback_data="district_briukhovychi")],
            [InlineKeyboardButton("📍 Галицький", callback_data="district_halytskyi")],
            [InlineKeyboardButton("📍 Сокільники", callback_data="district_sokilnyky")],
            [InlineKeyboardButton("📍 Залізничний", callback_data="district_zaliznychnyi")],
            [InlineKeyboardButton("📍 Лисиничі", callback_data="district_lysychnychi")],
            [InlineKeyboardButton("📍 Личаківський", callback_data="district_lychakivskyi")],
            [InlineKeyboardButton("📍 Винники", callback_data="district_vynnyky")],
            [InlineKeyboardButton("📍 Шевченківський", callback_data="district_shevchenkivskyi")],
            [InlineKeyboardButton("📍 Франківський", callback_data="district_frankivskyi")],
            [InlineKeyboardButton("↩ Назад", callback_data="edit_params")]
        ])
        await query.edit_message_text("Оберіть новий район:", reply_markup=keyboard)

    elif query.data == "edit_rooms":
        await query.edit_message_text("Оберіть нову кількість кімнат:", reply_markup=rooms_menu())

    elif query.data == "edit_budget":
        context.user_data["awaiting_budget"] = True
        await query.edit_message_text(
            "Введіть новий бюджет:\n\nНаприклад: `10000 25000`",
            parse_mode="Markdown"
        )

    elif query.data == "reset_all":
        context.user_data.clear()
        await query.edit_message_text(
            "⚠️ Усі параметри скинуто. Почнімо спочатку 🙂",
            reply_markup=main_menu()
        )

    elif query.data == "main_menu":
        await query.edit_message_text("🔽 Обери опції нижче:", reply_markup=main_menu())

# Обробка текстових повідомлень (зокрема бюджету та оголошень)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_budget"):
        try:
            parts = update.message.text.replace("\n", " ").split()
            if len(parts) != 2:
                raise ValueError("Неправильний формат")
            min_budget = int(parts[0])
            max_budget = int(parts[1])
            context.user_data["min_budget"] = min_budget
            context.user_data["max_budget"] = max_budget
            context.user_data["awaiting_budget"] = False

            district = context.user_data.get('district') or context.user_data.get('complex') or "не обрано"
            rooms = context.user_data.get('rooms') or "не обрано"

            summary = (
                f"✅ Обрано:\n"
                f"• Район/ЖК: *{district}*\n"
                f"• Кімнат: *{rooms}*\n"
                f"• Бюджет: *{min_budget} – {max_budget} грн*\n\n"
                f"Натисни '🛠 Почати пошук' щоб розпочати."
            )

            await update.message.reply_text(
                summary + "\n\n🔄 Ти можеш змінити параметри або запустити пошук.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🛠 Почати пошук", callback_data="start_search")],
                    [InlineKeyboardButton("🔄 Змінити параметри", callback_data="edit_params")]
                ])
            )

        except Exception:
            await update.message.reply_text(
                "❌ Введіть *два* числа: мінімальний і максимальний бюджет (наприклад `10000 20000`)",
                parse_mode="Markdown"
            )
    else:
    
        text = update.message.text
        await parse_and_save_listing(text)
        await update.message.reply_text("Дякую! Оголошення отримано і оброблено.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущено...")
    app.run_polling()
