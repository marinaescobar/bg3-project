#%%
from scrapping import scrapping as scr
import pandas as pd
pd.set_option('display.max_columns', None)

#%%
weapons_list = scr.weapons_list('https://baldursgate3.wiki.fextralife.com/Weapons')
#%%
weapons_details = scr.weapon_details(weapons_list)

weapons_details

# %%
df_weapons = pd.DataFrame(weapons_details)
# %%
df_weapons.to_csv('../files/weapon_details.csv')

# %%
df_weapons.head(20)
# %%
