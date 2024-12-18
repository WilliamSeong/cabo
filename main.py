import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    # A bit buggy with 2 digit numbers, fix later
    def __str__(self):
        s = self.suit
        res = "\n" + " -----" + "\n" + \
                    "|" + s + "    |" + "\n" + \
                    "|  " + str(self.value) + "  |" + "\n" + \
                    "|    " + s + "|" + \
                "\n" + " -----"
        return res


class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []

    def __str__(self):
        return "Player " + str(self.id)


class Game:
    def __init__(self, playercount):
        #Generate the deck
        deck = []
        suits = ["d", "h", "c", "s"]
        for x in suits:
            for y in range(13):
                deck.append(Card(x, y))
        random.shuffle(deck)
        self.deck = deck

        #Generate the players
        players = []
        for x in range(1, playercount + 1):
            players.append(Player(x))
        self.players = players

        #Reserve active card
        self.active = []

        #Create cabo flag
        self.cabo = -1

        #Deal the cards
        self.deal()
        
        #Start the game
        self.start()

    # Deal players
    def deal(self):
        for x in self.players:
            for _ in range(4):
                randint = random.randint(0,len(self.deck))
                x.hand.append(self.deck.pop(randint))

    def start(self):
        print("Let's Play!")
        print("---------------Testing Purposes---------------")
        self.checkAllPlayerHand()
        print("---------------Testing Purposes---------------")

        inc = 0
        while self.cabo == -1 or (self.cabo != -1 and inc % len(self.players) != self.cabo) :
            # loop while cabo == -1 or (cabo != -1 and cabo != the current player)
            turn = inc % len(self.players)
            currentPlayer = self.players[turn]
            
            print("------------------------------------------")
            self.checkPlayerHand(currentPlayer)

            # Check if player wants to use face up card
            if (len(self.active) > 0):
                print("Active card is " + str(self.active[-1]))
                active = input("Would you like to use active card? y/n")
                if (active == "y"):
                    card = self.active[-1]
                    print("Your drawn card is " + str(card))
                    self.replace(currentPlayer, card)
                else:
                    card = self.deck.pop(0)
                    print("Your drawn card is " + str(card))
                    self.ability(currentPlayer, card)
            else:
                card = self.deck.pop(0)
                print("Your drawn card is " + str(card))
                self.ability(currentPlayer, card)
            
            # Add logic for 7,8,9 abilities. Keep in mind that the abilities don't trigger if taken from face up pile.
            #   if (use active card)
            #   else (not use active card)


            # First condition -> Will you use the active card?
                # If yes then which card will you replace
                    # End turn
                # else no
                    # Second condition -> Will you use ability
                        # If yes then use ability and move card to active
                        # else no
                            # then which card will you replace

            # # Check what player wants to do with drawn card (either face up card or newly drawn)
            # action = input("Which card will " + str(self.players[turn]) + " replace? -1 for none ")
            # action = int(action)

            # # Logic for replacing cards
            # if (action == -1):
            #     self.active.append(card)
            # elif(action < len(self.players[turn].hand)):
            #     print("Removing " + str(self.players[turn].hand[action]))
            #     self.replaceCard(currentPlayer, card, action)

            if (self.cabo == -1):
                ans = input("Will you call cabo y/n ")
                if ans == "y":
                    self.cabo = turn

            inc += 1
        self.win()
    
    def ability(self, player, card):
        num = card.value
        if (card.value == 7 or card.value == 8 or card.value == 9):
            userDecision = input("Would you like to use the ability? y/n ")
            if ( userDecision == "y"):
                if (num == 7):
                    userinput = int(input("Which card would you like to see? "))
                    self.showCard(player, userinput)
                    self.active.append(card)
                elif (num == 8):
                    inputPlayer = int(input("Who's card would you like to see? "))
                    inputCard = int(input("Which card would you like to see? "))
                    chosenPlayer = self.players[inputPlayer]
                    self.showCard(chosenPlayer, inputCard)
                    self.active.append(card)
                elif (num == 9):
                    playerCard = int(input("Which card do you want to swap out"))
                    inputPlayer = int(input("Who would you like to swap with? "))
                    chosenPlayer = self.players[inputPlayer]
                    inputCard = int(input("Which of their card would you like to swap? "))
                    self.swapCard(player, chosenPlayer, playerCard, inputCard)
                    self.active.append(card)
            else:
                self.discard(player, card)
        else:
            self.discard(player, card)

    def win(self):
        self.checkAllPlayerHand()

        min = float('inf')
        winner = -1
        for x in self.players:
            acc = 0
            for y in x.hand:
                acc += y.value
            if acc < min:
                min = acc
                winner = x
        
        print("Winner! " + str(winner))
    
    def checkCards(self, lst):
        for x in lst:
            print(x)
        print("")

    # Check hand of player inputed
    def checkPlayerHand(self, player):
        hand = player.hand
        print("Player " + str(player.id))
        self.checkCards(hand)

    # Check hand of all players in game
    def checkAllPlayerHand(self):
        for x in self.players:
            self.checkPlayerHand(x)
    
    def discard(self, player, card):
        userinput = input("Would you like to replace a card? y/n ")
        if (userinput == "y"):
            self.replace(player, card)
        else:
            self.active.append(card)
    
    # Replace the card of the player's hand with the passed in card
    def replaceCard(self, player, card, index):
        self.active.append(player.hand[index])
        player.hand[index] = card

    def replace(self, player, card):
        action = int(input("Which card will " + str(player) + " replace?"))
        self.replaceCard(player, card, action)

    # Show the card of the input player at input index, for 7 and 8
    def showCard(self, player, index):
        print(player.hand[index])

    # swap cards between two players, for 9
    def swapCard(self, swapper, receiver, swapperindex, receiverindex):
        swapperhand = swapper.hand
        receiverhand = receiver.hand
        hold = receiverhand[receiverindex]
        receiverhand[receiverindex] = swapperhand[swapperindex]
        swapperhand[swapperindex] = hold
    
round = Game(2)