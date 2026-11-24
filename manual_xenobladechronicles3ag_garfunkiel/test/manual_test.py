from test.bases import WorldTestBase
from ..Game import game_name

class Xenoblade3AGManualTest(WorldTestBase):
    game = game_name

    # Check that the location becomes reachable only after all specified items are collected
    def checkItemsForLocation(self, loc, items):
        itemsToCollect = []
        itemsCollected = []

        for item in items:
            if ":" in item:
                itemName, count = item.split(":")
                count = int(count)
                for _ in range(count):
                    itemsToCollect.append(itemName)
            else:
                itemsToCollect.append(item)

        for i in range(len(itemsToCollect)):
            item = itemsToCollect[i]
            index = 0

            if item in itemsCollected:
                index = itemsCollected.count(item)
            itemsCollected.append(item)

            thisItems = self.get_items_by_name(item)

            self.collect(thisItems[index])

            if i == len(itemsToCollect) - 1:
                self.assertTrue(self.can_reach_location(loc))
            else:
                self.assertFalse(self.can_reach_location(loc))