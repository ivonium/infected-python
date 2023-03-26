### This is as simulation involving control bodies, infected people and healers.
### All objects move around a grid randomly in a turn-based system, they move one place per round.
### If an infected object gets within 2 places of a non-infected object, they become infected.
### If a healer object gets within 2 places of an infected object, they become cured.
### If two healers get within 2 places, they get a vaccinator. 
### Anyone who gets within 2 places of a vaccinator is permanently healed
### The script will tally the total amount of each type at the end of the simulation.

#################################################
import random
from tabulate import tabulate
import numpy as np
import pandas as pd
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init() ### This allows coloured text to be used later in the script.

print("\n----- \nWelcome to the infection simulation, please input your starting parameters: \n")
grid = [int(num) for num in list(input("What is the width and height of your grid, input as: WIDTH,HEIGHT (use only whole numbers):").split(","))]  ###This creates a list from the input which defines the grid
non_infectious = int(input("Starting number of non-infectious units: "))
infectious = int(input("Starting number of infectious units: "))
healer = int(input("Starting number of healer units: "))
rounds = int(input("How many rounds should this simulation go for? "))
infection_distance = 2
vaccinator = True
movement_per_round = 1

class Unit():
    def __init__(### init parameters and their default values
        self, 
        starting_infectious = False,
        grid_ref = [],
        id_number = "unassigned"
        ): 
        ### core variables
        self.infectious = starting_infectious
        self.grid_ref = grid_ref
        self.infected = starting_infectious
        self.id_number = id_number
    
    def __repr__(self):
        return "Unit {}".format(self.id_number)

    def move(self): #moves the object up, down, left or right by one place
        def rand_int_func():
            return random.randint(0,1)
        selector1 = rand_int_func()
        selector2 = rand_int_func() #its necessary to create a second separate random number because otherwise (if only one) then numbers will only increase
        #This is used to define whether the object moves horizontally or vertically
        self.grid_ref[selector1] = ( #randomly selects horizontal or vertical
            self.grid_ref[selector1] + (-2*selector2 + movement_per_round) #randomly selects to increase or decrease
            ) % grid[selector1]
        
        direction = ""
        magnitude = -2*selector2 + movement_per_round
        if selector1 == 0:
            direction = "Horizontal"
        else:
            direction = "Vertical"
        #print("{} has moved {} by {} and is now at {}.".format(self,direction,magnitude,self.grid_ref))
    
    def make_infectious_if_infected(self): ### The unit will only become infectious after being infected in the previous round (i.e. this will be called before 'make_infected').

            pass
            
    def make_infected(self):
        self.infected = True
        return self.infected
    
    def heal(self):
        self.infected = False

### Create healer, vaccinator and create script which causes them to interact
class Healer():
    def __init__(self, heal_radius = 1, grid_ref = [random.randint(0,grid[0]), random.randint(0,grid[1])]):
        self.heal_radius = heal_radius
        self.grid_ref = grid_ref

    def move(self): #moves the object up, down, left or right by one place
        selector = random.randint(0,1) #This is used to define whether the object moves horizontally or vertically
        self.grid_ref[selector] = (self.grid_ref[selector] + movement_per_round) % grid[selector]

    def heal(self,other_unit):
        pass
        ###to implement after simulation runtime is developed below

####### UNIT STORAGE LISTS #######
units_non_infectious = []
units_infectious = []
#units_healer = [] 

grid_storage = [] #this will temporarily store unique grid values (i.e. all X,Y coordinates). It is used for the purpose of making sure that the units do not overlap and so that they can be randomly distributed.

def create_grid():
    for i in range(0,grid[0]):
        for z in range (0, grid[1]):
            grid_storage.append([i,z])


def create_units():
    for i in range(0,non_infectious):
        units_non_infectious.append(Unit())  ### create non-infectious
    for i in range(0,infectious):
        units_infectious.append(Unit(starting_infectious = True))
    #units_healer = [Healer() for i in range(0,healer)] ### create healers
    
    counter = 0
    ### The below 3 for loops assigns a unique id number and assigns a unique grid ref to each unit.
    
    for unit in units_non_infectious:
        unit.id_number = counter
        counter += 1
        unit.grid_ref = grid_storage.pop(random.randint(0,len(grid_storage)-1)) #takes out a random part of the grid_storage list and assigns it to the unit
        #print("Unit {} (Infectious == {}) is at grid ref {}".format(unit.id_number, unit.infectious, unit.grid_ref))
    for unit in units_infectious:
        unit.id_number = counter
        counter += 1
        unit.grid_ref = grid_storage.pop(random.randint(0,len(grid_storage)-1)) #takes out a random part of the grid_storage list and assigns it to the unit
        #print("Unit {} (Infectious == {}) is at grid ref {}".format(unit.id_number, unit.infectious, unit.grid_ref))
    #for unit in units_healer:
    #    unit.id_number = counter
    #    counter += 1
    #    unit.grid_ref = grid_storage.pop(random.randint(0,len(grid_storage)-1)) #takes out a random part of the grid_storage list and assigns it to the unit
    #    print("Unit {} (Infectious == {}) is at grid ref {}".format(unit.id_number, unit.infectious, unit.grid_ref))

def infection_protocol(infectious_unit): #makes non-infected units that are near infected units get "infected", but not infectious.
    infected = []
    #print("Infection Protocol Running...")
    for unit in units_non_infectious:
        if abs(unit.grid_ref[0] - infectious_unit.grid_ref[0]) <= 1 and abs(unit.grid_ref[1] - infectious_unit.grid_ref[1]) <= 1: #will check if a non-infectious unit is within 1 vertical or horizontal square of the infectious unit. This will also include units that are diagonally 1 integer away
            unit.make_infected()
            infected.append(unit)
        else:
            pass
    #print("Infection Protocol for-loop completed...")
    #print("Unit {} has infected: {}".format(infectious_unit.id_number,infected))
    
def make_infected_into_infectious():
    #print ("Non-infectious Units: {}".format(len(units_non_infectious))) #debugging
    
    transfer = []

    for unit in units_non_infectious:
        if unit.infected == True and unit.infectious == False:
            #print("{} is about to become infectious...".format(unit))
            #print("Current units:\n  Non-infectious: {},\n  Infectious: {}".format(units_non_infectious,units_infectious))
            unit.infectious = True
            transfer.append(unit) ### temp holding variable which stores the unit that is going to be transferred from non-infectious to infectious
        else:
            pass
        
    for unit in transfer:
        units_infectious.append(unit) #appends this unit to the "infectious" list.
        units_non_infectious.remove(unit) #the use of the remove method here relies on each unit in the "transfer" being unique
    

def move_units():
    for unit in units_non_infectious:
        unit.move()
    for unit in units_infectious:
        unit.move()
    #for unit in units_healer:
    #    try:
    #        unit.move()
    #    except:
    #        print("Tried to move healer {} unsuccessfuly".format(unit.id_number))

visible_table = [] #the list carrying the table that will be printed to the terminal each round. The top level is the Y coordinate

def draw_table(): #creates the table that will be used to display the simulation
    visible_table.clear()
    for y in range(0,grid[1]+1):
        visible_table.append([])
        for x in range(0,grid[0]+1):
            visible_table[y].insert(x,"##\n##\n##")

def draw_table_objects(): #reminder: the visible_table list goes: visible_table[y-coordinate][x-coordinate]
    for i in units_infectious:
        x_coord = i.grid_ref[0]
        #print(x_coord)
        y_coord = i.grid_ref[1]
        #print(y_coord)
        #visible_table[y_coord][x_coord] #clears the cell to allow unit names to be appended cleanly
        visible_table[y_coord][x_coord] = "{start} U{unit} {fin}\n".format(start=Fore.RED, unit = i.id_number, fin=Style.RESET_ALL)
    for z in units_non_infectious:
        x_coord, y_coord = z.grid_ref[0],z.grid_ref[1]
        #visible_table[y_coord][x_coord] = "" #clears the cell to allow unit names to be appended cleanly
        visible_table[y_coord][x_coord] = "{start} U{unit} {fin}\n".format(start=Fore.GREEN, unit = z.id_number, fin=Style.RESET_ALL)

def print_table():
    df = pd.DataFrame(visible_table)
    print(tabulate(df, tablefmt="fancy_grid", showindex="none"))

def round_prompter(prompt):
    continue_prompt = False
    while continue_prompt != True:
        continue_input = input("{} (Y/N): ".format(prompt))
        if continue_input == "Y":
            continue_prompt = True
        elif continue_input == "N":
            print("Ending simulation.")
            return
        else:
            pass

def run(input_rounds):
    round_prompter("Commence simulation?")
    for i in range(1,input_rounds+1):
        if i > 1:
            round_prompter("Commence round {}?".format(i))
        print("\n --- Round {} --- \n".format(i))
        draw_table()
        draw_table_objects()
        print_table()
        move_units()
        for inf in units_infectious:
            infection_protocol(inf)
        make_infected_into_infectious()

    #print("Units after infection: \nNon-infectious: {}, Infectious: {}".format(units_non_infectious,units_infectious))

create_grid()

create_units()

run(rounds)



