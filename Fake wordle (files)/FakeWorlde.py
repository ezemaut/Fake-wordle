from random import choice
from PySimpleGUI import Window, Button,theme, Text,theme_background_color, Column,WINDOW_CLOSED,popup
from playsound import playsound
from re import match

#########################
Title = 'WORDLE?'       #
Fullscreen = False      # Change as needed
debugging = 1           #
#########################



def read_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().split()

def select_random_word(words):
    return choice(words)

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

filename = r"Guessing_words.txt" 
temp = read_words(filename)

num_words = len(temp)
if debugging:
    print(f"There are {num_words} words in the file.")

words= []
for line in (temp):
    words.append(line.split(','))

clean_words = []
removed_words = []
duplicates = []
count = 1
gate = 0

for line in words:
    palabra = line[0]
    try:
        music = line[1]
    except: music = 0
    if music == '0':
        music = 0
    if match("^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+$", palabra):
        clean = convert_to_english(palabra)
        if clean not in duplicates:
            clean_words.append([clean,music])
            duplicates.append(clean)
        else: print(f'{clean}/{palabra} line:{count} is already added.')
    else: removed_words.append(palabra)
    count +=1

if removed_words:
    print(f"Removed {(removed_words)} words containing non-alphabetic characters.")

words = clean_words


max_pass_size = 10 #HARDCODE MAX 10 LETTERS
turno = 0
max_turno = -1
min_turns = 6

def Reset():
    global cursor
    global max_turno
    global Debug_max_turns
    global Size_password
    global Random_list
    global random_word
    global sound

    Random_list = select_random_word(words)
    random_word = Random_list[0]
    sound = Random_list[1]

    if debugging:
        print(f"Randomly selected word: {random_word}")
    Size_password = len(random_word)

    cursor = 0
    # 4-5 5-6 6-6 7-7 8-7 9-8 10-8   (number of letters - numeber of possible guesses)
    if Size_password == 4:
        max_turno = min_turns
    elif Size_password in [5,6]:
        max_turno = min_turns+1
    elif Size_password in [7,8]:
        max_turno = min_turns+2
    elif Size_password in [9,10]:
        max_turno = min_turns+2
    else: max_turno = min_turns

    Debug_max_turns = min_turns+2

def musica():
    relative_path = "audios/" 
    if sound:
        try:   
            playsound(relative_path + sound)
        except:
            print(f'{sound} File failed to load')
            

Reset()

theme('LightGrey4')
color_teclas = ('black','grey')
color_IN = ('black','white')
color_correct = ('snow','green')
color_yellow = ('black','yellow')
color_grey = ('snow','grey25')
color_interface = ('white','grey30')
color_lifes = ('gold','none')

screen_width, screen_height = Window.get_screen_size()
button_size_1 = (5,1)
button_size_2 = (10,1)
font_size0 = int(screen_height / 35)  # Adjust as needed
font_size = int(screen_height / 70)  # Adjust as needed


alpha = 'abcdefgh'

# Define the layout
layoutGame = [
    [Text(f"{Title}", font=("Helvetica", font_size0),text_color=('black'))],
    [Button(size=button_size_1, key=f'-a{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-b{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-c{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-d{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-e{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-f{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-g{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button(size=button_size_1, key=f'-h{_}-',disabled=True,button_color = color_IN,disabled_button_color = color_IN,font=('Helvetica', font_size))for _ in range(max_pass_size)],
    [Button('', size=button_size_1,button_color = (theme_background_color(),theme_background_color()),border_width=0,disabled=True)],
    [Button(f'{max_turno}',key='Lifes' ,size=button_size_2,button_color = color_interface,disabled_button_color = color_lifes, disabled=True,font=('Helvetica', font_size))],
    [Button(letter, size=button_size_1,button_color = color_teclas,font=('Helvetica', font_size)) for letter in 'ABCDEFGHI'],
    [Button(letter, size=button_size_1,button_color = color_teclas,font=('Helvetica', font_size)) for letter in 'JKLMNÑOPQ'],
    [Button(letter, size=button_size_1,button_color = color_teclas,font=('Helvetica', font_size)) for letter in 'RSTUVWXYZ⌫'],
    [Button('Enter',key='Enter', size=button_size_2,button_color = color_interface,font=('Helvetica', font_size)),Button('New Game', size=button_size_2,visible=False,button_color = color_interface,font=('Helvetica', font_size))]
]
# Create the window
layout2 = Column(layoutGame, visible=False, key='-COL2-',element_justification='center')
layout = [[layout2,]]

window = (Window("", layout, layout,margins=(100, 0),finalize=True,element_justification='center',no_titlebar = Fullscreen,
                     resizable=True,return_keyboard_events=1,use_default_focus=False, scaling=1.7,icon = r"Icon.ico"))
window.Maximize()

for x in range(max_pass_size):
    for char in alpha[:Debug_max_turns]:
     window[f'-{char}{x}-'].update(visible=False)

for x in range(Size_password):
    window[f'-a{x}-'].update(visible=True)

window['-COL2-'].update(visible=True)

attemp = []
tracker = []
end = 0

while True:
    event, values = window.read()
    if event == WINDOW_CLOSED:
        break

    elif (event.upper() in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ') and (cursor < Size_password):
        window[f'-{alpha[turno]}{cursor}-'].update(event.upper())
        cursor += 1
        attemp.append(event.upper())

    elif (event == '⌫' or event == 'BackSpace:8') and cursor > 0 and end == 0:
        cursor -= 1
        attemp.pop()
        window[f'-{alpha[turno]}{cursor}-'].update('')

    elif event == 'New Game' or event == '\r' and end ==1:
        musica()
        if len(words)!=0:
            words.remove(Random_list)
        if len(words)== 0 and gate == 0:
            popup('No more words')
            sound = 0
            gate = 1
        elif len(words)== 0 and gate == 1:
            gate = 0
        else:    
            Reset()
            window['Enter'].update(visible=True)
            window['Lifes'].update(f'{max_turno}')

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


    elif event in ['Enter','\r'] and cursor == Size_password:
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
            window['Lifes'].update(f'{max_turno-turno}')
            if turno < max_turno:
                for x in range(Size_password):
                    window[f'-{alpha[turno]}{x}-'].update(visible=True)
            else:
                if end == 0:
                    popup(f'You lost\nThe word was {random_word}')
                    window['New Game'].update(visible=True)
                    end = 1
            attemp = []
            cursor = 0
        else:
            #FIN
            if end == 0:
                window['Enter'].update(visible=False)
                window['New Game'].update(visible=True)
                end = 1
    

window.close()