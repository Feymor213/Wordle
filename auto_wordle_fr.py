import time
import PIL.ImageGrab
import pyautogui
import webbrowser
import random
import Fuck_wordle_2


# https://www.nytimes.com/games/wordle/index.html
# yellow - 145, 144, 45; green - 68, 125, 61; grey - 44, 44, 46 - real wordle
# green = (121, 184, 81), yellow = (243, 194, 55), grey = (164, 174, 196), white = (255, 255, 255) - training wordle
# SAMPLE_COORDINATES = (
#     ((790, 280), (870, 280), (950, 280), (1030, 280), (1110, 280)),
#     ((790, 365), (870, 365), (950, 365), (1030, 365), (1110, 365)),
#     ((790, 450), (870, 450), (950, 450), (1030, 450), (1110, 450)),
#     ((790, 535), (870, 535), (950, 535), (1030, 535), (1110, 535)),
#     ((790, 620), (870, 620), (950, 620), (1030, 620), (1110, 620)),
#     ((790, 705), (870, 705), (950, 705), (1030, 705), (1110, 705)),
# ) - real wordle
COLOR_VALUE_CODES = {
    (68, 125, 61): 'correct',
    (145, 144, 45): 'partially_correct',
    (44, 44, 46): 'incorrect'
}
SAMPLE_COORDINATES = (
    ((790, 280), (870, 280), (950, 280), (1030, 280), (1110, 280)),
    ((790, 365), (870, 365), (950, 365), (1030, 365), (1110, 365)),
    ((790, 450), (870, 450), (950, 450), (1030, 450), (1110, 450)),
    ((790, 535), (870, 535), (950, 535), (1030, 535), (1110, 535)),
    ((790, 620), (870, 620), (950, 620), (1030, 620), (1110, 620)),
    ((790, 705), (870, 705), (950, 705), (1030, 705), (1110, 705)),
)
remaining_letters = 'qwertyuiopasdfghjklzxcvbnm'
prohibited_letters_positions = ['', '', '', '', '']

def approximate_color_of(given_color, deviation=40):
    matches = []
    for i in COLOR_VALUE_CODES.keys():
        for j in range(3):
            if abs(given_color[j] - i[j]) > deviation:
                break
        else:
            matches.append(i)
    if len(matches) != 1:
        raise Exception('Color match fault: '+str(matches))
    return matches[0]


def get_pixel_colour(i_x, i_y):
    return PIL.ImageGrab.grab().load()[i_x, i_y]


def getstate(level):
    coords = SAMPLE_COORDINATES[level]
    result = []
    for i in coords:
        result.append(COLOR_VALUE_CODES[approximate_color_of(get_pixel_colour(*i))])
    return tuple(result)


def step(step_n):
    global word, remaining_letters, prohibited_letters_positions
    if step_n == 0:
        with open('Database.txt') as D:
            word = random.choice(D.read().split())
    else:
        template = ''
        state = getstate(step_n - 1)
        must_include = ''
        for i in range(5):
            if state[i] == 'incorrect':
                remaining_letters = remaining_letters.replace(word[i], '')
                template += '*'
            elif state[i] == 'partially_correct':
                must_include += word[i]
                template += '*'
                prohibited_letters_positions[i] += word[i]
            elif state[i] == 'correct':
                template += word[i]
            else:
                raise Exception
        for i in must_include:
            if i not in remaining_letters:
                remaining_letters += i
        for i in template:
            if (i != '*') and i not in remaining_letters:
                remaining_letters += i
        for i in Fuck_wordle_2.compile_words(remaining_letters, must_include, template, only_one_result=False):
            for j in range(5):
                if i[j] in prohibited_letters_positions[j]:
                    break
            else:
                word = i
                break
        else:
            raise Exception
    pyautogui.write(word, interval=0.2)
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(7)

webbrowser.open('https://www.nytimes.com/games/wordle/index.html')
time.sleep(7)
for i in range(6):
    step(i)
