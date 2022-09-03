import numpy as np
import json


def main():
    Gear_set = Gearset('GNB')
    Gear_ID = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #Gear_set.show_JobGear()

    Gear_set(Gear_ID)
    print(Gear_set)

    Materia = [5, 5, 5, 5, 0, 2, 0]
    print(Materia, Gear_set.Test_Materia(Materia))


class Gearset():
    def __init__(self, Job):
        self.null = {'Materia_Matrix':np.zeros([7, 7]),
                    'AllowedMateria':[{},{},{},{},{},{},{},{},{},{},{},{}],
                    'Materia_Sockets':0,
                    'iLVL':0,
                    'Strength':0,
                    'Dexterity':0,
                    'Mind':0,
                    'Intelligence':0,
                    'Vitality':0,
                    'Critical Hit':0,
                    'Determination':0,
                    'Direct Hit Rate':0,
                    'Skill Speed':0,
                    'Spell Speed':0,
                    'Tenacity':0,
                    'Piety':0}
        self.reset()
        self.ID = None
        self.slots = {'Weapon':None,
                    'Head':None,
                    'Body':None,
                    'Hands':None,
                    'Legs':None,
                    'Feet':None,
                    'Earrings':None,
                    'Necklace':None,
                    'Bracelets':None,
                    'Ring1':None,
                    'Ring2':None}        
        self.JobGear = self.slots.copy()
        with open('database.json') as file:
            self.database = json.load(file)
        self.get_JobGear(Job)

    def reset(self):
        self.__dict__.update(self.null)

    def __call__(self, Gear_ID):
        Weapon, Shield, Head, Chest, Hands, Legs, Feet, Ear, Neck, Bracelet, Ring1, Ring2 = list(Gear_ID)
        self.ID = f"{Weapon}{Shield}{Head}{Chest}{Hands}{Legs}{Feet}{Ear}{Neck}{Bracelet}{Ring1}{Ring2}"
        Choice = {'Weapon':Weapon, 
                'Shield':Shield,
                'Head':Head, 
                'Body':Chest, 
                'Hands':Hands, 
                'Legs':Legs, 
                'Feet':Feet, 
                'Earrings':Ear, 
                'Necklace':Neck, 
                'Bracelets':Bracelet, 
                'Ring1':Ring1,
                'Ring2':Ring2}

        self.reset()
        for i, (Slot, ID) in enumerate(Choice.items()):
            if ID == 0:
                continue

            SaveSlot = Slot
            if 'Ring' in Slot:
                Slot = 'Ring'

            item = self.JobGear[Slot][ID].copy()
            self.slots[SaveSlot] = item.pop('Name')
            self.AllowedMateria[i].update(item.pop('AllowedMateria'))

            for stat, val in item.items():
                setattr(self, stat, self.__dict__.get(stat, 0) + val)

        self.iLVL = int(self.iLVL / 12)
                    
    def __repr__(self):
        for key, val in self.slots.items():
            print(f"{key:>10}:{val}")

        print('---Gearset Stats---')
        info = self.__dict__.copy()
        info.pop('slots')
        info.pop('database')
        info.pop('JobGear')
        info.pop('null')

        logger.debug('Allowed Materia')
        for i in info.pop('AllowedMateria'):
            logger.debug(i)


        for key, val in info.items():
            if key == 'Materia_Matrix':
                print(key)
                print(val)
            else:
                print(f"{key:15}: {val}")

        return ''

    def get_JobGear(self, Job):
        JobGear = {}
        for key, val in self.database.items():
            if Job in val['Jobs']:

                if 'Asphodelos' in key:
                    slot = 1
                elif 'Augmented' in key:
                    slot = 2
                else:
                    slot = 3

                Type = val['Type']
                if 'Arm' in Type:
                    Type = 'Weapon'

                Entry = {'Name':key}
                Entry.update(val)
                Entry.pop('Type')
                Entry.pop('Jobs')

                #Calculate materia matrix
                Materia_value = 30
                default_val = 0
                MatStats = {'Critical Hit':Entry.get('Critical Hit', default_val),
                            'Determination':Entry.get('Determination', default_val),
                            'Direct Hit':Entry.get('Direct Hit', default_val),
                            'Skill Speed':Entry.get('Skill Speed', default_val),
                            'Spell Speed':Entry.get('Spell Speed', default_val),
                            'Tenacity':Entry.get('Tenacity', default_val),
                            'Piety':Entry.get('Piety', default_val)}

                if val['Materia_Sockets'] > 0:
                    Stat_cap = max(MatStats.values())
                    for mkey, mval in MatStats.items():
                        MatStats.update({mkey:min(int((Stat_cap - mval)/Materia_value), val['Materia_Sockets'])})

                    A = np.ones([7, 7])
                    b = list(MatStats.values())
                    bA = b*A
                    Materia_Matrix = (bA + np.transpose(bA))
                    np.fill_diagonal(Materia_Matrix, b)
                    Materia_Matrix.clip(0, val['Materia_Sockets'])

                    logger.debug(Materia_Matrix)

                    Entry.update({'Materia_Matrix':Materia_Matrix})

                Entry.update({'AllowedMateria':MatStats})


                try:
                    JobGear[Type].update({slot:Entry})
                except:
                    JobGear.update({Type:{slot:Entry}})

        self.JobGear = JobGear

    def show_JobGear(self):
        for key, val in self.JobGear.items():
            print(' ')
            print(key)
            for subkey, subval in val.items():
                print(f"    {subkey}: {subval['Name']}")

    def Test_Materia(self, MatList):
        Possible = False

        #Test 1 are all the slots filled?
        if sum(MatList) == self.Materia_Sockets:
            A = np.ones([7,7])
            bA = MatList*A
            Test_Matrix = (bA + np.transpose(bA))
            np.fill_diagonal(Test_Matrix, MatList)

            logger.debug('Test_Matrix')
            logger.debug(Test_Matrix)

            T = self.Materia_Matrix - Test_Matrix
            T_bool = T[:, None] < 0

            if not T_bool.any():
                Possible = True
                logger.debug('Materia set allowed')
            else:
                logger.debug('Materia set failed matrix test')
        else:
            logger.debug('Materia set failed sum test')        

        return Possible    

if __name__ == "__main__":
    main()
