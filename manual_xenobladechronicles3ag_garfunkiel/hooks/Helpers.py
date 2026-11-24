from typing import Optional, Any
from BaseClasses import MultiWorld

import re

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    from ..Helpers import get_option_value

    gauntlets_included = int(get_option_value(multiworld, player, "gauntlets_included"))

    match category_name:
        case "BeginnerStages":
            if gauntlets_included & 1 == 0:
                return False
        case "IntermediateStages":
            if gauntlets_included & 2 == 0:
                return False
        case "ProStages":
            if gauntlets_included & 4 == 0:
                return False
        case "Archsage's Whimsy":
            if gauntlets_included & 2 == 0 and gauntlets_included & 4 == 0:
                return False
        case _:
            return None

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_location_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    from ..Helpers import get_option_value

    # Any location in the format "Stage ###-[BIP] Cleared" should be disabled if the number is greater than the highest stage required
    stage_regex_match = re.fullmatch(r"Stage (\d{3})-[BIP] Cleared", location["name"])

    if stage_regex_match:
        stage_num = int(stage_regex_match.group(1))
        highest_stage = int(get_option_value(multiworld, player, "highest_stage_required"))
        if stage_num > highest_stage:
            return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the event, False to disable it, or None to use the default behavior
def before_is_event_enabled(multiworld: MultiWorld, player: int, event:  dict[str, Any]) -> Optional[bool]:
    return None
