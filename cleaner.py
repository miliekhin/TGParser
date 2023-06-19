import re
from patterns import *


def clean_trucks(msg):
    # match_obj = re.search(DIGITS, msg)
    # if match_obj:
    #     print('[clean_trucks] Can\'t clean trucks as found digits in message.')
    #     return msg
    msg = re.sub(GRUZ_CLEAN, '', msg).replace('  ', ' ')
    print('[clean_trucks] Clean trucks result:', msg)
    return msg


def clean_invalid_data(msg):
    msg = re.sub(CLEANER_MIX, '', msg).replace('  ', ' ')
    print('[clean_invalid_data] Cleaned message:', msg)
    return msg

