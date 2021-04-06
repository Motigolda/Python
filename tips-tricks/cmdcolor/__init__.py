from os import system

colors = {
    'Black': 0,
    'Blue': 1,
    'Green': 2,
    'Aqua': 3,
    'Red': 4,
    'Purple': 5,
    'Yellow': 7,
    'Gray': 8,
    'LightBlue': 9,
    'LightGreen': 'a',
    'LightAqua': 'b',
    'LightRed': 'c',
    'LightPurple':'d',
    'LightYellow':'e',
    'BrightWhite':'f'
}

def change_text_color(color):
    if color in colors.values():
        system("color " + str(color))

def change_bg_and_text_color(bg_color, text_color):
    if bg_color != text_color and bg_color in colors.values() and text_color in colors.values():
        system("color " + str(bg_color) + str(text_color))

def set_default_color():
    system('color f')

def print_colors():
    for color in colors.keys():
        print(color)

def main():
    print("This little file is helping you to change the color of cmd.")
    print("Sometimes all you need as a programmer is a new color.")

if __name__ == "__main__":
    main()