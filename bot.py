import telebot
import requests
import os
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.environ.get("TOKEN"))

# Парсимо текст
url = 'https://www.gutenberg.org/cache/epub/730/pg730-images.html'


def parser(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    text = soup.find_all('p')
    return [s.get_text(strip=True) for s in text]


sentences = parser(url)


# Хендлер на команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id,
                     'Привіт ✋\n\nЯ󠁧󠁢󠁥󠁮󠁧󠁿 🤖, який допогає практикувати англійську 🏴󠁧󠁢󠁥󠁮󠁧󠁿 мову!\n\nНадішли мені '
                     'слово і я знайду кілька речень з ним у дуже відомому 📕 творі дуже відомого 🖋🧔 письменника.')


# Отримання повідомлень від користувача та виклик ф-ції обробки та складання відповіді
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, create_result_message(fill_matched_sentences(message)))


# Пошук речень
def fill_matched_sentences(message):
    random.shuffle(sentences)
    matched_sentences = []
    for sentence in sentences:
        sentence_txt = sentence
        if message.text in sentence_txt:
            matched_sentences = sentence_txt
    return matched_sentences


# Складання відповіді користувачеві
def create_result_message(matched_sentences: list) -> str:
    result_message = ""
    if not matched_sentences:
        result_message = "⛔ Вибач, я не знайшов речень з твоїм словом!!!\n\n❗ Воно точно англійське???  "
    if len(matched_sentences) >= 1:
        result_message = matched_sentences
    return result_message


# Запускаємо бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
