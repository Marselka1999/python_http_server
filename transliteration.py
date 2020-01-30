match_table = {
    'А': ['A'],   'а': ['a'],
    'Б': ['B'],   'б': ['b'],
    'В': ['V'],   'в': ['v'],
    'Г': ['G'],   'г': ['g'],
    'Д': ['D'],   'д': ['d'],
    'Е': ['E', 'Ye'],
    'е': ['e', 'ye'],
    'Ё': ['E', 'Yo'],
    'ё': ['e', 'yo'],
    'Ж': ['Zh'],  'ж': ['zh'],
    'З': ['Z'],   'з': ['z'],
    'И': ['I'],   'и': ['i'],
    'Й': ['J', 'Jj', 'I', 'Y'],
    'й': ['j', 'jj', 'i', 'y'],
    'К': ['K'],   'к': ['k'],
    'Л': ['L'],   'л': ['l'],
    'М': ['M'],   'м': ['m'],
    'Н': ['N'],   'н': ['n'],
    'О': ['O'],   'о': ['o'],
    'П': ['P'],   'п': ['p'],
    'Р': ['R'],   'р': ['r'],
    'С': ['S'],   'с': ['s'],
    'Т': ['T'],   'т': ['t'],
    'У': ['U'],   'у': ['u'],
    'Ф': ['F'],   'ф': ['f'],
    'Х': ['H', 'Kh'],
    'х': ['h', 'kh'],
    'Ц': ['C', 'Ts'],   
    'ц': ['c', 'ts'],
    'Ч': ['Ch'],  'ч': ['ch'],
    'Ш': ['Sh'],  'ш': ['sh'],
    'Щ': ['Shch', 'Shh'],
    'щ': ['shch', 'shh'],
    'Ъ': [''],    'ъ': [''],
    'Ы': ['Y'],   'ы': ['y'],
    'Ь': ['\''],  'ь': ['\''],
    'Э': ['E'],   'э': ['e'],
    'Ю': ['Yu'],  'ю': ['yu'],
    'Я': ['Ya'],  'я': ['ya'],
}

def translit(russian_string: str):
    '''
    Find transliterations of russian word according to the transliteration table.
    Arguments:
    - russian_string: cyrillic russian word.
    Return:
    List of possible transliterations.
    '''

    def translit_recursive(prefix, rest_part):
        # prefix - transliterated part of string
        result = []
        for i in range(len(rest_part)):
            symbol = rest_part[i]
            if symbol not in match_table: # Skip non-letter characters
                prefix += symbol
            else:
                for next_symbol in match_table[symbol]:
                    # "fork" for letters with multiple transliterations
                    result.extend(translit_recursive(prefix+next_symbol, rest_part[i+1:]))
                return result
        return [prefix]
    
    return translit_recursive('', russian_string)

        