import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import calculations

def calculate():

    shield_text = shield_entry.get()
    armor_text = armor_entry.get()

    # -----Error Handling for missing or invalid values

    if shield_text == "" or armor_text == "":
        messagebox.showerror(
            "Missing Values",
            "Please enter both Shield and Armor values."
        )
        return
    
    try:
        shield = float(shield_text)
        armor = float(armor_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Values",
            "Shield and Armor must be numbers."
        )
        return
    
    # -----End of error handling

    # Get selected weapon
    weapon1 = weapon_combo1.get()
    weapon2 = weapon_combo2.get()
    weapon3 = weapon_combo3.get()

    weapon_combo_list = [weapon1]

    if weapon2 != 'None':
        weapon_combo_list+=[weapon2]
    if weapon3 != 'None':
        weapon_combo_list+=[weapon3]

    # Run calculation
    shield_df, armor_df, comp_df = calculations.get_volley_results(
        shield=shield,
        armor=armor,
        mod='fighter_laser',
        weaponlist=weapon_combo_list,
        n=11
    )


    # Clear previous results
    result_box.delete("1.0", tk.END)


    results_text = (
        "SHIELD RESULTS\n\n"
        + shield_df.round(2).to_string(index=False)
        + "\n\nARMOR RESULTS\n\n"
        + armor_df.round(2).to_string(index=False)
        + "\n\nCOMPONENT DAMAGE\n\n"
        + comp_df.round(2).to_string(index=False)
    )

    result_box.insert(tk.END, results_text)


# --------------------------------------------------
# Main window
# --------------------------------------------------

root = tk.Tk()

root.title("JTL Damage Calculator")
root.geometry("500x600")

# --------------------------------------------------
# Shield
# --------------------------------------------------

ttk.Label(root, text="Shield").pack(pady=(20, 5))

shield_entry = ttk.Entry(root)
shield_entry.pack()


# --------------------------------------------------
# Armor
# --------------------------------------------------

ttk.Label(root, text="Armor").pack(pady=(10, 5))

armor_entry = ttk.Entry(root)
armor_entry.pack()

# --------------------------------------------------
# Weapon
# --------------------------------------------------

ttk.Label(root, text="Weapons").pack(pady=(10, 5))

weapon_options = calculations.df.index.get_level_values('Weapon').unique().tolist()

weapon_combo1 = ttk.Combobox(
    root,
    values=weapon_options,
    state="readonly"
)

weapon_combo2 = ttk.Combobox(
    root,
    values=['None'] + weapon_options,
    state="readonly"
)

weapon_combo3 = ttk.Combobox(
    root,
    values=['None'] + weapon_options,
    state="readonly"
)

weapon_combo1.pack()
weapon_combo2.pack()
weapon_combo3.pack()

# Select W0 by default
weapon_combo1.current(0)
weapon_combo2.current(0)
weapon_combo3.current(0)

# --------------------------------------------------
# Calculate button
# --------------------------------------------------

calculate_button = ttk.Button(
    root,
    text="Show Damages",
    command=calculate
)

calculate_button.pack(pady=20)

'''
chart_button = ttk.Button(
    root,
    text="Show Chart",
    command=show_chart
)

chart_button.pack(pady=5)
'''

# --------------------------------------------------
# Results
# --------------------------------------------------

ttk.Label(root, text="Results").pack()

result_box = tk.Text(
    root,
    width=100,
    height=25
)

result_box.pack(padx=20, pady=10)

# --------------------------------------------------
# Start application
# --------------------------------------------------

root.mainloop()




####################################### CODE DUMP ###########################################


"""
    # Display results
    result_box.insert(tk.END, "SHIELD % REMAINING\n\n")

    for i, tier in enumerate(calculations.TierList):
        percentage = (shield_remaining[0, i] / shield) * 100
        result_box.insert(
            tk.END,
            f"{tier}: {percentage:.2f}%\n"
        )

    result_box.insert(tk.END, "\nARMOR % REMAINING\n\n")

    for i, tier in enumerate(calculations.TierList):
        percentage = (armor_remaining[0, i] / armor) * 100
        result_box.insert(
            tk.END,
            f"{tier}: {percentage:.2f}%\n"
        )

    result_box.insert(tk.END, "\nCOMPONENT DAMAGE\n\n")

    for i, tier in enumerate(calculations.TierList):
        damage = component_damage[0, i]
        result_box.insert(
            tk.END,
            f"{tier}: {damage:.2f}\n"
        )

"""