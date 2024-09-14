from BaseClasses import Item, Location, Tutorial
from worlds.AutoWorld import WebWorld, World
from .options import wol_option_groups, wol_option_presets

class WOLLocation(Location):
    game: str = "West of Loathing"

class WOLItem(Item):
    game: str = "West of Loathing"

class WOLWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the West of Loathing AP mod for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["Xylen"]
        )
    ]
    theme = "dirt"
    game = "West of Loathing"
    option_groups = wol_option_groups
    options_presets = wol_option_presets

class WOLWorld(World):
    """
    Say howdy to West of Loathing -- a single-player slapstick comedy adventure role-playing game set in the wild west 
    of the Kingdom of Loathing universe. Traverse snake-infested gulches, punch skeletons wearing cowboy hats, grapple 
    with demon cows, and investigate a wide variety of disgusting spittoons.

    Talk your way out of trouble as a silver-tongued Snake Oiler, plumb the refried mysteries of the cosmos as a wise 
    and subtle Beanslinger, or let your fists do the talking as a fierce Cow Puncher. Explore a vast open world and 
    encounter a colorful cast of characters, some of whom are good, many of whom are bad, and a few of whom are ugly.
    """