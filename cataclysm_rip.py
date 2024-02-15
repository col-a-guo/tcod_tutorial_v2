import json
import pandas as pd
import numpy as np
from diceconvert import diceconvert

targets_armor_list = [["arms_armor", "arms"], ["boots", "feet"], ["gloves", "hands"], ["helmets", "head"], ["legs_armor", "legs"], ["shields", "other"], ["suits_protection", "suits"], ["torso_armor", "torso"]]
targets_ranged_list = ["archery", "crossbow", "slings", "throwing"]
targets_melee_list = ["axes", "bludgeons", "spears_and_polearms", "swords_and_blades", "unarmed_weapons"]

#Path: Find in data/json/items. Then search data/json/recipes/[armor, weapon, or ammo]
#TODO: manually make ammo categories? Steal from simple guns mod?
#TODO: check each category for unecessary stuff, remove

final_json_path = "item_jsons"
stat_path = "Cataclysm-BN/data/json/items"
recipe_path = "Cataclysm-BN/data/json/recipes"

armor_df_dict = {}

for armor in targets_armor_list:
    armor_item_df = pd.read_json(stat_path+f"\{armor[0]}")
    armor_item_df["recipe"] = ""
    armor_item_df["craft_level"] = ""
    armor_recipe_df = pd.read_json(recipe_path+f"\{armor[0]}")
    recipe_cat_path = recipe_path+f"\{armor[1]}"
    for index, row in armor_item_df.iterrows():
        armor_item_df.at[index,"recipe"] = armor_recipe_df.at[row["id"],"components"]
        armor_item_df.at[index,"craft_level"] = armor_recipe_df.at[row["id"],"difficulty"]
    


    armor_df_dict |= {f"\{armor[0]}":armor_item_df}


melee_df_dict = {}

for melee in targets_melee_list:
    melee_item_df = pd.read_json(stat_path+f"\{melee[0]}")
    melee_item_df["recipe"] = ""
    melee_item_df["craft_level"] = ""
    melee_item_df["attack"] = ""
    melee_item_df["power"] = ""
    melee_recipe_df = pd.read_json(recipe_path+f"\{melee[0]}")
    recipe_cat_path = recipe_path+f"\{melee[1]}"
    for index, row in melee_item_df.iterrows():
        melee_item_df.at[index,"recipe"] = melee_recipe_df.at[row["id"],"components"]
        melee_item_df.at[index,"craft_level"] = melee_recipe_df.at[row["id"],"difficulty"]
    


    melee_df_dict |= {f"\{melee[0]}":melee_item_df}



with open(final_json_path) as fjpf:
    print("TODO: write lol")