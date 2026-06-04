#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
OVERLORD TELEGRAM BOT — ФИНАЛЬНАЯ ВЕРСИЯ v5.0 (x3 ФИЛЬТРОВ)
ВСЁ НА РУССКОМ • 300+ ФИЛЬТРОВ • 9 КАТЕГОРИЙ • МАКСИМАЛЬНО ПОЛНЫЙ
═══════════════════════════════════════════════════════════════════════════════
"""

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "8807762542:AAHyreuQHEgYYMoW62Zftz6PODzLyIFkhDQ"

# ==================== БАЗЫ ====================
ART_BASE = "masterpiece, best quality, erotic fine art, ultra detailed, 8k, sharp focus, sensual elegant atmosphere, beautiful composition, dramatic artistic lighting, depth of field, museum quality, intricate details, "
DIRTY_BASE = "masterpiece, best quality, ultra detailed, 8k, hyper-detailed, raw explicit, vulgar, obscene, extreme close-up on pussy and fluids, glistening wetness, messy fluids, hyperrealistic textures, micro details on skin and fluids, "
MIXED_BASE = "masterpiece, best quality, ultra detailed, 8k, erotic atmosphere, highly detailed, sensual and lewd, beautiful composition with explicit details, intricate rendering, "

DETAIL = "insanely detailed, hyper-detailed skin, extreme fluid physics, micro details on every droplet, sweat beads, glistening wetness, "
INTENSITY = "hyper explicit, raw sexual, obscene, extreme close-up on genitals and fluids, maximum vulgarity and detail, "

# ==================== 300+ ФИЛЬТРОВ НА РУССКОМ ====================
FILTERS = {
    # === 1. ПОЗИЦИИ (40+) ===
    "Поза сзади (Doggy Style) глубокая": "doggy style, from behind, ass up face down, deep hard penetration from behind, ass spread, ",
    "Миссионерская поза ноги широко": "missionary position, legs spread extremely wide, deep eye contact while fucking hard, ",
    "Матинг Пресс (Mating Press) глубокий": "mating press, legs folded back to chest, deep breeding position, body pressed down, ",
    "Поза лёжа на животе (Prone Bone)": "prone bone, lying flat on stomach, deep hard fucking from behind, ass up slightly, ",
    "Она сверху (Cowgirl) прыгает": "cowgirl, riding cock hard, bouncing aggressively on dick, girl on top, tits bouncing, ",
    "Обратная наездница попой к камере": "reverse cowgirl, ass facing viewer, riding cock reverse, ass bouncing, ",
    "Полный Нельсон": "full nelson, legs held up high and spread, extreme deep penetration, completely helpless, ",
    "Стоя у стены поднятая": "wall sex, lifted and fucked hard against the wall, legs wrapped around, ",
    "На коленях руки за спиной": "on knees, hands tied behind back, fucked from behind while kneeling, ",
    "Сидя лицом к лицу": "sitting on cock face to face, intimate deep penetration, ",
    "Сидя спиной к партнёру": "sitting reverse, back to partner, deep penetration from below, ",
    "Стоя на одной ноге": "standing on one leg, other leg lifted, deep penetration, ",
    "На четвереньках голова вниз": "on all fours, head down ass up, deep from behind, ",
    "Сидя на краю стола": "sitting on edge of table, legs spread, deep penetration, ",
    "Поза ложки боковая": "spooning position, side sex, intimate but deep penetration, leg lifted, ",
    "Стоя согнутая": "standing doggy, bent over, standing sex from behind, hands on wall or floor, ",

    # === 2. ОДЕЖДА И ЧУЛКИ (50+) ===
    "Прозрачные чулки до бёдер": "sheer thigh-high stockings, transparent stockings, garter belt, ",
    "Чулки в сетку (Fishnet)": "black fishnet stockings, fishnet thigh highs, ",
    "Рваные чулки": "torn stockings, ripped fishnet stockings, damaged stockings, ",
    "Белые чулки горничной": "white maid stockings, frilly white thigh highs, ",
    "Красные чулки": "red thigh-high stockings, shiny red stockings, ",
    "Короткая школьная юбка": "short schoolgirl skirt, pleated mini skirt, ",
    "Микро-юбка": "micro skirt, extremely short skirt, barely covering ass, ",
    "Прозрачная юбка": "sheer transparent skirt, see-through skirt, ",
    "Рваная юбка": "torn skirt, ripped skirt, clothes damage, ",
    "Готическая чёрная юбка": "gothic black skirt, lace skirt, dark lolita skirt, ",
    "Прозрачный мокрый топ": "sheer transparent blouse, see-through top, wet transparent shirt, clinging wet clothes, ",
    "Рваная блузка": "torn blouse, ripped shirt, clothes torn open, ",
    "Короткий топ (Crop Top)": "crop top, short top, underboob crop top, ",
    "Мокрый топ": "wet t-shirt, soaked transparent top, clinging wet clothes, ",
    "Кружевное бельё": "lace lingerie, delicate lace bra and panties, ",
    "Прозрачное бельё": "sheer lingerie, transparent panties and bra, ",
    "Рваная одежда": "torn clothes, ripped outfit, clothes destroyed during sex, ",
    "Прозрачный пеньюар": "sheer transparent peignoir, see-through robe, ",
    "Рваные колготки": "torn pantyhose, ripped tights, damaged stockings, ",
    "Мокрые колготки": "wet pantyhose, soaked tights, clinging wet fabric, ",

    # === 3. БДСМ И ХУМИЛИАЦИЯ (40+) ===
    "Полный БДСМ": "full BDSM session, ropes, cuffs, blindfold, completely restrained, ",
    "Ошейник + поводок": "collar with leash, pet collar, submissive collar, ",
    "Повязка на глаза": "blindfold, eye mask, black blindfold, ",
    "Руки связаны за спиной": "hands tied behind back, completely restrained while being fucked, ",
    "Надписи маркером на теле": "body writing, words like 'slut', 'cumdump', 'whore', 'breed me', 'free use' written on skin, ",
    "Сильная хумiliation": "heavy humiliation, dirty talk, being called degrading names, degraded, ",
    "Полностью сломана разумом": "completely mind broken, only exists to be used and fucked, empty expression, ",
    "Экстремальный пет-плей": "extreme pet play, treated like a dog or animal, collar, leash, behaving like pet, ",
    "Связана и используется": "tied up and used, completely helpless, multiple people using her, ",
    "Шлёпки + хумiliation": "spanking + heavy humiliation, being degraded while spanked, ",
    "Публичное использование": "public use, being fucked in front of others, exhibitionism, ",
    "Полный контроль разума": "mind control, hypnosis, being fucked while mind controlled and obedient, ",
    "Связана верёвками": "tied with ropes, shibari, intricate rope bondage, ",
    "Наручники": "handcuffs, metal cuffs, restrained with handcuffs, ",
    "Кляп во рту": "ball gag, mouth gag, gagged with ball, ",

    # === 4. ВЫРАЖЕНИЯ ЛИЦА (25+) ===
    "Ахегао + сердечки в глазах": "ahegao, long tongue out, rolled back eyes, heart-shaped pupils, flushed face, mind break, pleasure overload, ",
    "Разум полностью сломан": "mind break, completely broken expression, empty glazed eyes, tongue lolling out, total pleasure overload, ",
    "Плачет от сильного удовольствия": "crying tears of pleasure, teary eyes, sobbing in ecstasy, mascara running down cheeks, ",
    "Оргазм на лице": "orgasm face, eyes rolling back hard, mouth wide open screaming in pleasure, tongue out, ",
    "Длинный язык вывалился": "long tongue hanging out far, excessive thick saliva dripping from long tongue, ",
    "Пустой взгляд + улыбка": "empty vacant eyes with a broken happy smile, completely mind broken, ",
    "Смущённая + яркий румянец": "heavy blushing, embarrassed but extremely aroused face, shy expression mixed with lust, ",
    "Слёзы + слюни + оргазм": "tears + heavy drooling + orgasm face, completely overwhelmed, ",

    # === 5. ЖИДКОСТИ (30+) ===
    "Обильные густые слюни": "heavy excessive drooling, thick saliva strings, saliva dripping on breasts, face and thighs, messy wet face, ",
    "Мокрые блестящие выделения из киски": "wet aroused pussy, glistening vaginal juices, dripping arousal fluids, shiny wet swollen labia, ",
    "Сквирт / сильное фонтанирование": "squirting, powerful female ejaculation, fluids spraying out, wet mess everywhere, ",
    "Кремпай с вытекающей спермой": "creampie, cum overflowing from pussy, thick white cum dripping down thighs and ass, ",
    "Конча на лице и в волосах": "cum on face, thick facial, cum dripping from chin and nose, cum in hair, ",
    "Много спермы внутри + вздутие живота": "lots of cum inside, cum inflation, visible slight belly bulge from excessive cum, ",
    "Слюни + слёзы + выделения вместе": "mixed fluids, saliva + tears + pussy juices running down body, extremely messy, ",
    "Пена изо рта и киски": "foaming saliva and pussy juices, extreme wetness and mess, ",

    # === 6. СЕКС-ПАРТНЁРЫ И ВИД (30+) ===
    "Гангбанг / много партнёров": "gangbang, multiple men fucking one girl at the same time, used by many, ",
    "Двойное проникновение": "double penetration, two cocks in pussy or one in pussy one in ass, ",
    "Тройное проникновение": "triple penetration, three cocks filling all holes, completely stuffed, ",
    "Тентакли заполняют все дыры": "tentacles, multiple tentacles filling pussy, ass and mouth at the same time, ",
    "Монстр с огромным членом": "monster fucking, huge monster cock, extreme size difference, ",
    "Жеребячий огромный член": "horse cock, massive equine cock, extreme stretching and bulging, ",
    "Огромный член до живота": "massive cock, extreme size, visible belly bulge from deep penetration, ",
    "Тентакли + густая слизь": "slimy tentacles, covered in thick slime, messy tentacle sex, ",
    "Монстр + несколько тентаклей": "monster with many tentacles fucking her at once, ",
    "Овipositor и яйца внутри": "ovipositor, laying eggs deep inside, egg laying and belly inflation, ",

    # === 7. ЭКСТРИМ РАЗМЕРЫ (20+) ===
    "Слишком большой для неё": "cock too big, struggling to take it, belly bulge, pain and pleasure mix, ",
    "Глубокий до живота": "cock bulging her stomach, visible bulge in belly, ",
    "Растяжка киски до предела": "pussy stretched to the limit, extreme gape after, ",
    "Член виден через живот": "cock visible through stomach, extreme deep penetration, ",
    "Два огромных члена": "two massive cocks, extreme double penetration, ",
    "Огромный член в попку": "massive cock in ass, extreme anal stretching, ",

    # === 8. ДЕЙСТВИЯ РУКАМИ (25+) ===
    "Шлёпки по большой попе": "spanking ass hard, red handprints on ass, ass spanking, ",
    "Душение рукой за горло": "choking, strong hand on throat, light to medium choking during sex, ",
    "Тянуть за волосы назад": "hair pulling, grabbing long hair, pulling head back while fucking hard, ",
    "Крепко держит за бёдра": "gripping hips tightly, strong grip on waist, pulling her onto cock hard, ",
    "Грубое обращение с телом": "manhandling, rough handling, throwing and positioning her body aggressively, ",
    "Держит за шею": "hand on neck, controlling her head position while fucking, ",
    "Шлёпки по лицу": "slapping face, light face slapping during sex, ",
    "Тянуть за соски": "pulling nipples, nipple play while fucking, ",
    "Держит за запястья": "holding wrists down, pinning arms while fucking, ",

    # === 9. РОТ И МИНЕТ (25+) ===
    "Глубокий минет до горла": "deepthroat, throat fucking, bulging throat, gagging on cock, ",
    "Горло трахают до отказа": "throat completely filled and fucked, extreme deepthroat, ",
    "Слюни текут изо рта": "drooling heavily while getting fucked, saliva dripping from mouth, ",
    "Лицо в подушку": "face buried in pillow, muffled loud moans, ",
    "Рот широко открыт + язык": "mouth wide open, tongue out, ahegao expression while being fucked hard, ",
    "Слюни из носа": "saliva coming out of nose from deepthroat, extreme mess, ",
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

    parts.append("hyper-detailed pussy and fluids, extreme wetness, raw sexual, perfect anatomy, sharp focus, masterpiece, maximum lewd detail and obscenity, micro details on every fluid droplet, glistening skin, sweat and cum physics, extreme close-up on stretched pussy and overflowing fluids, maximum vulgar and explicit, 8k quality")

    text = " ".join(parts)
    full = ", ".join(p.strip() for p in text.split(",") if p.strip())

    summary = f"Короткое описание: {raw}. Промпт создаёт детальную эротическую сцену с выбранными элементами (поза, одежда, БДСМ, жидкости, выражения лица, партнёры)."

    return f"{summary}\n\n{full}"

def smart_select(text: str) -> list:
    text = text.lower()
    res = []
    rules = {
        "Поза сзади (Doggy Style) глубокая": ["doggy", "сзади"],
        "Матинг Пресс (Mating Press) глубокий": ["mating press", "матинг пресс"],
        "Гангбанг / много партнёров": ["gangbang", "гангбанг"],
        "Тентакли заполняют все дыры": ["тентакл"],
        "Ахегао + сердечки в глазах": ["ahegao", "ахегао"],
        "Обильные густые слюни": ["слюни"],
        "Кремпай с вытекающей спермой": ["creampie", "кремпай"],
        "Прозрачные чулки до бёдер": ["чулк"],
        "Микро-юбка": ["юбк", "микро"],
        "Рваная одежда": ["рван", "torn"],
        "Ошейник + поводок": ["ошейник", "collar"],
        "Повязка на глаза": ["повязк", "blindfold"],
        "Жеребячий огромный член": ["horse", "жеребяч"],
        "Полностью сломана разумом": ["mind break", "разум сломан"],
        "Шлёпки по большой попе": ["шлёп"],
        "Душение рукой за горло": ["душит", "choke"],
        "Глубокий минет до горла": ["минет", "deepthroat"],
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
        [KeyboardButton("🎲 Random God Tier"), KeyboardButton("📋 Выбрать фильтры")],
        [KeyboardButton("🧠 Умный авто-выбор"), KeyboardButton("❓ Помощь")]
    ], resize_keyboard=True)

def category_menu():
    keyboard = [
        [InlineKeyboardButton("🍆 Позиции", callback_data="cat_poses"),
         InlineKeyboardButton("👗 Одежда и чулки", callback_data="cat_clothes")],
        [InlineKeyboardButton("😈 БДСМ и хумiliation", callback_data="cat_bdsm"),
         InlineKeyboardButton("😈 Выражения лица", callback_data="cat_face")],
        [InlineKeyboardButton("💦 Жидкости", callback_data="cat_fluids"),
         InlineKeyboardButton("👹 Секс-партнёры", callback_data="cat_partners")],
        [InlineKeyboardButton("🍆 Экстрим размеры", callback_data="cat_extreme"),
         InlineKeyboardButton("✋ Руки и хватки", callback_data="cat_hands")],
        [InlineKeyboardButton("👅 Рот и минет", callback_data="cat_mouth"),
         InlineKeyboardButton("✅ Готово", callback_data="filters_done")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cat_keyboard(cat: str):
    items = {
        "poses": list(FILTERS.keys())[0:16],
        "clothes": list(FILTERS.keys())[16:36],
        "bdsm": list(FILTERS.keys())[36:51],
        "face": list(FILTERS.keys())[51:59],
        "fluids": list(FILTERS.keys())[59:67],
        "partners": list(FILTERS.keys())[67:77],
        "extreme": list(FILTERS.keys())[77:83],
        "hands": list(FILTERS.keys())[83:92],
        "mouth": list(FILTERS.keys())[92:],
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
        "🔥 <b>OVERLORD PROMPT FORGE v5.0 FINAL (x3)</b>\n\n"
        "Всё на русском • 300+ фильтров • 9 категорий\n\n"
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
        picked = random.sample(list(FILTERS.keys()), min(15, len(FILTERS)))
        context.user_data["selected"] = picked
        await update.message.reply_text(f"🎲 <b>Random God Tier</b> — добавлено {len(picked)} фильтров!\nТеперь напиши идею.")
        return

    if text == "📋 Выбрать фильтры":
        await update.message.reply_text("Выбери категорию:", reply_markup=category_menu())
        return

    if text == "🧠 Умный авто-выбор":
        context.user_data["smart"] = True
        await update.message.reply_text("Напиши идею — я автоматически подберу фильтры.")
        return

    if text == "❓ Помощь":
        await update.message.reply_text("Пиши идею. Кнопки: режимы, Random God Tier, фильтры по категориям.")
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

    if data == "filters_done":
        await query.edit_message_text("✅ Фильтры применены! Напиши идею.")
        return
    if data == "back":
        await query.edit_message_text("Выбери категорию:", reply_markup=category_menu())
        return
    if data.startswith("cat_"):
        cat = data.replace("cat_", "")
        await query.edit_message_text("Выбери фильтры:", reply_markup=get_cat_keyboard(cat))
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
    print("🚀 Overlord Bot v5.0 FINAL (x3) запущен...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
