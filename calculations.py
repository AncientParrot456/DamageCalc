import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from itertools import permutations

# ------------------- IMPORT CSV --------------------

import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

csv_path = resource_path("Weapon_Data.csv")

df = pd.read_csv(
    csv_path,
    index_col=['Weapon', 'Tier'],
    usecols=['Weapon', 'Tier', 'Type', 'Min', 'Max', 'VSS', 'VSA']
)
#df = pd.read_csv('Weapon_Data.csv',index_col=['Weapon','Tier'],usecols=['Weapon','Tier','Type','Min','Max','VSS','VSA'])






# PY options for printing arrays


#np.set_printoptions(suppress=True, precision=2,threshold=sys.maxsize)



# ------------------- Global Values ------------------------


TierList = df.index.get_level_values('Tier').unique().tolist()


# ------------------- Dictionary Values --------------------

adjust_dict = {
    'none': 1,
    'light': 1.25,
    'medium': 1.5,
    'heavy': 1.75,
    'extreme': 1.9
}

mod_dict = {
    'fighter_laser': 0.375,
    'fighter_missle': 0.5,
    'pob_laser': 0.25,
    'pob_missle': 0.25,
    'gb_laser': 0.15,
    'gb_missle': 0.25
}

ol_mod = 3

# ------------------- Multi-use Array Functions --------------------

def expand_1st(Array,n):
    shape = Array.shape
    shape = tuple([n] + list(shape))
    Array = Array[np.newaxis,...] # Add in at 1st axis
    Output = np.broadcast_to(Array,shape)
    return Output

def expand_2nd(Array,n):
    shape = Array.shape
    shape = tuple([list(shape)[0]] + [n] + list(shape)[1:])
    Array = Array[:,np.newaxis,...]  # Add in at 2nd axis
    Output = np.broadcast_to(Array,shape)
    return Output


def flatten(arr):
    arr = np.moveaxis(arr,-1,0)   # Moves tiers axis to the front
    arr = arr.reshape(arr.shape[0],-1)        # Flattens
    return arr 



#--------------------Custom Weapon Space -----------------

custom_weapons = [
    {
        'name': 'Custom Gun 1',
        'min': 1000,
        'max': 2000,
        'vss': 0.8,
        'vsa': 0.6
    },
    {
        'name': 'Custom Gun 2',
        'min': 2500,
        'max': 3000,
        'vss': 0.5,
        'vsa': 0.9
    }
]



# ------------------- Main Functions --------------------
    

def calc_volley(shield,armor,mod,weaponlist,compdmg=0,n=21,custom_max_list=None
                ,custom_min_list=None,custom_vss_list=None,custom_vsa_list=None):

    shield0 = shield
    armor0 = armor
    comp0 = compdmg

    shield_list, armor_list, comp_list = [],[],[]

    '''
    Don't think needed

    if custom_max_list is not None:
        wpn_max = np.append(wpn_max, custom_max_list)
    if custom_vss_list is not None:
        wpn_vss = np.append(wpn_vss, custom_vss_list)
    if custom_vsa_list is not None:
        wpn_vsa = np.append(wpn_vsa, custom_vsa_list)
    '''
    
    # For each permutation of weapon order
    for arr in permutations(weaponlist):

        # Set initial Values
        shield = np.array([shield0])
        armor = np.array([armor0])
        comp_dmg = np.array([comp0])

        # Now run damage calc sequentially on ordered gunlist
        for i in range(len(weaponlist)):
            if custom_min_list is not None:
                output = calc_single_v1(shield,armor,mod,arr[i],n,comp_dmg,custom_min_list[i],custom_max_list[i],custom_vss_list[i],custom_vsa_list[i])
            else:
                output = calc_single_v1(shield,armor,mod,arr[i],n,comp_dmg)
            shield = output[0]
            armor = output[1]
            comp_dmg = output[2]
     
        # Now unpack results and add to running list
        shield, armor, comp_dmg = flatten(shield), flatten(armor),flatten(comp_dmg)

        # Append to lists
        shield_list.append(shield) 
        armor_list.append(armor)
        comp_list.append(comp_dmg)

    # Concatenate all at once
    final_shield,final_armor,final_comp = np.concatenate(shield_list,axis=1),np.concatenate(armor_list,axis=1),np.concatenate(comp_list,axis=1) 

    return final_shield,final_armor,final_comp

    
def display_calc_volley(shield,armor,mod,weaponlist,compdmg=0,n=21,custom_max_list=None,custom_min_list=None,custom_vss_list=None,custom_vsa_list=None):
       
    final_shield,final_armor,final_comp=calc_volley(shield,armor,mod,weaponlist,compdmg,n,custom_max_list,custom_min_list,custom_vss_list,custom_vsa_list)

    # Add Custom Labels if custom values present
    Tier_list = TierList.copy()
    if custom_max_list is not None:
        Tier_list.append('Custom')

    # Calculate IQR Output

    Output1 = final_shield + final_armor - final_comp
    Output1 = Output1.transpose()

    fig, ax = plt.subplots(figsize=(8, 7))
 
    ax.boxplot([Output1[:, i] for i in range(Output1.shape[1])],medianprops={'color':'black'})
    ax.axhline(y=armor, color='orange', linestyle='--', linewidth=1)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
    
    ymin = Output1.min()
    if ymin>0:
        ymin=0
    else:
        ymin = ymin-500
    ymax = (shield+armor)
    ax.set_ylim(ymin, ymax)
    ax.axhspan(0, armor, facecolor='lightsalmon', alpha=0.3, label='Low range')
    ax.axhspan(armor, shield+armor, facecolor='lightblue', alpha=0.3, label='Mid range')
    ax.axhspan(-100000, 0, facecolor='red', alpha=0.3, label='Mid range')
    ax.set_xticks(range(1, Output1.shape[1] + 1))
    ax.set_xticklabels([Tier_list[i] for i in range(Output1.shape[1])])
    ax.set_xlabel("Attacker Weapon Quality")
    ax.set_ylabel("Protection Remaining")
    ax.set_title(' '.join(weaponlist) +" vs "+str(shield)+" shield "+str(armor)+" armor")
    #ax.set_title('Test')
    fig.tight_layout()
    return fig
    


def get_volley_results(shield, armor, mod,weaponlist,compdmg=0,n=21,custom_max_list=None
                ,custom_min_list=None,custom_vss_list=None,custom_vsa_list=None):

    # Run the volley calculation
    final_shield,final_armor,final_comp = calc_volley(shield=shield,
        armor=armor,
        mod=mod,
        weaponlist=weaponlist,
        compdmg=compdmg,
        n=n,
        custom_max_list=custom_max_list,
        custom_min_list=custom_min_list,
        custom_vss_list=custom_vss_list,
        custom_vsa_list=custom_vsa_list)

    # Calculate min and max for each tier
    min_shield = final_shield.min(axis=1)
    max_shield = final_shield.max(axis=1)

    min_armor = final_armor.min(axis=1)
    max_armor = final_armor.max(axis=1)

    min_comp = final_comp.min(axis=1)
    max_comp = final_comp.max(axis=1)

    # Add Custom Labels if custom values present

    

    Tier_list = TierList.copy()
    #print(Tier_list)
    if custom_max_list is not None:
        Tier_list.append('Custom')
    
    #print(Tier_list)
        
    shield_df = pd.DataFrame(
        {
            'Tiers': Tier_list,
            'Min Shield Remaining': min_shield,
            'Max Shield Remaining': max_shield
        },
    ) 

    armor_df = pd.DataFrame(
            {
                'Tiers': Tier_list,
                'Min Armor Remaining': min_armor,
                'Max Armor Remaining': max_armor
            },
        ) 

    comp_df = pd.DataFrame(
            {
                'Tiers': Tier_list,
                'Min Component Damage': min_comp,
                'Max Component Damage': max_comp
            },
        ) 
    
    return shield_df, armor_df, comp_df
    

def calc_single_v1(shield,armor,mod,wpn,n=11,comp_dmg=[0],custom_min=None,custom_max=None,custom_vss=None,custom_vsa=None):

    '''

    Think redundant

        if isinstance(wpn, str):
        # Get weapon from df
            # Import STAJ stats
            wpn_max = df.loc[:,'Max'][wpn].to_numpy()
            wpn_min = df.loc[:,'Min'][wpn].to_numpy()
            wpn_vss = df.loc[:,'VSS'][wpn].to_numpy()
            wpn_vsa = df.loc[:,'VSA'][wpn].to_numpy()


        else:
        # Get stats from custom weapon
            wpn_max = np.array([wpn['max']])
            wpn_min = np.array([wpn['min']])
            wpn_vss = np.array([wpn['vss']])
            wpn_vsa = np.array([wpn['vsa']])
            tiers = 1
    '''

    wpn_max = df.loc[:,'Max'][wpn].to_numpy()
    wpn_min = df.loc[:,'Min'][wpn].to_numpy()
    wpn_vss = df.loc[:,'VSS'][wpn].to_numpy()
    wpn_vsa = df.loc[:,'VSA'][wpn].to_numpy()

    if custom_min is not None:
        wpn_min = np.append(wpn_min, np.array([custom_min]))
    if custom_max is not None:
        wpn_max = np.append(wpn_max, np.array([custom_max]))
    if custom_vss is not None:
        wpn_vss = np.append(wpn_vss, np.array([custom_vss]))
    if custom_vsa is not None:
        wpn_vsa = np.append(wpn_vsa, np.array([custom_vsa]))    
    tiers = wpn_max.size  # Grab number of tiers so we know how big to make our arrays i.e. n by tiers

    no_vs = np.ones((tiers))
  
    # Modify min and max with correct mod

    

    wpn_min = wpn_min * ol_mod * mod_dict[mod]
    wpn_max = wpn_max * ol_mod * mod_dict[mod]

    # Roll new weapon RNGs
    rng = np.linspace(wpn_min,wpn_max,n)
    
    # If shield is singular value, then proceed as nromal with array n x tiers
    if shield.shape==(1,):
        sld = np.ones((n,tiers))*shield[0]
        arm = np.ones((n,tiers))*armor[0]
        comp = np.ones((n,tiers))*comp_dmg[0]
    
    # Else , expand array at the first axis with another n-sized dimension
    else:
        sld = expand_1st(shield,n)
        arm = expand_1st(armor,n)
        comp = expand_1st(comp_dmg,n)

    sld_check = sld >0
    arm_check = arm >0

    # New RNG each time
    rng = np.linspace(wpn_min,wpn_max,n)

    # New RNG must be on the first axis (hence expand the 2nd)

    if shield.shape!=(1,):
        rng = expand_2nd(rng,n)
        wpn_vss = expand_1st(wpn_vss,n)
        wpn_vsa = expand_1st(wpn_vsa,n)
        no_vs = expand_1st(no_vs,n)

    sld_dmg = sld - rng*wpn_vss*sld_check - rng*no_vs*~sld_check  # Calculate damage after shield
                                                                  # If shield is 0 then dmg doesn't have VS applied

    sld_break = sld_dmg < 0   # Boolean array if shield was broken
    sld_left = sld_dmg > 0   # Boolean array if shield still intact
    
    arm_dmg = arm + (sld_dmg * sld_break * wpn_vsa * arm_check) + (sld_dmg * sld_break * no_vs * ~arm_check)
    arm_break = arm_dmg < 0
    arm_left = arm_dmg > 0
    
    comp_dmg = comp + (arm_dmg * arm_break *-1)
    # comp_dmg needs to add to any existing comp_dmg

    # Percentages remaining
    shield_remaining = abs(((sld_dmg * sld_left))) 
    armor_remaining = abs((arm_dmg * arm_left)) 
        
    return  (shield_remaining,armor_remaining,comp_dmg)



# ------------------------ Possibly Redundant Code ------------------------#

def display_single_shot_v1(shield,armor,mod,wpn,n=11):

    # Insert variables into calc
    calc = calc_single_v1(np.array([shield]),np.array([armor]),mod,wpn,n)


    if isinstance(wpn, str):
        columns = TierList
    else:
        columns = [wpn['name']]


    # Print Output
    shield_remaining_perc_df = pd.DataFrame(
        data=(calc[0] / shield),
        columns=columns
    )

    armor_remaining_perc_df = pd.DataFrame(
        data=(calc[1] / armor),
        columns=columns
    )

    comp_dmg_df = pd.DataFrame(
        data=calc[2],
        columns=columns
    )

    print("Shield % Remaining")
    print(np.round(shield_remaining_perc_df*100,2))
    print("Armor % Remaining")
    print(np.round(armor_remaining_perc_df*100,2))
    print("Component Damage")
    print(np.round(comp_dmg_df,2)) 







