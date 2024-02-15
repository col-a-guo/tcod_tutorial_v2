import json
import pandas as pd
import numpy as np
import math
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
material_path = "Cataclysm-BN/data/json/recipes/materials.json"

material_df = pd.read_json(material_path)

armor_df_dict = {}

for armor in targets_armor_list:
    armor_item_df = pd.read_json(stat_path+f"\{armor[0]}")
    armor_item_df["recipe"] = ""
    armor_item_df["craft_level"] = ""
    armor_item_df["protection"] = ""
    armor_item_df["armor"] = ""
    armor_item_df["mitigation"] = ""
    armor_item_df["acid_res"] = ""
    armor_item_df["elec_res"] = ""
    armor_item_df["fire_res"] = ""
    armor_item_df["cold_res"] = ""
    armor_recipe_df = pd.read_json(recipe_path+f"\{armor[0]}")
    recipe_cat_path = recipe_path+f"\{armor[1]}"
    for index, row in armor_item_df.iterrows():
        armor_item_df.at[index,"recipe"] = armor_recipe_df.at[row["id"],"components"]
        armor_item_df.at[index,"craft_level"] = armor_recipe_df.at[row["id"],"difficulty"]
        armor_mats = armor_item_df.at[index,"materials"]
        thickness = armor_item_df.at[index,"material_thickness"]
        coverage = armor_item_df.at[index,"coverage"]
        bash_res = 0
        cut_res = 0
        acid_res = 0
        elec_res = 0
        fire_res = 0
        cold_res = armor_item_df.at[index,"warmth"]/5
        for mat in armor_mats:
            row = material_df.loc[material_df['id'] == mat]
            bash_res += row[0, "bash_resist"]
            cut_res += row[0, "cut_resist"]
            acid_res += row[0, "acid_resist"]
            elec_res += row[0, "elec_resist"]
            fire_res += row[0, "fire_resist"]
        num_mats = len(armor_mats)
        bash_res /= num_mats*thickness
        cut_res /= num_mats*thickness
        acid_res /= num_mats*thickness
        elec_res /= num_mats*thickness
        fire_res /= num_mats*thickness

        #PROTECTION (reduce dismemberment)
        protection_val = round((2*cut_res+bash_res)*coverage/16)
        sigmoid_two_prot = 1/(1+2**(-protection_val/8)) #between 50% and 100%, positive sigmoid
        protection_final = sigmoid_two_prot*(coverage/128+(1-1/1.28)) 
        #another coverage multiplier; 0% -> 22%, 50% -> 61%, 100% -> 100%, linear
        armor_item_df.at[index,"protection"] = protection_final #percentage reduction of dismemberment chance to this body part.

        #MITIGATION (flat damage reduction)
        mitigation_final = round((156+coverage)/256*(cut_res+2*bash_res)/8) 
        #above, 156+coverage/256 gives flattened coverage multiplier, /8 with x1.5 from the 2+1 gives 5.33, to approx match 32/(64+speed). Should be 5-20 range
        armor_item_df.at[index,"mitigation"] = mitigation_final #flat damage reduction
        
        #ARMOR (avoid getting hit, as D&D)
        armor_item_df.at[index,"armor"] = (1+protection_final)*(20+mitigation_final)/8

    


    armor_df_dict |= {f"\{armor[0]}":armor_item_df}


melee_df_dict = {}

for melee in targets_melee_list:
    melee_item_df = pd.read_json(stat_path+f"\{melee[0]}")
    melee_item_df["recipe"] = ""
    melee_item_df["craft_level"] = ""
    melee_item_df["attack"] = ""
    melee_item_df["type"] = ""
    melee_item_df["power"] = ""
    melee_item_df["init"] = ""
    melee_recipe_df = pd.read_json(recipe_path+f"\{melee[0]}")
    recipe_cat_path = recipe_path+f"\{melee[1]}"
    for index, row in melee_item_df.iterrows():
        melee_item_df.at[index,"recipe"] = melee_recipe_df.at[row["id"],"components"]
        melee_item_df.at[index,"craft_level"] = melee_recipe_df.at[row["id"],"difficulty"]
        bash = melee_item_df.at[index,"bashing"]
        cut = melee_item_df.at[index,"cutting"]
        if bash > cut:
            melee_item_df.at[index,"type"] = "BASH"
        if "STAB" in melee_item_df.at[index,"flags"]:
            melee_item_df.at[index,"type"] = "STAB"
        else:
            melee_item_df.at[index,"type"] = "CUT"
        total_damage = bash+cut
        weight = melee_item_df.at[index,"weight"][:-2] #cuts off g
        volume = melee_item_df.at[index,"volume"][:-3] #cuts off ml
        swing_time = 64+weight/64+volume/64 #CDDA's formula but tweaked; 250/4 -> 64, 60 -> 64
        final_dmg_avg = round(total_damage/(65+swing_time)*32)
        melee_item_df.at[index,"init"] = round(100-swing_time)/8
        melee_item_df[index, "attack"] = melee_item_df[index, "to_hit"]+round(100-swing_time)/16
        melee_item_df["power"] = diceconvert(final_dmg_avg)
        
        #TODO: base damage on bash/stab/cut
        #Dismemberment has different forms: broken/bleeding/removed


    melee_df_dict |= {f"\{melee[0]}":melee_item_df}



with open(final_json_path) as fjpf:
    print("TODO: write lol")
