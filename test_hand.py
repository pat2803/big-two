from get_big2_hand import get_big_2_hand


# Test hands for big 2 to see if they can be played
def test_hand(playing_hand, previous_hand=[]):

    playing_hand_set = get_big_2_hand(playing_hand)
    if not playing_hand_set[0]:
        return "Select a valid hand"
    if previous_hand:
        if len(playing_hand) != len(previous_hand):
            return "Play the same number of cards as the previous hand"
        previous_hand_set = get_big_2_hand(previous_hand)
        if playing_hand_set[1] < previous_hand_set[1]:
            return "Play a higher hand than the previous one"

    return playing_hand_set[0]


# h1 = [48, 49]
# h2 = [50, 51]
# print(test_hand(h2))
