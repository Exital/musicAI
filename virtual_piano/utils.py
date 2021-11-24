notes_to_font = {'A': '&#40', 'B': '&#95', 'C': '&#37', 'D': '&#94', 'E': '&#38', 'F': '&#42', 'G': '&#41', 'cleff': '&#96', 'empty': '&#52'}


def str_to_notes(string: str):

    string_list = string.split(',')
    string_list.reverse()

    notes = ''
    for note in string_list:
        notes += notes_to_font[note]
    notes += notes_to_font['cleff']
    return notes
