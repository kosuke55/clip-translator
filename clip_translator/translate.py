#!/usr/bin/env python

import argparse
import socket
import subprocess
import sys
try:
    # Python 2
    from urllib import quote
except ImportError:
    # Python 3
    from urllib.parse import quote

import chromedriver_binary  # noqa
import pyperclip
import timeout_decorator
import wordninja
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PORT = 50001
BUFFER_SIZE = 1024


class Translator(object):
    def __init__(self, source='en', target='ja', mode='deepl',
                 split=0, remove_hyphen=0, remove_newline=0):
        print(
            'source: {}\ntarget: {}\nmode: {} \nsplit: {} \nremove_hyphen: {}'.format(
                source,
                target,
                mode,
                split,
                remove_hyphen))
        self.source = source
        self.target = target
        self.mode = mode
        self.split = split
        self.remove_hyphen = remove_hyphen
        self.remove_newline = remove_newline
        if mode == 'deepl':
            self.url = 'https://www.deepl.com/translator#{}/{}/{}'
        elif mode == 'google':
            self.url = 'https://translate.google.co.jp/?hl=ja#view=home&op=translate&sl={}&tl={}&text={}'
        options = Options()
        options.add_experimental_option(
            'prefs', {'intl.accept_languages': '{}'.format(self.target)})
        self.driver = webdriver.Chrome(options=options)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', PORT))
        self.driver_down = False

    @timeout_decorator.timeout(3)
    def accept(self):
        return self.socket.accept()

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

    def split_words(self, text):
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
                        if '.' in orig_word:
                            text += w + '. '
                        elif ',' in orig_word:
                            text += w + ', '
                        else:
                            text += w + ' '
                    else:
                        text += w + ' '
        return text

    def run(self):
        self.socket.listen(1)
        while True:
            if self.driver_down:
                self.driver.quit()
                self.socket.close()
                sys.exit()
            try:
                self.driver.get_window_position()
            except Exception:
                self.driver_down = True

            try:
                (connection, client) = self.accept()
            except Exception:
                continue

            try:
                print('Client connected', client)
                _ = connection.recv(BUFFER_SIZE)
                text = pyperclip.paste()
                text = text.replace('.', '. ').replace('  ', ' ')
                if self.remove_hyphen == 1:
                    text = text.replace('-\n', '')
                if self.remove_hyphen == 2:
                    text = text.replace('-', '')
                if self.remove_newline:
                    text = text.replace('\n', ' ')
                if self.split:
                    text = self.split_words(text)

                encoded_text = quote(text)
                if self.mode == 'deepl':
                    encoded_text = encoded_text.replace('%5C', '%5C%5C')
                    encoded_text = encoded_text.replace('%7C', '%5C%7C')

                self.driver.get(
                    self.url.format(self.source, self.target, encoded_text))
            finally:
                connection.close()
        self.driver.quit()
        self.socket.close()


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
    parser.add_argument('--remove-hyphen', '-rh', type=int,
                        help='Remove hypen.'
                        '1: Only hyphens at the end of sentences'
                        '2: All hyphens',
                        default=2)
    parser.add_argument('--remove-newline', '-rn', type=int,
                        help='Remove newline',
                        default=1)
    args = parser.parse_args()

    translator = Translator(args.source, args.target,
                            args.mode, args.split,
                            args.remove_hyphen, args.remove_newline)
    translator.run()


def run_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', PORT))
    s.send(''.encode())
    s.close()


def kill_server():
    p = subprocess.Popen('lsof -i :{}'.format(PORT).split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    pid = False
    for line in iter(p.stdout.readline, b''):
        if 'clip_t' in line:
            pid = line.split(' ')[1]
    if pid:
        cmd = 'kill {}'.format(pid)
        print(cmd)
        subprocess.call(cmd.split(' '))


if __name__ == '__main__':
    run_server()
