# -*- coding: utf-8 -*-
"""scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UY6CuKsMTr4Bw3gPgto0P1r_ISiYW8Xg
"""

import requests
from bs4 import BeautifulSoup

response = input("Did you update the page number (y/n)?: ")



""" Lists for the details to collect"""

urls = []
titles_english = []
titles_malayalam = []
lyrics_list = []
singer_list = []
musician_list = []
lyricist_list = []
movie_list = []

""" Collecing the urls and Song English titles"""

def collect_urls(soup):
  music_div = soup.find('div', class_='view-music-homepage')
  music_spans = music_div.find_all('span', class_='field-content')
  for i in music_spans:
    titles_english.append(i.a.get("href").replace("/lyric/", "").replace("-", " "))
    urls.append("https://m3db.com" + i.a.get("href"))

for i in range(3, 4):
  url = f'https://m3db.com/music?page={i}'
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  collect_urls(soup)

""" Collecting the details"""

for url in urls:
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  title = soup.find('h1', id = 'page-title')
  lyrics = soup.find('div', property='content:encoded')
  singer = soup.find('div', property="schema:byArtist")
  music_by = soup.find('div', property="schema:composer")
  lyrics_by = soup.find('div', property="schema:lyricist")
  movie = soup.find('div', property="schema:inAlbum")

  titles_malayalam.append(title.text)
  lyrics_list.append(lyrics)
  singer_list.append(singer.a.get('href').replace("/", "").replace("-", " "))
  musician_list.append(music_by.a.get('href').replace("/", "").replace("-", " "))
  lyricist_list.append(lyrics_by.a.get('href').replace("/", "").replace("-", " "))
  movie_list.append(movie.a.get('href').replace("/film/", "").replace("-", " "))

for i in range(len(titles_english)):
  titles_english[i] = " ".join([word.title() for word in titles_english[i].split()])
  singer_list[i] = " ".join([word.title() for word in singer_list[i].split()])
  musician_list[i] = " ".join([word.title() for word in musician_list[i].split()])
  lyricist_list[i] = " ".join([word.title() for word in lyricist_list[i].split()])
  movie_list[i] = " ".join([word.title() for word in movie_list[i].split()])

""" Saving the details in a file"""

with open("details.txt", "a") as file:
  for i in range(len(titles_english)):
    file.write(singer_list[i] + '\n')
    file.write(musician_list[i] + '\n')
    file.write(lyricist_list[i] + '\n')
    file.write(titles_english[i] + '\n')
    file.write(titles_malayalam[i] + '\n')
    file.write(movie_list[i] + '\n')

with open("lyrics.txt", "a") as file:
    for i in range(len(lyrics_list)):
      file.write(str(lyrics_list[i]))
