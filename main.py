#!/usr/bin/env python3
"""
OVERLORD TELEGRAM BOT — STABLE VERSION FOR RENDER
Упрощённая и стабильная версия специально для Render.com
"""

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "8807762542:AAHyreuQHEgYYMoW62Zftz6PODzLyIFkhDQ"

# ==================== БАЗЫ ====================
ART_BASE = "masterpiece, best quality, erotic fine art, ultra detailed, 8k, sharp focus, sensual elegant atmosphere, beautiful composition, dramatic artistic lighting, depth of field, "
DIRTY_BASE = "masterpiece, best quality, ultra detailed, 8k, hyper-detailed, raw explicit, vulgar, obscene, extreme close-up on pussy and fluids, glistening wetness, messy fluids, "
MIXED_BASE = "masterpiece, best quality, ultra detailed, 8k, erotic atmosphere, highly detailed, sensual and lewd, beautiful composition with explicit details, "

DETAIL = "insanely detailed, hyper-detailed skin, extreme fluid physics, micro details on every droplet, "
INTENSITY = "hyper explicit, raw sexual, obscene, extreme close-up on genitals and fluids, maximum vulgarity and detail, "

# ==================== ФИЛЬТРЫ ====================
FILTERS = {
    # Позиции
    "Поза сзади (Doggy Style)": "doggy style, from behind, ass up face down, deep hard penetration from behind, ",
    "Матинг Пресс": "mating press, legs folded back to chest, deep breeding position, ",
    "Миссионерская поза": "missionary position, legs spread extremely wide, ",
    "Она сверху (Cowgirl)": "cowgirl, riding cock hard, bouncing on dick, ",
    "Обратная наездница": "reverse cowgirl, ass facing viewer, ",
    "Полный Нельсон": "full nelson, legs held up high and spread, ",

    # Одежда
    "Прозрачные чулки": "sheer thigh-high stockings, transparent stockings, garter belt, ",
    "Чулки в сетку": "black fishnet stockings, fishnet thigh highs, ",
    "Микро-юбка": "micro skirt, extremely short skirt, ",
    "Рваная одежда": "torn clothes, ripped outfit, clothes destroyed during sex, ",
    "Прозрачный мокрый топ": "sheer transparent blouse, wet transparent shirt, ",

    # БДСМ
    "Ошейник + поводок": "collar with leash, pet collar, submissive collar, ",
    "Повязка на глаза": "blindfold, eye mask, black blindfold, ",
    "Надписи на теле": "body writing, words like 'slut', 'cumdump', 'whore' written on skin, ",
    "Полностью сломана": "completely mind broken, empty expression, ",

    # Выражения лица
    "Ахегао": "ahegao, long tongue out, rolled back eyes, heart-shaped pupils, mind break, ",
    "Разум сломан": "mind break, completely broken expression, empty glazed eyes, ",
    "Плачет от удовольствия": "crying tears of pleasure, teary eyes, sobbing in ecstasy, ",

    # Жидкости
    "Обильные слюни": "heavy excessive drooling, thick saliva strings, ",
    "Кремпай": "creampie, cum overflowing from pussy, thick white cum dripping down thighs, ",
    "Сквирт": "squirting, powerful female ejaculation, fluids spraying out, ",

    # Партнёры
    "Гангбанг": "gangbang, multiple men fucking one girl at the same time, ",
    "Тентакли": "tentacles, multiple tentacles filling pussy, ass and mouth, ",
    "Монстр / Horse cock": "monster fucking, huge monster cock, extreme size difference, ",

    # Экстрим
    "Огромный член": "massive cock, extreme size, visible belly bulge, ",
    "Глубокий до живота": "cock bulging her stomach, visible bulge in belly, ",
}

def build_prompt(raw: str, mode: str, selected: list) -> str:
    if mode == "art":
        base = ART_BASE
    elif mode == "mixed":
        base = MIXED_BASE
    else:
        base = DIRTY_BASE

    parts = [base, DETAIL, INTENSITY, raw + ", "]

    for f in selected:
        if f in FILTERS:
            parts.append(FILTERS[f])

    parts.append("hyper-detailed pussy and fluids, extreme wetness, raw sexual, perfect anatomy, sharp focus, masterpiece, maximum lewd detail, 8k quality")

    text = " ".join(parts)
    full = ", ".join(p.strip() for p in text.split(",") if p.strip())

    summary = f"Короткое описание: {raw}. Промпт создаёт детальную эротическую сцену."

    return f"{summary}\n\n{full}"

def smart_select(text: str) -> list:
    text = text.lower()
    res = []
    rules = {
        "Поза сзади (Doggy Style)": ["doggy", "сзади"],
        "Матинг Пресс": ["mating press", "матинг пресс"],
        "Гангбанг": ["gangbang", "гангбанг"],
        "Тентакли": ["тентакл"],
        "Ахегао": ["ahegao", "ахегао"],
        "Обильные слюни": ["слюни"],
        "Кремпай": ["creampie", "кремпай"],
        "Прозрачные чулки": ["чулк"],
        "Микро-юбка": ["юбк", "микро"],
        "Рваная одежда": ["рван", "torn"],
        "Ошейник + поводок": ["ошейник", "collar"],
        "Повязка на глаза": ["повязк", "blindfold"],
        "Монстр / Horse cock": ["horse", "жеребяч"],
        "Полностью сломана": ["mind break", "разум сломан"],
    }
    for name, keys in rules.items():
        for k in keys:
            if k in text:
                res.append(name)
                break
    return list(set(res))

# ==================== МЕНЮ ====================
def main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎨 Арт"), KeyboardButton("🔥 Грязный"), KeyboardButton("⚡ Смешанный")],
        [KeyboardButton("🎲 Random God Tier"), KeyboardButton("📋 Фильтры")],
        [KeyboardButton("🧠 Умный авто"), KeyboardButton("❓ Помощь")]
    ], resize_keyboard=True)

def category_menu():
    keyboard = [
        [InlineKeyboardButton("🍆 Позиции", callback_data="cat_poses"),
         InlineKeyboardButton("👗 Одежда", callback_data="cat_clothes")],
        [InlineKeyboardButton("😈 БДСМ", callback_data="cat_bdsm"),
         InlineKeyboardButton("😈 Лицо", callback_data="cat_face")],
        [InlineKeyboardButton("💦 Жидкости", callback_data="cat_fluids"),
         InlineKeyboardButton("👹 Партнёры", callback_data="cat_partners")],
        [InlineKeyboardButton("✅ Готово", callback_data="done")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_filters_keyboard(cat: str):
    items = {
        "poses": ["Поза сзади (Doggy Style)", "Матинг Пресс", "Миссионерская поза", "Она сверху (Cowgirl)", "Полный Нельсон"],
        "clothes": ["Прозрачные чулки", "Чулки в сетку", "Микро-юбка", "Рваная одежда", "Прозрачный мокрый топ"],
        "bdsm": ["Ошейник + поводок", "Повязка на глаза", "Надписи на теле", "Полностью сломана"],
        "face": ["Ахегао", "Разум сломан", "Плачет от удовольствия"],
        "fluids": ["Обильные слюни", "Кремпай", "Сквирт"],
        "partners": ["Гангбанг", "Тентакли", "Монстр / Horse cock"],
    }
    buttons = items.get(cat, [])
    keyboard = []
    for i in range(0, len(buttons), 2):
        row = [InlineKeyboardButton(buttons[i], callback_data=f"f_{buttons[i]}")]
        if i + 1 < len(buttons):
            row.append(InlineKeyboardButton(buttons[i+1], callback_data=f"f_{buttons[i+1]}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# ==================== ОБРАБОТЧИКИ ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "dirty"
    context.user_data["selected"] = []
    await update.message.reply_text(
        "🔥 <b>OVERLORD BOT</b> — Стабильная версия\n\n"
        "Пиши идею или используй кнопки.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "dirty")
    selected = context.user_data.get("selected", [])

    if text in ["🎨 Арт", "🔥 Грязный", "⚡ Смешанный"]:
        mode = "art" if "Арт" in text else "dirty" if "Грязный" in text else "mixed"
        context.user_data["mode"] = mode
        await update.message.reply_text(f"✅ Режим: <b>{text}</b>", parse_mode="HTML")
        return

    if text == "🎲 Random God Tier":
        picked = random.sample(list(FILTERS.keys()), min(8, len(FILTERS)))
        context.user_data["selected"] = picked
        await update.message.reply_text(f"🎲 Добавлено {len(picked)} фильтров! Напиши идею.")
        return

    if text == "📋 Фильтры":
        await update.message.reply_text("Выбери категорию:", reply_markup=category_menu())
        return

    if text == "🧠 Умный авто":
        context.user_data["smart"] = True
        await update.message.reply_text("Напиши идею — я подберу фильтры автоматически.")
        return

    if text == "❓ Помощь":
        await update.message.reply_text("Пиши идею. Используй кнопки для режимов и фильтров.")
        return

    if context.user_data.get("smart"):
        auto = smart_select(text)
        selected = list(set(selected + auto))
        context.user_data["smart"] = False

    prompt = build_prompt(text, mode, selected)
    await update.message.reply_text(f"✅ <b>Готово!</b>\n\n<code>{prompt}</code>", parse_mode="HTML")
    context.user_data["selected"] = []

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    selected = context.user_data.get("selected", [])

    if data == "done":
        await query.edit_message_text("✅ Фильтры применены! Напиши идею.")
        return
    if data == "back":
        await query.edit_message_text("Выбери категорию:", reply_markup=category_menu())
        return
    if data.startswith("cat_"):
        cat = data.replace("cat_", "")
        await query.edit_message_text("Выбери фильтры:", reply_markup=get_filters_keyboard(cat))
        return
    if data.startswith("f_"):
        name = data[2:]
        if name not in selected:
            selected.append(name)
        context.user_data["selected"] = selected
        await query.edit_message_text(
            f"✅ Добавлено: <b>{name}</b>\n\nТекущие: {', '.join(selected)}\n\nВыбери ещё или «Готово»",
            reply_markup=category_menu()
        )

def main():
    print("🚀 Overlord Stable Bot запущен...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
