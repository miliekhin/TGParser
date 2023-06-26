import re
from patterns import *


def clean_trucks(msg):
    # match_obj = re.search(DIGITS, msg)
    # if match_obj:
    #     print('[clean_trucks] Can\'t clean trucks as found digits in message.')
    #     return msg
    msg = clean_trucks_by_pattern(msg)
    msg = re.sub(GRUZ_CLEAN, '', msg).replace('  ', ' ')
    print('[clean_trucks] Clean trucks result:', msg)
    return msg


def clean_trucks_by_pattern(msg):
    p1 = fr'(грузовы[хе]|фуры?).{{1,10}}(мост|пост|заправ|луко|столов|поворот|гостиниц|кафе|душевы|мойк|азс' \
         fr'|склад|овощ|спуск)?.{{1,10}}{D_RANGE}'
    p2 = fr'(грузовы[хе]|фур) (шт\.?(ук)?|машин)? ?({D_RANGE}|нет|ноль|полоса пустая)'
    p3 = fr'{D_RANGE} фур'
    p4 = fr'(грузовы[хе]|фуры?) ?{D_RANGE} ?(шт\.?(ук)?|машин)?'
    ptrns = (
        {
            'ptrn_gruz': p1,
            'ptrn_full': fr'легковы[хе].+{p1}',
        },
        {
            'ptrn_gruz': p2,
            'ptrn_full': fr'{D_RANGE} (машин|авто(мобилей)?)? ?легковы[хе].+{p2}',
        },
        {
            'ptrn_gruz': p2,
            'ptrn_full': fr'легковы[хе] машины? {D_RANGE}.+{p2}',
        },
        {
            'ptrn_gruz': p3,
            'ptrn_full': fr'{D_RANGE} легковы[хе] машин.+{p3}',
        },
        {
            'ptrn_gruz': p2,
            'ptrn_full': fr'{p2}.+легковы[хе]',
        },
        {
            'ptrn_gruz': p3,
            'ptrn_full': fr'{p3}.+{D_RANGE} (легковы|авто)',
        },
        {
            'ptrn_gruz': p4,
            'ptrn_full': fr'{p4}',
        },
    )

    found = None
    for ptrn in ptrns:
        res = re.search(ptrn['ptrn_full'], msg)
        if res:
            sp = res.span()
            found = msg[sp[0]: sp[1]]
            msg = re.sub(ptrn['ptrn_gruz'], '', msg).replace('  ', ' ')
            break

    if found:
        print('[clean_trucks_by_pattern] pattern found:', found)

    return msg


def clean_invalid_data(msg):
    msg = re.sub(CLEANER_MIX, '', msg).replace('  ', ' ')
    print('[clean_invalid_data] Cleaned message:', msg)
    return msg

