from itertools import combinations

def cal_dis(card1, card2):
    #return abs((card1[2]-card2[2]))
    return ((card1[1]-card2[1])**2 + (card1[2]-card2[2])**2)**0.5

def check_clus(min_value, distances):
    avg_dis = 0
    cnt = 0
    max_dis = 0
    for i in min_value:
        tmp = []
        for j in min_value:
            if(i!=j):
                tmp.append(distances[i][j])
        tmp = sorted(tmp)
        avg_dis += tmp[0] + tmp[1]
        cnt += 2
        max_dis = max(max_dis, tmp[0])
    if(avg_dis/cnt < max_dis/2):
        return False
    else:
        return True

def check_8_9(cards):
    print('cards detection: ',cards)
    if(len(cards) < 9):
        return ''
    distances = []
    for i in range(len(cards)):
        tmp = []
        for j in range(len(cards)):
            tmp.append(cal_dis(cards[i], cards[j]))
        distances.append(tmp)
    if(len(cards) > 9):
        candidates = list(combinations(range(len(cards)), 10))
        dict_final = {}
        for x in candidates:
            sum = 0
            for i,j in combinations(x, 2):
                sum += distances[i][j]
            dict_final[x] = sum
        min_value, score = min(dict_final.items(), key=lambda x: x[1])
        if(check_clus(min_value, distances)):
            return(min_value)
    
    candidates = list(combinations(range(len(cards)), 9))
    dict_final = {}
    for x in candidates:
        sum = 0
        for i,j in combinations(x, 2):
            sum += distances[i][j]
        dict_final[x] = sum

    min_value, score = min(dict_final.items(), key=lambda x: x[1])
    if(check_clus(min_value, distances)):
        return(min_value)
    return ''

def check_pair(card1, card2, played):
    if(card1[0]==card2[0]):
        re_c = []
        for suit in ('h', 'd', 's', 'c'):
            if(suit != card1[1] and suit != card2[1]):
                if(not check_in_played(card1[0], suit, played)):
                    re_c.append([card1[0], suit])
        if(len(re_c)!=0):
            return True, re_c
    return False, []

def check_straight(card1, card2, played):
    if(card1[1]==card2[1]):
        if(card1[0]-card2[0] == 2 or card1[0]-card2[0] == -2):
            re_c = [(card1[0]+card2[0])/2, card1[1]]
            if(not check_in_played(re_c[0], re_c[1], played)):
                return True, [re_c]
        if(card1[0]-card2[0] == 1):
            cand = []
            re_c = []
            if(card1[0]+1<=13):
                cand.append([card1[0]+1, card1[1]])
            if(card2[0]-1>=1):
                cand.append([card2[0]-1, card1[1]])
            for x in cand:
                if(not check_in_played(x[0], x[1], played)):
                    re_c.append(x)
            if(len(re_c)!=0):
                return True, re_c
        if(card1[0]-card2[0] == -1):
            cand = []
            re_c = []
            if(card2[0]+1<=13):
                cand.append([card2[0]+1, card1[1]])
            if(card1[0]-1>=1):
                cand.append([card1[0]-1, card1[1]])
            for x in cand:
                if(not check_in_played(x[0], x[1], played)):
                    re_c.append(x)
            if(len(re_c)!=0):
                return True, re_c
    return False, []

def check_phom(re_c, mine):
    for x in re_c:
        if(check_in_played(x[0], x[1], mine)):
            return True
    return False

def check_in_played(num, suit, played):
    for x in played:
        if(num == x[0] and suit == x[1]):
            return True
    return False

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
            num = 1
        else:
            num = int(num)
        cards.append([num, suit])
    return cards

def unconvert_card(card):
    num = card[0]
    if(num == 11):
        num = 'J'
    elif(num == 12):
        num = 'Q'
    elif(num == 13):
        num = 'K'
    elif(num == 1):
        num = 'A'
    return str(num)+card[1]

def remove_card(cards):
    tmp_check = check_8_9(cards)
    if(len(tmp_check) != 9):
        return ''
    played = []
    mine = []
    if(tmp_check != None):
        for x in range(len(cards)):
            if(x in tmp_check):
                mine.append(cards[x][0])
            else:
                played.append(cards[x][0])
        played = convert_cards(played)
        mine = convert_cards(mine)
    print('Mine cards: ', mine)
    print('Played cards: ', played)
    remove_score = {}
    for x in mine:
        tmp_x = unconvert_card(x)
        remove_score[tmp_x] = 1000000000
        re_c = 0
        for y in mine:
            if(x!=y):
                check_bool_p, re_c_p = check_pair(x, y, played)
                check_bool_s, re_c_s = check_straight(x, y, played)
                if(check_bool_p or check_bool_s):
                    if(check_phom(re_c_p, mine) or check_phom(re_c_s, mine)):
                        remove_score[tmp_x] = min(x[0], remove_score[tmp_x])
                    re_c += len(re_c_p) + len(re_c_s)
        if(re_c > 0):
            remove_score[tmp_x] = min((100-re_c)*1000 + x[0], remove_score[tmp_x])
        else:
            remove_score[tmp_x] = min(1000000 + x[0], remove_score[tmp_x])
    print(remove_score)
    max_value, score = max(remove_score.items(), key=lambda x: x[1])
    return max_value

# remove_card([['Ah', 767, 470], ['2c', 159, 446], ['3d', 760, 75], ['4c', 370, 900], ['4h', 680, 830], ['4d', 545, 805], ['5d', 269, 100], ['6s', 588, 800], ['6h', 326, 98], ['6d', 447, 841], ['7d', 494, 821], ['7h', 813, 82], ['8c', 719, 481], ['9c', 801, 489], ['9d', 226, 70], ['10d', 868, 95], ['Jc', 182, 457], ['Kc', 412, 864], ['Kh', 725, 847], ['Kd', 631, 803]])
