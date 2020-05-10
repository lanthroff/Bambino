try:
    f = open('char_selection.txt')
    print([f.read()])
except OSError as err:
    background = 'sprites/background.png'
