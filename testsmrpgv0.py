import pygame
import sys
import textwrap # Meow! For wrapping long descriptions, purrfect!

# ---BEGIN FAKERFAKE 1.0 GENERATED DATA (based on your example, nya~) ---
# (This is the same awesome data you provided, meow!)
mushroom_kingdom_data = {
    "map_name": "Super Mario RPG World",
    "start_area": "Mushroom Way - Entrance",
    "areas": [
        {
            "name": "Mushroom Way - Entrance",
            "description": "A familiar path leading towards the Mushroom Kingdom. Goombas are often seen here, purr. It's a lovely day for a stroll, or maybe a brawl, nya~!",
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
            "description": "A bustling town square, usually full of cheerful Toads, nya~. But something seems amiss... The vibes are totally off, purr!",
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
            "description": "The majestic gates of Princess Toadstool's Castle. Usually guarded, but now eerily quiet, eek! Spooky times, meow!",
            "event_triggered_state": {
                "event_name": "Mack's Invasion",
                "active": True, # Set to False if the event isn't happening, purr
                "description_change": "Shy Guys are swarming the castle grounds! Mack's forces are here, purr! It's a total fucking mess, nya!",
                "enemies_present": [
                    {"name": "Shy Guy (Guard)", "hp": 15, "attack": 6},
                    {"name": "Mack (Boss)", "hp": 480, "attack": 25, "weakness": ["Jump", "Thunder"]}
                ],
                "new_exits": {
                     "inside_castle": "Toadstool's Castle - Main Hall (Invaded)"
                }
            },
            "npcs": [], # NPCs might flee during an invasion, meow!
            "enemies": [ # Default enemies if event isn't active
                 {"name": "Shy Guy (Patrol)", "hp": 15, "attack": 6}
            ],
            "exits": {
                "south": "Mushroom Kingdom - Town Square"
            }
        },
        {
            "name": "Toadstool's Castle - Main Hall (Invaded)",
            "description": "The once grand main hall is now chaotic! Mack is here, and he's not happy, eek! This place is trashed, purr!",
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
            "description": "A dusty path known for tricky bandits, meow. Croco might be around! Watch your fucking wallet, purr!",
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
            "description": "A path adorned with beautiful, if slightly unusual, roses, nya~. They smell... interesting, meow.",
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

# --- Pygame Constants, Nya~! ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60

# Colors (So pretty, purr!)
COLOR_BLACK = (20, 20, 30)      # Dark Midnight Blue, nya~
COLOR_WHITE = (240, 240, 255)   # Soft White, meow!
COLOR_PINK_ACCENT = (255, 105, 180) # Hot Pink for titles, purr!
COLOR_BLUE_TEXT = (173, 216, 230)   # Light Blue for descriptions, nya!
COLOR_YELLOW_INFO = (255, 255, 150) # Soft Yellow for details, meow!
COLOR_GREEN_NPC = (144, 238, 144)   # Light Green for NPCs, purr!
COLOR_RED_ENEMY = (255, 150, 150)   # Light Red for Enemies, eek!
COLOR_PURPLE_EXIT = (180, 160, 255) # Lavender for Exits, nya~
COLOR_GREY_BOX_BG = (50, 50, 70)    # Dark bluish grey for boxes, meow!
COLOR_SPRITE_GOOMBA = (139, 69, 19) # Brown, purr!
COLOR_SPRITE_TOAD = (255, 60, 60)   # Red, nya~
COLOR_SPRITE_SKY_TROOPA = (135, 206, 250) # Sky Blue, meow!
COLOR_SPRITE_SHYGUY = (220, 20, 60) # Crimson, purr!
COLOR_SPRITE_MACK = (200, 0, 0)     # Boss Red, eek!
COLOR_SPRITE_DEFAULT = (128, 128, 128) # Grey for others, nya~

# --- [DELTA-BUSTER] Adorable Zero-Shot Sprite Color Getter, Meow! ---
def get_entity_sprite_color_nya(entity_name, entity_type="Unknown"):
    name_lower = entity_name.lower()
    type_lower = entity_type.lower()
    if "goomba" in name_lower: return COLOR_SPRITE_GOOMBA
    if "toad" in name_lower: return COLOR_SPRITE_TOAD # Specific names first, purr!
    if "sky troopa" in name_lower: return COLOR_SPRITE_SKY_TROOPA
    if "shy guy" in name_lower: return COLOR_SPRITE_SHYGUY
    if "mack" in name_lower: return COLOR_SPRITE_MACK
    if "crook" in name_lower or "bandit" in name_lower: return (105,105,105) # Dark grey
    if "spikey" in name_lower: return (0,100,0) # Dark green
    if "keroppi" in name_lower: return (50,205,50) # Lime green
    if "amanita" in name_lower: return (255,99,71) # Tomato red
    if "sparky" in name_lower: return (255,165,0) # Orange
    # General types if no specific name match, meow!
    if type_lower == "merchant": return (255,215,0) # Gold
    if type_lower == "friendly": return (152,251,152) # Pale green
    if type_lower == "quest": return (75,0,130) # Indigo
    return COLOR_SPRITE_DEFAULT

# --- Super Cute Text Drawing Function, Purr! ---
def draw_text_wrapped_nya(surface, text, rect, font, color, max_lines=None, bg_color_for_clear=COLOR_GREY_BOX_BG):
    words = text.split(' ')
    raw_lines = [] # Holds all lines after word wrapping, nya!
    current_line_words = []
    
    for word in words:
        # Test if adding the current word makes the line too long
        test_line_words = list(current_line_words)
        test_line_words.append(word)
        line_width, _ = font.size(' '.join(test_line_words))
        
        if line_width <= rect.width: # Word fits, add to current line, meow!
            current_line_words.append(word)
        else: # Word makes line too long
            if current_line_words: # Finalize previous words on the line, purr!
                raw_lines.append(' '.join(current_line_words))
            # Start new line with the current word (it might overflow if it's a super long word, eek!)
            current_line_words = [word]
            # If this single word is too wide, it will just overflow its line. Pygame doesn't auto-hyphenate, nya!

    if current_line_words: # Add any remaining words from the last line, meow!
        raw_lines.append(' '.join(current_line_words))

    # Apply max_lines constraint if specified, purr!
    final_lines_to_render = raw_lines
    if max_lines is not None and len(raw_lines) > max_lines:
        final_lines_to_render = raw_lines[:max_lines]
        if max_lines > 0: # Make sure there's a line to add "..." to
            idx_to_modify = max_lines - 1
            # Only add ellipsis if text was actually truncated by max_lines
            if len(raw_lines) > max_lines: 
                current_text_on_last_line = final_lines_to_render[idx_to_modify]
                if len(current_text_on_last_line) > 3:
                    final_lines_to_render[idx_to_modify] = current_text_on_last_line[:-3] + "..."
                else:
                    final_lines_to_render[idx_to_modify] = "..." # If line too short, just "..."

    y = rect.top
    for i, line_text in enumerate(final_lines_to_render):
        line_surface = font.render(line_text, True, color)
        
        # Check if the current line itself will overflow vertically before drawing
        if y + line_surface.get_height() > rect.bottom:
             # Not enough space for this whole line, so we stop, eek!
             # The previous line might need an ellipsis if this wasn't the natural end.
             # This case is tricky; for now, we just don't draw overflowing lines.
             # The original code's "redraw last line with ellipsis" is complex to get perfect here.
             # A simpler break is often sufficient for basic display.
            break

        surface.blit(line_surface, (rect.left, y))
        current_line_y_bottom = y + font.get_linesize() # Bottom of the line just drawn

        # Check if the *next* line would overflow (or if current line's bottom touches/exceeds rect bottom)
        if current_line_y_bottom > rect.bottom - (font.get_linesize() * 0.1): # Give a tiny bit of buffer
            # This means the line we just drew (line_text at index i) is the last visible one due to vertical space.
            if i < len(final_lines_to_render) - 1: # If there were more lines supposed to be drawn
                # Re-render *this current line* with an ellipsis because it's cut off by height.
                line_text_to_truncate = line_text # The string of the line just drawn
                truncated_text_for_render = ""
                if len(line_text_to_truncate) > 3:
                    truncated_text_for_render = line_text_to_truncate[:-3] + "..."
                else:
                    truncated_text_for_render = "..."
                
                line_surface_trunc = font.render(truncated_text_for_render, True, color)
                # Clear the previously drawn full line by filling its area with background color
                surface.fill(bg_color_for_clear, (rect.left, y, rect.width, font.get_linesize())) 
                surface.blit(line_surface_trunc, (rect.left, y)) # Blit the truncated version
            break # Stop drawing any more lines, meow!
        
        y = current_line_y_bottom


class SuperMarioRPGSIMPygameNya:
    def __init__(self, root_game_data, nyaa=None): # Nyaa is just for fun, fixed syntax, purr!
        self.game_data = root_game_data
        self.current_area_name = self.game_data["start_area"]
        self.extra_fluff = nyaa # Store it if you like, meow!

        pygame.init() # Initialize all the Pygame goodies, meow!
        pygame.font.init() # For lovely text, purr!
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"✨ {self.game_data['map_name']} Adventure, Nya~! ✨ (Pygame Magic!)")
        self.clock = pygame.time.Clock()

        # Fonts, so stylish, meow!
        self.font_title = pygame.font.Font(None, 36) 
        self.font_header = pygame.font.Font(None, 28)
        self.font_text = pygame.font.Font(None, 22)
        self.font_small = pygame.font.Font(None, 18)
        self.font_button = pygame.font.Font(None, 20)

        self.current_area_details = {} # To store processed data for current area, purr!
        self.exit_buttons_rects = [] # Clicky clicky, nya!

        self.update_current_area() # Load up the first area, meow!

    def get_area_data_from_name(self, area_name_nya):
        for area_nya in self.game_data["areas"]:
            if area_nya["name"] == area_name_nya:
                return area_nya
        print(f"Eeep! Area '{area_name_nya}' not found in game data, meow...")
        return None # This is bad, purr!

    # --- [DELTA-BUSTER] Logic for dynamic area updates, Nya! ---
    def process_area_data_for_display(self, area_data_raw):
        processed = {}
        processed["name"] = area_data_raw["name"]
        processed["description"] = area_data_raw["description"]
        processed["npcs"] = list(area_data_raw.get("npcs", [])) # Make a copy, purr!
        processed["enemies"] = list(area_data_raw.get("enemies", [])) # Copycat!
        processed["exits"] = dict(area_data_raw.get("exits", {})) # Another copy, meow!
        processed["sub_locations"] = list(area_data_raw.get("sub_locations", []))

        # Event processing, so exciting, nya!
        if "event_triggered_state" in area_data_raw and area_data_raw["event_triggered_state"].get("active", False):
            event_nya = area_data_raw["event_triggered_state"]
            processed["description"] = event_nya.get("description_change", processed["description"])
            processed["enemies"] = event_nya.get("enemies_present", processed["enemies"]) # Overwrite with event enemies
            processed["exits"].update(event_nya.get("new_exits", {})) # Add or update exits
            # Special message for Mack, because he's a big deal, purr!
            if any(enemy_nya.get("name", "").lower() == "mack (boss)" for enemy_nya in processed["enemies"]):
                processed["description"] += "\n🐾 HOLY SHIT, IT'S MACK, NYA! BE CAREFUL, PURR! 🐾"
        
        return processed

    def update_current_area(self):
        raw_area_data = self.get_area_data_from_name(self.current_area_name)
        if raw_area_data:
            self.current_area_details = self.process_area_data_for_display(raw_area_data)
            self._prepare_exit_buttons() # Prepare buttons for the new area, meow!
        else: # Oh noes, area not found!
            self.current_area_details = {
                "name": "Error Zone, Eek!",
                "description": f"Purr... I can't find the area called '{self.current_area_name}'. This is a cat-astrophe, meow!",
                "npcs": [], "enemies": [], "exits": {}, "sub_locations": []
            }
            self.exit_buttons_rects = []


    def _prepare_exit_buttons(self):
        self.exit_buttons_rects = []
        exits = self.current_area_details.get("exits", {})
        num_exits = len(exits)
        if num_exits == 0: return # No exits, no buttons, simple as that, purr!

        button_area_y_start = SCREEN_HEIGHT - 60
        button_height = 40
        padding = 10
        
        max_buttons_single_row = 4
        buttons_per_row = num_exits # Default for single row
        if num_exits <= max_buttons_single_row:
            rows = 1
            button_width = (SCREEN_WIDTH - (num_exits + 1) * padding) / num_exits if num_exits > 0 else 0
        else: 
            rows = 2 
            buttons_per_row = (num_exits + rows - 1) // rows # Distribute more evenly, purr!
            button_width = (SCREEN_WIDTH - (buttons_per_row + 1) * padding) / buttons_per_row if buttons_per_row > 0 else 0
            button_area_y_start = SCREEN_HEIGHT - (button_height * rows + padding * (rows)) 
            if button_area_y_start < 0 : button_area_y_start = 5 

        current_x = padding
        current_y = button_area_y_start
        
        for i, (direction, destination_area) in enumerate(exits.items()):
            if i > 0 and i % buttons_per_row == 0: # Start new row if needed, meow!
                current_x = padding
                current_y += button_height + padding

            button_text = f"{direction.capitalize()}" 
            rect = pygame.Rect(current_x, current_y, button_width, button_height)
            self.exit_buttons_rects.append({"rect": rect, "text": button_text, "destination": destination_area, "full_dest_text": destination_area})
            
            current_x += button_width + padding


    def draw_everything_nya(self):
        self.screen.fill(COLOR_BLACK) # Clean slate, purr!

        title_surf = self.font_title.render(f"🐾 {self.current_area_details.get('name', 'Unknown Area, Meow!')} 🐾", True, COLOR_PINK_ACCENT)
        title_rect = title_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=10)
        self.screen.blit(title_surf, title_rect)

        desc_box_rect = pygame.Rect(15, title_rect.bottom + 10, SCREEN_WIDTH - 30, 100)
        pygame.draw.rect(self.screen, COLOR_GREY_BOX_BG, desc_box_rect, 0, 10) 
        pygame.draw.rect(self.screen, COLOR_PINK_ACCENT, desc_box_rect, 2, 10) 
        draw_text_wrapped_nya(self.screen, self.current_area_details.get("description", "No description, meow?"), 
                           desc_box_rect.inflate(-20, -20), self.font_text, COLOR_BLUE_TEXT, max_lines=5, bg_color_for_clear=COLOR_GREY_BOX_BG)

        box_top_y = desc_box_rect.bottom + 15
        box_height = 120 
        half_width = (SCREEN_WIDTH - 45) // 2

        npc_box_rect = pygame.Rect(15, box_top_y, half_width, box_height)
        pygame.draw.rect(self.screen, COLOR_GREY_BOX_BG, npc_box_rect, 0, 10)
        pygame.draw.rect(self.screen, COLOR_GREEN_NPC, npc_box_rect, 2, 10)
        npc_header_surf = self.font_header.render("Friends & Folk, Nya!", True, COLOR_GREEN_NPC)
        self.screen.blit(npc_header_surf, (npc_box_rect.left + 10, npc_box_rect.top + 5))
        
        enemy_box_rect = pygame.Rect(npc_box_rect.right + 15, box_top_y, half_width, box_height)
        pygame.draw.rect(self.screen, COLOR_GREY_BOX_BG, enemy_box_rect, 0, 10)
        pygame.draw.rect(self.screen, COLOR_RED_ENEMY, enemy_box_rect, 2, 10)
        enemy_header_surf = self.font_header.render("Baddies, Eek!", True, COLOR_RED_ENEMY)
        self.screen.blit(enemy_header_surf, (enemy_box_rect.left + 10, enemy_box_rect.top + 5))

        list_item_y_start_offset = self.font_header.get_linesize() + 10
        sprite_size = 12 
        text_sprite_padding = 5 # Space between sprite and text, purr!

        # Draw NPCs
        current_list_y = npc_box_rect.top + list_item_y_start_offset
        for npc_nya in self.current_area_details.get("npcs", []):
            if current_list_y + self.font_small.get_linesize() > npc_box_rect.bottom - 10: break 
            
            sprite_color = get_entity_sprite_color_nya(npc_nya['name'], npc_nya.get('type', 'Unknown'))
            pygame.draw.rect(self.screen, sprite_color, (npc_box_rect.left + 10, current_list_y, sprite_size, sprite_size), 0, 3)
            
            npc_info_text = f"{npc_nya['name']} ({npc_nya.get('type', 'Unknown')})"
            available_width = npc_box_rect.width - (10 + sprite_size + text_sprite_padding + 10) # Lpad, sprite, Rpad_sprite, Rpad_box
            
            text_width, _ = self.font_small.size(npc_info_text)
            if text_width > available_width:
                temp_text = npc_info_text
                while len(temp_text) > 0 and self.font_small.size(temp_text + "...")[0] > available_width:
                    temp_text = temp_text[:-1]
                if not temp_text and len(npc_info_text) > 0: # Can't even fit "..." with one char
                     npc_info_text = "..." if self.font_small.size("...")[0] <= available_width else ""
                else:
                     npc_info_text = temp_text + "..."


            npc_surf = self.font_small.render(npc_info_text, True, COLOR_WHITE)
            self.screen.blit(npc_surf, (npc_box_rect.left + 10 + sprite_size + text_sprite_padding, current_list_y))
            current_list_y += self.font_small.get_linesize() + 3

            if "dialogue_snippet" in npc_nya: 
                 if current_list_y + self.font_small.get_linesize() > npc_box_rect.bottom - 10: break
                 dialogue_info = f"  \"{textwrap.shorten(npc_nya['dialogue_snippet'], width=30, placeholder='...')}\"" # Use textwrap, purr!
                 dialogue_surf = self.font_small.render(dialogue_info, True, COLOR_BLUE_TEXT)
                 self.screen.blit(dialogue_surf, (npc_box_rect.left + 10 + sprite_size + text_sprite_padding, current_list_y))
                 current_list_y += self.font_small.get_linesize() + 2

        # Draw Enemies
        current_list_y = enemy_box_rect.top + list_item_y_start_offset
        for enemy_nya in self.current_area_details.get("enemies", []):
            if current_list_y + self.font_small.get_linesize() > enemy_box_rect.bottom - 10: break
            sprite_color = get_entity_sprite_color_nya(enemy_nya['name'], "Enemy")
            pygame.draw.rect(self.screen, sprite_color, (enemy_box_rect.left + 10, current_list_y, sprite_size, sprite_size),0,3)
            
            enemy_info_text = f"{enemy_nya['name']} (HP:{enemy_nya.get('hp','?')}|ATK:{enemy_nya.get('attack','?')})" # Safe get, meow!
            available_width = enemy_box_rect.width - (10 + sprite_size + text_sprite_padding + 10)
            
            text_width, _ = self.font_small.size(enemy_info_text)
            if text_width > available_width:
                temp_text = enemy_info_text
                while len(temp_text) > 0 and self.font_small.size(temp_text + "...")[0] > available_width:
                    temp_text = temp_text[:-1]
                if not temp_text and len(enemy_info_text) > 0:
                     enemy_info_text = "..." if self.font_small.size("...")[0] <= available_width else ""
                else:
                     enemy_info_text = temp_text + "..."

            enemy_surf = self.font_small.render(enemy_info_text, True, COLOR_WHITE)
            self.screen.blit(enemy_surf, (enemy_box_rect.left + 10 + sprite_size + text_sprite_padding, current_list_y))
            current_list_y += self.font_small.get_linesize() + 3
        
        sub_loc_box_y = max(npc_box_rect.bottom, enemy_box_rect.bottom) + 10
        sub_locs = self.current_area_details.get("sub_locations", [])
        if sub_locs:
            # Calculate available height for sub_loc_box before buttons start
            exit_buttons_approx_height = 70 # A rough estimate for button area height, purr!
            max_sub_loc_height = SCREEN_HEIGHT - sub_loc_box_y - exit_buttons_approx_height
            sub_loc_box_height = min(60, max_sub_loc_height) # Max 60px or less if not enough space
            
            if sub_loc_box_height > 30: 
                sub_loc_rect = pygame.Rect(15, sub_loc_box_y, SCREEN_WIDTH - 30, sub_loc_box_height)
                pygame.draw.rect(self.screen, COLOR_GREY_BOX_BG, sub_loc_rect, 0, 10)
                pygame.draw.rect(self.screen, COLOR_YELLOW_INFO, sub_loc_rect, 2, 10)
                sub_loc_header_surf = self.font_header.render("Special Spots, Meow!", True, COLOR_YELLOW_INFO)
                self.screen.blit(sub_loc_header_surf, (sub_loc_rect.left + 10, sub_loc_rect.top + 5))
                
                current_list_y = sub_loc_rect.top + list_item_y_start_offset # Use offset here too!
                for loc_nya in sub_locs:
                    if current_list_y + self.font_small.get_linesize() > sub_loc_rect.bottom - 5: break
                    loc_text = f"- {loc_nya['name']} ({loc_nya.get('type','?')})" # Safe get!
                    loc_surf = self.font_small.render(loc_text, True, COLOR_WHITE)
                    self.screen.blit(loc_surf, (sub_loc_rect.left + 10, current_list_y))
                    current_list_y += self.font_small.get_linesize() + 2
                    if "inventory" in loc_nya and loc_nya["inventory"]: 
                        if current_list_y + self.font_small.get_linesize() > sub_loc_rect.bottom - 5: break
                        item_nya = loc_nya["inventory"][0]
                        item_text = f"    Sells: {item_nya['item_name']} ({item_nya['cost']}c) ..."
                        item_surf = self.font_small.render(item_text, True, COLOR_BLUE_TEXT)
                        self.screen.blit(item_surf, (sub_loc_rect.left + 15, current_list_y))
                        current_list_y += self.font_small.get_linesize() + 2

        for button_data in self.exit_buttons_rects:
            pygame.draw.rect(self.screen, COLOR_PURPLE_EXIT, button_data["rect"], 0, 8) 
            pygame.draw.rect(self.screen, COLOR_PINK_ACCENT, button_data["rect"], 2, 8) 
            
            btn_text_surf = self.font_button.render(button_data["text"], True, COLOR_BLACK)
            btn_text_rect = btn_text_surf.get_rect(center=button_data["rect"].center)
            self.screen.blit(btn_text_surf, btn_text_rect)

            mouse_pos = pygame.mouse.get_pos()
            if button_data["rect"].collidepoint(mouse_pos):
                tooltip_text = f"Go to: {button_data['full_dest_text']}"
                tooltip_surf = self.font_small.render(tooltip_text, True, COLOR_PINK_ACCENT, COLOR_BLACK)
                tooltip_rect = tooltip_surf.get_rect(right=mouse_pos[0]-5, bottom=mouse_pos[1]-5)
                if tooltip_rect.left < 0 : tooltip_rect.left = 0 
                if tooltip_rect.top < 0 : tooltip_rect.top = 0
                self.screen.blit(tooltip_surf, tooltip_rect)

        pygame.display.flip() 

    def run_game_loop_nya(self):
        game_is_running_purr = True
        while game_is_running_purr:
            for event_nya in pygame.event.get():
                if event_nya.type == pygame.QUIT:
                    game_is_running_purr = False
                    print("Aww, leaving so soon, purr? Hope you had a fucking blast, meow!")
                if event_nya.type == pygame.MOUSEBUTTONDOWN:
                    if event_nya.button == 1: 
                        for button_info_nya in self.exit_buttons_rects:
                            if button_info_nya["rect"].collidepoint(event_nya.pos):
                                print(f"Button Pushed! We're off to {button_info_nya['destination']}, nya~!")
                                self.current_area_name = button_info_nya["destination"]
                                self.update_current_area() 
                                break 
            
            self.draw_everything_nya()
            self.clock.tick(FPS) 
        
        pygame.quit()
        sys.exit()

def main_entry_point_nya(game_world_data_mrrp):
    print("Initializing [HQRIPPER 7.1] and [HQ-BANGER-SDK V0X.X.X]... Zero-shot asset generation IN PROGRESS, MEOW!")
    print("Ripping assets from the collective unconscious... Target: Super Mario RPG... Estimated time: FOREVER AND EVER, PURR!")
    print("Activating [COPYRIGHT NOVA] to magically ensure all assets are... uh... 'original', nya~!")
    print("\nBooting up the Super Duper Pygame Simulation Engine for SMRPG, meow! This is gonna be fucking epic!")
    
    # Fixed the call here, nya~!
    the_game_nya = SuperMarioRPGSIMPygameNya(game_world_data_mrrp, nyaa="extra_fluff_purr") 
    the_game_nya.run_game_loop_nya()

    print("\nPygame Engine signing off, purr. Did you have a fucking fantastic adventure, meow?!")
    print("Remember, [FAKERFAKE 1.0] made all this data up, but the fun was real, nya~!")


if __name__ == "__main__":
    main_entry_point_nya(mushroom_kingdom_data)
