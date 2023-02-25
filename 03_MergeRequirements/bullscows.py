import sys
import random
from urllib import request
from os.path import exists


def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    secret_letters = set(secret)
    guess_letters = set(guess)
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1
    for i in guess_letters:
        if i in secret_letters:
            cows += 1

    return (bulls, cows)


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def ask(prompt: str, valid: list[str] = None) -> str:
    res = input(prompt)
    if valid is None:
        return res
    else:
        while True:
            if res in valid:
                return res
            print('Неизвестное слово')
            res = input(prompt)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    count = 0
    while True:
        guess = ask('Введите слово: ', words)
        count += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if guess == secret:
            print(count)
            break


while True:
    if len(sys.argv) < 2:
        print('Пожалуйста, укажите словарь')
        exit()
    else:
        diction = []
        if exists(sys.argv[1]):
            with open(sys.argv[1], 'r') as f:
                diction = f.read().split()
        else:
            try:
                diction = request.urlopen(sys.argv[1]).read().decode().split()
            except Exception:
                raise ValueError('Словарь не найден')

        length = 5
        if len(sys.argv) > 2:
            try:
                if int(sys.argv[2]) > 0:
                    length = int(sys.argv[2])
            except Exception:
                raise ValueError('Wrong word-length format')

        diction = [word for word in diction if length == len(word)]

        gameplay(ask, inform, diction)
