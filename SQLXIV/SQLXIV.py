import requests
import lxml
import json
import sqlite3
from tqdm import tqdm
from bs4 import BeautifulSoup as bfs


def main():
    print('Main')
    db = database('XIV.db')
    db.update_food()
    db.close()


class database:
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.c = self.connection.cursor()

        with self.connection:
            self.c.execute("""CREATE TABLE IF NOT EXISTS Actions(
                Job text,
                Action text,
                Type text,
                Cast text,
                Recast text,
                Effect text,
                DamageType text,
                Directpotency integer,
                DoTpotency integer
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

            self.c.execute("""CREATE TABLE IF NOT EXISTS Weapons(
                Name text,
                Type text,
                Relic boolean,
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
                SubstatLimit integer,
                SubstatPool integer
                )""")

    def close(self):
        self.connection.close()

    ###------------------------------------------------------------------------------###

    def insert_action(self, *Values):
        with self.connection:
            self.c.execute("DELETE FROM Actions WHERE Job = :Job AND Action = :Action",
                {'Job':Values[0], 'Action':Values[1]})
            self.c.execute("INSERT INTO Actions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(Values))

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

    def update_all(self):
        pass

    ###------------------------------------------------------------------------------###

    def update_actions(self):
        pass

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

    def update_urls(self, iLVL_gear = [620, 999], iLVL_food = [600, 999]):
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