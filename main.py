#!/usr/bin/env python3
"""
OVERLORD TELEGRAM BOT v10.0 — КОСПЛЕИ + МАКСИМАЛЬНО БОЛЬШОЕ КОЛИЧЕСТВО ОДЕЖДЫ
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

# ==================== ОГРОМНЫЙ СПИСОК ФИЛЬТРОВ ====================
FILTERS = {
    # === ПОЗИЦИИ (30+) ===
    "Поза сзади (Doggy Style) глубокая": "doggy style, from behind, ass up face down, deep hard penetration from behind, ass spread, ",
    "Матинг Пресс (Mating Press)": "mating press, legs folded back to chest, deep breeding position, body pressed down, ",
    "Миссионерская поза ноги широко": "missionary position, legs spread extremely wide, deep eye contact while fucking hard, ",
    "Она сверху (Cowgirl) прыгает": "cowgirl, riding cock hard, bouncing aggressively on dick, girl on top, tits bouncing, ",
    "Обратная наездница": "reverse cowgirl, ass facing viewer, riding cock reverse, ass bouncing, ",
    "Полный Нельсон": "full nelson, legs held up high and spread, extreme deep penetration, completely helpless, ",
    "Поза лёжа на животе (Prone Bone)": "prone bone, lying flat on stomach, deep hard fucking from behind, ass up slightly, ",
    "Стоя у стены поднятая": "wall sex, lifted and fucked hard against the wall, legs wrapped around, ",
    "На коленях руки за спиной": "on knees, hands tied behind back, fucked from behind while kneeling, ",
    "Сидя лицом к лицу": "sitting on cock face to face, intimate deep penetration, ",
    "Сидя спиной к партнёру": "sitting reverse, back to partner, deep penetration from below, ",
    "Стоя на одной ноге": "standing on one leg, other leg lifted, deep penetration, ",
    "На четвереньках голова вниз": "on all fours, head down ass up, deep from behind, ",
    "Сидя на краю стола": "sitting on edge of table, legs spread, deep penetration, ",
    "Поза ложки боковая": "spooning position, side sex, intimate but deep penetration, leg lifted, ",
    "Стоя согнутая": "standing doggy, bent over, standing sex from behind, hands on wall or floor, ",

    # === ОДЕЖДА + КОСПЛЕИ (50+ ВАРИАНТОВ) ===
    # Обычная одежда
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

    # Косплеи
    "Косплей Горничная (Maid)": "french maid outfit, black and white maid dress, frilly apron, maid headband, submissive maid, ",
    "Косплей Школьница": "sexy schoolgirl uniform, short pleated skirt, white blouse, loose tie, innocent but slutty schoolgirl, ",
    "Косплей Кошкодевочка (Neko)": "catgirl outfit, cat ears, tail, bell collar, cute neko maid, playful cat features, ",
    "Косплей Суккуб": "succubus costume, demon horns, tail, red/black leather outfit, seductive demonic beauty, ",
    "Косплей Готическая Лолита": "gothic lolita dress, black frilly dress, lace details, dark makeup, elegant gothic beauty, ",
    "Косплей Медсестра": "sexy nurse outfit, white nurse dress, nurse hat, stethoscope, naughty nurse, ",
    "Косплей Полицейская": "sexy policewoman uniform, tight police shirt, short skirt, police hat, handcuffs, dominant police girl, ",
    "Косплей Официантка": "sexy waitress outfit, short black dress, white apron, stockings, flirty waitress, ",
    "Косплей Стюардесса": "sexy flight attendant uniform, tight blouse, short skirt, stockings, seductive stewardess, ",
    "Косплей Спортивная форма": "sexy sportswear, tight sports bra, short shorts, athletic look, sweaty sporty girl, ",
    "Косплей Бикини": "tiny bikini, micro bikini, string bikini, barely covering anything, beach slut look, ",
    "Косплей Прозрачный пеньюар": "sheer transparent babydoll, see-through nightie, delicate lace, seductive nightwear, ",
    "Косплей Ролевая одежда": "sexy roleplay outfit, fantasy costume, revealing dress, erotic cosplay, ",
    "Косплей Офисная леди": "sexy office lady, tight blouse, pencil skirt, stockings, glasses, naughty secretary, ",
    "Косплей Чулки + Подвязки": "stockings with garter belt, lace top stockings, seductive legwear, elegant stockings, ",

    # === БДСМ (25+) ===
    "Полный БДСМ": "full BDSM session, ropes, cuffs, blindfold, completely restrained, ",
    "Ошейник + поводок": "collar with leash, pet collar, submissive collar, ",
    "Повязка на глаза": "blindfold, eye mask, black blindfold, ",
    "Руки связаны за спиной": "hands tied behind back, completely restrained while being fucked, ",
    "Надписи маркером на теле": "body writing, words like 'slut', 'cumdump', 'whore', 'breed me', 'free use' written on skin, ",
    "Сильная хумiliation": "heavy humiliation, dirty talk, being called degrading names, degraded, ",
    "Полностью сломана разумом": "completely mind broken, only exists to be used and fucked, empty expression, ",
    "Экстремальный пет-плей": "extreme pet play, treated like a dog or animal, collar, leash, behaving like pet, ",
    "Связана верёвками": "tied with ropes, shibari, intricate rope bondage, completely restrained, ",
    "Наручники": "handcuffs, metal cuffs, restrained with handcuffs, ",
    "Кляп во рту": "ball gag, mouth gag, gagged with ball, ",
    "Связана и используется": "tied up and used, completely helpless, multiple people using her, ",

    # === ВЫРАЖЕНИЯ ЛИЦА (15+) ===
    "Ахегао + сердечки в глазах": "ahegao, long tongue out, rolled back eyes, heart-shaped pupils, flushed face, mind break, pleasure overload, ",
    "Разум полностью сломан": "mind break, completely broken expression, empty glazed eyes, tongue lolling out, total pleasure overload, ",
    "Плачет от сильного удовольствия": "crying tears of pleasure, teary eyes, sobbing in ecstasy, mascara running down cheeks, ",
    "Оргазм на лице": "orgasm face, eyes rolling back hard, mouth wide open screaming in pleasure, tongue out, ",
    "Длинный язык вывалился": "long tongue hanging out far, excessive thick saliva dripping from long tongue, ",
    "Пустой взгляд + улыбка": "empty vacant eyes with a broken happy smile, completely mind broken, ",
    "Смущённая + яркий румянец": "heavy blushing, embarrassed but extremely aroused face, shy expression mixed with lust, ",

    # === ЖИДКОСТИ (15+) ===
    "Обильные густые слюни": "heavy excessive drooling, thick saliva strings, saliva dripping on breasts, face and thighs, messy wet face, ",
    "Мокрые блестящие выделения из киски": "wet aroused pussy, glistening vaginal juices, dripping arousal fluids, shiny wet swollen labia, ",
    "Сквирт / сильное фонтанирование": "squirting, powerful female ejaculation, fluids spraying out, wet mess everywhere, ",
    "Кремпай с вытекающей спермой": "creampie, cum overflowing from pussy, thick white cum dripping down thighs and ass, ",
    "Конча на лице и в волосах": "cum on face, thick facial, cum dripping from chin and nose, cum in hair, ",
    "Много спермы внутри + вздутие живота": "lots of cum inside, cum inflation, visible slight belly bulge from excessive cum, ",
    "Слюни + слёзы + выделения вместе": "mixed fluids, saliva + tears + pussy juices running down body, extremely messy, ",

    # === ПАРТНЁРЫ (МНОГО ВАРИАНТОВ) ===
    "Гангбанг": "gangbang, multiple men fucking one girl at the same time, used by many, ",
    "Двойное проникновение": "double penetration, two cocks in pussy or one in pussy one in ass, ",
    "Тройное проникновение": "triple penetration, three cocks filling all holes, completely stuffed, ",
    "Тентакли заполняют все дыры": "tentacles, multiple tentacles filling pussy, ass and mouth at the same time, ",
    "Монстр с огромным членом": "monster fucking, huge monster cock, extreme size difference, ",
    "Жеребячий член (Horse cock)": "horse cock, massive equine cock, extreme stretching and bulging, ",
    "Мускулистый накаченный мужчина": "muscular bodybuilder man, huge muscles, veiny arms, powerful physique, dominant muscular male, ",
    "Pet Play — девушка как собака": "pet play, girl acting like a dog, collar, leash, crawling on all fours, barking, tail plug, behaving like animal, ",
    "Огромный чернокожий мужчина": "bbc, big black cock, massive dark skinned muscular man, extreme size contrast, ",
    "Два мускулистых мужчины": "two muscular men, double teaming, two bodybuilders using one girl, ",
    "Толстый мужчина": "fat man, obese dominant male, big belly, heavy man fucking slim girl, size contrast, ",
    "Старый мужчина": "old man, elderly dominant male, wrinkled skin, grey hair, young girl with old man, ",

    # === ЭКСТРИМ РАЗМЕРЫ ===
    "Огромный член": "massive cock, extreme size, visible belly bulge from deep penetration, ",
    "Глубокий до живота": "cock bulging her stomach, visible bulge in belly, extreme deep penetration, ",
    "Слишком большой для неё": "cock too big, struggling to take it, belly bulge, pain and pleasure mix, ",
    "Растяжка киски до предела": "pussy stretched to the limit, extreme gape after, ",
    "Член виден через живот": "cock visible through stomach, extreme deep penetration, ",

    # === ДЕВУШКИ / ТИПАЖ ===
    "Блондинка": "beautiful blonde girl, long blonde hair, blue eyes, fair skin, ",
    "Брюнетка": "gorgeous brunette, long dark hair, brown eyes, seductive look, ",
    "Рыжеволосая": "stunning redhead, long red hair, green eyes, pale skin, freckles, ",
    "Азиатка": "beautiful asian girl, long black hair, dark eyes, petite body, ",
    "Школьница": "cute schoolgirl, short skirt, white blouse, innocent but slutty look, ",
    "Горничная": "sexy maid, french maid outfit, frilly dress, submissive maid, ",
    "Кошкодевочка": "catgirl, cat ears, tail, neko, cute cat features, ",
    "Суккуб": "succubus, demon girl, horns, tail, seductive demonic beauty, ",
    "Готическая девушка": "gothic girl, black hair, pale skin, dark makeup, black clothes, ",
    "Спортсменка": "athletic girl, fit body, toned muscles, sporty look, ",
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

    parts.append("hyper-detailed pussy and fluids, extreme wetness, raw sexual, perfect anatomy, sharp focus, masterpiece, maximum lewd detail and obscenity, 8k quality")

    text = " ".join(parts)
    full = ", ".join(p.strip() for p in text.split(",") if p.strip())

    summary = f"Короткое описание: {raw}. Промпт создаёт детальную эротическую сцену с выбранными элементами."

    return f"{summary}\n\n{full}"

def build_random_prompt_with_filters(selected: list) -> str:
    random_bases = [
        "beautiful young woman", "gorgeous girl", "sexy female", "stunning woman", 
        "cute girl", "hot babe", "seductive female", "innocent looking girl"
    ]
    random_appearances = [
        "long hair", "big breasts", "slim waist", "wide hips", "perfect body",
        "pale skin", "tanned skin", "athletic body", "curvy figure", "petite frame"
    ]
    
    base = random.choice(random_bases)
    appearance = random.choice(random_appearances)
    
    parts = [DIRTY_BASE, DETAIL, INTENSITY, f"{base} with {appearance}, "]
    
    for f in selected:
        if f in FILTERS:
            parts.append(FILTERS[f])
    
    parts.append("hyper-detailed pussy and fluids, extreme wetness, raw sexual, perfect anatomy, sharp focus, masterpiece, maximum lewd detail, 8k quality")
    
    text = " ".join(parts)
    full = ", ".join(p.strip() for p in text.split(",") if p.strip())
    
    summary = f"🎲 Random промпт с твоими фильтрами ({len(selected)} шт)"
    
    return f"{summary}\n\n{full}"

def smart_select(text: str) -> list:
    text = text.lower()
    res = []
    rules = {
        "Поза сзади (Doggy Style) глубокая": ["doggy", "сзади"],
        "Матинг Пресс (Mating Press)": ["mating press", "матинг пресс"],
        "Гангбанг": ["gangbang", "гангбанг"],
        "Тентакли заполняют все дыры": ["тентакл"],
        "Ахегао + сердечки в глазах": ["ahegao", "ахегао"],
        "Обильные густые слюни": ["слюни"],
        "Кремпай с вытекающей спермой": ["creampie", "кремпай"],
        "Прозрачные чулки до бёдер": ["чулк"],
        "Микро-юбка": ["юбк", "микро"],
        "Рваная одежда": ["рван", "torn"],
        "Ошейник + поводок": ["ошейник", "collar"],
        "Повязка на глаза": ["повязк", "blindfold"],
        "Мускулистый накаченный мужчина": ["muscular", "накаченн", "bodybuilder"],
        "Pet Play — девушка как собака": ["pet play", "собака", "dog", "petplay"],
        "Жеребячий член (Horse cock)": ["horse", "жеребяч"],
        "Полностью сломана разумом": ["mind break", "разум сломан"],
        "Блондинка": ["блондинк", "blonde"],
        "Брюнетка": ["брюнетк", "brunette"],
        "Азиатка": ["азиатк", "asian"],
        "Школьница": ["школьниц", "schoolgirl"],
        "Горничная": ["горничн", "maid"],
        "Кошкодевочка": ["кошкодевочк", "catgirl", "neko"],
        "Суккуб": ["суккуб", "succubus"],
        "Готическая девушка": ["готическ", "gothic"],
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
        [KeyboardButton("🎲 Random God Tier"), KeyboardButton("🎲 Random 15+ фильтров")],
        [KeyboardButton("🎲 Random с моими фильтрами"), KeyboardButton("📋 Фильтры")],
        [KeyboardButton("🧠 Умный авто"), KeyboardButton("❓ Помощь")]
    ], resize_keyboard=True)

def category_menu():
    keyboard = [
        [InlineKeyboardButton("🍆 Позиции", callback_data="cat_poses"),
         InlineKeyboardButton("👗 Одежда + Косплеи", callback_data="cat_clothes")],
        [InlineKeyboardButton("😈 БДСМ", callback_data="cat_bdsm"),
         InlineKeyboardButton("😈 Лицо", callback_data="cat_face")],
        [InlineKeyboardButton("💦 Жидкости", callback_data="cat_fluids"),
         InlineKeyboardButton("👹 Партнёры", callback_data="cat_partners")],
        [InlineKeyboardButton("👩 Девушки / Типаж", callback_data="cat_girls"),
         InlineKeyboardButton("✅ Готово", callback_data="done")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_filters_keyboard(cat: str):
    items = {
        "poses": list(FILTERS.keys())[0:16],
        "clothes": list(FILTERS.keys())[16:51],
        "bdsm": list(FILTERS.keys())[51:63],
        "face": list(FILTERS.keys())[63:70],
        "fluids": list(FILTERS.keys())[70:77],
        "partners": list(FILTERS.keys())[77:89],
        "girls": list(FILTERS.keys())[89:],
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
        "🔥 <b>OVERLORD BOT v10.0</b> — Косплеи + Максимум одежды\n\n"
        "Добавлено огромное количество косплеев и вариантов одежды.\n\n"
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
        await update.message.reply_text(f"🎲 Random God Tier — добавлено {len(picked)} фильтров!\nТеперь напиши идею.")
        return

    if text == "🎲 Random 15+ фильтров":
        picked = random.sample(list(FILTERS.keys()), min(20, len(FILTERS)))
        context.user_data["selected"] = picked
        await update.message.reply_text(f"🎲 Random 15+ фильтров — выбрано {len(picked)} случайных фильтров!\nТеперь напиши идею.")
        return

    if text == "🎲 Random с моими фильтрами":
        if not selected:
            await update.message.reply_text("Сначала выбери фильтры через «📋 Фильтры».")
            return
        prompt = build_random_prompt_with_filters(selected)
        await update.message.reply_text(f"✅ <b>Random промпт с твоими фильтрами:</b>\n\n<code>{prompt}</code>", parse_mode="HTML")
        return

    if text == "📋 Фильтры":
        await update.message.reply_text("Выбери категорию:", reply_markup=category_menu())
        return

    if text == "🧠 Умный авто":
        context.user_data["smart"] = True
        await update.message.reply_text("Напиши идею — я автоматически подберу фильтры.")
        return

    if text == "❓ Помощь":
        await update.message.reply_text("Пиши идею. Кнопки: режимы, Random God Tier, Random 15+, Random с моими фильтрами, Фильтры по категориям.")
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
    print("🚀 Overlord Bot v10.0 с Косплеями запущен...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
