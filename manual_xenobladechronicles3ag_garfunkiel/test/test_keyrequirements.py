from ..Game import game_name
from .manual_test import Xenoblade3AGManualTest

class Xenoblade3AGManualTest_KeyRequirements(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 4,
        "highest_stage_required": 140,
        "all_heroes_required": False,
        "nopwatch_refill_stage": 80
    }

    def test_KeyRequirements(self):
        self.checkItemsForLocation("Stage 011-P Cleared", [
            "Stage 011 Unlock Key"
        ])

class Xenoblade3AGManualTest_KeyRequirements2(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 5,
        "highest_stage_required": 140,
        "all_heroes_required": False,
        "nopwatch_refill_stage": 80
    }

    def test_KeyRequirements(self):
        self.checkItemsForLocation("Stage 011-P Cleared", [
            "Stage 011 Unlock Key:2"
        ])

class Xenoblade3AGManualTest_KeyRequirements3(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 7,
        "highest_stage_required": 140,
        "all_heroes_required": False,
        "nopwatch_refill_stage": 80
    }

    def test_KeyRequirements(self):
        self.checkItemsForLocation("Stage 011-P Cleared", [
            "Stage 011 Unlock Key:3"
        ])

class Xenoblade3AGManualTest_KeyRequirements3_WithRefills(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 7,
        "highest_stage_required": 140,
        "all_heroes_required": False,
        "nopwatch_refill_stage": 10
    }

    def test_KeyRequirements(self):
        self.checkItemsForLocation("Stage 011-P Cleared", [
            "Stage 011 Unlock Key:3",
            "Nopwatch Refill License"
        ])