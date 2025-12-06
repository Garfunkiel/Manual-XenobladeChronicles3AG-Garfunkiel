from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, is_option_enabled, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

def isEmblemInLogic(multiworld: MultiWorld, player: int, rarity: str):
    highest_stage = get_option_value(multiworld, player, "highest_stage_required")

    if (not isinstance(highest_stage, int)):
        return False

    stars = int(rarity)

    if (stars <= 1):
        return True

    mult = 0.34 if stars == 2 else 0.66

    rule = ""
    counter = 11

    while ((mult * highest_stage + 1) >= counter):
        if (rule != ""):
            rule += " AND "
        rule += f"|Stage {counter:03d} Unlock Key:1|"
        counter += 10

    return rule

def canClaimVictory(multiworld: MultiWorld, player: int):
    highest_stage = get_option_value(multiworld, player, "highest_stage_required")
    all = get_option_value(multiworld, player, "all_heroes_required")

    if (not isinstance(highest_stage, int)):
        return False

    rule = ""

    if (all):
        rule = "|@Heroes:ALL|"

    counter = 11

    while (highest_stage >= counter):
        if (rule != ""):
            rule += " AND "
        rule += f"|Stage {counter:03d} Unlock Key:1|"
        counter += 10

    return rule

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"
