from itertools import combinations
from rule_poker import check_hand, max_cards
from tqdm import tqdm

list_cards = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
  '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', 
  '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 
  'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']

def check_rank_score(rank, score, tmp_rank, tmp_score):
    if(rank > tmp_rank):
        return 1
    elif(rank < tmp_rank):
        return -1
    else:
        if(score > tmp_score):
            return 1
        elif(score < tmp_score):
            return -1
        else:
            return 0
        

def check_win(hand, five_cards):
    seven_cards = hand + five_cards
    max_card, rank, score = max_cards(hand, five_cards)
    re_cards = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
                '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', 
                '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 
                'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    for x in seven_cards:
        re_cards.remove(x)
    combination_list = list(combinations(re_cards, 2))
    win, draw, lose = 0, 0, 0
    for x in combination_list:
        _, tmp_rank, tmp_score = max_cards(list(x), five_cards)
        if(rank > tmp_rank):
            win += 1
        elif(rank < tmp_rank):
            # print('lose:', x)
            lose += 1
        else:
            if(score > tmp_score):
                win += 1
            elif(score < tmp_score):
                lose += 1
                # print('lose:', x)
            else:
                # print('draw:', x)
                draw += 1
    return max_card, win, draw, lose

def check_0card(hand):
    re_cards = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
                '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', 
                '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 
                'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    for x in hand:
        re_cards.remove(x)
    combination_list = list(combinations(re_cards, 5))
    win, draw, lose = 0, 0, 0
    for x in tqdm(combination_list):
        w, d, l = check_win(hand, list(x))
        win += w
        draw += d
        lose += l
    print(win, draw, lose)
    return win, draw, lose

def check_3card(hand, three_crads):
    re_cards = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
                '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', 
                '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 
                'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    for x in hand+three_crads:
        re_cards.remove(x)
    print(len(re_cards))
    combination_list = list(combinations(re_cards, 2))
    win, draw, lose = 0, 0, 0
    for x in tqdm(combination_list):
        w, d, l = check_win(hand, list(x)+three_crads)
        win += w
        draw += d
        lose += l
    print(win, draw, lose)
    return win, draw, lose

def check_4card(hand, four_crads):
    re_cards = ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
                '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', 
                '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 
                'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    for x in hand+four_crads:
        re_cards.remove(x)
    print(len(re_cards))
    combination_list = list(combinations(re_cards, 1))
    win, draw, lose = 0, 0, 0
    for x in tqdm(combination_list):
        w, d, l = check_win(hand, list(x)+four_crads)
        win += w
        draw += d
        lose += l
    return win, draw, lose

# check_win(['As','Ad'],['4s','3s','2s','7c','Kd'])
# check_4card(['As','Ad'], ['Ks','Qs','Js','10s'])


