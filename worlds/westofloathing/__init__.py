import settings, typing
from BaseClasses import Item, Location, Tutorial
from worlds.AutoWorld import WebWorld, World
from .options import wol_option_groups, wol_option_presets, WOLOptions

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

class WOLSettings(settings.Group):
    """May not need this at all, not sure yet"""

class WOLWorld(World):
    """
    Say howdy to West of Loathing -- a single-player slapstick comedy adventure role-playing game set in the wild west 
    of the Kingdom of Loathing universe. Traverse snake-infested gulches, punch skeletons wearing cowboy hats, grapple 
    with demon cows, and investigate a wide variety of disgusting spittoons. Explore a vast open world and encounter a 
    colorful cast of characters, some of whom are good, many of whom are bad, and a few of whom are ugly.
    """
    game = "West of Loathing"
    web = WOLWeb()

    options: WOLOptions
    options_dataclass = WOLOptions
    #settings: typing.ClassVar[WOLSettings]
    item_name_groups = {}
    location_name_groups = {}