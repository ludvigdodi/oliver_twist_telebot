import requests
import os
import sqlite3 as sq
from bs4 import BeautifulSoup as bs

# прописываем свой хедер чтоб не приняи нас за бота
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
}


# Парсимо текст
url = 'https://www.gutenberg.org/cache/epub/730/pg730-images.html'


def parser(url):
    req = requests.get(url)
    soup = bs(req.text, "html.parser")
    text = soup.find_all('p')
    return [s.get_text(strip=True) for s in text]

sentences = parser(url)

with sq.connect('sentences.db') as con:
    cur = con.cursor()

    # cur.execute("DROP TABLE sentences_2")
    cur.execute('''CREATE TABLE IF NOT EXISTS sentences(
        sentence INTEGER
        )''')
    for s in sentences:
        if s:
            cur.execute("INSERT INTO sentences VALUES (?)", (s,))

    # cur.execute("SELECT * FROM users WHERE score < 1000 AND old IN(19, 32)")
    # result = cur.fetchall()
    # print(result)

    # fatchmany(3) перші три записи
    # fetchone() - перша запись

# with sq.connect('sentences.db') as con:
#     cur = con.cursor()

#     sentences = cur.execute("SELECT * FROM sentences_1")
    
# for sentence in sentences:
#     print(sentence)