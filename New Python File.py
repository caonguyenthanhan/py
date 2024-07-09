from gtts import gTTS

def text_to_speech(input_file, output_file, lang='vi'):
    # Đọc nội dung từ tập tin văn bản
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Chuyển đổi văn bản thành âm thanh
    tts = gTTS(text, lang=lang)

    # Lưu âm thanh thành file mp3
    tts.save(output_file)
    print(f"Đã chuyển đổi và lưu thành công vào '{output_file}'")

# Gọi hàm để chuyển đổi và lưu âm thanh
input_file = r'C:\Users\ACER\Desktop\văn bản sang mp3\input.txt'
output_file = r'C:\Users\ACER\Desktop\văn bản sang mp3\output3.mp3'
text_to_speech(input_file, output_file)
