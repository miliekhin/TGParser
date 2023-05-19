import re


def prepare_message(msg):
    print('[prepare_message] Original message:', msg)
    msg = msg.strip().lower().replace('c', 'с')
    msg = re.sub(r'"|\n|\r\n?', ' ', msg).replace('  ', ' ')
    msg = clean_rational_numbers(msg)
    print('[prepare_message] Prepared message:', msg)
    return msg


def clean_rational_numbers(msg):
    # Удаление рациональных чисел и символов
    msg = re.sub(r'\d+\.\d+\.\d+|\d+[,.:|]\d+( ?час)?|\d+\s?%', '', msg).replace('  ', ' ')

    # remove slashes
    # msg = re.sub(r'\d+[,.:/\\\|]\d+|\d+/|\d+\s?%', '', msg).replace('  ', ' ')
    return msg
