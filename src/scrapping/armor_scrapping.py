import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

def get_list (url):
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    armor_table = soup.find('table', class_='wiki_table sortable searchable', attrs={'data-key': 'armor'})
    rows = armor_table.find_all('tr')
    row_elements = [row.text for row in rows]
    armor_names = [element.split('\n')[1].strip() for element in row_elements[1:]]

    return armor_names

def armor_details (armor_list):
    
    armors_data = {'Name': [],
                    'Description' : [],
                    'Class': [],
                    'Type': [],
                    'Required Proficiency' : [],
                    'Rarity' : [],
                    'Weight' : [],
                    'Price' : [],
                    'Special Attribute 1' : [],
                    'Special Attribute 2' : [],
                    'Special Attribute 3' : [],
                    'Special Attribute 4' : [],
                    'Location' : [],
                    'Img url' : [],
                    'UID' : [],
                    'UUID' : []
                    }
    
    for armor in armor_list:
        
        # Getting armor's name
        armors_data['Name'].append(armor)
        
        armor_search = armor.replace(' ', '_')
        
        if '+' in armor_search:
            armor_search = armor.replace('+', '%2B')
        
        response = requests.get(f'https://bg3.wiki/wiki/{armor_search}')
        #response = requests.get('https://bg3.wiki/wiki/Leather_Armour_%2B1')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Getting armor's description
        try:
            description = soup.find_all('p')
            description = [description.text for description in description]
            description = description[0].replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n')
            armors_data['Description'].append(description[0])    
        except:
            armors_data['Description'].append(np.nan)
        
        # Getting special attributes
        more_data = soup.find_all('ul')
        more_data = [element.text.replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n') for element in more_data]
        
        try:    
        # Getting armor's details 
            properties = soup.find('ul', class_='bg3wiki-property-list')
            properties = [element.text for element in properties]
            properties = [element.strip().replace('\xa0' , '').replace('\u202f' , '') for element in properties if element != '\n']
        except:
            properties = more_data[0]    

        # Getting Class
        try:
            armor_class = soup.find('div', class_='ac-value').text
            armors_data['Class'].append(armor_class)
        except:
            armors_data['Class'].append(np.nan)
        
        # Getting Type
        try:
            armor_type = properties[0]
            armors_data['Type'].append(armor_type)
        except:
            armors_data['Type'].append(np.nan)
            
        # Getting Required Proficiency
        try:
            proficiency = [element for element in properties if 'Required Proficiency:' in element][0].replace('Required Proficiency: ', '')
            armors_data['Required Proficiency'].append(proficiency.strip())
        except:
            armors_data['Required Proficiency'].append(np.nan)
            
        # Getting Rarity
        try:
            rarity = [element for element in properties if 'Rarity:' in element][0].replace('Rarity: ', '')
            armors_data['Rarity'].append(rarity)
        except:
            armors_data['Rarity'].append(np.nan)
                   
        # Getting weight
        try: 
            weight = [element for element in properties if 'Weight:' in element][0].replace('Weight: ', '').replace('  ', ' ')
            armors_data['Weight'].append(weight)
        except:
            armors_data['Weight'].append(np.nan)
        
        # Getting price
        try: 
            price = [element for element in properties if 'Price:' in element][0].replace('Price: ', '').replace('  ', ' ').strip()
            armors_data['Price'].append(price)
        except:
            armors_data['Price'].append(np.nan)
        
        # Getting UID and UUID
        try:
            uid = properties[-1].split('\n')[2]
            armors_data['UID'].append(uid)
            uuid = properties[-1].split('\n')[-1]
            armors_data['UUID'].append(uuid)
        except:
            armors_data['UID'].append(np.nan)
            armors_data['UUID'].append(np.nan)
        
        # Getting special attributes
        try: 
            h3 = soup.find_all('h3')
            h3 = [element.text.strip() for element in h3]
            
            if h3.count('Special') > 1:
            
                special_data = more_data[1]
                
                if len(special_data) >= 1:
                    armors_data['Special Attribute 1'].append(special_data[0].strip())
                    
                if len(special_data) >= 2:
                    armors_data['Special Attribute 2'].append(special_data[1].strip())  
                else: 
                    armors_data['Special Attribute 2'].append(np.nan)
                    
                if len(special_data) >= 3:
                    armors_data['Special Attribute 3'].append(special_data[2].strip())
                else:
                    armors_data['Special Attribute 3'].append(np.nan)
                    
                if len(special_data) >= 4:
                    armors_data['Special Attribute 4'].append(special_data[3].strip())
                else:
                    armors_data['Special Attribute 4'].append(np.nan)
                    
            else:
                armors_data['Special Attribute 1'].append(np.nan)
                armors_data['Special Attribute 2'].append(np.nan)
                armors_data['Special Attribute 3'].append(np.nan)
                armors_data['Special Attribute 4'].append(np.nan)
                
        except:
            armors_data['Special Attribute 1'].append(np.nan)
            armors_data['Special Attribute 2'].append(np.nan)
            armors_data['Special Attribute 3'].append(np.nan)
            armors_data['Special Attribute 4'].append(np.nan)
            
        # Getting location
        try:
            h2 = soup.find_all('h2')
            h2 = [element.text.strip() for element in h2]
                       
            if 'Where to find' in h2:
                location = soup.find_all(class_='bg3wiki-tooltip-box')
                location = [location.text for location in location]
                location = location[1].replace('\u202f', '').replace('  ', ' ').replace('\xa0', '').replace(' ()', '').replace('( ', '(').split('\n')
                location = ' '.join(location)
                armors_data['Location'].append(location.strip())
            else:
                armors_data['Location'].append(np.nan)
        except:
            armors_data['Location'].append(np.nan)

        
        # Getting images   
        try:
            images = soup.find_all('img')
            images = [image['src'] for image in images]
            url = 'https://bg3.wiki'+images[0]
            armors_data['Img url'].append(url)
        except:
            armors_data['Img url'].append(np.nan)
        
    
    return armors_data