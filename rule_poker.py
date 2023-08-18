from itertools import combinations

def convert_cards(hands):
    cards = []
    for x in hands:
        num = x[:-1]
        suit = x[-1]
        if(num == 'J'):
            num = 11
        elif(num == 'Q'):
            num = 12
        elif(num == 'K'):
            num = 13
        elif(num == 'A'):
            num = 14
        else:
            num = int(num)
        cards.append([num, suit])
    return cards

# tra ve True neu tat ca la bai cung chat
def check_flush(cards):
    c0 = cards[0]
    for c in cards[1:]:
        if(c[1] != c0[1]):
            return False
    return True

# tra ve dict cac la bai va so lan xuat hien
def check_num(cards):
    dict_card = {}
    for c in cards:
        if(c[0] in dict_card):
            dict_card[c[0]] += 1
        else:
            dict_card[c[0]] = 1
    return dict_card

# tra ve sanh va la bai lon nhat
def check_straight(nums):
    if(len(nums)<5):
        return False, 0
    if(max(nums) == 14):
        if(min(nums) == 10):
            return True, 14
        elif(sum(nums) == 28):
            return True, 5
        else:
            return False, 0
    else:
        if(max(nums) - min(nums) == 4):
            return True, max(nums)
        else:
            return False, 0

def check_four_of_a_kind(nums):
    if(len(nums) != 2):
        return False, 0
    nums_value = list(nums.values())
    nums_key = list(nums.keys())

    if nums_value[0] == 4:
        return True, nums_key[0]*100 + nums_key[1]
    elif nums_value[1] == 4:
        return True, nums_key[1]*100 + nums_key[0]
    else:
        return False, 0

def check_full_house(nums):
    if(len(nums) != 2):
        return False, 0

    nums_value = list(nums.values())
    nums_key = list(nums.keys())

    if nums_value[0] == 3:
        return True, nums_key[0]*100 + nums_key[1]
    else:
        return True, nums_key[1]*100 + nums_key[0]


def check_three_of_a_kind(nums):
    if(len(nums) != 3):
        return False, 0

    nums_value = list(nums.values())
    nums_key = list(nums.keys())

    three = []
    not_three = []
    for i in range(len(nums)):
        if nums_value[i] == 3:
            three.append(nums_key[i])
        elif nums_value[i] == 1:
            not_three.append(nums_key[i])
    not_three = sorted(not_three, reverse=True)
    if(len(three) == 1):
        return True, three[0]*10000 + not_three[0]*100 + not_three[1]
    else:
        return False, 0


def check_pair(nums):
    if(len(nums) > 4):
        return False, 0, 0

    nums_value = list(nums.values())
    nums_key = list(nums.keys())
    pair = []
    not_pair = []

    for i in range(len(nums)):
        if nums_value[i] == 2:
            pair.append(nums_key[i])
        elif nums_value[i] == 1:
            not_pair.append(nums_key[i])
    pair = sorted(pair, reverse=True)
    not_pair = sorted(not_pair, reverse=True)
    if len(pair) == 2:
        return True, 2, pair[0]*10000 + pair[1]*100 + not_pair[0]
    elif len(pair) == 1:
        return True, 1, pair[0]*1000000 + not_pair[0]*10000 + not_pair[1]*100 + not_pair[2]



def check_high_card(nums):
    if(len(nums) != 5):
        return False, 0
    else:
        nums_key = list(nums.keys())
        nums_key = sorted(nums_key, reverse=False)
        return True, sum(nums_key[i]*100**i for i in range(5))

# card = 5, 1 (5h)
def check_hand(hands):
    cards = convert_cards(hands)
    nums = check_num(cards)
    rank = 0
    score = 0
    if(check_flush(cards)):
        #Đồng chất
        #Check thùng phá sảnh
        straight, max_num = check_straight((nums.keys()))
        if straight:
            if(max_num == 14):
                rank = 10
                score = 14
            else:
                rank = 9
                score = max_num
        else:
            rank = 6
            tmp = sorted(nums)
            score = sum(tmp[i]*100**i for i in range(len(tmp)))

    else:
        chk_four, max_num = check_four_of_a_kind(nums)
        if chk_four:
            rank = 8
            score = max_num
        else:
            chk_full, max_num = check_full_house(nums)
            if chk_full:
                rank = 7
                score = max_num
            else:
                chk_straight, max_num = check_straight(nums)
                if chk_straight:
                    rank = 5
                    score = max_num
                else:
                    chk_three, max_num = check_three_of_a_kind(nums)
                    if chk_three:
                        rank = 4
                        score = max_num
                    else:
                        chk_pair, num_pair, score = check_pair(nums)
                        if chk_pair:
                            if num_pair == 2:
                                rank = 3
                            else:
                                rank = 2
                            score = score
                        else:
                            chk_high, score = check_high_card(nums)
                            if chk_high:
                                rank = 1
                                score = score

    #print("rank, score: ", rank, score)
    return rank, score

dict_rank = {10:'royal_flush', 9:'straight_flush', 8:'four_of_a_kind', 7:'full_house', 6:'flush',
              5:'straight', 4:'three_of_a_kind', 3:'two_pair', 2:'pair', 1:'high_card'}

def max_cards(hand, five_cards):
    # Tạo danh sách tổ hợp
    combination_list = list(combinations(hand + five_cards, 5))
    rank, score = 0, 0
    max_card = ()

    for five_cards in combination_list:
        tmp_rank, tmp_score = check_hand(list(five_cards))
        # print(tmp_rank, tmp_score, hand + list(three_cards))
        if(tmp_rank > rank or (tmp_rank == rank and tmp_score > score)):
            rank, score, max_card = tmp_rank, tmp_score, list(five_cards)
    # print(max_card, rank, score)
    return max_card, rank, score

# max_cards(['3h', '10d'], ['3s', '6s', 'Qd', 'Ac', '3d'])
# print(check_pair(['6s', '10c', '9s', '7s', '6d']))
# print(check_hand(['6s', '10c', '9s', '7s', '6d']))