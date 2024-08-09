import speech_recognition as sr
from gtts import gTTS
import datetime
import os
import pygame

def recognize_speech(lang='vi-VN'):
    """
    Hàm này sử dụng microphone để ghi âm và chuyển đổi thành văn bản.
    """

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Đang nghe................")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=lang)
        print("Bạn nói: " + text)
        return text
    except sr.UnknownValueError:
        print("Không thể hiểu được âm thanh")
        return None
    except sr.RequestError as e:
        print("Lỗi khi yêu cầu dịch vụ nhận dạng giọng nói; {0}".format(e))
        return None

def text_to_speech(text, output_dir, output_file, lang='ch'):
    """
    Hàm này chuyển đổi văn bản thành âm thanh và lưu vào file mp3.
    """

    # Chuyển đổi văn bản thành âm thanh
    tts = gTTS(text, lang=lang)

    # Tạo đường dẫn đầy đủ cho tệp đầu ra
    output_path = os.path.join(output_dir, output_file)

    # Lưu âm thanh thành file mp3
    tts.save(output_path)
    #print(f"Đã chuyển đổi và lưu thành công vào '{output_path}'")

    return output_path  # Trả về đường dẫn đến file âm thanh

if __name__ == "__main__":
    # Khởi tạo Pygame mixer
    pygame.mixer.init()

    stamp = 0

    while True:
        recognized_text = recognize_speech()
        if recognized_text:
            output_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = f"output_{stamp}.mp3"
            output_path = text_to_speech(recognized_text, output_dir, output_file)

            # Phát âm thanh sử dụng Pygame mixer
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()

            # Đảo ngược giá trị của stamp
            stamp = 1 - stamp

        user_input = input("Bạn có muốn tiếp tục không? (y/n): ")
        if user_input.lower() != 'y':
            break

    pygame.quit()
