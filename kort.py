#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

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
    def __init__(self, parent, name):
        """
        """
        self.parent = parent
        self.name = name
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

class CardUpOne(Card):
    """
    """
    def activate(self, player, targets):
        """
        Increase one target player's position by 1.
        """
        target = targets[0]
        old_position = target.position
        target.position += 1
        print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardDownOne(Card):
    """
    """
    def activate(self, player, targets):
        """
        Decrease one target player's position by 1.
        """
        target = targets[0]
        old_position = target.position
        target.position -= 1
        print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardAllUpOne(Card):
    """
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.number_of_targets = 'all'

    def activate(self, player, targets):
        """
        Increase all players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardAllDownOne(Card):
    """
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.number_of_targets = 'all'

    def activate(self, player, targets):
        """
        Decrease all players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position -= 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardOthersUpOne(Card):
    """
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.number_of_targets = 'others'

    def activate(self, player, targets):
        """
        Increase all other players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardOthersDownOne(Card):
    """
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.number_of_targets = 'others'

    def activate(self, player, targets):
        """
        Decrease all other players' positions by 1.
        """
        for target in targets:
            old_position = target.position
            target.position -= 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class CardApocalypseDownTwo(Card):
    """
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.number_of_targets = None

    def activate(self, player, targets):
        """
        Decrease the Apocalypse's position by 2.
        """
        game = self.parent.parent
        old_position = game.apocalypse_position
        game.apocalypse_position -= 2
        print "Apocalypse's position goes from %s to %s." % (old_position, game.apocalypse_position)


class Player(object):
    """
    """
    def __init__(self, name, parent, position = 5):
        self.name = name
        self.parent = parent
        self.position = position
        self.hand = []
        self.goal_in_sight = False

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
        self.parent.decks[0].discard_pile.append(card)
        self.hand.remove(card)
        print "%s discards %s." % (self, card)

    def pick_card(self):
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
            card = self.hand[key-1]
            return card

class Game(object):
    """
    """
    def __init__(self, name = 'Game'):
        self.name = name
        self.decks = []
        self.players = []
        self.graveyard = []
        self.safety = []
        self.turn = 0
        self.apocalypse_position = 0
        self.goal_position = random.randint(15, 20)

    def __repr__(self):
        return self.name

    def add_deck(self, deck):
        self.decks.append(deck)

    def add_player(self, player):
        self.players.append(player)

    def check_loss_conditions(self):
        to_graveyard = []
        for player in self.players:
            if player.position <= self.apocalypse_position:
                to_graveyard.append(player)
        for player in to_graveyard:
            self.players.remove(player)
            self.graveyard.append(player)
            print "%s is engulfed by the Apocalypse!" % player
            # print "graveyard is now", self.graveyard

    def check_win_conditions(self):
        to_safety = []
        for player in self.players:
            if player.position >= self.goal_position:
                to_safety.append(player)
        for player in to_safety:
            self.players.remove(player)
            self.safety.append(player)
            print "%s escapes the Apocalypse!" % player
            # print "%s are now in safety" % self.safety

    def run(self):
        while True:
            # Start game
            deck = self.decks[0]
            deck.shuffle()
            # Player draws three cards
            for player in self.players:
                player.draw(deck, 3)
            
            visible_goal_position = 10

            # Turn loop
            while True:
                self.turn += 1
                self.apocalypse_position += 1

                self.check_loss_conditions()
                self.check_win_conditions()
                if len(self.players) <= 0:
                    if self.safety:
                        print self.safety, "made it to safety."
                    if self.graveyard:
                        print self.graveyard, "died! Remember them fondly."
                    return False

                for player in self.players:
                    os.system('clear')
                    # Uncomment to hide previous player's turn:
                    # print "Press Enter to begin %s's turn!" % player
                    # raw_input()

                    print "%s's turn!" % player
                    print "\nTurn no %s\t\nCurrent players:" % self.turn
                    for p in self.players:
                        print "%s\t%s" % (p, p.position)
                    print "\nThe Apocalypse is now at", self.apocalypse_position
                    if player.position >= visible_goal_position and not player.goal_in_sight:
                        player.goal_in_sight = True
                        print "\nYou see safety at position %s" % self.goal_position
                    while len(player.hand) < 3:
                        player.draw(deck, 1)
                    print "\nYour hand is %s. Pick a card (number 1-%s), then press Enter." % (player.hand, len(player.hand))
                    card = player.pick_card()
                    print "\nYou pick %s." % card
                    target_list = card.choose_target(player)
                    card.activate(player, target_list)
                    player.discard(card)
                    print "\nPress Enter to end turn."
                    raw_input()

            return False


if __name__ == "__main__":
    game = Game()
    deck = Deck('deck1', game)
    game.add_deck(Deck('deck1', game))

    number_of_players = 4
    for i in range(number_of_players):
        player_name = 'p%s' % (i+1)
        game.add_player(Player(player_name, game))
        print "Player %s enters the game!" % player_name

    for i in range(number_of_players*20):
        card_name = 'up1_0%s' % (i+1)
        game.decks[0].cards.append(CardUpOne(deck, card_name))

    for i in range(number_of_players*15):
        card_name = 'down1_0%s' % (i+1)
        game.decks[0].cards.append(CardDownOne(deck, card_name))

    for i in range(number_of_players*12):
        card_name = 'allup1_0%s' % (i+1)
        game.decks[0].cards.append(CardAllUpOne(deck, card_name))

    for i in range(number_of_players*8):
        card_name = 'alldown1_0%s' % (i+1)
        game.decks[0].cards.append(CardAllDownOne(deck, card_name))

    for i in range(number_of_players*6):
        card_name = 'othersup1_0%s' % (i+1)
        game.decks[0].cards.append(CardOthersUpOne(deck, card_name))

    for i in range(number_of_players*8):
        card_name = 'othersdown1_0%s' % (i+1)
        game.decks[0].cards.append(CardOthersDownOne(deck, card_name))

    for i in range(number_of_players*10):
        card_name = 'apocdown2_0%s' % (i+1)
        game.decks[0].cards.append(CardApocalypseDownTwo(deck, card_name))

    game.run()
    sys.exit(0)

    # Cards
    # one player +1, the other -1 (shove past)
    # Apocalypse +-1 (reroute)

