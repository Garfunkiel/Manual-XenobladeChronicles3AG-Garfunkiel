from Options import OptionError
from typing import Optional, TYPE_CHECKING
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, is_option_enabled, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

if TYPE_CHECKING:
    from .. import ManualWorld

MAX_BEGINNER = 30
MAX_INTERMEDIATE = 50
MAX_PRO = 140

def getClampedStageRequirement(multiworld: MultiWorld, player: int) -> int:
    highest_stage = int(get_option_value(multiworld, player, "highest_stage_required"))

    if isGauntletIncluded(multiworld, player, "pro"):
        return min(highest_stage, MAX_PRO)
    elif isGauntletIncluded(multiworld, player, "intermediate"):
        return min(highest_stage, MAX_INTERMEDIATE)
    else:
        return min(highest_stage, MAX_BEGINNER)

def isRegionAccessible(multiworld: MultiWorld, player: int, stage: str, gauntlet: str) -> bool|str:
    if gauntlet == "beginner":
        keyrequirement = "1"
    elif gauntlet == "intermediate":
        if isGauntletIncluded(multiworld, player, "beginner"):
            keyrequirement = "2"
        else:
            keyrequirement = "1"
    elif gauntlet == "pro":
        if isGauntletIncluded(multiworld, player, "beginner") and isGauntletIncluded(multiworld, player, "intermediate"):
            keyrequirement = "3"
        elif isGauntletIncluded(multiworld, player, "intermediate"):
            keyrequirement = "2"
        else:
            keyrequirement = "1"
    else:
        raise Exception("Invalid gauntlet specified")

    highest_stage = int(get_option_value(multiworld, player, "highest_stage_required"))
    if int(stage) > highest_stage:
        return True

    nopwatch_refill_stage = int(get_option_value(multiworld, player, "nopwatch_refill_stage"))
    if int(stage) >= nopwatch_refill_stage:
        return f"|Stage {int(stage):03d} Unlock Key:{keyrequirement}| AND |Nopwatch Refill License|"

    return f"|Stage {int(stage):03d} Unlock Key:{keyrequirement}|"

def isRegionAccessibleRule(player: int, stage: str, gauntlet: str, world: "ManualWorld") -> str:
    value = isRegionAccessible(world.multiworld, player, stage, gauntlet)
    if (value == True):
        return ""
    if (value == False):
        raise Exception("isRegionAccessible returned False")
    return value

def isGauntletIncluded(multiworld: MultiWorld, player: int, difficulty: str) -> bool:
    gauntlets_included = int(get_option_value(multiworld, player, "gauntlets_included"))
    difficulty_map = {
        "beginner": 1,
        "intermediate": 2,
        "pro": 4
    }
    return (int(gauntlets_included) & difficulty_map.get(difficulty, 0)) != 0

def isEmblemInLogic(multiworld: MultiWorld, player: int, rarity: str):
    highest_stage = getClampedStageRequirement(multiworld, player)

    if isGauntletIncluded(multiworld, player, "beginner"):
        keyrequirement = "1"
    elif isGauntletIncluded(multiworld, player, "intermediate"):
        keyrequirement = "2"
    elif isGauntletIncluded(multiworld, player, "pro"):
        keyrequirement = "3"
    else:
        raise Exception("Invalid gauntlet specified")

    stars = int(rarity)

    if (stars <= 1):
        return True

    mult = 0.34 if stars == 2 else 0.66

    rule = ""
    counter = 11

    while ((mult * highest_stage + 1) >= counter):
        if (rule != ""):
            rule += " AND "
        rule += f"|Stage {counter:03d} Unlock Key:{keyrequirement}|"
        counter += 10

    return rule

def isEmblemInLogicRule(player: int, rarity: str, world: "ManualWorld") -> str:
    value = isEmblemInLogic(world.multiworld, player, rarity)
    if (value == True):
        return ""
    if (value == False):
        raise Exception("isEmblemInLogic returned False")
    return value

def canClaimVictory(multiworld: MultiWorld, player: int):
    highest_stage = getClampedStageRequirement(multiworld, player)
    all = get_option_value(multiworld, player, "all_heroes_required")

    if isGauntletIncluded(multiworld, player, "pro"):
        keyrequirement = "3"
    elif isGauntletIncluded(multiworld, player, "intermediate"):
        keyrequirement = "2"
    elif isGauntletIncluded(multiworld, player, "beginner"):
        keyrequirement = "1"
    else:
        raise Exception("No valid difficulty included")

    rule = ""

    if (all):
        rule = "|@Heroes:ALL|"

    counter = 11

    while (highest_stage >= counter):
        if (rule != ""):
            rule += " AND "
        rule += f"|Stage {counter:03d} Unlock Key:{keyrequirement}|"
        counter += 10

    return rule

def canClaimVictoryRule(player: int, world: "ManualWorld") -> str:
    value = canClaimVictory(world.multiworld, player)
    if (value == True):
        return ""
    if (value == False):
        raise Exception("canClaimVictory returned False")
    return value

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
