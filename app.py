import langcodes
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, LangDetectException, detect
from nltk.tokenize import TreebankWordDetokenizer, wordpunct_tokenize
from spellchecker import SpellChecker

DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3

SPELL_LANGS = {
    "en", "es", "fr", "pt", "de",
    "ru", "ar", "eu", "lv", "nl"
}

TARGET_LANGS = {
    "Vietnamese": "vi",
    "English": "en",
    "French": "fr",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Spanish": "es",
    "German": "de",
}

EXAMPLES_T = [
    "Every morning, I drink a cup of coffee.",
    "Bonjour, comment allez-vous?",
    "Xin chao, hom nay troi dep qua.",
]

EXAMPLES_S = [
    "Yesturday, I recieveed a mesage from my freind.",
    "Definately a great oppurtunity.",
    "Je voudraiis allerr au marchee.",
]

# Lấy từ điển đúng ngôn ngữ
@st.cache_resource(show_spinner=False)
def get_spellchecker(code):
    return SpellChecker(language=code)

# Hiển thị tên ngôn ngữ cho người dùng
def language_name(code):
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or "Unknown"
    
# Nhận diện ngôn ngữ trước khi dịch
def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None

# Sửa lỗi chính tả
def fix_typos(text, code):
    spell = get_spellchecker(code) # Lấy từ điển của ngôn ngữ đó ra
    tokens = wordpunct_tokenize(text) # Tách câu thành danh sách các từ
    fixed = []
    for token in tokens: # Duyệt qua từng từ một
        if token.isalpha() and len(token) > 1: # Chỉ sửa những từ toàn chữ cái và dài hơn 1 ký tự (bỏ qua dấu câu như . ,)
            suggestion = spell.correction(token.lower()) or token # Gợi ý sửa lỗi chính tả
            suggestion = suggestion.title() if token.istitle() else suggestion # Giữ nguyên kiểu chữ
            suggestion = suggestion.upper() if token.isupper() else suggestion
            fixed.append(suggestion) # Thêm từ đã sửa vào danh sách
        else:
            fixed.append(token) # Nếu không phải từ cần sửa thì giữ nguyên
    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens # Ghép các từ lại thành câu hoàn chỉnh. Trả về True nếu có sửa từ nào, False nếu không sửa gì


# Pipeline dịch văn bản
def run_translation(text, target_code):
    raw = text.strip() # Xóa khoảng trắng thừa đầu/cuối
    if len(raw) < MIN_INPUT_LENGTH: 
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    source = detect_language(raw)
    if source is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if source == target_code:
        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": raw,
            "note": "Câu đã ở ngôn ngữ đích, không cần dịch.",
        }

    try:
        translated = GoogleTranslator(source=source, target=target_code).translate(raw)
    except Exception as e:
        return {"ok": False, "error": f"Lỗi dịch: {e}"}

    return {
        "ok": True,
        "source": language_name(source),
        "target": language_name(target_code),
        "translated": translated,
    }

# Pipeline sửa lỗi chính tả
def run_spellcheck(text):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    code = detect_language(raw)
    if code is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if code not in SPELL_LANGS:
        return {
            "ok": False,
            "error": f"pyspellchecker chưa hỗ trợ {language_name(code)} ({code}).",
        }

    fixed, changed = fix_typos(raw, code)
    return {
        "ok": True,
        "language": language_name(code),
        "fixed": fixed,
        "changed": changed,
    }
