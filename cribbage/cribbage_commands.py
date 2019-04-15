"""The implementation of web commands for cribbage."""
from cribbage.hand import Hand
from typing import Dict


def cribbage_command(command: str, query: Dict[str, str]) -> str:
    """Central method to control cribbage commands."""
    # Start a new game.  Returns id of new hand plus initial six cards.  Parameter specifies whether the human is the
    # dealer.
    if command.lower() == 'start':
        is_dealer = query.get('dealer', 'False') == 'True'
        new_hand = Hand.create_hand(is_dealer)
        return new_hand.id, new_hand.player_cards()
    # Choose two cards to discard to the crib.  If player us dealer returns computer's first card played.
    # Must be the first command for a given hand.
    elif command.lower() == 'discard':
        hand = Hand.get_hand_by_id(query.get('id', ''))
        return hand.discard(query.get('cards', ''))
    # Choose card to play.  If there are fewer than eight cards in the sequence returns  computer's card or "go".
    # Can only be called after discard has been called.
    elif command.lower() == 'play':
        hand = Hand.get_hand_by_id(query.get('id', ''))
        return hand.play(query.get('card', ''))
    # Return crib.  Can only be called after all eight cards have been played.
    elif command.lower() == 'crib':
        hand = Hand.get_hand_by_id(query.get('id', ''))
        return hand.crib()
    else:
        raise Exception('Unknown cribbage command: {}.'.format(command))
