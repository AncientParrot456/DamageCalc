import tkinter as tk
from tkinter import ttk
import numpy as np

import calculations

def calculate():
    shield = float(shield_entry.get())
    armor = float(armor_entry.get())


    # Get selected weapon
    weapon = weapon_combo.get()


    # Run calculation
    results = calculations.get_volley_results(
        shield=shield,
        armor=armor,
        mod='fighter_laser',
        weaponlist=[weapon]
    )


    # Clear previous results
    result_box.delete("1.0", tk.END)


    result_box.insert(
        tk.END,
        results.round(2).to_string()
    )

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

ttk.Label(root, text="Weapon").pack(pady=(10, 5))

weapon_combo = ttk.Combobox(
    root,
    values=calculations.df.index.get_level_values('Weapon').unique().tolist(),
    state="readonly"
)

weapon_combo.pack()

# Select W0 by default
weapon_combo.current(0)

# --------------------------------------------------
# Calculate button
# --------------------------------------------------

calculate_button = ttk.Button(
    root,
    text="Calculate",
    command=calculate
)

calculate_button.pack(pady=20)

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