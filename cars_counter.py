import re
import random
from patterns import *
from settings import *


def find_cars_count(final_object):
    cars_count = None
    cars_neutralka = find_neutralka_full(final_object)
    if cars_neutralka == RESULT_NEED_ASSIST:
        return cars_neutralka
    if cars_neutralka is not None:
        cars_count = cars_neutralka

    cars_count_by_place = get_cars_count_by_place(final_object)
    if cars_count_by_place == RESULT_NEED_ASSIST:
        return cars_count_by_place
    if cars_count_by_place is not None:
        if cars_count is None:
            cars_count = cars_count_by_place
        else:
            print('[find_cars_count] Many cars counts found after get_cars_count_by_place. Need assist.')
            final_object['cars_num'] = cars_count
            return RESULT_NEED_ASSIST

    cars_pusto = find_pusto(final_object['comment'])
    if cars_pusto == RESULT_NEED_ASSIST:
        return cars_pusto
    if cars_pusto is not None:
        if cars_count is None:
            cars_count = cars_pusto
        elif cars_neutralka is None:
            print('[find_cars_count] Many cars counts found after find_pusto. Need assist.')
            final_object['cars_num'] = cars_count
            return RESULT_NEED_ASSIST

    cars_palka_dnr = find_palka_dnr(final_object)
    if cars_palka_dnr == RESULT_NEED_ASSIST:
        return cars_palka_dnr
    if cars_palka_dnr is not None:
        if cars_count is None:
            cars_count = cars_palka_dnr
        else:
            print('[find_cars_count] Many cars counts found after find_palka_dnr. Need assist.')
            final_object['cars_num'] = cars_count
            return RESULT_NEED_ASSIST

    cars_povorot = find_povorot(final_object)
    if cars_povorot == RESULT_NEED_ASSIST:
        return cars_povorot
    if cars_povorot is not None:
        if cars_count is None:
            cars_count = cars_povorot
        else:
            print('[find_cars_count] Many cars counts found after find_povorot. Need assist.')
            final_object['cars_num'] = cars_count
            return RESULT_NEED_ASSIST

    cars_count_by_digits_and_range = cars_by_digits_and_range(final_object['comment'])
    if cars_count_by_digits_and_range == RESULT_NEED_ASSIST:
        return cars_count_by_digits_and_range
    if cars_count_by_digits_and_range is not None:
        if cars_palka_dnr is not None:
            cars_count = cars_palka_dnr + cars_count_by_digits_and_range
        elif cars_povorot is not None:
            cars_count = cars_povorot + cars_count_by_digits_and_range
        elif cars_count is not None or (cars_palka_dnr is not None and cars_povorot is not None):
            print('[find_cars_count] Many cars counts found after cars_by_digits_and_range. Need assist.')
            final_object['cars_num'] = cars_count
            return RESULT_NEED_ASSIST
        else:
            cars_count = cars_count_by_digits_and_range


    if cars_count:
        cars_count += random.randint(1, 2)

    print('[find_cars_count] Result:', cars_count)
    return cars_count


def is_input_object_consistent(final_object):
    if any([not bool(final_object['kpp_name']), not bool(final_object['way'])]):
        print('[is_input_object_consistent] Error: Not enough data (kpp_name, way) for logic')
        return False
    return True


def find_pattern_in_sentence(ptrn, msg):
    spans = [i.span() for i in re.finditer(ptrn, msg)]
    if len(spans) > 1:
        print('[find_pattern_in_sentence] Many items found. Need assist:', [msg[sp[0]: sp[1]] for sp in spans])
        return RESULT_NEED_ASSIST
    if not len(spans):
        print('[find_pattern_in_sentence] No items found.')
        return None
    print('[find_pattern_in_sentence] Founded item:', msg[spans[0][0]: spans[0][1]])
    return True


def find_pusto(msg):
    spans = [i.span() for i in re.finditer(PUSTO_MIX, msg)]
    if len(spans) > 1:
        print('[find_pusto] Many pusto found. Need assist:', [msg[sp[0]: sp[1]] for sp in spans])
        return RESULT_NEED_ASSIST
    if len(spans) == 1:
        print('[find_pusto] Found pusto text:', msg[spans[0][0]: spans[0][1]])
        return 0

    print('[find_pusto] No pusto found')
    return None


def find_neutralka_full(final_object):
    if not is_input_object_consistent(final_object):
        return None

    print('[find_neutralka_full] Matching:')
    fpis_result = find_pattern_in_sentence(NEUTRAL_FULL, final_object['comment'])
    if fpis_result == RESULT_NEED_ASSIST or fpis_result is None:
        return fpis_result

    cars_count = None
    if final_object['way'] == WAY_TO_DNR:
        print('[find_neutralka_full] Neutralka on the way to dnr. Need assist.')
        return RESULT_NEED_ASSIST
    elif final_object['kpp_name'] == KPP_NAMES[0]:
        cars_count = CARS_COUNT_NEUTRAL_USPEN
    elif final_object['kpp_name'] == KPP_NAMES[1]:
        cars_count = CARS_COUNT_NEUTRAL_MARIN
    elif final_object['kpp_name'] == KPP_NAMES[2]:
        cars_count = CARS_COUNT_NEUTRAL_NOVOAZ
    elif final_object['kpp_name'] == KPP_NAMES[3]:
        print('[find_neutralka_full] Neutralka on the kpp shramko. Need assist.')
        cars_count = RESULT_NEED_ASSIST
    return cars_count


def find_povorot(final_object):
    if not is_input_object_consistent(final_object):
        return None

    print('[find_povorot] Matching:')
    fpis_result = find_pattern_in_sentence(POVOROT, final_object['comment'])
    if fpis_result == RESULT_NEED_ASSIST or fpis_result is None:
        return fpis_result

    cars_count = None
    if final_object['kpp_name'] == KPP_NAMES[0]:
        if final_object['way'] == WAY_TO_RF:
            cars_count = CARS_COUNT_USPEN_TO_RF_POVOROT
        else:
            cars_count = CARS_COUNT_USPEN_TO_DNR_POVOROT
    if final_object['kpp_name'] == KPP_NAMES[1]:
        if final_object['way'] == WAY_TO_RF:
            cars_count = CARS_COUNT_MARIN_TO_RF_POVOROT
        else:
            cars_count = CARS_COUNT_MARIN_TO_DNR_POVOROT
    if final_object['kpp_name'] == KPP_NAMES[2]:
        if final_object['way'] == WAY_TO_RF:
            cars_count = CARS_COUNT_NOVOAZ_TO_RF_POVOROT
        else:
            cars_count = CARS_COUNT_NOVOAZ_TO_DNR_POVOROT
    if final_object['kpp_name'] == KPP_NAMES[3]:
        print('[find_povorot] Povorot on the kpp shramko. Need assist.')
        cars_count = RESULT_NEED_ASSIST

    print('[find_povorot] Result:', cars_count)
    return cars_count


def find_palka_dnr(final_object):
    print('[find_palka_dnr] Matching:')
    fpis_result = find_pattern_in_sentence(EX_PALKA, final_object['comment'])
    if fpis_result == RESULT_NEED_ASSIST or fpis_result is None:
        return fpis_result

    if not final_object['way']:
        final_object['way'] = WAY_TO_RF

    if not is_input_object_consistent(final_object):
        return None

    cars_count = None
    if final_object['way'] == WAY_TO_DNR:
        print('[find_palka_dnr] Palka_dnr on the way to dnr. Need assist.')
        cars_count = RESULT_NEED_ASSIST
    elif final_object['kpp_name'] == KPP_NAMES[0]:
        cars_count = CARS_COUNT_PALKA_DNR_USPEN
    elif final_object['kpp_name'] == KPP_NAMES[1]:
        cars_count = CARS_COUNT_PALKA_DNR_MARIN
    elif final_object['kpp_name'] == KPP_NAMES[2]:
        cars_count = CARS_COUNT_PALKA_DNR_NOVOAZ
    elif final_object['kpp_name'] == KPP_NAMES[3]:
        print('[find_palka_dnr] Palka_dnr on the kpp shramko. Need assist.')
        cars_count = RESULT_NEED_ASSIST
    return cars_count


def find_place_name(final_object):
    msg = final_object['comment']
    # print('[find_place_name] place msg:', msg)
    places = (
        {'gostinica': 'гостиниц|столов|кафе|душевы'},
        {'moyka': 'мойк'},
        {'zapravka': 'заправк|азс|луко'},
        {'sklad': r'склад|овощебаз|овощн\D+ баз'},
        {'most_pochti': r'почти\D{,8} мост'},
        {'most': r'мост'},
        {'kust': 'куст'},
        {'ostanovka': 'остановк|коне?ц[ае]? (магазинов|ларьков)'},
        {'spusk': 'спуск'},
        {'post_gai': 'пост(а|ом)? гаи'},
        {'stella': 'стелл'},
        {'vyselki': fr'до поворота на {VYSELKI}'},
    )
    ptrn = ''
    key_place = ''
    finded_places = []
    for place in places:
        for key_place in place:
            ptrn = place[key_place]
        spans = [i.span() for i in re.finditer(ptrn, msg)]
        if len(spans) > 1:
            print('[find_place_name] Many same places found. Need assist:', [msg[sp[0]: sp[1]] for sp in spans])
            return RESULT_NEED_ASSIST
        if len(spans) == 1:
            print('[find_place_name] Finded place text:', msg[spans[0][0]: spans[0][1]])
            if key_place == 'most' and 'most_pochti' in finded_places:
                continue
            finded_places.append(key_place)
    if len(finded_places) > 1:
        print('[find_place_name] Finded many place names. Need assist:', finded_places)
        return RESULT_NEED_ASSIST
    if len(finded_places) == 1:
        print('[find_place_name] Finded place name:', finded_places[0])
        return finded_places[0]

    return None


def get_cars_count_by_place(final_object):
    cars_count = None

    place_name = find_place_name(final_object)
    if place_name == RESULT_NEED_ASSIST:
        return place_name
    if not place_name:
        return None

    match place_name:
        case 'gostinica':
            if not final_object['way']:
                final_object['way'] = WAY_TO_DNR
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_DNR:
                print('[get_cars_count_by_place] Gostinica not on the kpp Uspenka to dnr. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_GOSTINICA
        case 'moyka':
            if not final_object['way']:
                final_object['way'] = WAY_TO_DNR
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_DNR:
                print('[get_cars_count_by_place] Moyka not on the kpp Uspenka to dnr. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_MOYKA
        case 'sklad':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Sklad not on the kpp Uspenka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_SKLAD
        case 'most':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Most not on the kpp Uspenka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_MOST
        case 'most_pochti':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Pochti most not on the kpp Uspenka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_MOST_POCHTI
        case 'kust':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[1] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Kust not on the kpp Marinovka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_KUST
        case 'ostanovka':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Ostanovka not on the kpp Uspenka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_OSTANOVKA
        case 'stella':
            if final_object['kpp_name'] != KPP_NAMES[1]:
                print('[get_cars_count_by_place] Stella not on the kpp Marinovka. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_STELLA
        case 'spusk':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[1] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Spusk not on the kpp Marinovka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_SPUSK
        case 'post_gai':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[2] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Post GAI not on the kpp Novoaz to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_POST_GAI
        case 'zapravka':
            if final_object['kpp_name'] == KPP_NAMES[0]:
                if not final_object['way']:
                    final_object['way'] = WAY_TO_RF
                if final_object['way'] == WAY_TO_RF:
                    cars_count = CARS_COUNT_ZAPRAVKA_USPEN_TO_RF
                else:
                    cars_count = CARS_COUNT_ZAPRAVKA_USPEN_TO_DNR
            if final_object['kpp_name'] == KPP_NAMES[1]:
                print('[get_cars_count_by_place] Zapravka on the kpp Marinovka. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            if final_object['kpp_name'] == KPP_NAMES[2]:
                if final_object['way'] == WAY_TO_RF:
                    print('[get_cars_count_by_place] Zapravka on the kpp Novoaz to rf. Need assist.')
                    cars_count = RESULT_NEED_ASSIST
                else:
                    cars_count = CARS_COUNT_ZAPRAVKA_NOVOAZ_TO_DNR
            if final_object['kpp_name'] == KPP_NAMES[3]:
                print('[get_cars_count_by_place] Zapravka on the kpp shramko. Need assist.')
                cars_count = RESULT_NEED_ASSIST
        case 'vyselki':
            if not final_object['way']:
                final_object['way'] = WAY_TO_RF
            if final_object['kpp_name'] != KPP_NAMES[0] or final_object['way'] != WAY_TO_RF:
                print('[get_cars_count_by_place] Vyselki not on the kpp Uspenka to RF. Need assist.')
                cars_count = RESULT_NEED_ASSIST
            else:
                cars_count = CARS_COUNT_VYSELKI

    print('[get_cars_count_by_place] Result', cars_count)
    return cars_count


def cars_by_digits_and_range(msg):
    """ Распознавание количества по словам, цифрам, и диапазону из цифр и слов """
    ptrn_digit_word = fr'{"|".join(CARS_COUNT_WORDS)}|\d+'
    digits_iter_results = [i for i in re.finditer(ptrn_digit_word, msg)]
    if len(digits_iter_results) > 2:
        print(
            '[cars_by_digits_and_range] More than two digits found. Need assist:',
            [msg[ir.span()[0]: ir.span()[1]] for ir in digits_iter_results]
        )
        return RESULT_NEED_ASSIST

    if len(digits_iter_results) == 1:
        for dr in digits_iter_results:
            result = str_to_int(msg[dr.span()[0]: dr.span()[1]])
            print('[cars_by_digits_and_range] Result:', result)
            return result

    ptrn_range = fr'(?P<r1>{ptrn_digit_word})(?! ?[,\.] ?)\D{{1,4}}(?P<r2>{ptrn_digit_word})'
    range_iter_results = [i for i in re.finditer(ptrn_range, msg)]
    if len(range_iter_results) > 1:
        print(
            '[cars_by_digits_and_range] More than one range found. Need assist:',
            [msg[ir.span()[0]: ir.span()[1]] for ir in range_iter_results]
        )
        return RESULT_NEED_ASSIST

    if len(range_iter_results) == 1:
        for rng in range_iter_results:
            num_from_range = number_from_range(rng)
            print('[cars_by_digits_and_range] Result:', num_from_range)
            return num_from_range

    if len(digits_iter_results) == 2:
        print(
            '[cars_by_digits_and_range] Two digits found but not range. Need assist:',
            [msg[ir.span()[0]: ir.span()[1]] for ir in digits_iter_results]
        )
        return RESULT_NEED_ASSIST

    return None


def number_from_range(find_range_object):
    frg1 = find_range_object.group('r1')
    frg2 = find_range_object.group('r2')
    # print('frg1, frg2', frg1, frg2)
    if not all([frg1, frg2]):
        print('[number_from_range] Range error. Need assist:', frg1, frg2)
        return RESULT_NEED_ASSIST

    r1 = str_to_int(frg1)
    r2 = str_to_int(frg2)
    if not all([r1, r2]) or r2 <= r1:
        print('[number_from_range] Range error. Need assist:', r1, r2)
        return RESULT_NEED_ASSIST
    print('[number_from_range] Range digits:', r1, r2)
    result = r1 + abs((round((r2 - r1) / 2)))
    print('[number_from_range] Result:', result)
    return result


def str_to_int(msg):
    i = 1
    for w in CARS_COUNT_WORDS:
        r = re.match(w, msg)
        if r:
            return i
        i += 1

    r = re.match(r'\d+', msg)
    if not r:
        return None
    return int(r.group(0))

