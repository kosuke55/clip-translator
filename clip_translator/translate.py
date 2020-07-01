#!/usr/bin/env python

import argparse
import socket
import urllib

import chromedriver_binary  # noqa
import pyperclip
import wordninja
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PORT = 50001
BUFFER_SIZE = 1024


class Translator(object):
    def __init__(self, source='en', target='ja', mode='deepl', split=False):
        print('source: {}\ntarget: {}\nmode: {}'.format(source, target, mode))
        self.source = source
        self.target = target
        self.mode = mode
        self.split = split
        if mode == 'deepl':
            self.url = 'https://www.deepl.com/translator#{}/{}/{}'
        elif mode == 'google':
            self.url = 'https://translate.google.co.jp/?hl=ja#view=home&op=translate&sl={}&tl={}&text={}'
        options = Options()
        options.add_experimental_option(
            'prefs', {'intl.accept_languages': '{}'.format(self.target)})
        self.driver = webdriver.Chrome(options=options)

    def count_consecutive_uppper(self, word):
        count = 0
        count_max = 0
        for i, w in enumerate(word):
            if str.isupper(w):
                count += 1
                if count > count_max:
                    count_max = count
            else:
                count = 0
        return count_max

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', PORT))
        s.listen(1)
        while True:
            (connection, client) = s.accept()
            try:
                print('Client connected', client)
                _ = connection.recv(BUFFER_SIZE)
                text = pyperclip.paste()
                text = text.replace('.', '. ').replace('  ', ' ')
                if self.split:
                    words = text.split(' ')
                    splited_words = []
                    for word in words:
                        if self.count_consecutive_uppper(word) < 2:
                            splited_words.append(wordninja.split(word))
                        else:
                            splited_words.append([word])
                    text = ''
                    for orig_word, word in zip(words, splited_words):
                        if len(word) == 1:
                            text += orig_word + ' '
                        else:
                            for i, w in enumerate(word):
                                text += w + ' '
                                if i == len(word) - 1:
                                    if ',' in orig_word:
                                        text += w + ', '
                                    if '.' in orig_word:
                                        text += w + '. '

                encoded_text = urllib.quote(text)
                self.driver.get(
                    self.url.format(self.source, self.target, encoded_text))
            finally:
                connection.close()
        s.close()


def run_server():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--source', '-s', type=str,
                        help='source language', default='en')
    parser.add_argument('--target', '-t', type=str,
                        help='target language', default='ja')
    parser.add_argument('--mode', '-m', type=str,
                        help='Translation site (deepl or google)',
                        default='deepl')
    args = parser.parse_args()

    translator = Translator(args.source, args.target, args.mode)
    translator.run()


def run_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', PORT))
    s.send(''.encode())
    s.close()


if __name__ == '__main__':
    run_server()
