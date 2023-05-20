import re
from patterns import *
from settings import *
from preparator import prepare_message
from cleaner import clean_invalid_data
from cleaner import clean_trucks
from cars_counter import find_cars_count
from cars_counter import cars_by_digits_and_range


def get_final_object(msg):
    print('--------------------------------')
    print('Start getting final object')
    raw_msg = msg
    msg = prepare_message(msg)
    final_object = dict(FINAL_OBJECT)

    final_object['comment'] = msg
    if find_by_pattern(final_object):
        final_object['recognition_result'] = RESULT_ACCEPT
        final_object['comment'] = raw_msg
        return final_object

    if is_msg_unacceptable(msg):
        return final_object
    msg = clean_invalid_data(msg)
    msg = clean_trucks(msg)
    final_object['comment'] = msg

    kpp_name = find_kpp(msg)
    if not kpp_name:
        final_object['comment'] = raw_msg
        return final_object
    final_object['kpp_name'] = kpp_name

    result_find_way = find_way(final_object)
    if result_find_way in [RESULT_NEED_ASSIST, RESULT_BAD_MSG]:
        final_object['recognition_result'] = result_find_way
        final_object['comment'] = raw_msg
        return final_object
    final_object['way'] = result_find_way

    result_cars_count = find_cars_count(final_object)
    if result_cars_count == RESULT_NEED_ASSIST:
        final_object['recognition_result'] = RESULT_NEED_ASSIST
        final_object['comment'] = raw_msg
        return final_object
    if result_cars_count is not None:
        final_object['cars_num'] = result_cars_count

    if is_some_need_assist_conditions_exists(msg):
        final_object['recognition_result'] = RESULT_NEED_ASSIST
        final_object['comment'] = raw_msg
        return final_object

    if result_cars_count is None:
        final_object['recognition_result'] = RESULT_BAD_MSG
        final_object['comment'] = raw_msg
        return final_object

    final_object['comment'] = raw_msg
    final_object['recognition_result'] = RESULT_ACCEPT
    return final_object


def find_by_pattern(final_object):
    msg = final_object['comment']
    for ptrn_map in HARD_PATTERNS:
        match_obj = re.search(ptrn_map['ptrn'], msg)
        if match_obj:
            sp = match_obj.span()
            print('[find_by_pattern] Found pattern:', msg[sp[0]: sp[1]])
            final_object['way'] = ptrn_map['way']
            if not ptrn_map['kpp_name']:
                final_object['kpp_name'] = find_kpp(msg)
                if not final_object['kpp_name']:
                    print('[find_by_pattern] No kpp name found.')
                    return False
            else:
                final_object['kpp_name'] = ptrn_map['kpp_name']

            if ptrn_map['cars_num'] != -1:
                final_object['cars_num'] = ptrn_map['cars_num']
            else:
                digit = cars_by_digits_and_range(msg)
                if not isinstance(digit, int):
                    print('[find_by_pattern] cars_by_digits_and_range return not integer')
                    return False
                final_object['cars_num'] = digit
            return True

    print('[find_by_pattern] No patterns found.')
    return False


def is_some_need_assist_conditions_exists(msg):
    warn_obj = re.search(WARNING_WORDS, msg)
    if warn_obj:
        sp = warn_obj.span()
        print('[is_some_need_assist_conditions_exists] Warning word found. Need assist:', msg[sp[0]: sp[1]])
        return RESULT_NEED_ASSIST
    return False


def is_msg_unacceptable(msg):
    if len(msg) < MSG_SHORT:
        print(f'[is_msg_unacceptable] Too short message: <', MSG_SHORT)
        return True
    if len(msg) > MSG_LONG:
        print(f'[is_msg_unacceptable] Too long message: {len(msg)} > {MSG_LONG} chars')
        return True
    bw_obj = re.search(BAD_WORDS, msg)
    if bw_obj:
        sp = bw_obj.span()
        print('[is_msg_unacceptable] Bad word found:', msg[sp[0]: sp[1]])
        return True
    if msg[-1] == '?':
        print('[is_msg_unacceptable] ? at the end of message.')
        return True
    return False


def message_preparer(msg):
    msg = pre_cleaner(msg)
    print('Prepared message:', msg)
    return msg


def pre_cleaner(msg):
    # Удаление рациональных чисел и символов
    msg = re.sub(r'\d+[,.:/]\d+|\d+/|\d+\s?%', '', msg).replace('  ', ' ')
    # удаление символов переноса строки
    msg = re.sub(r'\n|\r\n?', ' ', msg).replace('  ', ' ')
    pusto_fake = r'(ноль.+забит|полный)|(пеш[еи]х(одов)? нет)|н[и|е]кого н[и|е]\s?((в|вы|за)пускают|слуш)' \
                 r'|н(ей|и)тралке.+(машин нет|пусто|никого)'
    msg = re.sub(fr'внутри|опять|сем[ьъ][яёе]|до [56]5\s?лет|{pusto_fake}', '', msg).replace('  ', ' ')
    return msg


def is_many_kpp(msg):
    res = re.findall(r'(нов[о|а]{0,2}з|в[оа]знес|успен|матвее|кург|марин|куйб)', msg)
    if bool(res):
        print(f'Many kpps in message detected: ', res)
    return bool(res)


def find_kpp(msg):
    spans = [i.span() for i in re.finditer(RE_KPP_ALL, msg)]
    if not len(spans):
        print('[find_kpp] KPP not found.')
        return None
    if len(spans) > 1:
        if len(spans) == 2:
            sp1 = msg[spans[0][0]: spans[0][1]]
            sp2 = msg[spans[1][0]: spans[1][1]]
            if sp1 == sp2:
                del spans[1]
        else:
            print('[find_kpp] Many KPPs was founded:', [msg[sp[0]: sp[1]] for sp in spans])
            return None

    w = msg[spans[0][0]: spans[0][1]]
    print('[find_kpps] Result:', w)

    kpp_name = ''
    if re.match(f'{RE_KPP_USP_RF}|{RE_KPP_USP_DNR}', w):
        kpp_name = KPP_NAMES[0]
    elif re.match(f'{RE_KPP_MAR_RF}|{RE_KPP_MAR_DNR}', w):
        kpp_name = KPP_NAMES[1]
    elif re.match(f'{RE_KPP_NOV_RF}|{RE_KPP_NOV_DNR}', w):
        kpp_name = KPP_NAMES[2]
    elif re.match(f'{RE_KPP_SHR_RF}|{RE_KPP_ULN_DNR}', w):
        kpp_name = KPP_NAMES[3]

    if not kpp_name:
        return None
    print('[find_kpp] KPP name:', kpp_name)
    return kpp_name


def find_way(final_object):
    msg = final_object['comment']
    res_rf = find_way_rf(msg)
    res_dnr = find_way_dnr(msg)
    if any([res_rf == RESULT_NEED_ASSIST, res_dnr == RESULT_NEED_ASSIST]):
        return RESULT_NEED_ASSIST
    if all([res_dnr, res_rf]):
        print('[find_way] Many ways found. Need assist:', res_dnr, res_rf)
        return RESULT_NEED_ASSIST
    if all([not res_dnr, not res_rf]):
        if re.search(PUSTO_OBE_STORONY, msg):
            res_rf = WAY_TO_RF
        elif final_object['kpp_name']:
            print('[find_way] Ways not found but KPP exist. Need assist.')
            return RESULT_NEED_ASSIST
        else:
            print('[find_way] Ways not found. Bad message.')
            return RESULT_BAD_MSG
        # match_obj = re.search(RE_KPP_RF, msg)
        # if match_obj:
        #     print('[find_way] No ways found but set way to_dnr.')
        #     res_rf = WAY_TO_DNR
        # else:
        #     print('[find_way] No ways found but set way to_rf.')
        #     res_rf = WAY_TO_RF
    res = res_rf if res_rf else res_dnr
    print('[find_way] Result:', res)
    return res


def find_way_rf(msg):
    spans = [i.span() for i in re.finditer(WAY_RF_MIX, msg)]
    res_ex_palka = None
    # print('Result find_way_rf spans:', spans)
    if not len(spans):
        res_ex_palka = re.search(EX_PALKA, msg)
        if not res_ex_palka:
            print('[find_ways_rf] No ways to RF found.')
            return None
    # elif len(spans) > 1:
    #     print('[find_ways_rf] Many ways to RF found. Need assist:', [msg[sp[0]: sp[1]] for sp in spans])
    #     return RESULT_NEED_ASSIST

    if len(spans):
        print('[find_ways_rf] Way to RF found:', [msg[sp[0]: sp[1]] for sp in spans])
    elif res_ex_palka:
        sp = res_ex_palka.span()
        print('[find_ways_rf] Way to RF found as old palka:', msg[sp[0]: sp[1]])

    return WAY_TO_RF


def find_way_dnr(msg):
    spans = [i.span() for i in re.finditer(WAY_DNR_MIX, msg)]
    # print('Result find_way_rf spans:', spans)
    if not len(spans):
        print('[find_way_dnr] No ways to DNR found.')
        return None
    # if len(spans) > 1:
    #     print('[find_ways_dnr] Many ways to DNR found. Need assist:', [msg[sp[0]: sp[1]] for sp in spans])
    #     return RESULT_NEED_ASSIST
    print('[find_way_dnr] Way to DNR found:', [msg[sp[0]: sp[1]] for sp in spans])
    return WAY_TO_DNR
