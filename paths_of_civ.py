import itertools
from cards import *
import datetime
import cProfile

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


#    0:4,
#    1:5, leader
#    2: 6
#    3: leader
#    4: 7
#    5:leader
#    6: 8 leader
#    7: leader
#    8: leader 9
#    9: 1 vp
#    10:10, 2 vp
#    +1 up to 12 
#
class PlayerState:
    def __init__(self,hand):
        self.hand = hand
        self.tech_dict = {}
        self.cube_dict = {}
        self.events = []

    def __eq__(self, other):
        if isinstance(other, PlayerState):
            return (self.hand == other.hand and
                    self.tech_dict == other.tech_dict and
                    self.cube_dict == other.cube_dict)
        return False

    def __hash__(self):
        return hash((tuple(self.hand), frozenset(self.tech_dict.items()), frozenset(self.cube_dict.items())))

    def add_card_to_hand(self, card_name):
        self.hand.append(card_name)

    def remove_card_from_hand(self, card_name):
        self.hand.remove(card_name)

    def add_tech_amount(self, tech):
        if tech.type in self.tech_dict:
            self.tech_dict[tech.type] += tech.value
        else:
            self.tech_dict[tech.type] = tech.value

    def remove_tech_amount(self, tech):
        if tech.type in self.tech_dict:
            self.tech_dict[tech.type] -= tech.value
            if self.tech_dict[tech.type] <= 0:
                del self.tech_dict[tech.type]
    
    def has_enought_tech(self, tech):
        if tech.type in self.tech_dict:
            return self.tech_dict[tech.type] >= tech.value
        else:
            return False

    def add_cube_amount(self, cube):
        if cube.type in self.cube_dict:
            self.cube_dict[cube.type] += cube.value
        else:
            self.cube_dict[cube.type] = cube.value

    def remove_cube_amount(self, cube):
        if cube.type in self.cube_dict:
            self.cube_dict[cube.type] -= cube.value
            if self.cube_dict[cube.type] <= 0:
                del self.cube_dict[cube.type]

    def tech_score(self):
        score = 0
        for card_name in self.hand:
            score += playable_cards[card_name].cost.value
        for key, value in self.tech_dict.items():
            score += value
        return score

    def add_event(self, event):
        self.events.append(event)

    def deep_copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        tech_str = "\n".join([f"\t{tech}: {amount}" for tech, amount in self.tech_dict.items()])
        cube_str = "\n".join([f"\t{cube}: {amount}" for cube, amount in self.cube_dict.items()])
        events_str = "\n\t".join(self.events)
        hand_str = "\n".join(f"\t{card}" for card in self.hand)
        return f"Hand: {hand_str}\nTech:\n{tech_str}\nCubes:\n{cube_str}\nEvents:\n{events_str}"



def runCode():
    turn_1_hand = list(starting_cards.keys())
    turn_1_player_state =PlayerState(turn_1_hand) #todo add board specific bonus
    starts_of_turn = [turn_1_player_state]
    next_turn_starts=set()
    for turn in range(1,6):
        for starting in starts_of_turn:
            starting.events.append(f"Turn {turn}")
            # step 1 generate all 30 card placements for this hand
            combinations = get_card_combinations(starting.hand)[:10]
            
            card_placements = []
            for left_group, right_group, discard in combinations:
                card_placement=starting.deep_copy()
                # step 2 remove discarded card
                # todo this should save for final game scoring 
                if(len(discard)==0):
                    raise Exception(starting.hand)
                for card_name in discard:
                    card_placement.events.append("\tDiscard:"+str(card_name))
                    #card_placement.hand.remove(card)
                    card_placement.remove_card_from_hand(card_name)
                
                # step 3 add left resource
                # todo add population check
                for card_name in left_group:
                    card_placement.events.append("\tLeft:"+str(card_name))
                    for cube in playable_cards[card_name].left:
                        card_placement.add_cube_amount(cube)
                # Step 4 buy wonders & leaders
            
                # Step 5 add right resource
                # todo add pop check
                for card_name in right_group:
                    card_placement.events.append("\tRight:"+str(card_name))
                    for tech in playable_cards[card_name].right:
                        card_placement.add_tech_amount(tech)
                #step 6 buy card
                #check which techs you have enough of
                
                for card_name, card in buyable_cards.items():
                    if card_placement.has_enought_tech(card.cost):
                        #print("can afford card")
                        next_turn_starting = card_placement.deep_copy()
                        next_turn_starting.add_card_to_hand(card_name)
                        next_turn_starting.events.append("\tBought:"+str(card_name))
                        next_turn_starting.remove_tech_amount(card.cost)
                        for bonus in  card.bonus:
                            if isinstance(bonus, TechAmount):
                                next_turn_starting.add_tech_amount(bonus)
                            elif isinstance(bonus, CubeAmount):
                                next_turn_starting.add_cube_amount(bonus)
                            else:
                                print("something bad"+bonus)
                        #print(next_turn_starting)
                        next_turn_starts.add(next_turn_starting)
                        #print("---------")
        print(datetime.datetime.now())
        print(f"At end of {turn} there are {len(next_turn_starts)} possible")
            # copy over the starts for next turn and reset next_turn_starts to 
            # be used for the following turn
        starts_of_turn=next_turn_starts
        next_turn_starts=set() #reset possibilities for next 
    
    sorted_objects = sorted(starts_of_turn, key=lambda obj: obj.tech_score(), reverse=True)
    
    # Print the top ten objects
    for i, obj in enumerate(sorted_objects[:5], start=1):
        print(f"{obj} - \nTech Score: {obj.tech_score()}")
        print("-----------------------------------")

if __name__ == '__main__':
    cProfile.run('runCode()')