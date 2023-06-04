import random as r
import tkinter as tk


class MyButton:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.command = lambda: change_text(self.text)
        self.Object = tk.Button(root, text=self.text, command=self.command, width=2, height=1, font=('Helvectica', 8),
                                bg='grey', fg='white')
        self.Object.place(x=x, y=y)


def change_text(new_text):
    global active_column, active_row, paused
    if paused:
        return
    warning_label.config(text='')
    if active_column == 5:
        return
    active_label = labels[active_row * 5 + active_column]
    active_label.config(text=new_text)
    active_column += 1


def enter_command():
    global active_column, active_row, WORD, is_clearable, paused
    if paused:
        return
    user_word = list(map(lambda a: a['text'], labels[(active_row*5):(active_row*5)+active_column]))
    if len(user_word) != 5:
        warning_label.config(text='Too short')
        backspace_command(full_row=True)
        return
    if ''.join(user_word).lower() == WORD:
        warning_label.config(text='You won!')
        paused = True
        for i in range(5):
            labels[active_row * 5 + i].config(bg='green')
        is_clearable = True
        again_button.config(bg='grey', fg='white')
        return
    if ''.join(user_word).lower() not in DATABASE:
        warning_label.config(text='Not in word list')
        backspace_command(full_row=True)
        return
    not_letters, correct_letters, correct_pos_letters = [], [], []
    user_word = ''.join(user_word)
    user_word = user_word.lower()
    for i in range(5):
        if user_word[i] not in WORD:
            not_letters.append(i)
            continue
        if (user_word[i] in WORD) and (user_word[i] != WORD[i]):
            correct_letters.append(i)
            continue
        if user_word[i] == WORD[i]:
            correct_pos_letters.append(i)
            continue
        print('analysis error')
    letters_yellowed = []
    for i in not_letters:
        butt = buttons[KEYBOARD.index(user_word[i].upper())]
        butt.Object.config(bg='#111111')
        labels[active_row * 5 + i].config(bg='#111111')
    for i in correct_letters:
        if (user_word.count(user_word[i]) <= letters_yellowed.count(user_word[i])) \
                and (user_word.count(user_word[i]) > correct_pos_letters.count(user_word[i])):#fix that shit
            butt = buttons[KEYBOARD.index(user_word[i].upper())]
            butt.Object.config(bg='#111111')
            labels[active_row * 5 + i].config(bg='#111111')
            continue
        butt = buttons[KEYBOARD.index(user_word[i].upper())]
        butt.Object.config(bg='#ab922c')
        labels[active_row * 5 + i].config(bg='#ab922c')
        letters_yellowed.append(user_word[i])
    for i in correct_pos_letters:
        butt = buttons[KEYBOARD.index(user_word[i].upper())]
        letters_yellowed.append(user_word[i])
        butt.Object.config(bg='green')
        labels[active_row * 5 + i].config(bg='green')
    active_row += 1
    active_column = 0
    if active_row == 5:
        warning_label.config(text=f'Correct word was "{WORD}"')
        paused = True
        is_clearable = True
        again_button.config(bg='grey', fg='white')


def backspace_command(full_row = False):
    global active_column, active_row, paused
    if paused:
        return
    if full_row:
        active_column = 0
        for i in range(5):
            labels[active_row * 5 + i].config(text='')
        return
    if active_column == 0:
        return
    labels[active_row*5 + active_column-1].config(text='')
    active_column -= 1


def clear_field():
    global active_column, active_row, is_clearable, WORD, paused
    if not is_clearable:
        return
    for i in range(25):
        buttons[i].Object.config(bg='grey')
        labels[i].config(text='', bg='#707070')
    active_row = active_column = 0
    is_clearable = False
    again_button.config(bg='#111111', fg='grey')
    warning_label.config(text='')
    WORD = r.choice(DATABASE)
    paused = False


DATABASE = open('Database.txt', 'r').read().split(sep='\n')
KEYBOARD = open('Keys.txt', 'r').read()
WORD = r.choice(DATABASE)
# WORD = 'aabbc'
active_row = 0
active_column = 0
labels = []
buttons = []
is_clearable = False
paused = False
# if input('Print correct word? y/n') == 'y':
#     print(WORD)
# else:
#     print('OK')

root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry('400x500')
root.config(bg='#191919')
Main_label = tk.Label(root, text='Wordle!', bg='#191919', fg='white', font=('Helvectica', 25))
Main_label.pack()
warning_label = tk.Label(root, text='', font=('Helvectica', 11), height=1, width=25, bg='#191919', fg='white')
warning_label.place(x=83, y=300)
enter_button = tk.Button(root, text='Enter', command=lambda: enter_command(), height=1, width=6, font=('Helvectica', 8),
                         bg='grey', fg='white')
enter_button.place(x=256, y=400)
backspace_button = tk.Button(root, text='←', command=lambda: backspace_command(), height=1, width=2,
                             font=('Helvectica', 8), bg='grey', fg='white')
backspace_button.place(x=292, y=375)
again_button = tk.Button(root, text="Play again", bg='#111111', fg='grey', width=11, height=1, font=('Helvectica', 8),
                         command=lambda: clear_field())
again_button.place(x=160, y=450)

for i in range(26):
    if i < 10:
        x = 23 * i + 85
        y = 350
    elif i < 19:
        x = 23 * (i - 10) + 85
        y = 375
    else:
        x = 23 * (i - 19) + 95
        y = 400
    b = str(i)
    a = MyButton(x, y, KEYBOARD[i])
    buttons.append(a)

for i in range(25):
    labels.append(tk.Label(root, bg='#707070', width=2, height=1, fg='white', font=('Helvectica', 14)))
    labels[i].place(x=30 * (i % 5) + 125, y=50 * (i // 5) + 60)

root.mainloop()
# ←
