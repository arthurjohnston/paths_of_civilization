import itertools
from cards import *
import datetime
import cProfile
import sys
from collections import Counter

# fix this to handle duplicate cards properly, currently itertools treats them as the same
def get_card_combinations_old(cards):
    if(len(cards)!=5):
        raise Exception(str(cards))
    # Generate all combinations of choosing 2 cards for the first group
    first_group_combinations = list(itertools.combinations(cards, 2))

    all_combinations = []
    for first_group in first_group_combinations:
        remaining_index = [card for card in cards if card not in first_group]
        # Generate all combinations of choosing 2 cards for the second group
        second_group = list(itertools.combinations(remaining_index, 2))
        for second_group in second_group:
            # Generate all combinations of choosing 2 cards for the third group
            third_group = [card for card in remaining_index if card not in second_group]
            all_combinations.append([first_group, second_group, third_group])

    return all_combinations

def get_card_combinations(cards):
    if len(cards) != 5:
        raise ValueError("Input must be a list of 5 cards")
    
    all_combinations = set()
    all_combinations.add(tuple([tuple([cards[0], cards[1]]),tuple([cards[2], cards[3]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[1]]),tuple([cards[2], cards[4]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[1]]),tuple([cards[3], cards[4]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[2]]),tuple([cards[1], cards[3]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[2]]),tuple([cards[1], cards[4]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[2]]),tuple([cards[3], cards[4]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[3]]),tuple([cards[1], cards[2]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[3]]),tuple([cards[1], cards[4]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[3]]),tuple([cards[2], cards[4]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[4]]),tuple([cards[1], cards[2]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[4]]),tuple([cards[1], cards[3]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[0], cards[4]]),tuple([cards[2], cards[3]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[2]]),tuple([cards[0], cards[3]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[2]]),tuple([cards[0], cards[4]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[2]]),tuple([cards[3], cards[4]]), tuple([cards[0]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[3]]),tuple([cards[0], cards[2]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[3]]),tuple([cards[0], cards[4]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[3]]),tuple([cards[2], cards[4]]), tuple([cards[0]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[4]]),tuple([cards[0], cards[2]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[4]]),tuple([cards[0], cards[3]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[1], cards[4]]),tuple([cards[2], cards[3]]), tuple([cards[0]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[3]]),tuple([cards[0], cards[1]]), tuple([cards[4]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[3]]),tuple([cards[0], cards[4]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[3]]),tuple([cards[1], cards[4]]), tuple([cards[0]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[4]]),tuple([cards[0], cards[1]]), tuple([cards[3]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[4]]),tuple([cards[0], cards[3]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[2], cards[4]]),tuple([cards[1], cards[3]]), tuple([cards[0]])]))
    all_combinations.add(tuple([tuple([cards[3], cards[4]]),tuple([cards[0], cards[1]]), tuple([cards[2]])]))
    all_combinations.add(tuple([tuple([cards[3], cards[4]]),tuple([cards[0], cards[2]]), tuple([cards[1]])]))
    all_combinations.add(tuple([tuple([cards[3], cards[4]]),tuple([cards[1], cards[2]]), tuple([cards[0]])]))

    return list(all_combinations)

# religion_level
# 2 x1 3
# 2 x1 6
# 3 x2 10
# 4 x2 15
# 5 x3 21
pop_to_allowed_and_bonus = {
    0:(4,None),
    1:(5, Cubes.LEADER),
    2:(6,None),
    3:(6,Cubes.LEADER),
    4:(7,None),
    5:(7,Cubes.LEADER),
    6: (8, Cubes.LEADER),
    7: (8,Cubes.LEADER),
    8: (9,Cubes.LEADER),
    9: (9,None), # 1 vp
    10: (10,None), # 2 vp
    11: (10,None), # 3 vp
    12: (10,None), # 4 vp
    13: (10,None) # still just 4
    }
#    9: 1 vp
#    10:10, 2 vp
#    +1 up to 12 
#

class PlayerState:
    def __init__(self, hand):
        self.hand = Counter(hand)
        self.techs = Counter()
        self.cubes = Counter()
        self.events = []
        self.collectable_limit = 4;
        self.paths_to_this_state = 1;

    def __eq__(self, other):
        if isinstance(other, PlayerState):
            return (self.hand == other.hand and
                    self.techs == other.techs and
                    self.cubes == other.cubes)
        return False

    def __hash__(self):
        return hash((frozenset(self.hand.items()), frozenset(self.techs.items()), frozenset(self.cubes.items())))

    def add_card_to_hand(self, card_name):
        self.hand[card_name] += 1

    def remove_card_from_hand(self, card_name):
        if card_name in self.hand:
            self.hand[card_name] -= 1
            if self.hand[card_name] == 0:
                del self.hand[card_name]

    def add_tech_amount(self, tech):
        self.techs[tech.type] += tech.value

    def remove_tech_amount(self, tech):
        if tech.type in self.techs:
            self.techs[tech.type] -= tech.value
            if self.techs[tech.type] <= 0:
                del self.techs[tech.type]

    def has_enough_tech(self, tech):
        return self.techs[tech.type] >= tech.value

    def amount_cubes(self, cubeType):
        return self.cubes[cubeType] 
    def clear_cube(self, cubeType):
        del self.cubes[cubeType]

    def add_cube_amount(self, cube):
        self.cubes[cube.type] += cube.value
        if(cube.type==Cubes.POP):
            increase_in_population = pop_to_allowed_and_bonus[self.cubes[cube.type]]
            self.collectable_limit =increase_in_population[0]
            self.events.append(f"\tIncreasing collectable limit to {increase_in_population[0]}")
            if increase_in_population[1] is not None:
                self.add_cube_amount(CubeAmount(increase_in_population[1])) 

    def tech_score(self):
        score = 0
        for card_name in self.hand.elements():
                for tech in playable_cards[card_name].right:
                    score += tech.value * 3
        #score += sum(self.techs.values())
        #for cube, value in self.cubes.items():
            #score += value/ 2
        for tech, value in self.techs.items():
            score += value/ 2
        return score

    def add_event(self, event):
        self.events.append(event)

    def convert_hand_to_list(self):
        return sorted(self.hand.elements())
    def deepcopy(self):
        return copy.deepcopy(self)

    def __str__(self):
        tech_str = "".join([f" {tech.name}:{amount}" for tech, amount in sorted(self.techs.items())])
        cube_str = "".join([f" {cube.name}:{amount}" for cube, amount in sorted(self.cubes.items())])
        # todo add current collectable amount
        events_str = "\n\t".join(self.events)
        return f"Events:\n{events_str}\nHand: {self.convert_hand_to_list()}\nTech:\n{tech_str}\nCubes:\n{cube_str}\n"
    def log_cubes_and_tech(self):
        tech_str = "".join([f" {tech.name}:{amount}" for tech, amount in sorted(self.techs.items())])
        cube_str = "".join([f" {cube.name}:{amount}" for cube, amount in sorted(self.cubes.items())])
        # todo add current collectable amount
        self.events.append(f"\tAt end of turn have{tech_str}{cube_str}")

import random

def get_top_x_and_sampling_y(rankedList, X, Y):
    # Check if the list is smaller than X+Y, return the entire list in that case
    if len(rankedList) <= X + Y:
        return rankedList

    # Get the first X items
    firstXItems = rankedList[:X]
    
    # Get a random sample of size Y from the rest of the list
    restOfList = rankedList[X:]
    sampleY = random.sample(restOfList, Y)
    
    # Concatenate the first X items and the sample of size Y
    result = firstXItems + sampleY
    return result

def runCode(turns, top_N_to_print):
    turn_1_hand = list(starting_cards.keys())
    turn_1_player_state =PlayerState(turn_1_hand) #todo add board specific bonus
    starts_of_turn = [turn_1_player_state]
    next_turn_starts=set()
    # todo make this a parameter
    for turn in range(1,turns+1):
        for starting in starts_of_turn:
            starting.events.append(f"Turn {turn}")
            # step 1 generate all 30 card placements for this hand
            combinations = get_card_combinations(starting.convert_hand_to_list())
            # before turn 5 you should only dump level 0 cards
            if turn < 5:
                combinations = {entry for entry in combinations if  entry[2][0].endswith('0')}
            
            for left_group, right_group, discard in combinations:
                card_placement=starting.deepcopy()
                # step 2 remove discarded card
                # todo this should save for final game scoring 
                for card_name in discard:
                    card_placement.events.append("\tDiscard:"+str(card_name))
                    #card_placement.hand.remove(card)
                    card_placement.remove_card_from_hand(card_name)
                
                # step 3 add left resource
                # todo: if pop too low they this splits into choices
                total_productions = sum(cube.value for card_name in left_group for cube in playable_cards[card_name].left)
                if total_productions> card_placement.collectable_limit:
                    card_placement.events.append("\tOver collectable for cubes limit!!")

                for card_name in left_group:
                    result = ""
                    for cube in playable_cards[card_name].left:
                        card_placement.add_cube_amount(cube)
                        result += str(cube) + " "
                    card_placement.events.append(f"\tLeft:{str(card_name)} collecting {result}")
                    
                # Step 4 buy wonders & leaders
            
                # Step 5 add right resource
                # todo: if pop too low they this splits into choices
                total_productions = sum(cube.value for card_name in right_group for cube in playable_cards[card_name].left)
                if total_productions> card_placement.collectable_limit:
                    card_placement.events.append("\tOver collectable for tech limit!!")

                for card_name in right_group:
                    result = ""
                    for tech in playable_cards[card_name].right:
                        card_placement.add_tech_amount(tech)
                        result += str(tech) + " "
                    card_placement.events.append(f"\tRight:{str(card_name)} collecting {result}")
                    
                #step 6 buy card
                #check which techs you have enough of
                
                for card_name, card in buyable_cards.items():
                    if card_placement.has_enough_tech(card.cost):
                        #print("can afford card")
                        next_turn_starting = card_placement.deepcopy()
                        next_turn_starting.add_card_to_hand(card_name)
                        next_turn_starting.remove_tech_amount(card.cost)
                        result = ""

                        for bonus in  card.bonus:
                            result += str(bonus) + " "
                            if isinstance(bonus, TechAmount):
                                next_turn_starting.add_tech_amount(bonus)
                            elif isinstance(bonus, CubeAmount):
                                next_turn_starting.add_cube_amount(bonus)
                            else:
                                print("something bad"+bonus)
                        next_turn_starting.events.append(f"\tBought:{str(card_name)} collecting {result}")
                        
                        if (turn in {3,5,7,9}):
                            amount=next_turn_starting.amount_cubes(Cubes.SCRIBE)
                            next_turn_starting.clear_cube(Cubes.SCRIBE)
                            next_turn_starting.events.append(f"\tScoring for event with {amount} scribes")

                        if (turn in {4,6,8,9}):
                            # warriors are worth 2
                            amount = next_turn_starting.amount_cubes(Cubes.WARRIOR)*2
                            amount+=next_turn_starting.amount_cubes(Cubes.POW)
                            next_turn_starting.clear_cube(Cubes.WARRIOR)
                            next_turn_starting.events.append(f"\tScoring for war with {amount} warriors and POWs")
                        next_turn_starting.log_cubes_and_tech()
                        next_turn_starts.add(next_turn_starting)
                            
        print(datetime.datetime.now())
        print(f"At end of {turn} there are {len(next_turn_starts)} possible")
            # copy over the starts for next turn and reset next_turn_starts to 
            # be used for the following turn
        sorted_turns = sorted(next_turn_starts, key=lambda turn: turn.tech_score(), reverse=True)
        starts_of_turn =get_top_x_and_sampling_y(sorted_turns,1000,9000)
        print(f"At end of {turn} there are {len(starts_of_turn)} possible after filtering")
        
        next_turn_starts=set() #reset possibilities for next 
    
    sorted_objects = sorted(starts_of_turn, key=lambda obj: obj.tech_score(), reverse=True)
    #sorted_objects = sorted(starts_of_turn, key=lambda obj: str(obj), reverse=True)
    
    # Print the top objects
    for i, obj in enumerate(sorted_objects[:top_N_to_print]):
        print(f"{obj} - \nTech Score: {obj.tech_score()}")
        print("-----------------------------------")
    #  Print the worst
    #for i, obj in enumerate(sorted_objects[-10:]):
    #    print(f"{obj} - \nTech Score: {obj.tech_score()}")
    #    print("-----------------------------------")

if __name__ == '__main__':
    turns = 3
    top_N_to_print = 30
    if(len(sys.argv)>=2):
        turns = int(sys.argv[1])

    if(len(sys.argv)==3):
        top_N_to_print = int(sys.argv[2])
    runCode(turns,top_N_to_print)