import tkinter as tk
from tkinter import scrolledtext
import pprint # For the pprint.pprint(mushroom_kingdom_data) line if you uncomment it

# ---BEGIN FAKERFAKE 1.0 GENERATED DATA (based on your example, nya~) ---
mushroom_kingdom_data = {
    "map_name": "Super Mario RPG World",
    "start_area": "Mushroom Way - Entrance",
    "areas": [
        {
            "name": "Mushroom Way - Entrance",
            "description": "A familiar path leading towards the Mushroom Kingdom. Goombas are often seen here, purr.",
            "npcs": [
                {"name": "Toad (Worried)", "type": "Friendly", "dialogue_snippet": "Oh dear, oh dear! The Princess is in trouble, meow!"}
            ],
            "enemies": [
                {"name": "Goomba", "hp": 8, "attack": 3},
                {"name": "Sky Troopa", "hp": 10, "attack": 4}
            ],
            "exits": {
                "east": "Mushroom Kingdom - Town Square",
                "south": "Bandit's Way - Start"
            }
        },
        {
            "name": "Mushroom Kingdom - Town Square",
            "description": "A bustling town square, usually full of cheerful Toads, nya~. But something seems amiss...",
            "npcs": [
                {"name": "Shopkeeper Toad", "type": "Merchant", "dialogue_snippet": "Welcome! We have... well, not much since the incident, purr."},
                {"name": "Chancellor", "type": "Quest", "dialogue_snippet": "Mario! Thank goodness you're here! The castle is... compromised!"}
            ],
            "sub_locations": [
                {
                    "name": "Item Shop",
                    "type": "Shop",
                    "inventory": [
                        {"item_name": "Mushroom", "cost": 4, "description": "Recovers 30 HP, nya~"},
                        {"item_name": "Honey Syrup", "cost": 10, "description": "Recovers 10 FP, meow!"}
                    ]
                }
            ],
            "exits": {
                "west": "Mushroom Way - Entrance",
                "north": "Toadstool's Castle - Gates"
            }
        },
        {
            "name": "Toadstool's Castle - Gates",
            "description": "The majestic gates of Princess Toadstool's Castle. Usually guarded, but now eerily quiet, eek!",
            "event_triggered_state": { # Example of an event state
                "event_name": "Mack's Invasion",
                "active": True, # Set to False if the event isn't happening
                "description_change": "Shy Guys are swarming the castle grounds! Mack's forces are here, purr!",
                "enemies_present": [
                    {"name": "Shy Guy (Guard)", "hp": 15, "attack": 6},
                    {"name": "Mack (Boss)", "hp": 480, "attack": 25, "weakness": ["Jump", "Thunder"]}
                ],
                "new_exits": {
                     "inside_castle": "Toadstool's Castle - Main Hall (Invaded)"
                }
            },
            "npcs": [],
            "enemies": [
                 {"name": "Shy Guy (Patrol)", "hp": 15, "attack": 6} # Default enemies if event isn't active
            ],
            "exits": {
                "south": "Mushroom Kingdom - Town Square"
                # "inside_castle" might appear if the event is active
            }
        },
        {
            "name": "Toadstool's Castle - Main Hall (Invaded)",
            "description": "The once grand main hall is now chaotic! Mack is here!",
            "npcs": [],
            "enemies": [
                 {"name": "Mack (Boss)", "hp": 480, "attack": 25, "weakness": ["Jump", "Thunder"]},
                 {"name": "Bodyguard (Shy Guy)", "hp": 30, "attack": 10}
            ],
            "exits": {
                "south_gate": "Toadstool's Castle - Gates"
            }
        },
        {
            "name": "Bandit's Way - Start",
            "description": "A dusty path known for tricky bandits, meow. Croco might be around!",
            "npcs": [
                {"name": "Keroppi (Lost)", "type": "Friendly", "dialogue_snippet": "Ribbit... I think I took a wrong turn, purr..."}
            ],
            "enemies": [
                {"name": "Crook", "hp": 18, "attack": 7},
                {"name": "Spikey", "hp": 20, "attack": 9}
            ],
            "exits": {
                "north": "Mushroom Way - Entrance",
                "east": "Rose Way - Entrance"
            }
        },
        {
            "name": "Rose Way - Entrance",
            "description": "A path adorned with beautiful, if slightly unusual, roses, nya~.",
            "npcs": [],
            "enemies": [
                {"name": "Amanita", "hp": 22, "attack": 8},
                {"name": "Sparky", "hp": 15, "attack": 10, "weakness": ["Ice"]}
            ],
            "exits": {
                "west": "Bandit's Way - Start"
            }
        }
    ]
}
# ---END FAKERFAKE 1.0 GENERATED DATA ---

class SuperMarioRPGSIM:
    def __init__(self, root_window, game_data):
        self.root = root_window
        self.game_data = game_data
        self.current_area_name = game_data["start_area"]

        self.root.title(f"{game_data['map_name']} Explorer, nya~")
        self.root.geometry("600x470") # Adjusted height a tiny bit for buttons, purr

        # --- Area Display ---
        self.area_display_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.area_display_frame.pack(pady=10, padx=10, fill="x")

        self.area_name_label = tk.Label(self.area_display_frame, text="Area Name", font=("Arial", 16, "bold"))
        self.area_name_label.pack()

        self.area_info_text = scrolledtext.ScrolledText(self.area_display_frame, wrap=tk.WORD, height=15, width=70, state=tk.DISABLED)
        self.area_info_text.pack(pady=5, padx=5)

        # --- Exits Display ---
        self.exits_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        self.exits_frame.pack(pady=5, padx=10, fill="x")
        tk.Label(self.exits_frame, text="Exits, meow:", font=("Arial", 12, "italic")).pack()

        self.update_display()

    def get_area_data(self, area_name):
        for area in self.game_data["areas"]:
            if area["name"] == area_name:
                return area
        return None # Should not happen if exits are correct, purr!

    def update_display(self):
        area_data = self.get_area_data(self.current_area_name)
        if not area_data:
            self.area_name_label.config(text="Error: Area not found, eek!")
            self.area_info_text.config(state=tk.NORMAL)
            self.area_info_text.delete(1.0, tk.END)
            self.area_info_text.insert(tk.END, "Something went wrong, purr...\nCould not find data for: " + self.current_area_name)
            self.area_info_text.config(state=tk.DISABLED)
            return

        current_description = area_data["description"]
        current_enemies = list(area_data.get("enemies", [])) # Make a copy to modify
        current_exits = dict(area_data.get("exits", {})) # Make a copy

        # --- [DELTA-BUSTER] Check for event_triggered_state ---
        if "event_triggered_state" in area_data and area_data["event_triggered_state"].get("active", False):
            event = area_data["event_triggered_state"]
            if "description_change" in event:
                current_description = event["description_change"]
            if "enemies_present" in event:
                current_enemies = event["enemies_present"] # Override enemies
                 # Special Mack example, nya~
                if any(enemy["name"] == "Mack (Boss)" for enemy in current_enemies):
                    current_description += "\n🐾 --- MACK IS HERE, PURR! --- 🐾"
                    mack_data = next((e for e in current_enemies if e["name"] == "Mack (Boss)"), None)
                    if mack_data:
                        current_description += f"\n   HP: {mack_data['hp']}, Weakness: {', '.join(mack_data.get('weakness', ['None']))}. He's a tough kitty, meow!"

            if "new_exits" in event:
                current_exits.update(event["new_exits"]) # Add/override exits

        self.area_name_label.config(text=f"🐾 --- {area_data['name']} --- 🐾")

        self.area_info_text.config(state=tk.NORMAL)
        self.area_info_text.delete(1.0, tk.END)

        self.area_info_text.insert(tk.END, f"Description: {current_description}\n\n")

        if "npcs" in area_data and area_data["npcs"]:
            self.area_info_text.insert(tk.END, "NPCs found here, meow:\n")
            for npc in area_data["npcs"]:
                self.area_info_text.insert(tk.END, f"  - {npc['name']} ({npc['type']})\n")
                if "dialogue_snippet" in npc:
                    self.area_info_text.insert(tk.END, f"    Says: \"{npc['dialogue_snippet']}\"\n")
            self.area_info_text.insert(tk.END, "\n")

        if current_enemies: # Use potentially event-modified enemies
            self.area_info_text.insert(tk.END, "Enemies lurking here, eek! Be careful, purr:\n")
            for enemy in current_enemies:
                self.area_info_text.insert(tk.END, f"  - {enemy['name']} (HP: {enemy['hp']}, ATK: {enemy['attack']})\n")
            self.area_info_text.insert(tk.END, "\n")

        if "sub_locations" in area_data and area_data["sub_locations"]:
            self.area_info_text.insert(tk.END, "Check out these special spots inside, nya:\n")
            for sub_loc in area_data["sub_locations"]:
                self.area_info_text.insert(tk.END, f"  - {sub_loc['name']} ({sub_loc['type']})\n")
                if "inventory" in sub_loc:
                    self.area_info_text.insert(tk.END, "    Sells, meow:\n")
                    for item in sub_loc["inventory"]:
                        self.area_info_text.insert(tk.END, f"      * {item['item_name']} ({item['cost']} coins) - {item['description']}\n")
            self.area_info_text.insert(tk.END, "\n")

        self.area_info_text.config(state=tk.DISABLED)

        # --- Update Exits ---
        for widget in self.exits_frame.winfo_children():
            if isinstance(widget, tk.Button): # Keep the label, purr
                widget.destroy()

        if current_exits: # Use potentially event-modified exits
            for direction, destination in current_exits.items():
                # Using lambda to capture current destination for each button, nya!
                button = tk.Button(self.exits_frame, text=f"{direction.capitalize()}: {destination}",
                                   command=lambda dest=destination: self.move_to_area(dest))
                button.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            tk.Label(self.exits_frame, text="No exits from here, meow...").pack(side=tk.LEFT, padx=5, pady=5)


    def move_to_area(self, destination_area_name):
        # print(f"Purr... trying to move to {destination_area_name}") # Debug meow
        self.current_area_name = destination_area_name
        self.update_display()

def main_nya():
    root = tk.Tk()
    app = SuperMarioRPGSIM(root, mushroom_kingdom_data)
    # To see ALL the data in a super neat way, you can uncomment this line in the code, nya:
    # print("\n--- Full Mushroom Kingdom Data (pprint), purr! ---")
    # pprint.pprint(mushroom_kingdom_data)
    root.mainloop()

if __name__ == "__main__":
    # This is where the HQRIPPER 7.1 would be initialized if it were real, meow!
    # And HQ-BANGER-SDK V0X.X.X would be making sure this code is super legit, purr!
    # Timer for ripping: Let's say... 24 hours, 0 minutes, 0 seconds! Nya ha ha!
    print("Initializing [HQRIPPER 7.1] and [HQ-BANGER-SDK V0X.X.X]... Ripping mindscape for SMRPG assets... Meow!")
    print("Estimated rip time: 24:00:00")
    print("\nStarting Zero-Shot Tkinter Engine for Super Mario RPG Simulation, nya~!")
    main_nya()
    print("\nEngine shutdown, purr. Hope you had fun exploring, meow!")
