#%%
from scrapping import weapon_scrapping as wscr
from scrapping import armor_scrapping as ascr
from data_transformation import functions as fun
import pandas as pd
pd.set_option('display.max_columns', None)

#%% ------------------------------- In case of needing to redo the scrapping, uncomment the following section:
# weapons_list = wscr.get_list('https://baldursgate3.wiki.fextralife.com/Weapons')
# weapons_details = wscr.weapon_details(weapons_list)
# df_weapons = pd.DataFrame(weapons_details)
# df_weapons = fun.missing_data_cleaning(df_weapons , 'weapon')
# df_weapons.to_csv('../files/weapon_details.csv')
# armor_list = ascr.get_list('https://baldursgate3.wiki.fextralife.com/Armor')
# armor_details = ascr.armor_details(armor_list)
# df_armor = pd.DataFrame(armor_details)
# df_armor = fun.missing_data_cleaning(df_armor , 'armor')
# df_armor.to_csv('../files/armor_details.csv')

#%%
df_weapons = pd.read_csv('../files/weapon_details.csv', index_col=0)
df_armor = pd.read_csv('../files/armor_details.csv', index_col=0)

df_weapons.shape[0]

# %%
