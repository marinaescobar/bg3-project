import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

def get_list (url):
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    weapons_table = soup.find('table', class_='wiki_table sortable searchable', attrs={'data-key': 'weapons'})
    rows = weapons_table.find_all('tr')
    row_elements = [row.text for row in rows]
    weapon_names = [element.split('\n')[1].strip() for element in row_elements[1:]]

    return weapon_names

def weapon_details (weapon_list):
    
    weapons_data = {'Name': [],
                    'Description' : [],
                    'One-Handed Damage': [],
                    'Two-Handed Damage': [],
                    'Main Damage Type' : [],
                    'Extra Damage': [],
                    'Extra Damage Type': [],
                    'Type' : [],
                    'Rarity' : [],
                    'Enchantment' : [],
                    'Wielding-Type' : [],
                    'Throwable' : [],
                    'Dippable' : [],
                    'Extra Reach' : [],
                    'Light' : [],
                    'Melee/Range' : [],
                    'Weight' : [],
                    'Price' : [],
                    'Special Attribute 1' : [],
                    'Special Attribute 2' : [],
                    'Special Attribute 3' : [],
                    'Special Attribute 4' : [],
                    'Action 1' : [],
                    'Action 2' : [],
                    'Action 3' : [],
                    'Action 4' : [],
                    'Special Action 1' : [],
                    'Special Action 2' : [],
                    'Special Action 3' : [],
                    'Special Action 4' : [],
                    'Location' : [],
                    'Img url' : [],
                    'UID' : [],
                    'UUID' : []
                    }
    
    for weapon in weapon_list:
        
        # Getting weapon's name
        weapons_data['Name'].append(weapon)
        
        weapon_search = weapon.replace(' ', '_')
        
        if '+' in weapon_search:
            weapon_search = weapon.replace('+', '%2B')
        
        response = requests.get(f'https://bg3.wiki/wiki/{weapon_search}')
        #response = requests.get('https://bg3.wiki/wiki/Club_of_Hill_Giant_Strength')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Getting weapon's description
        try:
            description = soup.find_all(class_='bg3wiki-tooltip-box')
            description = [description.text for description in description]
            description = description[0].replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n')
            weapons_data['Description'].append(description[1])    
        except:
            weapons_data['Description'].append(np.nan)
        
        # Getting special attributes
        more_data = soup.find_all('ul')
        more_data = [element.text.replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n') for element in more_data]
        
        try:    
        # Getting weapon's details 
            properties = soup.find('ul', class_='bg3wiki-property-list')
            properties = [element.text for element in properties]
            properties = [element.strip().replace('\xa0' , '').replace('\u202f' , '') for element in properties if element != '\n']
        except:
            properties = more_data[0]
            
        # Getting Wielding type
        try:
            wield = [properties[i+1] for i, element in enumerate(properties) if 'Enchantment:' in element][0]
            weapons_data['Wielding-Type'].append(wield)
        except:
            weapons_data['Wielding-Type'].append(np.nan)

        # Getting Damage
        try:
            i = properties.index('Damage:')+1
            dmg_combo = properties[i].split('modifier')
            dmg = dmg_combo[0].strip().replace('  ', ' ') + ' modifier'
            dmg_type = dmg_combo[1].strip()
            
            if wield == 'One-Handed':
                weapons_data['One-Handed Damage'].append(dmg)
                weapons_data['Two-Handed Damage'].append(np.nan)
                weapons_data['Main Damage Type'].append(dmg_type)
            else:
                weapons_data['Two-Handed Damage'].append(dmg)
                weapons_data['One-Handed Damage'].append(np.nan)
                weapons_data['Main Damage Type'].append(dmg_type)
        except:
            try:
                i = properties.index('One-handed damage:')+1
                dmg_combo = properties[i].split('modifier')
                dmg = dmg_combo[0].strip().replace('  ', ' ') + ' modifier'
                dmg_type = dmg_combo[1].strip()
                weapons_data['One-Handed Damage'].append(dmg)
                weapons_data['Main Damage Type'].append(dmg_type)

                i2 = properties.index('Two-handed damage:')+1
                dmg_combo2 = properties[i2].split('modifier')
                dmg2 = dmg_combo2[0].strip().replace('  ', ' ') + ' modifier'
                weapons_data['Two-Handed Damage'].append(dmg2)
                
            except: 
                weapons_data['One-Handed Damage'].append(np.nan)
                weapons_data['Main Damage Type'].append(np.nan)
                weapons_data['Two-Handed Damage'].append(np.nan)
        
        # Getting Extra Damage 
        try:
            i = properties.index('Extra damage:')+1
            if 'modifier' in properties[i]:
                dmg_combo = properties[i].split('modifier')
                dmg = dmg_combo[0].strip().replace('  ', ' ') + ' modifier'
                dmg_type = dmg_combo[1].strip()
                weapons_data['Extra Damage'].append(dmg)
                weapons_data['Extra Damage Type'].append(dmg_type)
            else:
                dmg_combo = properties[i].split('  ')
                dmg = dmg_combo[0] + ' ' + dmg_combo[1]
                dmg_type = dmg_combo[2].strip()
                weapons_data['Extra Damage'].append(dmg)
                weapons_data['Extra Damage Type'].append(dmg_type)                
        except:
            weapons_data['Extra Damage'].append(np.nan)   
            weapons_data['Extra Damage Type'].append(np.nan)         

        # Getting Type
        try:
            i = properties.index('Details:')+1
            weapon_type = properties[i]
            weapons_data['Type'].append(weapon_type)
        except:
            weapons_data['Type'].append(np.nan)
            
        # Getting Rarity
        try:
            rarity = [element for element in properties if 'Rarity:' in element][0].replace('Rarity: ', '')
            weapons_data['Rarity'].append(rarity)
        except:
            weapons_data['Rarity'].append(np.nan)
        
        # Getting Enchantment
        try:
            enchantment = [element for element in properties if 'Enchantment:' in element][0].replace('Enchantment: ', '')
            weapons_data['Enchantment'].append(enchantment)
        except:
            weapons_data['Enchantment'].append(np.nan)
        
        # Getting Throwable
        try:
            throw = [element for element in properties if 'Thrown' in element]
            if throw:
                weapons_data['Throwable'].append(True)
            else:
                weapons_data['Throwable'].append(False)
        except:
            weapons_data['Throwable'].append(np.nan)
            
        # Getting Dippable
        try: 
            dipp = [element for element in properties if 'Dippable' in element]
            if dipp:
                weapons_data['Dippable'].append(True)
            else:
                weapons_data['Dippable'].append(False)
        except:
            weapons_data['Dippable'].append(np.nan)
        
        # Getting Light
        try: 
            light = [element for element in properties if 'Light' in element]
            if light:
                weapons_data['Light'].append(True)
            else:
                weapons_data['Light'].append(False)
        except:
            weapons_data['Light'].append(np.nan)
            
        # Getting Extra Reach
        try: 
            reach = [element for element in properties if 'Extra Reach' in element]
            if reach:
                weapons_data['Extra Reach'].append(True)
            else:
                weapons_data['Extra Reach'].append(False)
        except:
            weapons_data['Extra Reach'].append(np.nan)
        
        # Getting melee/range
        try:
            melee = [element for element in properties if 'Melee:' in element or 'Range:' in element][0].replace('Melee: ', '').replace('Range: ', '').replace('  ', ' ')
            weapons_data['Melee/Range'].append(melee)
        except:
            weapons_data['Melee/Range'].append(np.nan)
        
        # Getting weight
        try: 
            weight = [element for element in properties if 'Weight:' in element][0].replace('Weight: ', '').replace('  ', ' ')
            weapons_data['Weight'].append(weight)
        except:
            weapons_data['Weight'].append(np.nan)
        
        # Getting price
        try: 
            price = [element for element in properties if 'Price:' in element][0].replace('Price: ', '').replace('  ', ' ').strip()
            weapons_data['Price'].append(price)
        except:
            weapons_data['Price'].append(np.nan)
        
        # Getting UID and UUID
        try:
            uid = properties[-1].split('\n')[2]
            weapons_data['UID'].append(uid)
            uuid = properties[-1].split('\n')[-1]
            weapons_data['UUID'].append(uuid)
        except:
            weapons_data['UID'].append(np.nan)
            weapons_data['UUID'].append(np.nan)
        
        try: 
            h3 = soup.find_all('h3')
            h3 = [element.text.strip() for element in h3]
            
            if h3.count('Special') > 1:
            
                special_data = more_data[1]
                
                if len(special_data) >= 1:
                    weapons_data['Special Attribute 1'].append(special_data[0].strip())
                    
                if len(special_data) >= 2:
                    weapons_data['Special Attribute 2'].append(special_data[1].strip())  
                else: 
                    weapons_data['Special Attribute 2'].append(np.nan)
                    
                if len(special_data) >= 3:
                    weapons_data['Special Attribute 3'].append(special_data[2].strip())
                else:
                    weapons_data['Special Attribute 3'].append(np.nan)
                    
                if len(special_data) >= 4:
                    weapons_data['Special Attribute 4'].append(special_data[3].strip())
                else:
                    weapons_data['Special Attribute 4'].append(np.nan)
                    
            else:
                weapons_data['Special Attribute 1'].append(np.nan)
                weapons_data['Special Attribute 2'].append(np.nan)
                weapons_data['Special Attribute 3'].append(np.nan)
                weapons_data['Special Attribute 4'].append(np.nan)
                
        except:
            weapons_data['Special Attribute 1'].append(np.nan)
            weapons_data['Special Attribute 2'].append(np.nan)
            weapons_data['Special Attribute 3'].append(np.nan)
            weapons_data['Special Attribute 4'].append(np.nan)
            
        # Getting location
        try:
            h2 = soup.find_all('h2')
            h2 = [element.text.strip() for element in h2]
                       
            if 'Where to find' in h2:
                location = soup.find_all(class_='bg3wiki-tooltip-box')
                location = [location.text for location in location]
                location = location[1].replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n')
                location = ' '.join(location)
                weapons_data['Location'].append(location.strip())
            else:
                weapons_data['Location'].append(np.nan)
        except:
            weapons_data['Location'].append(np.nan)
            
        # Getting actions and special actions
        try:
            all_actions = soup.find_all('div', class_='bg3wiki-tablelist')
            all_actions = [element.text.replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n') for element in all_actions]
            
            actions = [element.strip() for element in all_actions[0] if element != '']
                
            if len(actions) >= 2:
                weapons_data['Action 1'].append(actions[0] + ': ' + actions[1])
                
            if len(actions) >= 4:
                weapons_data['Action 2'].append(actions[2] + ': ' + actions[3])
            else: 
                weapons_data['Action 2'].append(np.nan)
                
            if len(actions) >= 6:
                weapons_data['Action 3'].append(actions[4] + ': ' + actions[5])
            else:
                weapons_data['Action 3'].append(np.nan)
                
            if len(actions) >= 8:
                weapons_data['Action 4'].append(actions[6] + ': ' + actions[7])
            else:
                weapons_data['Action 4'].append(np.nan)
            
            if len(all_actions) > 1:
                
                special_actions = [element.strip() for element in all_actions[1] if element != '']
                
                if len(special_actions) >= 2:
                    weapons_data['Special Action 1'].append(special_actions[0] + ': ' + special_actions[1])
                
                if len(special_actions) >= 4:
                    weapons_data['Special Action 2'].append(special_actions[2] + ': ' + special_actions[3])
                else: 
                    weapons_data['Special Action 2'].append(np.nan)
                    
                if len(special_actions) >= 6:
                    weapons_data['Special Action 3'].append(special_actions[4] + ': ' + special_actions[5])
                else:
                    weapons_data['Special Action 3'].append(np.nan)
                    
                if len(special_actions) >= 8:
                    weapons_data['Special Action 4'].append(special_actions[6] + ': ' + special_actions[7])
                else:
                    weapons_data['Special Action 4'].append(np.nan)
            
            else:
                weapons_data['Special Action 1'].append(np.nan)
                weapons_data['Special Action 2'].append(np.nan)
                weapons_data['Special Action 3'].append(np.nan)
                weapons_data['Special Action 4'].append(np.nan)
                
        except:
            weapons_data['Action 1'].append(np.nan)
            weapons_data['Action 2'].append(np.nan)
            weapons_data['Action 3'].append(np.nan)
            weapons_data['Action 4'].append(np.nan)
            weapons_data['Special Action 1'].append(np.nan)
            weapons_data['Special Action 2'].append(np.nan)
            weapons_data['Special Action 3'].append(np.nan)
            weapons_data['Special Action 4'].append(np.nan)
            
        try:
            images = soup.find_all('img')
            images = [image['src'] for image in images]
            url = 'https://bg3.wiki'+images[0]
            weapons_data['Img url'].append(url)
        except:
            weapons_data['Img url'].append(np.nan)
        
        
    return weapons_data