import pygame
from Speech_to_Speech import recognize_speech, text_to_speech
from googletrans import Translator
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 900
window_height = 900  # Increased height for language selection and displays
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Speech-to-Speech App")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

# Button dimensions
button_width = 150
button_height = 50

# Create buttons
start_button = pygame.Rect((window_width - button_width) // 2, 50, button_width, button_height)
stop_button = pygame.Rect((window_width - button_width) // 2, 120, button_width, button_height)

# Language selection buttons (two columns)
language_buttons_source = []
language_buttons_target = []
# Thêm các ngôn ngữ mới vào danh sách
languages = ["Vietnamese", "Japanese", "English", "French", "Spanish", "Korean: 한국어", "Chinese: 中文", "German: Deutsch", "Italian: Italiano", "Portuguese: Português", "Russian: Русский", "Arabic: العربية", 
             "Hindi: हिन्दी", "Chinese (Simplified): 中文（简体）", "Spanish: Español", "Thai: ไทย", "Indonesian: Bahasa Indonesia", "Dutch: Nederlands", "Swedish: Svenska", "Turkish: Türkçe"] 

for i, lang in enumerate(languages):
    button_source = pygame.Rect(20, 200 + i * 60, button_width, button_height)
    button_target = pygame.Rect(window_width - button_width - 20, 200 + i * 60, button_width, button_height)
    language_buttons_source.append(button_source)
    language_buttons_target.append(button_target)

# Button labels
font = pygame.font.Font(None, 36)
start_text = font.render("Start Listening", True, black)
stop_text = font.render("Stop", True, black)
language_texts = [font.render(lang, True, black) for lang in languages]

# Language displays
display_source_lang = "Vietnamese"
display_target_lang = "Japanese"
source_lang_display = pygame.Rect(20, 0, button_width, button_height)
target_lang_display = pygame.Rect(window_width - button_width - 20, 0, button_width, button_height)
source_lang_text = font.render(display_source_lang, True, black)
target_lang_text = font.render(display_target_lang, True, black)

# Initial language
source_lang = "vi"
target_lang = "ja"

# Initialize translator
translator = Translator()

# Translation history
translation_history = []

#từ điển
## dừng
stop_phrase = {'dừng lại', '停止', 'stop', 'arrêt', 'detener', '멈추다', '停止', 'stoppen', 'fermare', 'parar', 'останавливаться', 'قف', 'रुकना', 'หยุด', 'berhenti', 'stop', 'stopp', 'durmak'}
## thoát khỏi ứng dụng
exit_phrase = {'thoát khỏi ứng dụng', 'アプリケーションを終了する', 'exit the application', "quitter l'application", 'salir de la aplicación', '응용 프로그램 종료', '退出应用程序', 
               'Beenden Sie die Anwendung', "uscire dall'applicazione", 'saia do aplicativo', 'выйти из приложения', 'الخروج من التطبيق', 'एप्लिकेशन से बाहर निकलें', 'ออกจากแอปพลิเคชัน', 
               'keluar dari aplikasi', 'verlaat de applicatie', 'a      avsluta applikationen', 'uygulamadan çık'}

# Main loop
running = True
is_recording = False
stamp = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                is_recording = True
                print("Start recording...")
            if stop_button.collidepoint(event.pos):
                is_recording = False
                print("Stop recording.")

            # Xử lý chọn ngôn ngữ nguồn
            for i, button in enumerate(language_buttons_source):
                if button.collidepoint(event.pos):
                    if i == 0:  # Vietnamese
                        source_lang = "vi"
                        display_source_lang = "Vietnamese"
                    elif i == 1:  # Japanese
                        source_lang = "ja"
                        display_source_lang = "Japanese"
                    elif i == 2:  # English
                        source_lang = "en"
                        display_source_lang = "English"
                    elif i == 3:  # French
                        source_lang = "fr"
                        display_source_lang = "French"
                    elif i == 4:  # Spanish
                        source_lang = "es"
                        display_source_lang = "Spanish"
                    elif i == 5:  # Korean
                        source_lang = "ko"
                        display_source_lang = "Korean: 한국어"
                    elif i == 6:  # Chinese
                        source_lang = "zh-CN"  # Simplified Chinese
                        display_source_lang = "Chinese: 中文"
                    elif i == 7:  # German
                        source_lang = "de"
                        display_source_lang = "German: Deutsch"
                    elif i == 8:  # Italian
                        source_lang = "it"
                        display_source_lang = "Italian: Italiano"
                    elif i == 9:  # Portuguese
                        source_lang = "pt"
                        display_source_lang = "Portuguese: Português"
                    elif i == 10: # Russian
                        source_lang = "ru"
                        display_source_lang = "Russian: Русский"
                    elif i == 11: # Arabic
                        source_lang = "ar"
                        display_source_lang = "Arabic: العربية"
                    elif i == 12: # Hindi
                        source_lang = "hi"
                        display_source_lang = "Hindi: हिन्दी"
                    elif i == 13: # Chinese (Simplified)
                        source_lang = "zh-CN" 
                        display_source_lang = "Chinese (Simplified): 中文（简体）"
                    elif i == 14: # Spanish
                        source_lang = "es"
                        display_source_lang = "Spanish: Español"
                    # ... (thêm các điều kiện cho các ngôn ngữ mới khác nếu cần)
                    else: 
                        source_lang = translator.detect(languages[i]).lang
                        display_source_lang = languages[i]

                    # If already recording, restart with the new source language
                    if is_recording:
                        is_recording = False
                        pygame.mixer.music.stop()
                        is_recording = True
                        print("Start recording...")


                    # Update language display texts
                    source_lang_text = font.render(display_source_lang, True, black)

            # Xử lý chọn ngôn ngữ đích tương tự như trên
            for i, button in enumerate(language_buttons_target):
                if button.collidepoint(event.pos):
                    if i == 0:  # Vietnamese
                        target_lang = "vi"
                        display_target_lang = "Vietnamese"
                    elif i == 1:  # Japanese
                        target_lang = "ja"
                        display_target_lang = "Japanese"
                    elif i == 2:  # English
                        target_lang = "en"
                        display_target_lang = "English"
                    elif i == 3:  # French
                        target_lang = "fr"
                        display_target_lang = "French"
                    elif i == 4:  # Spanish
                        target_lang = "es"
                        display_target_lang = "Spanish"
                    elif i == 5:  # Korean
                        target_lang = "ko"
                        display_target_lang = "Korean: 한국어"
                    elif i == 6:  # Chinese
                        target_lang = "zh-CN"  # Simplified Chinese
                        display_target_lang = "Chinese: 中文"
                    elif i == 7:  # German
                        target_lang = "de"
                        display_target_lang = "German: Deutsch"
                    elif i == 8:  # Italian
                        target_lang = "it"
                        display_target_lang = "Italian: Italiano"
                    elif i == 9:  # Portuguese
                        target_lang = "pt"
                        display_target_lang = "Portuguese: Português"
                    elif i == 10: # Russian
                        target_lang = "ru"
                        display_target_lang = "Russian: Русский"
                    elif i == 11: # Arabic
                        target_lang = "ar"
                        display_target_lang = "Arabic: العربية"
                    elif i == 12: # Hindi
                        target_lang = "hi"
                        display_target_lang = "Hindi: हिन्दी"
                    elif i == 13: # Chinese (Simplified)
                        target_lang = "zh-CN" 
                        display_target_lang = "Chinese (Simplified): 中文（简体）"
                    elif i == 14: # Spanish
                        target_lang = "es"
                        display_target_lang = "Spanish: Español"
                    # ... (thêm các điều kiện cho các ngôn ngữ mới khác nếu cần)
                    else:
                        target_lang = translator.detect(languages[i]).lang
                        display_target_lang = languages[i]

                    # If already recording, restart with the new target language
                    if is_recording:
                        is_recording = False
                        pygame.mixer.music.stop()
                        is_recording = True
                        print("Start recording...")

                    # Update language display texts
                    target_lang_text = font.render(display_target_lang, True, black)

    # Fill the screen with white
    screen.fill(white)

    # Draw buttons
    pygame.draw.rect(screen, gray, start_button)
    screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
    pygame.draw.rect(screen, gray, stop_button)
    screen.blit(stop_text, (stop_button.x + 10, stop_button.y + 10))
    for i, button in enumerate(language_buttons_source):
        pygame.draw.rect(screen, gray, button)
        screen.blit(language_texts[i], (button.x + 10, button.y + 10))
    for i, button in enumerate(language_buttons_target):
        pygame.draw.rect(screen, gray, button)
        screen.blit(language_texts[i], (button.x + 10, button.y + 10))

    # Draw language displays
    pygame.draw.rect(screen, gray, source_lang_display)
    screen.blit(source_lang_text, (source_lang_display.x + 10, source_lang_display.y + 10))
    pygame.draw.rect(screen, gray, target_lang_display)
    screen.blit(target_lang_text, (target_lang_display.x + 10, target_lang_display.y + 10))

    # Speech recognition and translation
    if not pygame.mixer.music.get_busy():
        if is_recording:
            recognized_text = recognize_speech(lang=source_lang)
            if recognized_text:
                # Check for stop phrases in any language
                for lang_name in languages:
                    if recognized_text.lower() in exit_phrase:
                        running = False
                        break 
                    if recognized_text.lower() in stop_phrase:
                        is_recording = False
                        print("Stop recording.")
                        break 

                try:
                    # Translate if source language is not the target language
                    if source_lang != target_lang:
                        translated_text = translator.translate(recognized_text, src=source_lang, dest=target_lang).text
                        print(f"Translated: {translated_text}")
            

                    output_dir = os.path.dirname(os.path.abspath(__file__))
                    output_file = f"output_{stamp}.mp3"
                    output_path = os.path.join(output_dir, output_file)
                    text_to_speech(translated_text, output_dir, output_file, lang=target_lang[:2])

                    pygame.mixer.music.load(output_path)
                    pygame.mixer.music.play()

                    # Lấy đường dẫn thư mục chứa file code hiện tại
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                                        # Get today's date in YYYY-MM-DD format
                    today = datetime.now().strftime("%Y-%m-%d")

                    # Create file name with today's date
                    history_file_name = f"translation_history_{today}.txt"

                    # Tạo đường dẫn đầy đủ đến file lịch sử dịch thuật
                    history_file_path = os.path.join(current_dir, history_file_name)    

                    # Kiểm tra xem file đã tồn tại chưa, nếu chưa thì tạo mới
                    if not os.path.exists(history_file_path):
                        with open(history_file_path, "w", encoding="utf-8") as f:
                            pass  # Tạo file mới (chỉ cần mở ở chế độ ghi là đủ)

                    # Add to translation history and save to file
                    translation_history.append((recognized_text, translated_text))

                    with open(history_file_path, "a", encoding="utf-8") as f:
                        f.write(f"{source_lang}: {recognized_text}, {target_lang}: {translated_text}\n")

                    stamp = 1 - stamp
                except Exception as e:
                    print(f"Error during translation or speech synthesis: {e}")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
