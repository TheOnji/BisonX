#Import modules
import numpy as np
import json
import itertools
import multiprocessing as mproc
from time import time, strftime, gmtime, sleep
from tqdm import tqdm

#Import project files
import Allagan
import Decorators
#from Components import GearX
#from Components import MateriaX
#from Components import FoodX
#from Components import CharacterX
#from SQLXIV import SQLXIV

DEBUG = True

#---------------------------------Main Function-------------------------------#

def main():

    Bison = BisonX(cores = 6)
    GNB_bis = Bison('GNB')
    print(GNB_bis)

#-----------------------------------------------------------------------------#

class BisonX:
    def __init__(self, cores = 1):
        self.Gear_IDs = itertools.product(*([[1, 2]] * 11))
        self.Food_IDs = 'All'
        self.cores = cores
        self.BIS_IDs = {}

    @Decorators.timer
    def __call__(self, Job):
        print(f"[BISON] Starting optimization for {Job} using {self.cores} cores")
        #self.Gear = GearX.Gearset(Job)
        #self.Food = FoodX.Menu()
        #self.Materia = MateriaX.Materia()

        Gear_gen = itertools.product(*([[1, 2]] * 11))
        Gear_list = list(Gear_gen)
        Gear_IDs_cores = np.array_split(Gear_list, self.cores)

        procs = []
        for Gear_IDs_core in Gear_IDs_cores:
            p = mproc.Process(target=self.test, args=Gear_IDs_core)
            procs.append(p)

        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

        return 'Finished!'

    def test(self, *glist):
        print('New process')
        sleep(5)
        print('Process finished')
        return 'Done'

    def run(self, Gear_IDs):
        print('New process')
        for Gear_ID in Gear_IDs:
            self.Gear(Gear_ID)
            Materia_Allowance = [int(limit * tick) for limit, tick in zip(np.diagonal(Gear.Materia_Matrix), config['Materia'].values())]
            Materia_list = [list(range(int(limit) + 1)) for limit in Materia_Allowance]
            Materia_IDs = itertools.product(*Materia_list)

            for Materia_ID in Materia_IDs:
                if Gear.Test_Materia(Materia_ID) == False:
                    continue

                Materia(Materia_ID)

                for Food_ID in Food_IDs:
                    Food(Food_ID)

                    GCD = Allagan_functions.Speedtest(0, 
                                                    getattr(Gear, 'Skill Speed'),
                                                    getattr(Materia, 'Skill Speed'),
                                                    getattr(Food, 'Skill Speed'),
                                                    getattr(Food, 'percentage'))
                    if GCD in config['GCDs']:
                        BIS_IDs.update({GCD:{'Gear_ID':Gear_ID,
                                                'Materia_ID':Materia_ID,
                                                'Food_ID':Food_ID}})

                        #Allagan_functions.Equipper(None, Gear, Materia, Food)

        return BIS_IDs


#def BISON(Job):
#     _init = True

#     #Create callable equipent objects
#     Gear = GearX.Gearset(Job)
#     Food = FoodX.Menu()
#     Materia = MateriaX.Materia()

#     #Gear IDs to check
#     Gear_IDs = itertools.product(*([[1, 2]] * 11))

#     #Food IDs to check
#     Food_list = list(config['Food'].values())
#     Food_IDs = [ID for ID, tick in enumerate(Food_list) if tick]

#     #BIS_IDs for storing results
#     BIS_IDs = {}

#     for Gear_ID in Gear_IDs:
#         Gear(Gear_ID)

#         #Materia IDs to check
#         Materia_Allowance = [int(limit * tick) for limit, tick in zip(np.diagonal(Gear.Materia_Matrix), config['Materia'].values())]
#         Materia_list = [list(range(int(limit) + 1)) for limit in Materia_Allowance]
#         Materia_IDs = itertools.product(*Materia_list)

#         for Materia_ID in Materia_IDs:
#             if Gear.Test_Materia(Materia_ID) == False:
#                 continue

#             Materia(Materia_ID)

#             for Food_ID in Food_IDs:
#                 Food(Food_ID)

#                 GCD = Allagan_functions.Speedtest(0, 
#                                                 getattr(Gear, 'Skill Speed'),
#                                                 getattr(Materia, 'Skill Speed'),
#                                                 getattr(Food, 'Skill Speed'),
#                                                 getattr(Food, 'percentage'))
#                 if GCD in config['GCDs']:
#                     BIS_IDs.update({GCD:{'Gear_ID':Gear_ID,
#                                             'Materia_ID':Materia_ID,
#                                             'Food_ID':Food_ID}})

#                     #Allagan_functions.Equipper(None, Gear, Materia, Food)

#     return BIS_IDs


if __name__ == '__main__':
    main()