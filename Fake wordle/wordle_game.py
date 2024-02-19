################################################################################
# Words can be from 4 to 10 chars
# 4-5 5-6 6-6 7-7 8-7 9-8 10-8   (number of letters - numeber of possible guesses)
################################################################################

import random
import re
import PySimpleGUI as sg

guess_has_to_be_on_list = 1
debugging = 1

def read_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().split()

def select_random_word(words):
    return random.choice(words)

def convert_to_english(word):
    replacements = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ü': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'Ü': 'U',
    }
    for spanish_letter, english_letter in replacements.items():
        word = word.replace(spanish_letter, english_letter)
    return word.upper()

filename = "Fake wordle\Guessing_words.txt" 
words = read_words(filename)
num_words = len(words)

clean_words = [convert_to_english(word) for word in words if re.match("^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+$", word)]
removed_words = [word for word in words if convert_to_english(word) not in clean_words]
words = clean_words
words = set(words)
words = list(words)
if removed_words:
    print(f"Removed {(removed_words)} words containing non-alphabetic characters.")

random_word = select_random_word(words)
if debugging:
    print(f"Randomly selected word: {random_word}")


max_pass_size = 10
turno = 0
max_turno = -1
Size_password = len(random_word)
cursor = 0
# 4-5 5-6 6-6 7-7 8-7 9-8 10-8   (number of letters - numeber of possible guesses)
if Size_password == 4:
    max_turno = 5
elif Size_password in [5,6]:
    max_turno = 6
elif Size_password in [7,8]:
    max_turno = 7
elif Size_password in [9,10]:
    max_turno = 8
else: max_turno = 6

color_teclas = ('black','grey')
color_IN = ('black','white')
color_correct = ('snow','green')
color_yellow = ('black','yellow')
color_grey = ('snow','grey25')
color_interface = ('white','grey30')

sg.theme('LightGrey1')

# Define the layout
input_box = []
alpha = 'abcdefghijklmnop'
for letter in alpha:
    input_box.append([sg.Button(size=(3,1),expand_x=True,expand_y=True,visible = False, key=f'-{letter}{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN) for _ in range(max_pass_size)]) #HARDCODE MAX 10 LETTERS

layout = [
    [sg.Text("CONORDLE", font=("Helvetica", 20))],
    input_box,
    [sg.VerticalSeparator()],
    [sg.Button(letter, size=(3,1),expand_x=True,expand_y=True,button_color = color_teclas) for letter in 'ABCDEFG'],
    [sg.Button(letter, size=(3,1),expand_x=True,expand_y=True,button_color = color_teclas) for letter in 'HIJKLMN'],
    [sg.Button(letter, size=(3,1),expand_x=True,expand_y=True,button_color = color_teclas) for letter in 'ÑOPQRST'],
    [sg.Button(letter, size=(3,1),expand_x=True,expand_y=True,button_color = color_teclas) for letter in 'UVWXYZ⌫'],
    [sg.Button('Enter', size=(10, 2),button_color = color_interface),sg.Button('New Game', size=(10, 2),visible=False,button_color = color_interface)]
]
# Create the window
window = sg.Window("Wordle Interface", layout, layout,margins=(100, 10),finalize=True,element_justification='center', resizable=True,return_keyboard_events=1,use_default_focus=False)
for x in range(Size_password):
    window[f'-a{x}-'].update(visible=True)

attemp = []
tracker = []
end = 0

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    elif (event.upper() in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ') and (cursor < Size_password):
        window[f'-{alpha[turno]}{cursor}-'].update(event.upper())
        cursor += 1
        attemp.append(event.upper())

    elif (event == '⌫' or event == 'BackSpace:8') and cursor > 0 and end == 0:
        cursor -= 1
        attemp.pop()
        window[f'-{alpha[turno]}{cursor}-'].update('')

    elif event in ['Enter','\r'] and cursor == Size_password:
        if guess_has_to_be_on_list and ''.join(attemp) not in words:
            pass
        else:
            tracker = []
            for i in range(Size_password):
                letter = attemp[i]
                if letter in random_word: #Se peude optimizar
                    if letter == random_word[i]:
                        window[f'-{alpha[turno]}{i}-'].update(button_color = color_correct ,disabled_button_color=color_correct )
                        window[letter].update(button_color = color_correct ,disabled_button_color=color_correct )
                        tracker.append(letter)
                    
                else:
                    window[f'-{alpha[turno]}{i}-'].update(button_color = color_grey,disabled_button_color=color_grey)
                    window[letter].update(button_color = color_grey,disabled_button_color=color_grey)
            ### (no) WIN condition ###
            if len(tracker) != Size_password:
                for i in range(Size_password):
                    letter = attemp[i]
                    if letter in random_word and letter != random_word[i]:
                        if  tracker.count(letter) < list(random_word).count(letter):
                            window[f'-{alpha[turno]}{i}-'].update(button_color = color_yellow,disabled_button_color=color_yellow)
                            window[letter].update(button_color = color_yellow,disabled_button_color=color_yellow)
                            tracker.append(letter)

                        elif  tracker.count(letter) == list(random_word).count(letter):
                            window[f'-{alpha[turno]}{i}-'].update(button_color = color_grey,disabled_button_color=color_grey)

                turno +=1
                if turno < max_turno:
                    for x in range(Size_password):
                        window[f'-{alpha[turno]}{x}-'].update(visible=True)
                else:
                    if end == 0:
                        sg.popup(f'Perdiste\nLa palabra era {random_word}')
                        window['New Game'].update(visible=True)
                        end = 1
                attemp = []
                cursor = 0
            else:
                #FIN
                if end == 0:
                    # sg.popup('Ganaste')
                    window['New Game'].update(visible=True)
                    end = 1
    elif event == 'New Game':
        if len(words)!=0:
            words.remove(random_word)
        if len(words)== 0:
            sg.popup('No mas palabras')

        else: 
            random_word = select_random_word(words)    
            Size_password = len(random_word)
            if debugging:
                print(f"Randomly selected word: {random_word}")
            for w in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
                window[w].update(button_color = color_teclas)
            for l in alpha:
                for n in range(max_pass_size):
                    window[f'-{l}{n}-'].update('')
                    window[f'-{l}{n}-'].update(button_color = color_IN ,disabled_button_color = color_IN )
                    window[f'-{l}{n}-'].update(visible = False)
            
            for x in range(Size_password):
                window[f'-a{x}-'].update(visible=True)
            window['New Game'].update(visible = False)
            turno = 0
            cursor = 0
            end = 0
            attemp = []

window.close()