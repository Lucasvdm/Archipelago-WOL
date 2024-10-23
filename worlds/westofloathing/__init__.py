import settings
from typing import List, Dict
from BaseClasses import Item, Location, Tutorial, ItemClassification, Region
from worlds.AutoWorld import WebWorld, World
from .options import wol_option_groups, wol_option_presets, WOLOptions
from .items import item_table, item_name_groups, item_name_to_id
from .locations import location_table, location_name_groups, location_name_to_id
from .regions import region_table
from .rules import set_location_rules, set_region_rules

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
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def create_item(self, name: str, classification: ItemClassification = None) -> WOLItem:
        item_data = item_table[name]
        return WOLItem(name, classification or item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        wol_items: List[WOLItem] = []
        items_to_create: Dict[str, int] = {item: data.copies_in_pool for item, data in item_table.items()}

        #Logic for modifying the item pool contents based on options and such will go here

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                wol_items.append(self.create_item(item))

        self.multiworld.itempool += wol_items

    def create_regions(self) -> None:
        for region_name in region_table:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in region_table.items():
            region = self.get_region(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.location_name_to_id.items():
            region = self.get_region(location_table[location_name].region)
            location = WOLLocation(self.player, location_name, location_id, region)
            region.locations.append(location)

        victory_region = self.get_region("Frisco")
        victory_location = WOLLocation(self.player, "Temp Victory Location", None, victory_region)
        victory_location.place_locked_item(WOLItem("Temp Victory Item", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Temp Victory Item", self.player)
        victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)