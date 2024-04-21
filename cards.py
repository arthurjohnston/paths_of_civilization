from enum import Enum
import itertools
import copy

# Enum for cubes
class Cubes(Enum):
    WARRIOR = 1
    SCRIBE = 2
    LEADER = 3
    RELIGION = 4
    MONUMENT = 6
    POW = 7
    POP = 8
    def __lt__(self, other):
        if isinstance(other, Cubes):
            return self.value < other.value
        raise TypeError("Comparison with non-Cubes enum")

# Enum for tech
class Tech(Enum):
    BROWN = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    RED = 5
    def __lt__(self, other):
        if isinstance(other, Tech):
            return self.value < other.value
        raise TypeError("Comparison with non-Tech enum")
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
        return f"{self.type.name}:{self.value}"
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
        return f"{self.type.name}:{self.value}"

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


# brown makes green 1,2,2,2 & red 1,1,2,3
# red makes brown & blue
# blue makes red & yellow 
# yellow makes blue & green
# green makes yellow & brown

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

green1 = Card(cost=TechAmount(Tech.GREEN,1 ),
    left=[CubeAmount(Cubes.LEADER)],
    right=[TechAmount(Tech.YELLOW,1),TechAmount(Tech.BROWN,1)],
    bonus=[CubeAmount(Cubes.POP)])

green2 = Card(cost=TechAmount(Tech.GREEN,4 ),
    left=[CubeAmount(Cubes.LEADER,1), CubeAmount(Cubes.SCRIBE,1)],
    right=[TechAmount(Tech.YELLOW,2),TechAmount(Tech.BROWN,1)],
    bonus=[CubeAmount(Cubes.POP,2),CubeAmount(Cubes.MONUMENT)])

green3 = Card(cost=TechAmount(Tech.GREEN,7 ),
    left=[CubeAmount(Cubes.LEADER,2), CubeAmount(Cubes.SCRIBE)],
    right=[TechAmount(Tech.YELLOW,2),TechAmount(Tech.BROWN,2)],
    bonus=[TechAmount(Tech.BLUE),CubeAmount(Cubes.POP,3),CubeAmount(Cubes.MONUMENT)])

green4 = Card(cost=TechAmount(Tech.GREEN,10 ),
    left=[CubeAmount(Cubes.SCRIBE,2), CubeAmount(Cubes.RELIGION),CubeAmount(Cubes.LEADER)],
    right=[TechAmount(Tech.YELLOW,2),TechAmount(Tech.BROWN,3)],
    bonus=[TechAmount(Tech.BLUE),CubeAmount(Cubes.POP,3),CubeAmount(Cubes.MONUMENT,2)])


greens=[green1, green2,green3,green4]


buyable_cards = { "brown1":brown1
,"brown2":brown2
,"brown3":brown3
,"brown4":brown4
,"red1":red1
,"red2":red2
,"red3":red3
,"red4":red4
,"blue1":blue1
,"blue2":blue2
,"blue3":blue3
,"blue4":blue4
,"yellow1":yellow1
,"yellow2":yellow2
,"yellow3":yellow3
,"yellow4":yellow4
,"green1":green1
,"green2":green2
,"green3":green3
,"green4":green4}

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


starting_cards = {
    "brown0":brown0,
    "red0":red0,
    "yelllow0":yellow0,
    "blue0":blue0,
    "green0":green0
}

playable_cards = {**buyable_cards, **starting_cards}