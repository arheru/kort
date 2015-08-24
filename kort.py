#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

### Clamber - Henrik Lysell 2015

import random
import sys
import os

class Deck(object):
    """
    """
    def __init__(self, name, parent):
        """
        """
        self.name = name
        self.parent = parent
        self.cards = []
        self.discard_pile = []

    def __repr__(self):
        return self.name

    def shuffle(self):
        random.shuffle(self.cards)

class Card(object):
    """
    """
    def __init__(self, parent, id):
        """
        """
        self.parent = parent
        self.id = id
        self.name = 'Card'
        self.number_of_targets = 1

    def __repr__(self):
        return self.name

    def activate(self, player, target):
        """
        Activate Card's effect on target Player.
        """
        pass

    def choose_target(self, player):
        if self.number_of_targets == None:
            return None
        targets = []
        # "All" means all players including card's owner.
        players = self.parent.parent.players
        if self.number_of_targets == 'all':
            targets = players
            return targets
        # "Others" means all players except card's owner.
        elif self.number_of_targets == 'others':            
            for p in players:
                if p != player:
                    targets.append(p)
            return targets
        # Limited number of targets
        while len(targets) < self.number_of_targets:
            print "This card affects %s player(s). Whom do you want the card to affect?" % self.number_of_targets
            player_number = 0
            for player in players:
                player_number += 1
                print "%s: %s" % (player_number, players[player_number-1])
            print "Choose a player (number 1-%s), then press Enter." % len(players)
            key = raw_input()
            try:
                key = int(key)
            except:
                print "Error: Choose a number between 1-%s, then press Enter." % len(players)
                continue
            if key not in range(len(players)+1):
                print "Error: Only keys 1-%s are valid options. Try again." % len(players)
                continue
            targets.append(players[key-1])
            return targets

class CardClimb(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Climb!'
        self.number_of_targets = 1

    def activate(self, player, targets):
        """
        Increase one target player's position by 1.
        """
        target = targets[0]
        old_position = target.position
        target.position += 1
        print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardKickInTheFace(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Kick to the face!'
        self.number_of_targets = 1

    def activate(self, player, targets):
        """
        Decrease one target player's position by 1.
        """
        target = targets[0]
        old_position = target.position
        target.position -= 1
        print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardEveryoneTogether(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Everyone together!'
        self.number_of_targets = 'all'

    def activate(self, player, targets):
        """
        Increase all players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardCollapse(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Collapse!'
        self.number_of_targets = 'all'

    def activate(self, player, targets):
        """
        Decrease all players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position -= 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardMeFirst(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Me first!'
        self.number_of_targets = 1

    def activate(self, player, targets):
        """
        Increase own position by 1, but decrease target's position by one.
        """
        old_position = player.position
        player.position += 1
        print "%s's position goes from %s to %s." % (player, old_position, player.position)
        target = targets[0]
        old_position = target.position
        target.position -= 1
        print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardHeroism(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = "Heroism!"
        self.number_of_targets = 'others'

    def activate(self, player, targets):
        """
        Increase all other players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardNotWithoutMe(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = "You're not going without me!"
        self.number_of_targets = 'others'

    def activate(self, player, targets):
        """
        Decrease all other players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position -= 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardBaitTheSkittering(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Bait the Skittering!'
        self.number_of_targets = None

    def activate(self, player, targets):
        """
        Decrease the Skittering's position by 2.
        """
        game = self.parent.parent
        old_position = game.skittering_position
        game.skittering_position -= 2
        print "Skittering's position goes from %s to %s." % (old_position, game.skittering_position)

class CardSabotage(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'Sabotage!'
        self.number_of_targets = None

    def activate(self, player, targets):
        """
        Increase the Skittering's position by 1.
        """
        game = self.parent.parent
        old_position = game.skittering_position
        game.skittering_position += 1
        print "Skittering's position goes from %s to %s." % (old_position, game.skittering_position)

class CardThereMustBeAnotherWay(Card):
    """
    """
    def __init__(self, parent, id):
        self.parent = parent
        self.id = id
        self.name = 'There must be another way!'
        self.number_of_targets = None

    def activate(self, player, targets):
        """
        Discards all cards in hand.
        """
        while len(player.hand) > 0:
            player.discard(player.hand[0])



class Player(object):
    """
    """
    def __init__(self, name, role, parent, position = 5):
        self.name = name
        self.parent = parent
        self.role = role
        self.position = position
        self.hand = []
        self.history = []

    def __repr__(self):
        return self.name

    def draw(self, deck, number = 1):
        """
        Player draws number amount of Cards from Deck.
        """
        for i in range(number):
            # When deck is empty, the entire discard pile is shuffled into the deck.
            if not deck.cards:
                deck.cards = deck.discard_pile
                deck.shuffle()
            print "%s draws %s" % (self, deck.cards[-1])
            self.hand.append(deck.cards.pop())

    def discard(self, card):
        if card in self.hand:
            self.parent.deck.discard_pile.append(card)
            self.hand.remove(card)
            print "%s discards %s." % (self, card)

    def examine_cards_in_hand(self):
        print "Which card do you want to know about?"
        while True:
            key = raw_input()
            try:
                key = int(key)
            except:
                print "Error: Choose a number between 1-%s" % len(self.hand)
                continue
            if key not in range(1,len(self.hand)+1):
                print "Error: Only keys 1-%s are valid options. Try again." % len(self.hand)
                continue
            print self.hand[key-1].activate.__doc__
            return 

    def pick_card(self):
        while True:
            # print "\nYour hand is %s. Pick a card (number 1-%s), then press Enter." % (self.hand, len(self.hand))
            print "\nYour hand:"
            i = 0
            for card in self.hand:
                i += 1
                print "%s: %s" % (i, card)
            print "Pick a card (number 1-%s), then press Enter." % len(self.hand)
            key = raw_input()
            if key == '?':
                self.examine_cards_in_hand()
                continue
            try:
                key = int(key)
            except:
                print "Error: Choose a number between 1-%s" % len(self.hand)
                continue
            if key not in range(1,len(self.hand)+1):
                print "Error: Only keys 1-%s are valid options. Try again." % len(self.hand)
                continue
            card = self.hand[key-1]
            return card

    def score(self):
        score = 0
        if self.role == 'hero':
            for player in self.parent.safety:
                # 3 for surviving, and 5 for each other player that survived.
                if player == self:
                    score += 3
                else:
                    score += 5
            for card_tuple in self.history:
                # 1 for each card positively affecting others.
                card_name = card_tuple[0].name
                target_list = card_tuple[1]
                if card_name == "Climb!" and self not in target_list:
                    score  += 1
                if card_name in ["Everyone together!", "Heroism!", "Bait the Skittering!"]:
                    score += 1
        if self.role == 'sadist':
            # 5 for surviving.
            if self in self.parent.safety:
                score += 5
            for player in self.parent.graveyard:
                # 5 for each other player that died.
                if player != self:
                    score += 5
            for card_tuple in self.history:
                # 2 for each card negatively affecting others.
                card_name = card_tuple[0].name
                target_list = card_tuple[1]
                if card_name == "Kick to the face!" and self not in target_list:
                    score  += 2
                if card_name in ["Collapse!", "Me first!", "You're not going without me!"]:
                    score += 2
                # 3 for advancing the Skittering.
                if card_name == "Sabotage!":
                    score += 3
        return score


class Game(object):
    """
    """
    def __init__(self, name):
        self.name = name
        self.deck = None
        self.players = []
        self.graveyard = []
        self.safety = []
        self.turn = 0
        self.skittering_position = 0
        self.visible_goal_position = 10
        self.goal_position = random.randint(15, 20)

    def __repr__(self):
        return self.name

    def add_player(self, player):
        self.players.append(player)

    def check_loss_conditions(self):
        to_graveyard = []
        for player in self.players:
            if player.position <= self.skittering_position:
                to_graveyard.append(player)
        for player in to_graveyard:
            self.players.remove(player)
            self.graveyard.append(player)
            print "%s is engulfed by the Skittering!" % player
        if to_graveyard:
            return True

    def check_win_conditions(self):
        to_safety = []
        for player in self.players:
            if player.position >= self.goal_position:
                to_safety.append(player)
        for player in to_safety:
            self.players.remove(player)
            self.safety.append(player)
            print "%s escapes the Skittering!" % player
        if to_safety:
            return True

    def run(self):
        while True:
            # Start game
            deck = self.deck
            deck.shuffle()
            # Player draws four cards
            for player in self.players:
                player.draw(deck, 4)

            # Turn loop
            while True:
                self.turn += 1
                self.skittering_position += 1

                for player in self.players:
                    loss = self.check_loss_conditions()
                    win = self.check_win_conditions()

                if len(self.players) <= 0:
                    os.system('clear')
                    if self.safety:
                        print self.safety, "made it to safety."
                    if self.graveyard:
                        print self.graveyard, "died! Remember them fondly."
                    # Scoring, post-game
                    print "\nEnd score:"
                    for p in self.safety:
                        score = p.score()
                        print p, score
                    for p in self.graveyard:
                        score = p.score()
                        print p, score
                    return False

                for player in self.players:
                    os.system('clear')
                    # Uncomment to hide previous player's turn:
                    print "Press Enter to begin %s's turn!" % player
                    raw_input()

                    print "%s's turn!" % player
                    print "Your role is", player.role
                    print "\nTurn no %s\t\nCurrent players:" % self.turn
                    for p in self.players:
                        print "%s\t%s" % (p, p.position)
                    print "\nThe Skittering is now at %s" % self.skittering_position
                    if player.position >= self.visible_goal_position:
                        print "\nYou see safety at position %s\n" % self.goal_position
                    while len(player.hand) < 4:
                        player.draw(deck, 1)
                    card = player.pick_card()
                    print "\nYou pick %s." % card
                    target_list = card.choose_target(player)
                    card.activate(player, target_list)
                    player.history.append((card, target_list))
                    player.discard(card)
                    print "\nPress Enter to end turn."
                    raw_input()
            return False


if __name__ == "__main__":
    game = Game('game')
    deck = Deck('deck1', game)
    game.deck = deck

    global_discard_pile = True

    number_of_players = 4
    for i in range(number_of_players):
        player_name = 'p%s' % (i+1)
        role_index = random.randint(0,2)
        if 0 <= role_index <= 1:
            role = 'hero'
        # if role_index == 2:
        #     role = 'competitor'
        if role_index == 2:
            role = 'sadist'
        game.add_player(Player(player_name, role, game))
        print "Player %s enters the game!" % player_name

    for i in range(number_of_players*10):
        card_id = 'climb1_%s' % (i+1)
        game.deck.cards.append(CardClimb(deck, card_id))

    for i in range(number_of_players*6):
        card_id = 'kick1_%s' % (i+1)
        game.deck.cards.append(CardKickInTheFace(deck, card_id))

    for i in range(number_of_players*5):
        card_id = 'everyone1_%s' % (i+1)
        game.deck.cards.append(CardEveryoneTogether(deck, card_id))

    for i in range(number_of_players*4):
        card_id = 'collapse1_%s' % (i+1)
        game.deck.cards.append(CardCollapse(deck, card_id))

    for i in range(number_of_players*6):
        card_id = 'mefirst1_%s' % (i+1)
        game.deck.cards.append(CardMeFirst(deck, card_id))

    for i in range(number_of_players*3):
        card_id = 'heroism1_%s' % (i+1)
        game.deck.cards.append(CardHeroism(deck, card_id))

    for i in range(number_of_players*4):
        card_id = 'notwithoutme1_%s' % (i+1)
        game.deck.cards.append(CardNotWithoutMe(deck, card_id))

    for i in range(number_of_players*1):
        card_id = 'baittheskittering2_%s' % (i+1)
        game.deck.cards.append(CardBaitTheSkittering(deck, card_id))

    for i in range(number_of_players*1):
        card_id = 'sabotage1_%s' % (i+1)
        game.deck.cards.append(CardSabotage(deck, card_id))

    for i in range(number_of_players*1):
        card_id = 'anotherway_%s' % (i+1)
        game.deck.cards.append(CardThereMustBeAnotherWay(deck, card_id))

    game.run()
    sys.exit(0)

    # Cards
    # up1 ("Climb!")
    # down1 ("Kick to the face!")
    # allup1 ("Everyone together!")
    # alldown1 ("Collapse!")
    # othersup1 ("Heroism")
    # othersdown1 ("Me first!")
    # one player +1, the other -1 ("Shove past")
    # Skittering -2 ("Bait the Skittering")
    # Skittering +1 ("Sabotage!")
    # Discard hand ("There must be another way...")
    # oneup1onedown1 ("Me first!")