from googletrans import Translator
import datetime

translator = Translator()

# Define a dictionary to map language names to their codes
lang_name_to_code = {
    "Vietnamese": "vi",
    "Japanese": "ja",
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "Korean": "ko",
    "Chinese": "zh-CN",  # Assuming Simplified Chinese
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Hindi": "hi",
    "Thai": "th",
    "Indonesian": "id",
    "Dutch": "nl",
    "Swedish": "sv",
    "Turkish": "tr"
}

languages = list(lang_name_to_code.keys())  # Use the keys of the dictionary

stop_phrases = {}

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
print("Đang chạy................"+ timestamp)

for lang_name in languages:
    lang_code = lang_name_to_code[lang_name]  # Get the language code
    translated_phrase = translator.translate("thoát khỏi ứng dụng", src='vi', dest=lang_code).text
    stop_phrases[lang_code] = translated_phrase

print(stop_phrases.values())

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
print("Đang chạy................"+ timestamp)
