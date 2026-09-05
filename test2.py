import tkinter as tk
from tkinter import ttk
import numpy as np

import calculations


"""
calculations.get_volley_results(
        shield=1000,
        armor=1000,
        mod='fighter_laser',
        weaponlist=list('W0')
    )
"""

#calculations.calc_volley(shield=1000,armor=1000,mod='fighter_laser',weaponlist=['W0'],n=15)
#calculations.display_calc_volley(shield=1000,armor=1000,mod='fighter_laser',weaponlist=['W0'],n=15)

calculations.get_volley_results(1000, 1000, mod='fighter_laser',weaponlist=['W0'])
