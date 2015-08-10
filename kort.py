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
            print "This card affects %s players. Who do you want the card to affect?" % self.number_of_targets
            player_number = 0
            for player in players:
                player_number += 1
                print "%s: %s" % (player_number, players[player_number-1])
            print "Choose a player (number 1-%s), then press Enter." % len(players)
            key = raw_input()
            try:
                key = int(key)
            except:
                print "Error: Choose a number between 1-%s" % len(players)
                continue
            if key not in range(len(players)+1):
                print "Error: Only keys 1-%s are valname options. Try again." % len(players)
                continue
            targets.append(players[key-1])
            return targets

class CardUpOne(Card):
    """
    """
    def __init__(self, parent, name):
        """
        """
        self.parent = parent
        self.name = name
        self.number_of_targets = 1

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
    def __init__(self, parent, name):
        """
        """
        self.parent = parent
        self.name = name
        self.number_of_targets = 1

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
        """
        """
        self.parent = parent
        self.name = name
        self.number_of_targets = 'all'

    def activate(self, player, targets):
        """
        Increase one target player's position by 1.
        """
        for target in targets:
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)


class Player(object):
    """
    """
    def __init__(self, name, parent, position = 3):
        """
        """
        self.name = name
        self.parent = parent
        self.position = position
        self.hand = []

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
        self.turn = 0

    def __repr__(self):
        return self.name

    def add_deck(self, deck):
        self.decks.append(deck)

    def add_player(self, player):
        self.players.append(player)

    def run(self):
        while True:
            # Start game
            deck = self.decks[0]
            deck.shuffle()
            # Player draws three cards
            for player in self.players:
                player.draw(deck, 3)

            # Turn loop
            turn_number = 0
            apocalypse_position = 0

            while True:
                turn_number += 1
                apocalypse_position += 1

                # End of game conditions
                os.system('clear')
                for player in self.players:
                    if player.position <= apocalypse_position:
                        print "%s is engulfed by the apocalypse!" % player
                        self.graveyard.append(player)
                        self.players.remove(player)
                        print "graveyard is now", self.graveyard
                        continue
                if len(self.players) <= 0:
                    print "Everyone died!"
                    return False
                print "\n\n\nTurn no %s\t\nCurrent players:" % turn_number
                for player in self.players:
                    print "%s\t%s\t%s" % (player, player.hand, player.position)
                print "The Apocalypse is now at", apocalypse_position

                for player in self.players:
                    while len(player.hand) < 3:
                        player.draw(deck, 1)
                    print "\n%s's turn!" % player
                    print "Your hand is %s. Pick a card (number 1-%s), then press Enter." % (player.hand, len(player.hand))
                    card = player.pick_card()
                    print "You pick %s." % card
                    # Choose target and activate effect
                    target_list = card.choose_target(player)
                    card.activate(player, target_list)
                    player.discard(card)

            return False


if __name__ == "__main__":
    game = Game()
    deck = Deck('deck1', game)
    game.add_deck(Deck('deck1', game))
    for i in range(4):
        card_name = 'up1_0%s' % (i+1)
        game.decks[0].cards.append(CardUpOne(deck, card_name))

    for i in range(3):
        card_name = 'down1_0%s' % (i+1)
        game.decks[0].cards.append(CardDownOne(deck, card_name))

    for i in range(3):
        card_name = 'allup1_0%s' % (i+1)
        game.decks[0].cards.append(CardAllUpOne(deck, card_name))

    for i in range(3):
        player_name = 'p%s' % (i+1)
        game.add_player(Player(player_name, game))
        print "Player %s enters the game!" % player_name
    game.run()
    sys.exit(0)