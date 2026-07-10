import re


# DOXXING DETECTION
DOXX_PATTERNS = [
    r'\+?[78]\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}',
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',          # phone numbers
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # emails
    r'\b\d{1,5}\s\w+\s(Street|St|Avenue|Ave|Road|Rd|Lane|Ln)\b',  # addresses
    r'real name is',
    r'her real name',
    r'his real name',
    r'they live in',
    r'found her address',
    r'found his address',
    r'found address',
    r'leaked face',
    r'exposing',
    r'past life', 
    r'素顔',       # Japanese: "real face"
    r'正体',       # Japanese: "true identity"
    r'本名',       # Japanese: "real name"
    r'住所',       # Japanese: "address"
    r'個人情報',   # "personal information"
    r'特定した',   # "identified them"
    r'晒す',       # "expose/publicly shame"
    r'凸待ち',     # "waiting to confront" 
    r'前世',       # "Zense" — прошлая жизнь 
    r'顔バレ',     # "Kao bare" — когда лицо случайно засветилось/слили
    r'実物',       # "Jitsubutsu" — как выглядит в реальной жизни
    r'卒アル',     # "Sotsuaru" — слив фото из школьного выпускного альбома
    r'裏垢',       # "Ura aka" — скрытый/приватный личный твиттер-аккаунт
    r"加工厨",       # "Kakou chuu" — "монстр автотюна" 
    r"調子乗るな",   # "Choushi noru na" — не выебывайся / знай свое место
    r"ウザい",       # "Uzai" — раздражаешь / бесишь
    r"ブス",         # "Busu" — урод/уродка 
    r"売名",         # "Baimei" — хайпожор / пиарится на других
    r"オワコン",     # "Owakon" — скатился / мертвый контент
    r'настоящее имя',
    r'живет в',
    r'слив лица',
    r'фото без маски'

]


# HATE SPEECH DETECTION
HATE_KEYWORDS_EN = [
    "kys", "kill yourself", "go die", "worthless",
    "garbage", "trash", "nobody likes you"
]

HATE_KEYWORDS_RU = [
    "умри", "убейся", "никчёмная", "мусор"
]

HATE_KEYWORDS_JP = [
    "死ね",    # "go die"
    "消えろ",  # "disappear"
    "気持ち悪い",  # "disgusting"
    "下手くそ",     # "Hetakuso" — криворукий
    "嫌い"        # "Kirai" — ненавижу
]

ALL_HATE_KEYWORDS = HATE_KEYWORDS_EN + HATE_KEYWORDS_RU + HATE_KEYWORDS_JP


# MAIN ANALYZER
def check_doxxing(text):
    for pattern in DOXX_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True, pattern
    return False, None

def check_hate_speech(text):
    text_lower = text.lower()
    found = [word for word in ALL_HATE_KEYWORDS if word in text_lower]
    return len(found) > 0, found

def analyze_message(author, text):
    result = {
        "author": author,
        "text": text,
        "flagged": False,
        "reasons": []
    }

    doxx, pattern = check_doxxing(text)
    if doxx:
        result["flagged"] = True
        result["reasons"].append(f"Doxxing pattern detected")

    hate, words = check_hate_speech(text)
    if hate:
        result["flagged"] = True
        result["reasons"].append(f"Hate speech: {words}")

    return result