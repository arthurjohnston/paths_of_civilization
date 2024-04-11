from enum import Enum

# Enum for cubes
class Cubes(Enum):
    SOLDIER = 1
    SCHOLAR = 2
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

    def __str__(self):
        return f"{self.value} {self.type}"

# CubeAmount class to represent cost tuple for cubes
class CubeAmount:
    def __init__(self,type: Cubes, value: int=1 ):
        self.value = value
        self.type = type

    def __str__(self):
        return f"{self.value} {self.type}"

class Card:
    def __init__(self, cost: TechAmount, left: list , right: list, bonus:list):
        self.cost = cost
        self.right = right
        self.bonus = bonus
        self.left = left

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
import itertools

def get_card_combinations(cards):
    # Generate all combinations of choosing 2 cards for the first group
    first_group_combinations = list(itertools.combinations(cards, 2))

    all_combinations =[]
    for  first_group in first_group_combinations:
        remaining_cards=[card for card in cards if card not in first_group]
        # Generate all combinations of choosing 2 cards for the second group
        second_group_combinations = itertools.combinations(remaining_cards, 2)
        for second_group in second_group_combinations: 
    # Generate all possible pairs of first and second group combinations
            all_combinations.append([first_group,second_group])

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
    left=[CubeAmount(Cubes.MONUMENT,2), CubeAmount(Cubes.LEADER,1), CubeAmount(Cubes.SOLDIER)],
    right=[TechAmount(Tech.GREEN,2),TechAmount(Tech.RED,3)],
    bonus=[CubeAmount(Cubes.MONUMENT,4), CubeAmount(Cubes.POW,2), CubeAmount(Cubes.POP,1)])

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

starting_hand = [brown0,red0,yellow0,blue0,green0]

# Example usage
combinations = get_card_combinations(starting_hand)

for first_group, second_group in combinations:
    print("First Group:")
    for card in first_group:
        print(card)
    print("Second Group:")
    for card in second_group:
        print(card)
    print("---------")
print(len(combinations))
# Example usage
