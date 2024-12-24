import random


class Card:
    def __init__(self, suit, value, ghost):
        self.suit = suit
        self.value = value
        self.ghost = ghost

    def __str__(self):
        s = self.suit
        if (self.value < 10):
            res = "\n" + " -----" + "\n" + \
                        "|" + str(self.value) + "    |" + "\n" + \
                        "|  " + s + "  |" + "\n" + \
                        "|    " + str(self.value) + "|" + \
                    "\n" + " -----"
        else:
            res = "\n" + " -----" + "\n" + \
                        "|" + str(self.value) + "   |" + "\n" + \
                        "|  " + s + "  |" + "\n" + \
                        "|   " + str(self.value) + "|" + \
                    "\n" + " -----"
        return res


class Player:
    def __init__(self, id, brain):
        self.id = id
        self.hand = []
        self.brain = brain

    def __str__(self):
        return "Player " + str(self.id)


class Game:
    def __init__(self, playercount):
        #Generate the deck
        deck = []
        suits = ["d", "h", "c", "s"]
        for x in suits:
            for y in range(13):
                deck.append(Card(x, y, False))
        random.shuffle(deck)
        self.deck = deck

        #Generate the players
        players = []
        players.append(Player(1, True))
        for x in range(2, playercount + 1):
            players.append(Player(x, False))
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
                randint = random.randint(0,len(self.deck)-1)
                x.hand.append(self.deck.pop(randint))

    def start(self):
        # print("Let's Play!")
        # print("---------------Testing Purposes---------------")
        # self.checkAllPlayerHand()
        # print("---------------Testing Purposes---------------")


        # print("")

        print("You're cards 1 and 2 are: ")
        print(self.players[0].hand[0])
        print(self.players[0].hand[1])

        inc = 0
        while self.cabo == -1 or (self.cabo != -1 and inc % len(self.players) != self.cabo) :
            # loop while cabo == -1 or (cabo != -1 and cabo != the current player)
            turn = inc % len(self.players)
            currentPlayer = self.players[turn]
            print("------------------------------------------")
            print(currentPlayer)

            if(not currentPlayer.brain):
                # self.showHiddenPlayerCard(currentPlayer)
                # print("Active card is " + str(self.active[-1]))
                self.cpu(currentPlayer)
            else:
                self.showHiddenPlayerCard(currentPlayer)
                print("------------------------------------------")
                # Check if player wants to use face up card
                if (len(self.active) > 0):
                    print("Active card is " + str(self.active[-1]))
                    active = input("Would you like to use active card? y/n ")
                    if (active == "y"):
                        card = self.active[-1]
                        print("------------------------------------------")
                        print("Your drawn card is " + str(card))
                        print("------------------------------------------")
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
                    ans = input("Will you call cabo? y/n ")
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
                    userinput = int(input("Which card would you like to see? ")) - 1
                    self.showCard(player, userinput)
                    self.active.append(card)
                    self.stacking()
                elif (num == 8):
                    inputPlayer = int(input("Who's card would you like to see? ")) - 1
                    inputCard = int(input("Which card would you like to see? ")) - 1
                    chosenPlayer = self.players[inputPlayer]
                    self.showCard(chosenPlayer, inputCard)
                    self.active.append(card)
                    self.stacking()
                elif (num == 9):
                    playerCard = int(input("Which card do you want to swap out? ")) - 1
                    inputPlayer = int(input("Who would you like to swap with? ")) - 1
                    chosenPlayer = self.players[inputPlayer]
                    inputCard = int(input("Which of their card would you like to swap? ")) - 1
                    self.swapCard(player, chosenPlayer, playerCard, inputCard)
                    self.active.append(card)
                    self.stacking()
            else:
                self.discard(player, card)
        else:
            self.discard(player, card)

    def stacking(self):
        print("New Active Card!")
        print(self.active[-1])
        userinput = input("Would you like to stack? y/n ")

        if userinput == "y":
            print("Which card would you like to stack? ")
            # this is only being offered to player 1

            self.showHiddenPlayerCard(self.players[0])
            userstack = int(input("Stack? ")) - 1

            self.showCard(self.players[0], userstack)

            playerval = self.players[0].hand[userstack].value
            activeval = self.active[-1].value
            if playerval == activeval:
                card = self.players[0].hand[userstack]
                self.active.append(card)
                self.players[0].hand[userstack] = Card("?", -1, True)
                print("Nice! New hand:")
                self.showHiddenPlayerCard(self.players[0])
                self.stacking()
            else:
                print("you fucked up")
                card = self.deck.pop(0)
                self.players[0].hand.append(card)


    def cpu(self, player):
        if(len(self.active) > 0):
            if(random.random() < 0.5):
                card = self.active[-1]
                cardNumber = random.randint(0, len(player.hand)-1)
                self.replaceCard(player, card, cardNumber)
            else:
                card = self.deck.pop(0)
                self.cpuAbility(player, card)
        else:
            card = self.deck.pop(0)
            self.cpuAbility(player, card)
    
    def cpuAbility(self, player, card):
        if (card.value == 9):
            lst = [x.id - 1 for x in self.players if x != player]
            playerNumber = random.choice(lst)
            recievePlayer = self.players[playerNumber]
            recieveNumber = random.randint(0, len(recievePlayer.hand)-1)
            cpuNumber = random.randint(0, len(player.hand)-1)
            self.swapCard(player, recievePlayer, recieveNumber, cpuNumber)
        else:
            cardNumber = random.randint(0, len(player.hand)-1)
            self.replaceCard(player, card, cardNumber)

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
            if not x.ghost:
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
            self.stacking()
    
    # Replace the card of the player's hand with the passed in card
    def replaceCard(self, player, card, index):
        # print(len(player.hand))
        self.active.append(player.hand[index])
        player.hand[index] = card
        self.stacking()

    def replace(self, player, card):
        action = int(input("Which card will " + str(player) + " replace? ")) - 1
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

    def showHiddenCard(self, number):
        res = "\n" + " -----" + "\n" + \
                    "|?    |" + "\n" + \
                    "|  " + str(number) + "  |" + "\n" + \
                    "|    ?|" + \
                "\n" + " -----"
        return res
    
    def showHiddenPlayerCard(self, player):
        for i, x in enumerate(player.hand):
            if not x.ghost:
                print(self.showHiddenCard(i+1))


round = Game(2)