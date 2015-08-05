#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import random
import sys

class Deck(object):
    """
    """
    def __init__(self, name, parent):
        """
        """
        self.name = name
        self.parent = parent
        self.cards = []

    def __repr__(self):
        return self.name

    def shuffle(self):
        random.shuffle(self.cards)

class Card(object):
    """
    """
    def __init__(self, name, parent):
        """
        """
        self.name = name
        self.parent = parent

    def __repr__(self):
        return self.name

    def activate(self, target):
        """
        Activate Card's effect on target Player.
        """
        if self.name[:3] == 'up1':
            old_position = target.position
            target.position += 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)
        if self.name[:5] == 'down1':
            old_position = target.position
            target.position -= 1
            print "%s's position goes from %s to %s." % (target, old_position, target.position)

class Player(object):
    """
    """
    def __init__(self, name, parent, position = 5):
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
            print "%s draws %s" % (self, deck.cards[-1])
            self.hand.append(deck.cards.pop())

    def discard(self, card):
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

    def choose_target(self):
        while True:
            key = raw_input()
            try:
                key = int(key)
            except:
                print "Error: Choose a number between 1-%s" % len(self.parent.players)
                continue
            if key not in range(len(self.parent.players)+1):
                print "Error: Only keys 1-%s are valid options. Try again." % len(self.parent.players)
                continue
            target_player = self.parent.players[key-1]
            return target_player

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
                print "\n\n\nTurn no %s\t\nCurrent players:\n" % turn_number
                for player in self.players:
                    print "%s\t%s\t%s" % (player, player.hand, player.position)

                for player in self.players:
                    while len(player.hand) < 3:
                        player.draw(deck, 1)
                    print "\n%s's turn!" % player
                    print "Your hand is %s. Pick a card (number 1-%s), then press Enter." % (player.hand, len(player.hand))
                    card = player.pick_card()
                    print "You pick %s." % card
                    # Choose target and activate effect
                    print "Who do you want to the card to affect? Choose a player (number 1-%s), then press Enter." % len(self.players)
                    target = player.choose_target()
                    card.activate(target)
                    player.discard(card)

                # End of game conditions
                for player in self.players:
                    if player.position < apocalypse_position:
                        print "%s is engulfed by the apocalypse!" % player
                        self.graveyard.append(player)
                        self.players.remove(player)
                        print "graveyard is now", self.graveyard
                        continue
                if len(self.players) <= 0:
                    print "Everyone died!"
                    return False
            return False


if __name__ == "__main__":
    game = Game()
    deck = Deck('deck1', game)
    game.add_deck(Deck('deck1', game))
    print "Deck in play is '%s'" % deck
    for i in range(50):
        card_name = 'up1_0%s' % (i+1)
        game.decks[0].cards.append(Card(card_name, deck))

    for i in range(28):
        card_name = 'down1_0%s' % (i+1)
        game.decks[0].cards.append(Card(card_name, deck))

    for i in range(2):
        player_name = 'p%s' % (i+1)
        game.add_player(Player(player_name, game))
        print "Player %s enters the game!" % player_name
    game.run()
    sys.exit(0)