from ..Game import game_name
from .manual_test import Xenoblade3AGManualTest

class Xenoblade3AGManualTest_Victory(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 1,
        "highest_stage_required": 30,
        "all_heroes_required": False,
        "nopwatch_refill_stage": 31
    }

    def test_Victory(self):
        self.checkItemsForLocation("Gauntlet Complete", [
            "Stage 011 Unlock Key",
            "Stage 021 Unlock Key"
        ])

class Xenoblade3AGManualTest_Victory_Heroes(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 1,
        "highest_stage_required": 30,
        "all_heroes_required": True,
        "nopwatch_refill_stage": 31,
        "DLC": False,
        "FutureRedeemed": False,
        "PostGame": False,
        "Switch2": False
    }

    def test_Victory(self):
        self.checkItemsForLocation("Gauntlet Complete", [
            "Stage 011 Unlock Key",
            "Stage 021 Unlock Key",
            "Ethel, Silvercoat",
            "Valdi, Artificer",
            "Zeon, Dutiful",
            "Teach, Inscrutable",
            "Riku & Manana, Peerless",
            "Isurd, Dawnhero",
            "Juniper, Ghostbow",
            "Gray, Ashenpelt",
            "Alexandria, Craftmaiden",
            "Ashera, Undying Blade",
            "Monica, City's Bulwark",
            "Triton, Defiant",
            "Fiona, Proudbanner",
            "Ghondor, Wrathfist",
            "Miyabi, Glorysong",
            "Cammuravi, Smoldering",
            "Segiri, No. 7"
        ])

class Xenoblade3AGManualTest_Victory_HeroesAndRefills(Xenoblade3AGManualTest):
    game = game_name
    options = {
        "gauntlets_included": 1,
        "highest_stage_required": 30,
        "all_heroes_required": True,
        "nopwatch_refill_stage": 1,
        "DLC": False,
        "FutureRedeemed": False,
        "PostGame": False,
        "Switch2": False
    }

    def test_Victory(self):
        self.checkItemsForLocation("Gauntlet Complete", [
            "Stage 011 Unlock Key",
            "Stage 021 Unlock Key",
            "Nopwatch Refill License",
            "Ethel, Silvercoat",
            "Valdi, Artificer",
            "Zeon, Dutiful",
            "Teach, Inscrutable",
            "Riku & Manana, Peerless",
            "Isurd, Dawnhero",
            "Juniper, Ghostbow",
            "Gray, Ashenpelt",
            "Alexandria, Craftmaiden",
            "Ashera, Undying Blade",
            "Monica, City's Bulwark",
            "Triton, Defiant",
            "Fiona, Proudbanner",
            "Ghondor, Wrathfist",
            "Miyabi, Glorysong",
            "Cammuravi, Smoldering",
            "Segiri, No. 7"
        ])