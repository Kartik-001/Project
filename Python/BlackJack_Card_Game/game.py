import random

cards = []
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
ranks = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
values = {'Ace': 11, 'Jack': 10, 'Queen': 10, 'King': 10}

for suit in suits:
    for rank in ranks:
        cards.append(f'{rank} of {suit}')


def shuffle():
    random.shuffle(cards)


def deal(times):
    return [cards.pop() for _ in range(times)], [cards.pop() for _ in range(times)]


def check(cards_dealt):
    scores = []
    for card_dealt in cards_dealt:
        score = 0
        for card in card_dealt:
            value = card.split()[0]
            if value in values:
                value = values[value]
            score += int(value)
            print(f'{card} = {value}')

        print(f'Player score is: {score}\n')
        scores.append(score)
    return scores


def main():
    while True:
        shuffle()
        cards_dealt = deal(times=3)
        player, opponent = check(cards_dealt)
        if player == opponent:
            print("Draw\n")
            continue
        else:
            break


if __name__ == '__main__':
    main()
