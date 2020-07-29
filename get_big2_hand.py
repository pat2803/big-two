# Function to return the type of hand that is inputted (specific to big 2)
def get_big_2_hand(cards):

    if len(cards) == 0:
        return [0, 0]

    play_set = []
    numbers = [x // 4 + 2 for x in cards]
    numbers = [15 if x == 2 else x for x in numbers]
    suits = [x % 4 for x in cards]

    sorted_numbers = sorted(numbers)
    len_numbers = len(numbers)
    max_number = max(numbers)

    # Check for sets of the same number e.g. pairs, triples, etc
    if numbers == [numbers[0]] * len_numbers:
        if len_numbers == 1:
            play_set = ['single', numbers[0], suits[0]]
            score = numbers[0] * 10 + suits[0]
        elif len_numbers == 2:
            play_set = ['pair', numbers[0], max(suits)]
            score = numbers[0] * 1000 + max(suits)
        elif len_numbers == 3:
            play_set = ['triple', numbers[0], max(suits)]
            score = numbers[0] * 100000 + max(suits)
        elif len_numbers == 4:
            play_set = ['four of a kind', numbers[0], max(suits)]
            score = numbers[0] * 10000000 + max(suits)

    # Check for poker hands
    elif len_numbers == 5:
        if sorted_numbers == list(range(9, 14)) and suits == suits[0] * 5:
            play_set = ['royal flush', max_number, suits[0]]
            score = 30000000
        elif sorted_numbers == [min(numbers) + x for x in range(5)] and suits == suits[0] * 5:
            play_set = ['straight flush', max_number, suits[0]]
            score = 20000000 + max_number
        elif numbers.count(sorted_numbers[0]) + numbers.count(sorted_numbers[4]) == 5 and \
                numbers.count(numbers[0]) in [2, 3]:
            triple = sorted_numbers[0] if numbers.count(sorted_numbers[0]) == 3 else sorted_numbers[4]
            pair = sorted_numbers[0] if numbers.count(sorted_numbers[0]) == 2 else sorted_numbers[4]
            play_set = ['Full house', [triple, pair], max([suits[x] if numbers[x] == triple else 0 for x in range(len_numbers)])]
            score = 10000000 + triple
        elif suits == [suits[0]] * 5:
            play_set = ['flush', max_number, suits[0]]
            score = 1000000 + sorted_numbers[0] + 15 * sorted_numbers[1] + 225 * sorted_numbers[2] + \
                        3375 * sorted_numbers[3] + 50625 * max_number
        elif sorted_numbers == [min(numbers) + x for x in range(5)]:
            play_set = ['straight', max_number, suits[numbers.index(max_number)]]
            score = 10000 + max_number
        else:
            play_set = 0
            score = 0
    else:
        play_set = 0
        score = 0

    return [play_set, score]


# Full house ace on jack
# test_hand = [48, 49, 50, 38, 39]
# Four kind 2s
# test_hand = [0, 1, 2, 3]
# Pair aces
# test_hand = [48, 49]
# test_hand = [12, 20, 24, 28, 36]
# print(get_big_2_hand(test_hand))

