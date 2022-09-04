import requests
import lxml
import json
import sqlite3
from tqdm import tqdm
from bs4 import BeautifulSoup as bfs

import pmapUI


def main():
    print('Main')
    db = database('XIV.db')
    db.update_pmap()
    #db.update_actions()
    #stuff = db.get_Equipment(Job='GNB', Type='Body', Keyword='Asphodelos')
    db.close()


class database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.c = self.connection.cursor()

        with self.connection:
            self.c.execute("""CREATE TABLE IF NOT EXISTS Actions(
                Job text,
                Name text,
                Type text,
                Cast text,
                Recast text,
                Cost text,
                Effect text,
                DamageType text,
                Directpotency text,
                DoTpotency text
                )""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS URLs(
                Category text,
                Name text,
                Type text,
                URL text
                )""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS Equipment(
                Name text,
                Type text,
                iLVL integer,
                Jobs text,
                Materia_Sockets integer,
                MainStat text,
                MainStatValue integer,
                Vitality integer,
                Substat1 text,
                Substat1Value integer,
                Substat2 text,
                Substat2Value integer
                )""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS Food(
                Name text,
                iLVL integer,
                PercentBonus integer,
                VitalityMax integer,
                Stat1 text,
                Stat1Max integer,
                Stat2 text, 
                Stat2Max integer
                )""")

            self.c.execute("""CREATE TABLE IF NOT EXISTS pmaps(
                Job text,
                Buff1 integer,
                Buff2 integer,
                #
                APotency integer,
                Potency integer,
                PotencyDoT integer,
                Mpotency integer,
                MpotencyDoT integer,
                #
                APotency1 integer,
                Potency1 integer,
                PotencyDoT1 integer,
                Mpotency1 integer,
                MpotencyDoT1 integer,
                #
                APotency2 integer,
                Potency2 integer,
                PotencyDoT2 integer,
                Mpotency2 integer,
                MpotencyDoT2 integer,
                #
                APotency12 integer,
                Potency12 integer,
                PotencyDoT12 integer,
                Mpotency12 integer,
                MpotencyDoT12 integer,
                #
                APotencyCrit integer,
                PotencyCrit integer,
                PotencyDoTCrit integer,
                MpotencyCrit integer,
                MpotencyDoTCrit integer,
                #
                APotencyCDH integer,
                PotencyCDH integer,
                PotencyDoTCDH integer,
                MpotencyCDH integer,
                MpotencyDoTCDH integer
                )""")

    def close(self):
        self.connection.close()

    ###------------------------------------------------------------------------------###

    def insert_action(self, *Values):
        with self.connection:
            self.c.execute("DELETE FROM Actions WHERE Job = :Job AND Name = :Name",
                {'Job':Values[0], 'Name':Values[1]})
            self.c.execute("INSERT INTO Actions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(Values))

    ###------------------------------------------------------------------------------###

    def insert_Equipment(self, *Values):
        with self.connection:
            self.c.execute("DELETE FROM Equipment WHERE Name = :Name",{'Name':Values[0]})
            self.c.execute("INSERT INTO Equipment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (Values))

    ###------------------------------------------------------------------------------###

    def insert_Food(self, *Values):
        with self.connection:
            self.c.execute("DELETE FROM Food WHERE Name = :Name",{'Name':Values[0]})
            self.c.execute("INSERT INTO Food VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (Values))

    ###------------------------------------------------------------------------------###
    # Returns dictionary of equipment using 3 arguments
    def get_Equipment(self, Job, Type, Keyword):
        sjob = f"%{Job}%"
        sKeyword = f"%{Keyword}%"
        with self.connection:
            self.c.execute("""SELECT json_object(
                            'Name', Name,
                            'iLVL', iLVL,
                            'MateriaSockets', Materia_Sockets,
                            'MainStat', MainStat,
                            'MainStatValue', MainStatValue,
                            'Vitality', Vitality,
                            'Substat1', Substat1,
                            'Substat1Value', Substat1Value,
                            'Substat2', Substat2,
                            'Substat2Value', Substat2Value
                            ) FROM Equipment WHERE Jobs LIKE :Job 
                            AND Type = :Type 
                            AND Name LIKE :kw""",{'Job':sjob, 'Type': Type, 'kw':sKeyword})
            res = self.c.fetchall()
            if not len(res) == 1:
                raise ValueError('[SQLXIV] Error in "get_Equipment. Arguments yielded multiple results in database.')
        
        #Convert to dictionary
        res = list(res[0])[0]
        res = json.loads(res)

        return res

    ###------------------------------------------------------------------------------###

    def update_pmap(self):
        Job = input('Job: ')
        Time = float(input('Encounter length (seconds): '))

        print('\n Personal buffs \n')
        Buff1_Name = input('Buff 1 name: ')
        Buff2_Name = input('Buff 2 name: ')
        Buff1 = input(f"Percent damage increase from {Buff1_Name}: ")
        Buff2 = input(f"Percent damage increase from {Buff2_Name}: ")
        
        print('\n Potency with no personal buffs \n')
        APotency = float(input('Auto Attack Potency: '))/Time
        Potency = float(input('Direct Physical Potency: '))/Time
        PotencyDoT = float(input('DoT Physical Potency: '))/Time
        Mpotency = float(input('Direct Magical Potency: '))/Time
        MpotencyDoT = float(input('DoT Magical Potency: '))/Time

        print(f"\n Potency under {Buff1_Name} \n")
        APotency1 = float(input('Auto Attack Potency: '))/Time
        Potency1 = float(input('Direct Physical Potency: '))/Time
        PotencyDoT1 = float(input('DoT Physical Potency: '))/Time
        Mpotency1 = float(input('Direct Magical Potency: '))/Time
        MpotencyDoT1 = float(input('DoT Magical Potency: '))/Time

        print(f"\n Potency under {Buff2_Name} \n")
        APotency2 = float(input('Auto Attack Potency: '))/Time
        Potency2 = float(input('Direct Physical Potency: '))/Time
        PotencyDoT2 = float(input('DoT Physical Potency: '))/Time
        Mpotency2 = float(input('Direct Magical Potency: '))/Time
        MpotencyDoT2 = float(input('DoT Magical Potency: '))/Time

        print(f"\n Potency under both {Buff1_Name} and {Buff2_Name} \n")
        APotency12 = float(input('Auto Attack Potency: '))/Time
        Potency12 = float(input('Direct Physical Potency: '))/Time
        PotencyDoT12 = float(input('DoT Physical Potency: '))/Time
        Mpotency12 = float(input('Direct Magical Potency: '))/Time
        MpotencyDoT12 = float(input('DoT Magical Potency: '))/Time
        
        print('\n Potency with guaranteed critical hit \n')
        APotencyCrit = float(input('Auto Attack Potency: '))/Time
        PotencyCrit = float(input('Direct Physical Potency: '))/Time
        PotencyDoTCrit = float(input('DoT Physical Potency: '))/Time
        MpotencyCrit = float(input('Direct Magical Potency: '))/Time
        MpotencyDoTCrit = float(input('DoT Magical Potency: '))/Time

        with self.connection:
            self.c.execute("DELETE FROM pmaps WHERE Job = :Job",{'Job':Job})
            self.c.execute("""INSERT INTO pmaps VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(
                Job,
                Buff1,
                Buff2,
                 #Normal
                APotency, 
                Potency,
                PotencyDoT,
                Mpotency,
                MpotencyDoT,
                 #Buff 1
                APotency1,
                Potency1,
                PotencyDoT1,
                Mpotency1,
                MpotencyDoT1,
                 #Buff 2
                APotency2, 
                Potency2,
                PotencyDoT2,
                Mpotency2,
                MpotencyDoT2,
                #Both buffs
                APotency12,  
                Potency12,
                PotencyDoT12,
                Mpotency12,
                MpotencyDoT12,
                 #Crit
                APotencyCrit,  
                PotencyCrit,
                PotencyDoTCrit,
                MpotencyCrit,
                MpotencyDoTCrit
                 #Crit direct hit
                APotencyCDH,  
                PotencyCDH,
                PotencyDoTCDH,
                MpotencyCDH,
                MpotencyDoTCDH))


    ###------------------------------------------------------------------------------###

    def update_all(self):
        self.update_food()
        self.update_equipment()
        self.update_actions() #Not finished - Experimental parsing

    ###------------------------------------------------------------------------------###

    def update_actions(self):
        print('Updating Actions database...')
        with self.connection:
            self.c.execute("SELECT URL FROM URLs WHERE Category = 'JobGuide' AND Type = 'Specific'")
            URLs = self.c.fetchall()

        for url in tqdm(URLs):
            url = list(url)[0]
            source = requests.get(url).text
            soup = bfs(source, 'lxml')

            pve_actions = soup.find('tbody', class_="job__tbody")
            pve_actions_list = pve_actions.find_all('tr')

            Job = url.split("/")[-1]

            for action in pve_actions_list:
                if "pve_action" not in str(action):
                    continue

                Name = action.find('td', class_="skill").find('strong').text
                Type = action.find('td', class_="classification").text
                Cast = action.find('td', class_="cast").text
                Recast = action.find('td', class_="recast").text
                Cost = action.find('td', class_="cost").text
                Effect = action.find('td', class_="content").text.replace("\n","").lstrip()

                #Now parse skill potency etc
                Magical_keywords = ["unaspected", "aspected", "magical", "fire", "wind", "earth", "water", "ice", "lightning"]
                Magical = any([kw in Effect for kw in Magical_keywords])

                DamageType = "-"
                DirectPotency = "-"
                DoTPotency = "-"

                if "potency" in Effect:
                    if Magical:
                        DamageType = 'Magical'
                    else:
                        DamageType = 'Physical'
    
                    s = ""
                    if "Combo Potency" in Effect:
                        s = Effect.split("Combo Potency: ")[1] 
                    elif "a potency of " in Effect:
                        s = Effect.split("a potency of ")[1]

                    if not s == "":
                        Potency = ""
                        for char in s:
                            if char.isdigit():
                                Potency += char
                            else:
                                break
                        DirectPotency = Potency
                
                self.insert_action(Job,
                                    Name,
                                    Type,
                                    Cast,
                                    Recast,
                                    Cost,
                                    Effect,
                                    DamageType,
                                    DirectPotency,
                                    DoTPotency)

    ###------------------------------------------------------------------------------###

    def update_equipment(self):
        print('Updating Equipment database...')
        with self.connection:
            self.c.execute("SELECT URL FROM URLs WHERE Category = 'Equipment' AND Type = 'Specific'")
            URLs = self.c.fetchall()

        for url in tqdm(URLs):
            url = list(url)[0]
            source = requests.get(url).text
            soup = bfs(source, 'lxml')

            Name = soup.find('h2', class_= "db-view__item__text__name").text.strip()  
            Type = soup.find('p', class_="db-view__item__text__category").text
            if "Arm" in Type:
                Type = "Weapon"
            iLVL = int(soup.find('div', class_="db-view__item_level").text.split('Item Level ')[1])
            Jobs = soup.find('div', class_="db-view__item_equipment__class").text
            Materia_Sockets = str(soup.find('ul', class_='db-view__materia_socket')).count('socket normal')
            
            Bonuses = soup.find('ul', class_="db-view__basic_bonus").text
            Split = Bonuses.split('\n')

            for info in Split[1:-2]:
                stat, val = info.split(' +')

                if stat in 'Strength Dexterity Intelligence Mind':
                    MainStat, MainStatValue = [stat, int(val)]
                elif stat == 'Vitality':
                    Vitality = int(val)
                
            Sub1, Sub1Value = Split[3].split(' +')
            Sub2, Sub2Value = Split[4].split(' +')
            Sub1Value = int(Sub1Value)
            Sub2Value = int(Sub2Value)

            if Sub1Value > Sub2Value:
                SubStat1, SubStat1Value = [Sub1, Sub1Value]
                SubStat2, SubStat2Value = [Sub2, Sub2Value]  
            else:
                SubStat1, SubStat1Value = [Sub2, Sub2Value]
                SubStat2, SubStat2Value = [Sub1, Sub1Value]  

                
            self.insert_Equipment(Name, 
                                Type, 
                                iLVL, 
                                Jobs, 
                                Materia_Sockets, 
                                MainStat, 
                                MainStatValue, 
                                Vitality,
                                SubStat1,
                                SubStat1Value,
                                SubStat2, 
                                SubStat2Value)

    ###------------------------------------------------------------------------------###

    def update_food(self):
        print(f"Updating food...")
        with self.connection:
            self.c.execute("SELECT URL FROM URLs WHERE Category = 'Food' AND Type = 'Specific'")
            URLs = self.c.fetchall()

        for url in tqdm(URLs):    
            url = list(url)[0]
            source = requests.get(url).text
            soup = bfs(source, 'lxml')

            Name = soup.find('h2', class_="db-view__item__text__name").text.strip().split("\n")[0]
            iLVL = soup.find('div', class_="db-view__item_level").text.split(' ')[2]
            
            Bonuses = soup.find('ul', class_="sys_hq_element").text

            #Ignore crafting food
            if "Craftsmanship" in Bonuses or "CP" in Bonuses or "Perception" in Bonuses or "Gathering" in Bonuses:
                continue

            #Extract data from soup object
            secondstat = False
            for bonus in Bonuses.split("\n"):
                if len(bonus) < 1:
                    continue
                if "Vitality" in bonus:
                    VitalityMax = bonus.split("Max ")[1].split(")")[0]
                    PercentBonus = bonus.split("+")[1].split("%")[0]
                elif secondstat == False: 
                    Stat1_pre = bonus.split(" +")[0]
                    Stat1Max_pre = bonus.split("Max ")[1].split(")")[0]
                    secondstat = True
                elif secondstat == True: 
                    Stat2_pre = bonus.split(" +")[0]
                    Stat2Max_pre = bonus.split("Max ")[1].split(")")[0]

            #Set major stat to stat1 etc
            if Stat1Max_pre > Stat2Max_pre:
                Stat1 = Stat1_pre
                Stat1Max = Stat1Max_pre
                Stat2 = Stat2_pre
                Stat2Max = Stat2Max_pre
            else:
                Stat1 = Stat2_pre
                Stat1Max = Stat2Max_pre
                Stat2 = Stat1_pre
                Stat2Max = Stat1Max_pre

            self.insert_Food(Name,
                           iLVL,
                           PercentBonus,
                           VitalityMax,
                           Stat1,
                           Stat1Max,
                           Stat2,
                           Stat2Max)

    ###------------------------------------------------------------------------------###

    def update_urls(self, iLVL_gear = [630, 999], iLVL_food = [610, 999]):
        print(f"Updating URLs...")

        Equipment = [('Weapon', 'Page', 'Entry Point', "https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1"),
                    ('Gear', 'Page', 'Entry Point', "https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3"),
                    ('Accessories', 'Page', 'Entry Point', "https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=4")]

        Food = [('Food', 'Page', 'Entry Point', "https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=5&category3=46")]
        
        Actions = [('JobGuide', 'Page', 'Entry Point', "https://na.finalfantasyxiv.com/jobguide")]

        Entry_points = Equipment + Food + Actions


        ###----Scrape specific equipment urls----###
        print(f"{' ':5}Updating Equipment urls")
        Equipment_url_base = "https://na.finalfantasyxiv.com"
        Equipment_url_list = []

        for val in Equipment:
            link = list(val)[3]
            source = requests.get(f"{link}&min_item_lv={iLVL_gear[0]}&max_item_lv={iLVL_gear[1]}").text
            soup = bfs(source, 'lxml')
            Gear = soup.find_all('a', class_='db_popup db-table__txt--detail_link')

            Pages_left = True
            while Pages_left == True:
    
                #Get all equipment links from page
                for g in Gear: 
                    Link = Equipment_url_base + g.get('href')
                    Name = g.text
                    Equipment_url_list.append(('Equipment', Name, 'Specific', Link))

                #Check for next page
                Next_page = soup.find('li', class_="next").find('a')
                if Next_page == None:
                    Pages_left = False 
                else:
                    Next_url = Next_page.get('href')
                    source = requests.get(Next_url).text
                    soup = bfs(source, 'lxml')
                    Gear = soup.find_all('a', class_='db_popup db-table__txt--detail_link')


        ###-------Scrape specific food urls-------###
        print(f"{' ':5}Updating Food urls")
        Food_url_base = "https://na.finalfantasyxiv.com"
        Food_url_list = []
        link = list(Food[0])[3]

        source = requests.get(f"{link}&min_item_lv={iLVL_food[0]}&max_item_lv={iLVL_food[1]}").text
        soup = bfs(source, 'lxml')
        Food = soup.find_all('a', class_='db_popup db-table__txt--detail_link')

        Pages_left = True
        while Pages_left == True:

            #Get all food links from page
            for f in Food: 
                Link = Food_url_base + f.get('href')
                Name = f.text
                Food_url_list.append(('Food', Name, 'Specific',Link))

            #Check for next page
            Next_page = soup.find('li', class_="next").find('a')
            if Next_page == None:
                Pages_left = False 
            else:
                Next_url = Next_page.get('href')
                source = requests.get(Next_url).text
                soup = bfs(source, 'lxml')
                Food = soup.find_all('a', class_='db_popup db-table__txt--detail_link')


        ###--------Create Action URLs--------###
        print(f"{' ':5}Updating Jobguide urls")
        Actions_url_base = list(Actions[0])[3]
        Actions_url_list = []

        JobList = ['paladin', 'gunbreaker', 'warrior', 'darkknight',
                    'whitemage', 'scholar', 'astrologian', 'sage',
                    'monk', 'samurai', 'dragoon', 'reaper', 'ninja',
                    'bard', 'dancer', 'machinist',
                    'blackmage', 'redmage', 'summoner']

        for Job in JobList:
            Actions_url = f"{Actions_url_base}/{Job}"
            Actions_url_list.append(('JobGuide', Job, 'Specific', Actions_url))


        ###--------Insert URLs into database--------###
        All_urls = Entry_points + Actions_url_list + Equipment_url_list + Food_url_list

        with self.connection:
            self.c.execute("DELETE FROM URLs")
            self.c.executemany("INSERT INTO URLs VALUES (?, ?, ?, ?)", All_urls)

    ###------------------------------------------------------------------------------###



if __name__ == "__main__":
    main()