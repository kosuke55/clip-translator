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
    def __init__(self, source='en', target='ja', mode='deepl',
                 split=0, remove_hyphen=0):
        print('source: {}\ntarget: {}\nmode: {} \nsplit: {} \nremove_hyphen: {}'.format(
            source, target, mode, split, remove_hyphen))
        self.source = source
        self.target = target
        self.mode = mode
        self.split = split
        self.remove_hyphen = remove_hyphen
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
        for w in word:
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
                if self.remove_hyphen:
                    text = text.replace('-', '')
                if self.split:
                    words = text.split(' ')
                    splited_words = []
                    for word in words:
                        if self.count_consecutive_uppper(word) < 2 \
                                and not any(map(str.isdigit, word)):
                            splited_words.append(wordninja.split(word))
                        else:
                            splited_words.append([word])
                    text = ''
                    for orig_word, word in zip(words, splited_words):
                        if len(word) == 1:
                            text += orig_word + ' '
                        else:
                            for i, w in enumerate(word):
                                if i == len(word) - 1:
                                    if ',' in orig_word:
                                        text += w + ', '
                                    if '.' in orig_word:
                                        text += w + '. '
                                else:
                                    text += w + ' '

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
    parser.add_argument('--split', '-sp', type=int,
                        help='Use wordninja split',
                        default=0)
    parser.add_argument('--remove_hyphen', '-rh', type=int,
                        help='Remove hypen',
                        default=0)
    args = parser.parse_args()

    translator = Translator(args.source, args.target,
                            args.mode, args.split, args.remove_hyphen)
    translator.run()


def run_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', PORT))
    s.send(''.encode())
    s.close()


if __name__ == '__main__':
    run_server()
