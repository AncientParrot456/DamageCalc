import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import calculations

def calculate():
    # Step 1: grab the numbers the user typed into the boxes.
    shield_text = shield_entry.get()
    armor_text = armor_entry.get()

    # Step 2: if a number is missing, stop and tell the user.
    if shield_text == "" or armor_text == "":
        messagebox.showerror(
            "Missing Values",
            "Please enter both Shield and Armor values."
        )
        return

    # Step 3: turn the text into real numbers Python can use.
    try:
        shield = float(shield_text)
        armor = float(armor_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Values",
            "Shield and Armor must be numbers."
        )
        return

    # Step 4: make a list of the weapons the user picked.
    weapon_selection_tuple = (
        weapon_combo1.get(),
        weapon_combo2.get(),
        weapon_combo3.get()
    )

    weapon_combo_list = [
        weapon for weapon in weapon_selection_tuple
        if weapon != "None"
    ]

    # Check for Custom Weapons

    # ------------------------------------------ NEED BETTER ERROR HANDLING 

    custom_max_list=[]
    custom_min_list=[]
    custom_vss_list=[]
    custom_vsa_list=[]

    if weapon_combo1.get() != "None" and custom_entries1["Max"].get() != "" and custom_entries1["Min"].get() != "" and custom_entries1["VSS"].get() != "" and custom_entries1["VSA"].get() != "":
        custom_max_list+= [float(custom_entries1["Max"].get())]
        custom_min_list+= [float(custom_entries1["Min"].get())]
        custom_vss_list+= [float(custom_entries1["VSS"].get())]
        custom_vsa_list+= [float(custom_entries1["VSA"].get())]

    if weapon_combo2.get() != "None" and custom_entries2["Max"].get() != "" and custom_entries2["Min"].get() != "" and custom_entries2["VSS"].get() != "" and custom_entries2["VSA"].get() != "":
        custom_max_list+= [float(custom_entries2["Max"].get())]
        custom_min_list+= [float(custom_entries2["Min"].get())]
        custom_vss_list+= [float(custom_entries2["VSS"].get())]
        custom_vsa_list+= [float(custom_entries2["VSA"].get())]

    if weapon_combo3.get() != "None" and custom_entries3["Max"].get() != "" and custom_entries3["Min"].get() != "" and custom_entries3["VSS"].get() != "" and custom_entries3["VSA"].get() != "":
        custom_max_list+= [float(custom_entries3["Max"].get())]
        custom_min_list+= [float(custom_entries3["Min"].get())]
        custom_vss_list+= [float(custom_entries3["VSS"].get())]
        custom_vsa_list+= [float(custom_entries3["VSA"].get())]

    if custom_entries1["Max"].get() == "" and custom_entries1["Min"].get() == "" and custom_entries1["VSS"].get() == "" and custom_entries1["VSA"].get() == "" and custom_entries2["Max"].get() == "" and custom_entries2["Min"].get() == "" and custom_entries2["VSS"].get() == "" and custom_entries2["VSA"].get() == "" and custom_entries3["Max"].get() == "" and custom_entries3["Min"].get() == "" and custom_entries3["VSS"].get() == "" and custom_entries3["VSA"].get() == "":
        custom_max_list=None
        custom_min_list=None
        custom_vss_list=None
        custom_vsa_list=None



    if (weapon_selection_tuple[0] != "None" and custom_entries1["Max"].get() == "" and custom_entries1["Min"].get() == "" and custom_entries1["VSS"].get() == "" and custom_entries1["VSA"].get() == "") or (weapon_selection_tuple[1] != "None" and custom_entries2["Max"].get() == "" and custom_entries2["Min"].get() == "" and custom_entries2["VSS"].get() == "" and custom_entries2["VSA"].get() == "") or (weapon_selection_tuple[2] != "None" and custom_entries3["Max"].get() == "" and custom_entries3["Min"].get() == "" and custom_entries3["VSS"].get() == "" and custom_entries3["VSA"].get() == ""):
        custom_max_list=None
        custom_min_list=None
        custom_vss_list=None
        custom_vsa_list=None

    # Step 5: ask the math helper to do the big calculations.
    shield_df, armor_df, comp_df = calculations.get_volley_results(
        shield=shield,
        armor=armor,
        mod='fighter_laser',
        weaponlist=weapon_combo_list,
        n=21,
        custom_max_list=custom_max_list,
        custom_min_list=custom_min_list,
        custom_vss_list=custom_vss_list,
        custom_vsa_list=custom_vsa_list
    )

    # Step 6: clear the old text, then show the new results.
    result_box.delete("1.0", tk.END)

    results_text = (
        "SHIELD RESULTS\n\n"
        + shield_df.round(1).to_string(index=False)
        + "\n\nARMOR RESULTS\n\n"
        + armor_df.round(1).to_string(index=False)
        + "\n\nCOMPONENT DAMAGE\n\n"
        + comp_df.round(1).to_string(index=False)
    )

    result_box.insert(tk.END, results_text)

    # Step 7: clear the old chart, then draw a fresh chart.
    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig = calculations.display_calc_volley(
        shield=shield,
        armor=armor,
        mod='fighter_laser',
        weaponlist=weapon_combo_list,
        n=21,
        custom_max_list=custom_max_list,
        custom_min_list=custom_min_list,
        custom_vss_list=custom_vss_list,
        custom_vsa_list=custom_vsa_list
    )

    volley_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    volley_canvas.draw()

    volley_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# --------------------------------------------------
# Main window
# --------------------------------------------------

root = tk.Tk()

root.title("JTL PvP Damage Calculator")
root.geometry("1600x900")

# --------------------------------------------------
# Input section
# --------------------------------------------------

# You can change this title later if you want.
section_header1 = ttk.Label(root, text="Defender Stats")
section_header1.pack(anchor="w", padx=20, pady=(20, 0))

input_frame = ttk.Frame(root)
input_frame.pack(anchor="w", padx=20, pady=(0, 0))

shield_label = ttk.Label(input_frame, text="Shield")
shield_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
shield_entry = ttk.Entry(input_frame)
shield_entry.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

armor_label = ttk.Label(input_frame, text="Armor")
armor_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
armor_entry = ttk.Entry(input_frame)
armor_entry.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

# --------------------------------------------------
# Weapon
# --------------------------------------------------

# HEADER
section_header2 = ttk.Label(root, text="Attacker Weapon Stats")
section_header2.pack(anchor="w", padx=20, pady=(10, 0))

weapon_options = calculations.df.index.get_level_values('Weapon').unique().tolist()


def create_weapon_row(parent, values, label_text):
    # This makes one little row:
    # 1) a label like "Weapon 1"
    # 2) a dropdown for choosing the weapon
    # 3) custom boxes that only show up when a real weapon is chosen
    row = ttk.Frame(parent)
    row.pack(fill="x", padx=20, pady=4)

    ttk.Label(row, text=label_text, width=12, anchor="w").pack(side="left")

    combo = ttk.Combobox(
        row,
        values=values,
        state="readonly",
        width=18
    )
    combo.pack(side="left", padx=(10, 10))
    combo.current(0)

    # These are the extra little boxes for custom stats.
    custom_label = ttk.Label(row, text="Custom Gun", width=12, anchor="w")
    custom_frame = ttk.Frame(row)

    entries = {}
    for field in ("Min", "Max", "VSS", "VSA"):
        ttk.Label(custom_frame, text=field, width=6, anchor="e").pack(side="left", padx=(8, 0))
        entry = ttk.Entry(custom_frame, width=8)
        entry.pack(side="left", padx=(0, 8))
        entries[field] = entry

    # This helper decides if the custom boxes should be seen.
    # If the dropdown says "None", we hide them.
    # If it says a weapon, we show them.
    def toggle_custom_fields(event=None):
        if combo.get() == "None":
            custom_label.pack_forget()
            custom_frame.pack_forget()
        else:
            custom_label.pack(side="left", padx=(10, 0))
            custom_frame.pack(side="left", padx=(10, 0))

    combo.bind("<<ComboboxSelected>>", toggle_custom_fields)
    toggle_custom_fields()

    return combo, entries


# Build the three weapon rows.
# Weapon 1 starts with a real weapon.
# Weapon 2 and Weapon 3 start with "None", so their custom boxes stay hidden.
weapon_combo1, custom_entries1 = create_weapon_row(root, weapon_options, "Weapon 1")
weapon_combo2, custom_entries2 = create_weapon_row(root, ['None'] + weapon_options, "Weapon 2")
weapon_combo3, custom_entries3 = create_weapon_row(root, ['None'] + weapon_options, "Weapon 3")

# --------------------------------------------------
# Calculate button
# --------------------------------------------------

calculate_button = ttk.Button(
    root,
    text="Calculate",
    command=calculate,
)

calculate_button.pack(pady=10,padx=20,anchor="w")


# --------------------------------------------------
# Results Area
# --------------------------------------------------

results_frame = ttk.Frame(root)
results_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

# Allow both columns to expand
results_frame.columnconfigure(0, weight=1)
results_frame.columnconfigure(1, weight=2)

# Allow the row to expand
results_frame.rowconfigure(0, weight=1)


result_box = tk.Text(
    results_frame,
    width=45,
    height=30
)

result_box.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10)
)


# --------------------------------------------------
# Chart
# --------------------------------------------------

chart_frame = ttk.Frame(results_frame)

chart_frame.grid(
    row=0,
    column=1,
    sticky="nsew"
)

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