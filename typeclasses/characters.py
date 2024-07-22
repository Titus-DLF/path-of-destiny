"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is set up to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import Object


class Character(Object, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the prelogout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    prelogout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    # List containing valid player races
    valid_player_races = ("Human", "Supreme Being")

    def set_race(self, attribute_name, race):
        """
        Validates input when updating the player_race variable.
        Sets the value for the attribute or overwrites a previous value.
        The attribute could be an integer, string, bool, etc.

        Args:
           attribute_name: The name of the attribute to set.
           race: Sets the race attribute.
        """
        if attribute_name == "player_race" and race not in self.valid_player_races:
            raise ValueError(
                f"Invalid input for player race. Valid races are: {', '.join(self.valid_player_races)}"
            )
        setattr(self, attribute_name, race)

    equipment_slots = [
        "light",
        "Ring",
        "Ring",
        "Wrist",
        "Wrist",
        "Helm",
        "Neck",
        "Shoulders",
        "Body Armor",
        "Arms",
        "Waist",
        "Scroll",
        "Cloak",
        "Hands",
        "Legs",
        "Boots",
        "Main Wield",
        "Dual Wield",
        "Shield",
        "Aura",

    ]

    player_equipment = {
        "equipment slot": "value from the object's short description"
    }

    def at_object_creation(self):
        #  Define base attributes as class variables.

        super().at_object_creation()

        # Sets the base values for the character object
        base_mod = 0
        base_resource_value = 100
        base_stat_attributes = 10

        # A dictionary containing specific attributes and a tuple containing their corresponding values
        self.resource_attributes = {
            "current_hp": (base_resource_value, base_mod),
            "max_hp": (base_resource_value, base_mod),
            "current_mana": (base_resource_value, base_mod),
            "max_mana": (base_resource_value, base_mod),
            "current_stam": (base_resource_value, base_mod),
            "max_stam": (base_resource_value, base_mod),
        }
        self.stat_attributes = {
            "strength": (base_stat_attributes, base_mod),
            "intelligence": (base_stat_attributes, base_mod),
            "agility": (base_stat_attributes, base_mod),
            "constitution": (base_stat_attributes, base_mod),
            "luck": (0, base_mod),
            "armor": (0, base_mod),
        }
        self.string_attributes = {
            "player_class": "",
            "player_race": "Human",
            "player_alignment": "Neutral"
        }
        self.integer_attributes = {
            "player_level": 1,
        }
        # Initializing character variables and their values using the corresponding dictionary.
        for attr, value in self.resource_attributes.items():
            self.attributes.add(attr, value[0])

        for attr, value in self.stat_attributes.items():
            self.attributes.add(attr, value[0])

        for attr, value in self.string_attributes.items():
            self.attributes.add(attr, value)

        for attr, value in self.integer_attributes.items():
            self.attributes.add(attr, value)

        self.save()  # Stores the character attributes in the database.
        self.update_stat_sheet()  # Stores the updated score-sheet in the database.

    # Updates and displays player attributes and stats.

    def update_stat_sheet(self):
        try:
            player_name = self.get_display_name().capitalize()

            attributes_list = []
            stat_sheet_dict = {}

            # Collect all attribute keys in attributes_list
            for key in self.resource_attributes.keys():  # hp, mana, stamina, etc
                attributes_list.append(key)

            for key in self.stat_attributes.keys():  # strength, intelligence, etc
                attributes_list.append(key)

            for key in self.string_attributes.keys():  # class, race, alignment, etc
                attributes_list.append(key)

            for key in self.integer_attributes.keys():  # level, exp, etc.
                attributes_list.append(key)

            # Debugging, printing attributes_list
            # self.msg(attributes_list)

            # Populate stat_sheet_dict with attribute keys and their corresponding values
            for elem in attributes_list:
                value = self.attributes.get(elem)

                if isinstance(value, tuple):
                    value = value[0] if len(value) > 0 else None

                # Debugging
                # self.msg(f"The following value has been added to the stat_sheet_dict: {value}")

                stat_sheet_dict[elem] = value

            # Use the collected data in stat_sheet_dict to format the score-sheet
            stat_sheet = f"""
    ============================================================
    Level: ({stat_sheet_dict["player_level"]}) Name: {player_name} Race: {stat_sheet_dict["player_race"]} Alignment: {stat_sheet_dict["player_alignment"]}
    ============================================================
    Health ({stat_sheet_dict["max_hp"]}) Mana ({stat_sheet_dict["max_mana"]}) Stamina ({stat_sheet_dict["max_stam"]}) 
    ------------------------------------------------------------
    Str({stat_sheet_dict["strength"]}) Int({stat_sheet_dict["intelligence"]}) Agi({stat_sheet_dict["agility"]}) Con({stat_sheet_dict["constitution"]}) Luck({stat_sheet_dict["luck"]})
    ------------------------------------------------------------
    Armor({stat_sheet_dict["armor"]})
    ============================================================
    """

            # Store the updated score-sheet in the database
            self.db.stat_sheet = stat_sheet
        except (KeyError, AttributeError) as e:
            print(f"Error updating the score-sheet: {e}")
