_Debug = False

import math
import logging

#---------------Logger setup----------------#
logger = logging.getLogger(__name__)
logger.propagate = False

if not logger.hasHandlers():

    if _Debug == True:
        loglevel = logging.DEBUG 
    else:
        loglevel = logging.ERROR

    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(f"Bison2.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(loglevel)
    logger.addHandler(stream_handler)
#-----------Logger setup finished------------#


def main():
    T = Equip()
    print(T.fDET)

    T(200)
    print(T.fDET)

def Speedtest(Character = 0, Gear = 0, Materia = 0, Food = 0, percentage = 0):
    Equipment = Character + Gear + Materia
    SkillSpeed = min( (1 + percentage)*Equipment, Equipment+Food ) 

    k = 1900 / 130
    mults_of_k = math.floor((SkillSpeed - 400) / k)

    if mults_of_k < 1:
        GCD = 2.50
    elif mults_of_k == 1:
        GCD = 2.50 - 0.01
    elif mults_of_k > 1:
        m = math.floor((mults_of_k - 1) / 4)
        GCD = 2.49 - 0.01 * m

    return round(GCD, 2)


class Equipper():
    def __init__(Character, Gear, Materia, Food):

        #Level 90 properties
        self.MAIN = 390
        self.SUB = 400
        self.DIV = 1900
        self.HP = 3000

        self.DET = 100

    @property
    def fDET(self):
        print('property called')
        return math.floor(140*(self.DET - self.MAIN) / self.DIV + 1000)

    def __call__(self, Character, Gear, Materia, Food):
        self.DET = det


#---------------------------------------#




def Damage(self, Potency):
    Damage = (((Potency * self.fDET * self.fAP) / 100) / 1000)
    return Damage





def JobModifier(self):
    match self.Character.Job:

        case 'CUSTOM':
            jobmod = {'HP':142.5, 'MP':100, 'STR':102.5, 'VIT':110, 'DEX':95, 'INT':60, 'MND':77.5}

        case 'GNB':
            jobmod = {'HP':120, 'MP':100, 'STR':100, 'VIT':110, 'DEX':95, 'INT':60, 'MND':100}

        case 'DRK':
            jobmod = {'HP':140, 'MP':100, 'STR':105, 'VIT':110, 'DEX':95, 'INT':60, 'MND':40}

        case 'WAR':
            jobmod = {'HP':145, 'MP':100, 'STR':105, 'VIT':110, 'DEX':95, 'INT':60, 'MND':55}

        case 'PLD':
            jobmod = {'HP':140, 'MP':100, 'STR':100, 'VIT':110, 'DEX':95, 'INT':60, 'MND':100}

    return jobmod




def fCriticalHit(self, CRIT = -1):
    if CRIT < 0:
        CriticalHit = self.CriticalHit
    else:
        CriticalHit = CRIT

    pCRIT = math.floor(200 * (CriticalHit - self.SUB)/self.DIV + 50) / 10
    fCRIT = math.floor(200 * (CriticalHit - self.SUB)/self.DIV + 1400)
    return fCRIT, pCRIT


def fDirectHit(self, DH = -1):
    if DH < 0:
        DirectHit = self.DirectHitRate
    else:
        DirectHit = DH

    fDH = 125
    pDH = math.floor(550*(DirectHit - self.SUB)/self.DIV) / 10

    return fDH, pDH


def fTenacity(self, TEN = -1):
    if TEN < 0:
        Tenacity = self.Tenacity
    else:
        Tenacity = TEN

    fTEN = math.floor(100 * (Tenacity - self.SUB) / self.DIV + 1000)
    return fTEN


def fSpeed(self, SKS = -1):
    if SKS < 0:
        SkillSpeed = self.SkillSpeed
    else:
        SkillSpeed = SKS

    fSPD = math.floor(130 * (SkillSpeed - self.SUB) / self.DIV + 1000)
    return fSPD


def fAutoAttack(self):
    fAUTO = math.floor(math.floor(self.MAIN * self.JobMod['STR'] / 1000 + self.Gear.PhysicalDamage) * self.Delay/3)
    return fAUTO


def fWeaponDamage(self):
    fWD = math.floor(self.MAIN * self.JobMod['STR'] / 1000 + self.Gear.PhysicalDamage)
    return fWD


def fAttack(self):
    # fAP = (165  * ( AP - 340 ) / 340 ) + 100 #Non-Tanks Level 80
    fATK = math.floor(115 * (self.AttackPower - 340) / 340) + 100  # Tanks Level 80
    return fATK

def HP_Tank(self):
    HealthPoints = self.Character.HP + math.floor(self.HP_LV * self.JobMod['HP'] / 100) + math.floor((self.Vitality - self.MAIN) * 31.5 )
    return HealthPoints

def GCD(self, SKS = -1):
    if SKS < 0:
        SkillSpeed = self.SkillSpeed
    else:
        SkillSpeed = SKS

    k = 1900 / 130
    mults_of_k = math.floor((SkillSpeed - 400) / k)

    if mults_of_k < 1:
        GCD = 2.50
    elif mults_of_k == 1:
        GCD = 2.50 - 0.01
    elif mults_of_k > 1:
        m = math.floor((mults_of_k - 1) / 4)
        GCD = 2.49 - 0.01 * m

    return round(GCD, 2)

def fGCD(self, CD, SKS = -1):
    if SKS < 0:
        SkillSpeed = self.SkillSpeed
    else:
        SkillSpeed = SKS

    CD = CD * 1000
    GCD = math.floor(CD * (1000 + math.ceil(130 * (self.SUB - SkillSpeed)/ self.DIV)) / 10000) / 100 
    return GCD


def dps(self):
    job = self.Character.Job
    gain = 1.0

    match job:

        case 'CUSTOM':
            #PLD and WAR combined for omni

            dps1_normal = 16.28 * self.AutoAtk_Damage(110, buff_1 = 1.0) + self.Direct_Damage(5584, buff_1 = 1.0) + self.DoT_Damage(677, buff_1 = 1.0) + self.DoT_Magical(459, buff_1 = 1.0)
            dps1_fof = 10.14 * self.AutoAtk_Damage(110, buff_1 = 1.25) + self.Direct_Damage(3786, buff_1 = 1.25) + self.DoT_Damage(506, buff_1 = 1.25)
            dps1 = (dps1_normal + dps1_fof) / 60
            dps1_rating = 10000 * dps1 / (5584+677+459+3786+506)

            dps2_normal = 17.81 * self.AutoAtk_Damage(110) + self.Direct_Damage(7004)
            dps2_CDH = self.Direct_Damage(3303, CDH = 1)                
            dps2 = (dps2_normal + dps2_CDH) / 60
            dps2_rating = 10000 * dps2 / (7004 + 3303)

            dps = (dps1 + dps2) / 2
            dps_rating = (dps1_rating + dps2_rating) / 2


        case 'GNB':
            dps_normal = 14.35 * self.AutoAtk_Damage(110) + self.Direct_Damage(6375)
            dps_NM = 7.04 * self.AutoAtk_Damage(110, buff_1 = 1.2) + self.Direct_Damage(5981, buff_1 = 1.2) + self.DoT_Damage(893, buff_1 = 1.2)
            dps = (dps_normal + dps_NM) / 60
            dps_rating = 10000 * dps / (6375 + 5981 + 893)

        case 'DRK':
            dps = 20.19 * self.AutoAtk_Damage(110) + self.Direct_Damage(15002)
            dps = dps / 60
            dps_rating = 10000 * dps / (15002)

        case 'WAR':
            dps_normal = 17.81 * self.AutoAtk_Damage(110) + self.Direct_Damage(7004)
            dps_CDH = self.Direct_Damage(3303, CDH = 1)
            
            dps = (dps_normal + dps_CDH) / 60
            dps_rating = 10000 * dps / (7004 + 3303)

        case 'PLD':
            dps_normal = 16.28 * self.AutoAtk_Damage(110, buff_1 = 1.0) + self.Direct_Damage(5584, buff_1 = 1.0) + self.DoT_Damage(677, buff_1 = 1.0) + self.DoT_Magical(459, buff_1 = 1.0)
            dps_fof = 10.14 * self.AutoAtk_Damage(110, buff_1 = 1.25) + self.Direct_Damage(3786, buff_1 = 1.25) + self.DoT_Damage(506, buff_1 = 1.25)
            dps = (dps_normal + dps_fof) / 60
            dps_rating = 10000 * dps / (5584+677+459+3786+506)

    return math.floor(dps), round(dps_rating, 2)


def Direct_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1, CDH = 0):
    D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) / 100) / 1000)
    D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) / 1000) * self.fWD) / 100) * self.Trait) / 100)
    if CDH == 1:
        modCRIT = self.fCRIT
        modDH = self.fDH
    elif CalcAverage == 1:
        modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
        modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
    else:
        #To be added...
        modCRIT = 1
        modDH = 1
    D3 = math.floor(math.floor(math.floor(math.floor(D2 * modCRIT) / 1000) * modDH) / 100)
    D = math.floor(math.floor(math.floor(math.floor(D3 * 100) / 100) * buff_1) * buff_2)
    return D

def DoT_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
    D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) / 100) / 1000)
    D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) / 1000) * self.fSPD) / 1000) * self.fWD) / 100) * self.Trait) / 100) + 1
    if CalcAverage == 1:
        modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
        modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
    else:
        #To be added...
        modCRIT = 1.0
        modDH = 1.0
    D3 = math.floor(math.floor(D2 * 100) / 100)
    D = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D3 * modCRIT) / 1000) * modDH) / 100) * buff_1) * buff_2)
    return D

def DoT_Magical(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
    D1 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * self.fWD)/100)*self.fATK)/100)*self.fSPD)/1000)
    D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fDET)/1000)*self.fTEN)/1000)*self.Trait)/100)+1
    D3 = math.floor(math.floor(D2 * 100)/100)
    if CalcAverage == 1:
        modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
        modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100

    D = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D3*modCRIT)/1000)*modDH)/100)*buff_1)*buff_2)
    return D

def AutoAtk_Damage(self, Potency, buff_1 = 1.0, buff_2 = 1.0, CalcAverage = 1):
    D1 = math.floor(math.floor(math.floor(Potency * self.fATK * self.fDET) /100 ) /1000 )
    D2 = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(D1 * self.fTEN) /1000 ) * self.fSPD ) /1000 ) * self.fAUTO ) /100 ) * self.Trait ) /100 )
    if CalcAverage == 1:
        modCRIT = (self.fCRIT * self.pCRIT + (100-self.pCRIT) * 1000) / 100
        modDH = (self.fDH * self.pDH + (100 - self.pDH) * 100) / 100
    else:
        #To be added...
        modCRIT = 1.0
        modDH = 1.0

    D3 = math.floor(math.floor(math.floor(math.floor(D2 * modCRIT ) /1000 ) * modDH ) /100 )
    D = math.floor(math.floor(math.floor(math.floor(D3 * 100 ) /100 ) * buff_1 ) * buff_2 )
    return D



if __name__ == '__main__':
    main()
