#%%
from scrapping import weapon_scrapping as wscr
from scrapping import armor_scrapping as ascr
import pandas as pd
pd.set_option('display.max_columns', None)

#%% -------------------------------- In case of needing to redo the scrapping, uncomment the following section:
# weapons_list = wscr.get_list('https://baldursgate3.wiki.fextralife.com/Weapons')
# weapons_details = wscr.weapon_details(weapons_list)
# df_weapons = pd.DataFrame(weapons_details)
# df_weapons.to_csv('../files/weapon_details.csv')
# %%
armor_list = ascr.get_list('https://baldursgate3.wiki.fextralife.com/Armor')
#%%
armor_details = ascr.armor_details(armor_list)
# %%
df_armors = pd.DataFrame(armor_details)
df_armors.to_csv('../files/armor_details.csv')