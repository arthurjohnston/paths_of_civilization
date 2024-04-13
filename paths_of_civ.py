from enum import Enum
import itertools

# Enum for cubes
class Cubes(Enum):
    WARRIOR = 1
    SCRIBE = 2
    PEOPLE = 3
    RELIGION = 4
    LEADER = 5
    MONUMENT = 6
    POW = 7
    POP = 8

# Enum for tech
class Tech(Enum):
    BROWN = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    RED = 5
    
# TechAmount class to represent cost tuple for tech
class TechAmount:
    def __init__(self,  type: Tech, value: int=1):
        self.value = value
        self.type = type
    def __eq__(self, other):
        if not isinstance(other, TechAmount):
            return False
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))
    def __str__(self):
        return f"{self.value} {self.type}"
    def __add__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return TechAmount(self.type, self.value + other.value)
        else:
            raise ValueError("Cannot add TechAmount with different types or non-TechAmount object")

    def __sub__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return TechAmount(self.type, self.value - other.value)
        else:
            raise ValueError("Cannot subtract TechAmount with different types or non-TechAmount object")

    def is_same_type(self, other):
        if isinstance(other, TechAmount):
            return self.type == other.type
        return False

    def __lt__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return self.value < other.value
        else:
            raise ValueError("Cannot compare TechAmount with different types or non-TechAmount object")

    def __le__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return self.value <= other.value
        else:
            raise ValueError("Cannot compare TechAmount with different types or non-TechAmount object")

    def __gt__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return self.value > other.value
        else:
            raise ValueError("Cannot compare TechAmount with different types or non-TechAmount object")

    def __ge__(self, other):
        if isinstance(other, TechAmount) and self.type == other.type:
            return self.value >= other.value
        else:
            raise ValueError("Cannot compare TechAmount with different types or non-TechAmount object")

# CubeAmount class to represent cost tuple for cubes
class CubeAmount:
    def __init__(self,type: Cubes, value: int=1 ):
        self.value = value
        self.type = type
    def __eq__(self, other):
        if not isinstance(other, CubeAmount):
            return False
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))
    def __str__(self):
        return f"{self.value} {self.type}"
    def __str__(self):
        return f"{self.value} {self.type}"

    def __add__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return CubeAmount(self.type, self.value + other.value)
        else:
            raise ValueError("Cannot add CubeAmount with different types or non-CubeAmount object")

    def __sub__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return CubeAmount(self.type, self.value - other.value)
        else:
            raise ValueError("Cannot subtract CubeAmount with different types or non-CubeAmount object")

    def is_same_type(self, other):
        if isinstance(other, CubeAmount):
            return self.type == other.type
        return False

    def __lt__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return self.value < other.value
        else:
            raise ValueError("Cannot compare CubeAmount with different types or non-CubeAmount object")

    def __le__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return self.value <= other.value
        else:
            raise ValueError("Cannot compare CubeAmount with different types or non-CubeAmount object")

    def __gt__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return self.value > other.value
        else:
            raise ValueError("Cannot compare CubeAmount with different types or non-CubeAmount object")

    def __ge__(self, other):
        if isinstance(other, CubeAmount) and self.type == other.type:
            return self.value >= other.value
        else:
            raise ValueError("Cannot compare CubeAmount with different types or non-CubeAmount object")

class Card:
    def __init__(self, cost: TechAmount, left: list , right: list, bonus:list):
        self.cost = cost
        self.right = right
        self.bonus = bonus
        self.left = left

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.cost == other.cost
                and self.right == other.right
                and self.bonus == other.bonus
                and self.left == other.left)

    def __hash__(self):
        return hash((self.cost, tuple(self.right), tuple(self.bonus), tuple(self.left)))

    def __str__(self):
        cost_type = self.cost.type.name
        bonus_str = []
        for item in self.bonus:
            if isinstance(item, TechAmount):
                bonus_str.append(f"{item.value} {item.type.name}")
            elif isinstance(item, CubeAmount):
                bonus_str.append(f"{item.value} {item.type.name}")
        right = ", ".join([f"{tech.value} {tech.type.name}" for tech in self.right])
        left = ", ".join([f"{cube.value} {cube.type.name}" for cube in self.left])
        return f"Cost: {self.cost.value} {cost_type}, Bonus: {bonus_str}, Right: [{right}], Left: [{left}]"






def get_card_combinations(cards):
    # Generate all combinations of choosing 2 cards for the first group
    first_group_combinations = list(itertools.combinations(cards, 2))

    all_combinations = []
    for first_group in first_group_combinations:
        remaining_cards = [card for card in cards if card not in first_group]
        # Generate all combinations of choosing 2 cards for the second group
        second_group_combinations = list(itertools.combinations(remaining_cards, 2))
        for second_group in second_group_combinations:
            # Generate all combinations of choosing 2 cards for the third group
            third_group = [card for card in remaining_cards if card not in second_group]
            all_combinations.append([first_group, second_group, third_group])

    return all_combinations

# https://boardgamegeek.com/image/8141472/path-of-civilization
brown1 = Card(cost=TechAmount(Tech.BROWN,1 ),
    left=[CubeAmount(Cubes.MONUMENT,1)],
    right=[TechAmount(Tech.GREEN,1),TechAmount(Tech.RED,1)],
    bonus=[CubeAmount(Cubes.MONUMENT,1)])

brown2 = Card(cost=TechAmount(Tech.BROWN,4 ),
    left=[CubeAmount(Cubes.MONUMENT,1), CubeAmount(Cubes.LEADER,1)],
    right=[TechAmount(Tech.GREEN,2),TechAmount(Tech.RED,1)],
    bonus=[CubeAmount(Cubes.MONUMENT,2), CubeAmount(Cubes.POW,1)])

brown3 = Card(cost=TechAmount(Tech.BROWN,7 ),
    left=[CubeAmount(Cubes.MONUMENT,2), CubeAmount(Cubes.LEADER,1)],
    right=[TechAmount(Tech.GREEN,2),TechAmount(Tech.RED,2)],
    bonus=[CubeAmount(Cubes.MONUMENT,3), CubeAmount(Cubes.POW,1), CubeAmount(Cubes.POP,1)])

brown4 = Card(cost=TechAmount(Tech.BROWN,10 ),
    left=[CubeAmount(Cubes.MONUMENT,2), CubeAmount(Cubes.LEADER,1), CubeAmount(Cubes.WARRIOR)],
    right=[TechAmount(Tech.GREEN,2),TechAmount(Tech.RED,3)],
    bonus=[CubeAmount(Cubes.MONUMENT,4), CubeAmount(Cubes.POW,2), CubeAmount(Cubes.POP,1)])


browns=[brown1, brown2,brown3,brown4]

red1 = Card(cost=TechAmount(Tech.RED,1 ),
    left=[CubeAmount(Cubes.WARRIOR,1)],
    right=[TechAmount(Tech.BROWN,1),TechAmount(Tech.BLUE,1)],
    bonus=[CubeAmount(Cubes.POW,1)])

red2 = Card(cost=TechAmount(Tech.RED,4 ),
    left=[CubeAmount(Cubes.WARRIOR,1), CubeAmount(Cubes.MONUMENT,1)],
    right=[TechAmount(Tech.BROWN,2),TechAmount(Tech.BLUE,1)],
    bonus=[CubeAmount(Cubes.POW,2), CubeAmount(Cubes.RELIGION,1)])

red3 = Card(cost=TechAmount(Tech.RED,7 ),
    left=[CubeAmount(Cubes.WARRIOR,2), CubeAmount(Cubes.MONUMENT,1)],
    right=[TechAmount(Tech.BROWN,2),TechAmount(Tech.BLUE,2)],
    bonus=[CubeAmount(Cubes.POW,3), CubeAmount(Cubes.RELIGION,1), CubeAmount(Cubes.WARRIOR,1)])

red4 = Card(cost=TechAmount(Tech.RED,10 ),
    left=[CubeAmount(Cubes.WARRIOR,2), CubeAmount(Cubes.MONUMENT,1), CubeAmount(Cubes.RELIGION)],
    right=[TechAmount(Tech.BROWN,2),TechAmount(Tech.BLUE,3)],
    bonus=[CubeAmount(Cubes.POW,4), CubeAmount(Cubes.RELIGION,2), CubeAmount(Cubes.WARRIOR,1)])


reds=[red1, red2,red3,red4]


blue1 = Card(cost=TechAmount(Tech.BLUE,1 ),
    left=[CubeAmount(Cubes.RELIGION,1)],
    right=[TechAmount(Tech.RED,1),TechAmount(Tech.YELLOW,1)],
    bonus=[CubeAmount(Cubes.RELIGION,1)])

blue2 = Card(cost=TechAmount(Tech.BLUE,4 ),
    left=[CubeAmount(Cubes.RELIGION,1), CubeAmount(Cubes.WARRIOR,1)],
    right=[TechAmount(Tech.RED,2),TechAmount(Tech.YELLOW,1)],
    bonus=[CubeAmount(Cubes.RELIGION,2), TechAmount(Tech.GREEN)])

blue3 = Card(cost=TechAmount(Tech.BLUE,7 ),
    left=[CubeAmount(Cubes.RELIGION,2), CubeAmount(Cubes.WARRIOR,1)],
    right=[TechAmount(Tech.RED,2),TechAmount(Tech.YELLOW,2)],
    bonus=[CubeAmount(Cubes.RELIGION,3), TechAmount(Tech.GREEN),CubeAmount(Cubes.POW,1)])

blue4 = Card(cost=TechAmount(Tech.BLUE,10 ),
    left=[CubeAmount(Cubes.RELIGION,2), CubeAmount(Cubes.WARRIOR,1), CubeAmount(Cubes.SCRIBE)],
    right=[TechAmount(Tech.RED,2),TechAmount(Tech.YELLOW,3)],
    bonus=[CubeAmount(Cubes.RELIGION,3), TechAmount(Tech.GREEN), TechAmount(Tech.BROWN),CubeAmount(Cubes.POW,1)])


blues=[blue1, blue2,blue3,blue4]


yellow1 = Card(cost=TechAmount(Tech.YELLOW,1 ),
    left=[CubeAmount(Cubes.SCRIBE,1)],
    right=[TechAmount(Tech.BLUE,1),TechAmount(Tech.GREEN,1)],
    bonus=[TechAmount(Tech.BROWN)])

yellow2 = Card(cost=TechAmount(Tech.YELLOW,4 ),
    left=[CubeAmount(Cubes.RELIGION,1), CubeAmount(Cubes.SCRIBE,1)],
    right=[TechAmount(Tech.BLUE,2),TechAmount(Tech.GREEN,1)],
    bonus=[TechAmount(Tech.BROWN),TechAmount(Tech.RED),CubeAmount(Cubes.POP)])

yellow3 = Card(cost=TechAmount(Tech.YELLOW,7 ),
    left=[CubeAmount(Cubes.SCRIBE,2), CubeAmount(Cubes.RELIGION)],
    right=[TechAmount(Tech.BLUE,2),TechAmount(Tech.GREEN,2)],
    bonus=[TechAmount(Tech.BROWN),TechAmount(Tech.RED),CubeAmount(Cubes.POP),CubeAmount(Cubes.SCRIBE),CubeAmount(Cubes.RELIGION)])

yellow4 = Card(cost=TechAmount(Tech.YELLOW,10 ),
    left=[CubeAmount(Cubes.SCRIBE,2), CubeAmount(Cubes.RELIGION),CubeAmount(Cubes.LEADER)],
    right=[TechAmount(Tech.BLUE,2),TechAmount(Tech.GREEN,3)],
    bonus=[TechAmount(Tech.BROWN),TechAmount(Tech.RED),CubeAmount(Cubes.POP),CubeAmount(Cubes.SCRIBE,2),CubeAmount(Cubes.RELIGION,2)])


yellows=[yellow1, yellow2,yellow3,yellow4]

## todo green


## starting

brown0  = Card(cost=TechAmount(Tech.BROWN,0),left=[],
    right=[TechAmount(Tech.BROWN)], bonus=[])

red0  = Card(cost=TechAmount(Tech.RED,0),left=[],
    right=[TechAmount(Tech.RED)], bonus=[])
yellow0  = Card(cost=TechAmount(Tech.YELLOW,0),left=[],
    right=[TechAmount(Tech.YELLOW)], bonus=[])
blue0  = Card(cost=TechAmount(Tech.BLUE,0),left=[],
    right=[TechAmount(Tech.BLUE)], bonus=[])
green0  = Card(cost=TechAmount(Tech.GREEN,0),left=[],
    right=[TechAmount(Tech.GREEN)], bonus=[])

import copy

class PlayerState:
    def __init__(self,hand):
        self.hand = hand
        self.tech_dict = {}
        self.cube_dict = {}
        self.events = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def remove_card_from_hand(self, card):
        self.hand.remove(card)

    def add_tech_amount(self, tech, amount):
        if tech in self.tech_dict:
            self.tech_dict[tech] += amount
        else:
            self.tech_dict[tech] = amount

    def remove_tech_amount(self, tech, amount):
        if tech in self.tech_dict:
            self.tech_dict[tech] -= amount
            if self.tech_dict[tech].value <= 0:
                del self.tech_dict[tech]

    def add_cube_amount(self, cube, amount):
        if cube in self.cube_dict:
            self.cube_dict[cube] += amount
        else:
            self.cube_dict[cube] = amount

    def remove_cube_amount(self, cube, amount):
        if cube in self.cube_dict:
            self.cube_dict[cube] -= amount
            if self.cube_dict[cube].value <= 0:
                del self.cube_dict[cube]

    def add_event(self, event):
        self.events.append(event)

    def deep_copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        tech_str = "\n".join([f"{tech}: {amount}" for tech, amount in self.tech_dict.items()])
        cube_str = "\n".join([f"{cube}: {amount}" for cube, amount in self.cube_dict.items()])
        events_str = "\n".join(self.events)
        return f"Hand: {self.hand}\nTech:\n{tech_str}\nCubes:\n{cube_str}\nEvents:\n{events_str}"




starting_hand = [brown0,red0,yellow0,blue0,green0]
starting =PlayerState(starting_hand)
starting.events.append("Turn 1")
# step 1 generate all 30 card placements for this hand
combinations = get_card_combinations(starting.hand)
new_player_states = []
for left_group, right_group, discard in combinations:
    new_player_state=starting.deep_copy()
    print(new_player_state)
    for card in left_group:
        new_player_state.events.append("Left:"+str(card))
    for card in right_group:
        new_player_state.events.append("Right:"+str(card))
    for card in discard:
        print("Discard")
        new_player_state.events.append("Discard:"+str(card))
        #step 2 remove discarded card
        for x in new_player_state.hand:
            print(hash(x))
            print(x)
        print(card)
        print(hash(card))
        new_player_state.hand.remove(card)
        print(len(new_player_state.hand))
        #new_player_state.remove_card_from_hand(card)

    #step3
    print("---------")

print(len(combinations))
# Example usage