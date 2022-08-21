from gtts import gTTS
from art import tprint
import pdfplumber
from pathlib import Path
import pyttsx3
import json

def pdf_to_mp3(start_page: int, file_path='test.pdf', language='en'):

    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':

        print(f'[+] Original file: {Path(file_path).name}')
        print(f'[+] Original file: {start_page}')
        print('[+] Processing...')

        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text()
                     for page in pdf.pages[start_page - 1:start_page]]

        text = ''.join(pages)
        text = text.replace('\n', '')

        # Конвертация целого файла целеком в mp3.
        # my_audio = gTTS(text=text, lang=language, slow=False)
        # file_name = Path(file_path).stem
        # my_audio.save(f'{file_name}.mp3')
        # return f'[+] {file_name}.mp3 saved successfully!\n---Have a good day!---'

        converter = pyttsx3.init()
        # Set properties before adding
        # Sets speed percent
        # Can be more than 100
        converter.setProperty('rate', 280)
        # Set volume 0-1
        converter.setProperty('volume', 1)
        converter.setProperty(
            'voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_ruRU_PavelM')

        # Queue the entered text
        # There will be a pause between
        # each one like a pause in
        # a sentence

        # read text in page.
        converter.say(text)

        # read custom text.
        # converter.say("""
        #                """)

        # Convert text in page to mp3.
        # converter.save_to_file(text, '1.mp3')

        converter.runAndWait()

    else:
        return "The file doesn't exist, check the file path!"


def main():
    tprint('PDF>>TO>>MP3', font='bulbhead')

    while True:
        with open("config.json", mode="r+") as data:
            config = json.load(data)
            file_path = config.get("file_path")
            l_pages = config.get("l_pages")
            language = 'ru'
            while language not in ("en", "ru"):
                language = input("Choose language, for example 'en' or 'ru': ")
            print(pdf_to_mp3(file_path=file_path,
                  start_page=l_pages, language=language))
            config["l_pages"] = l_pages + 1
        with open("config.json", mode='w') as f:
            f.write(json.dumps(config))


if __name__ == '__main__':
    main()
