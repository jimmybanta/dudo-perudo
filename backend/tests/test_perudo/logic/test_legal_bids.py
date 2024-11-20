
import pytest

from perudo.logic.legal_bids import legal_bids, same_quantity_bids, higher_quantity_bids, legal_starting_bids


@pytest.mark.parametrize("quantity,value,sides_per_die,expected", [
    (4, 2, 6, [(4, 3), (4, 4), (4, 5), (4, 6),]),
    (4, 5, 6, [(4, 6),]),
    (4, 2, 10, [(4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), 
                (4, 10),]),
    (4, 5, 10, [(4, 6), (4, 7), (4, 8), (4, 9), (4, 10),]),
    
])
def test_same_quantity_bids(quantity, value, sides_per_die, expected):
    assert list(same_quantity_bids(quantity, value, sides_per_die=sides_per_die)) == expected


@pytest.mark.parametrize("quantity,total_dice,value_range,expected", [
    (4, 10, (2, 6), [(5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 2), (6, 3), 
                        (6, 4), (6, 5), (6, 6), (7, 2), (7, 3), (7, 4), (7, 5), 
                        (7, 6), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 2), 
                        (9, 3), (9, 4), (9, 5), (9, 6), (10, 2), (10, 3), (10, 4), 
                        (10, 5), (10, 6),]),
    (4, 10, (1, 6), [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 1), 
                        (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1), (7, 2), 
                        (7, 3), (7, 4), (7, 5), (7, 6), (8, 1), (8, 2), (8, 3), 
                        (8, 4), (8, 5), (8, 6), (9, 1), (9, 2), (9, 3), (9, 4), 
                        (9, 5), (9, 6), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), 
                        (10, 6)]),  
    (4, 10, (1, 1), [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),]),
])
def test_higher_quantity_bids(quantity, total_dice, value_range, expected):
    assert list(higher_quantity_bids(quantity, total_dice, value_range)) == expected




@pytest.mark.parametrize("current,total_dice,sides_per_die,palifico,ex_palifico,expected", [
    # Standard round, normie bet, 10 dice, 6 sided dice
    ((5, 2), 10, 6, False, False, [(5, 3), (5, 4), (5, 5), (5, 6), (6, 2), (6, 3), (6, 4), 
                                    (6, 5), (6, 6), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), 
                                    (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 2), (9, 3), 
                                    (9, 4), (9, 5), (9, 6), (10, 2), (10, 3), (10, 4), (10, 5), 
                                    (10, 6), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), 
                                    (9, 1), (10, 1),]),

    # Standard round, jessie bet, 10 dice, 6 sided dice
    ((3, 1), 10, 6, False, False, [(7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (8, 2), (8, 3), 
                                    (8, 4), (8, 5), (8, 6), (9, 2), (9, 3), (9, 4), (9, 5), 
                                    (9, 6), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), 
                                    (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)]),

    # Standard round, normie betting, 10 dice, 4 sided dice
    ((5, 2), 10, 4, False, False, [(5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 2), (7, 3), 
                                        (7, 4), (8, 2), (8, 3), (8, 4), (9, 2), (9, 3), (9, 4), 
                                        (10, 2), (10, 3), (10, 4), (3, 1), (4, 1), (5, 1), (6, 1), 
                                        (7, 1), (8, 1), (9, 1), (10, 1),]),

    # Palifico round, non-ex-palifico player, 10 dice, 6 sided dice
    ((2, 3), 10, 6, True, False, [(3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), 
                                    (10, 3),]),

    # Palifico round, ex-palifico player, 10 dice, 6 sided dice
    ((2, 3), 10, 6, True, True, [(2, 4), (2, 5), (2, 6), (3, 1), (3, 2), (3, 3), (3, 4), 
                                    (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), 
                                    (4, 6), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), 
                                    (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1), 
                                    (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (8, 1), (8, 2), 
                                    (8, 3), (8, 4), (8, 5), (8, 6), (9, 1), (9, 2), (9, 3), 
                                    (9, 4), (9, 5), (9, 6), (10, 1), (10, 2), (10, 3), (10, 4), 
                                    (10, 5), (10, 6),]),
    
    # Palifico round, ex-palifico player, 10 dice, 4 sided dice
    ((4, 1), 10, 4, True, True, [(4, 2), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (5, 4), 
                                    (6, 1), (6, 2), (6, 3), (6, 4), (7, 1), (7, 2), (7, 3), 
                                    (7, 4), (8, 1), (8, 2), (8, 3), (8, 4), (9, 1), (9, 2), 
                                    (9, 3), (9, 4), (10, 1), (10, 2), (10, 3), (10, 4),]),

    # Edge case: total_dice equals current quantity, non-palifico round, 10 dice, 6 sided dice
    ((10, 3), 10, 6, False, False, [(10, 4), (10, 5), (10, 6), (5, 1), (6, 1), (7, 1), (8, 1), 
                                        (9, 1), (10, 1),]),

    # Edge case: total_dice equals current quantity, Palifico, non-ex-palifico player, 10 dice, 6 sided dice
    ((10, 3), 10, 6, True, False, []),


])
def test_legal_bids(current, total_dice, sides_per_die, palifico, ex_palifico, expected):
    assert sorted(legal_bids(current, total_dice, 
                             sides_per_die=sides_per_die,
                             palifico=palifico, ex_palifico=ex_palifico)) == sorted(expected)
    


@pytest.mark.parametrize("total_dice,sides_per_die,palifico,expected", [
    # Standard round, default sides_per_die
    (10, 6, False, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), 
                        (2, 4), (2, 5), (2, 6), (3, 2), (3, 3), (3, 4), (3, 5), 
                        (3, 6), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 2), 
                        (5, 3), (5, 4), (5, 5), (5, 6), (6, 2), (6, 3), (6, 4), 
                        (6, 5), (6, 6), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), 
                        (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 2), (9, 3), 
                        (9, 4), (9, 5), (9, 6), (10, 2), (10, 3), (10, 4), (10, 5), 
                        (10, 6), 
                   ]),
    # Palifico round, default sides_per_die
    (10, 6, True, [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), 
                        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 1), (3, 2), 
                        (3, 3), (3, 4), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), 
                        (4, 4), (4, 5), (4, 6), (5, 1), (5, 2), (5, 3), (5, 4), 
                        (5, 5), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), 
                        (6, 6), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), 
                        (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 1), 
                        (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (10, 1), (10, 2), 
                        (10, 3), (10, 4), (10, 5), (10, 6),
                  ]),
    # Standard round, different sides_per_die
    (5, 8, False, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), 
                        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), 
                        (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), 
                        (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), 
                        (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), 
                  ]),
    # Edge case: Only 2 dice in the game
    (2, 6, False, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), 
                        (2, 4), (2, 5), (2, 6),
                ]),
])
def test_legal_starting_bids(total_dice, sides_per_die, palifico, expected):
    assert sorted(legal_starting_bids(total_dice, sides_per_die, palifico)) == sorted(expected)