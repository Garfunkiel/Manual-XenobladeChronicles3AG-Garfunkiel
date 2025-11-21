# Xenoblade Chronicles 3: Archsage's Gauntlet Manual APWorld
This is a Manual APWorld that can be used with the Archsage's Gauntlet in Xenoblade Chronicles 3 to participate in an Archipelago multi-world.

## Instructions/Rules:
- This is a Manual APWorld, so no rules can be enforced, but these are the intended rules to follow.
- Gauntlet (Beginner, Intermediate, and Pro) and Difficulty (Easy, Normal, and Hard) are your choice for any given run, but stages 31 through 50 require Intermediate/Pro, and stages 51 through 140 require Pro.
- You start with one unlocked party member (Noah, Mio, Eunie, Taion, Lanz, Sena) and one of their classes.  When starting a run, you must only use unlocked party members and classes.  The rest are in the pool of random items to receive/collect.
- Heroes can only be recruited in the Gauntlet if you have received/collected the item unlocking them.
- The Nopwatch can only be refilled in a given run as many times as you have received/collected the Nopwatch Refills item.
- Only stages 1 through 10 are unlocked at first. You must receive/collect at least one unlock key for a set of 10 stages to attempt those stages.
- If you have a Chosen Hero Unlock (3 in the pool), when recruiting a hero, you can treat that as the unlock item for that hero.
- If you have a Chosen Class Unlock (1 in the pool), you can use a locked class of your choice when building your character.
- When editing your YAML, choose your desired victory condition:
  - The highest stage you plan to complete (minimum 30, maximum 140)
  - Whether recruiting every hero is required
- Do not use Infinity Blade or Unlimited Sword until you receive/collect the Lucky Seven License.
- If you have Traps enabled, you may occasionally receive/collect a Skip Next Shop trap. When you do, buy nothing from the next shop you encounter at the end of a stage.

## YAML Options:
- Death Link: If you Game Over in the Gauntlet, send a Death Link. When you receive a Death Link, press Minus and quit the current attempt.
- DLC: Set based on whether you want Masha and Ino to be included as locations (recruitments) and items (hero and class unlocks).
- Future Redeemed: Set based on whether you want Shulk and Rex to be included as locations (recruitments) and items (hero unlocks; class unlocks are included as filler items as no party member can inherit these classes).
- Post Game: Set based on whether you want Nia and Melia to be included as locations (recruitments) and items (hero and class unlocks).
- Highest Stage Required: Choose a value between 30 and 140, inclusive.  Beginner (30), Intermediate (50), and Pro (140) are included as standard values.
- All Heroes Required: Set based on whether you want your Victory condition to require recruiting every hero in the pool.

## Notes:
- If you choose a low stage number in your YAML, some useful items may be discarded at random when randomization occurs. The lowest allowed stage (30) has enough locations to include all progression items.

## Credits:
- Github Actions (for Fuzzing and Testing): https://github.com/Eijebong
- Poptracker Template Pack: https://github.com/Cyb3RGER/template_pack