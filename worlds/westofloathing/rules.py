from typing import Dict, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import WOLWorld

def has_stench_resistance(percent: int = 1) -> bool:
    #TODO: Add item group for items with stench resistance, and maybe a property for the amount they
    # provide so I can check for if the player has enough (in cases where there's a specific requirement)
    #Can probably generalize this for all resistances and just take a parameter for the type
    return True

def has_hot_resistance() -> bool:
    #For this and other required resistances, need to consider what consumables give them as well and if
    #there are any places where you can reliably craft/loot those consumables in addition to pool items
    return True

def can_get_breadwood_lumber(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    if not state.can_reach_region("Breadwood", player): return False

    count = 1 #The cemetery quest is basically free, at least as far as AP logic goes
    count += (state.has("NE North Central Logging Permit", player) +
        state.has("Breadwood's Missing Mail", player) +
        state.has("Half A Ton Of Yeast", player) +
        state.has("Forty Loaves Of Bread", player) +
        state.has("Overdue Breadwood Book", player) +
        (state.has("Overdue Breadwood Book x5", player) and
         state.can_reach_region("Soupstock Lode", player) and
         (state.has("Monkey Wrench", player) or state.has("Percussive Maintenance", player)) and
         has_hot_resistance()))

    return count >= 5

def can_build_bridge(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    if not state.can_reach_region("Railroad Camp (West)", player): return False

    #Might want another requirement for the El Vibrato bridge route later too, like activating the relevant facility or something
    return (state.has("El Vibrato Model Bridge", player) or
            (state.has("Progressive Nex-Mex Skillbook", player, 4) and state.can_reach_region("Buffalo Pile", player)) or 
            can_get_breadwood_lumber(state, world))

def set_region_rules(world: "WOLWorld") -> None:
    player = world.player
    #options = world.options

    world.get_entrance("Dirtwater -> Tony's Boots").access_rule = \
        lambda state: (state.can_reach_region("Fort of Darkness", player) and
                       state.has("A Bunch Of Really Small Guns", player))
    world.get_entrance("Dirtwater -> Murray's Curiosity & Bean").access_rule = \
        lambda state: (state.can_reach_region("Lost Dutch Oven Mine", player) and
                       has_stench_resistance() and
                       #Percussive Maintenance OR Can of oil, haven't decided how to handle cans of oil and similar
                       state.has("Percussive Maintenance", player) and
                       state.has("El Vibrato Headband", player))
    world.get_entrance("Dirtwater -> Grady's Fine Leather Goods").access_rule = \
        lambda state: (state.can_reach_region("Danny's Tannery", player) and
                       state.has("Tannery Back Door Key", player) and
                       state.has("Tannery St. Rage Key", player))
    world.get_entrance("Dirtwater -> Alexandria's Bookstore").access_rule = \
        lambda state: (state.can_reach_region("Alexandria Ranch", player) and
                       state.has("Key-Shaped El Vibrato Device", player))

    world.get_entrance("Dirtwater -> The Perfessor's House").access_rule = \
        lambda state: state.has("Strange Stone Arrow", player)

    world.get_entrance("Silversmith's House -> The Silver Plater").access_rule = \
        lambda state: state.has("Locks And How To Pick Them", player)

    #TODO: Logic for bounty locations (past the first two):
    #   The Potemkin Gang
    #   Old Millinery
    #   Abandoned Pickle Factory
    #A new bounty unlocks when either of the active ones is completed, so to get access to all of their regions
    #you need the item requirements to complete either of the first two, then either of the remaining, then again
    
    world.get_entrance("Railroad Camp (East) -> Railroad Camp (West)").access_rule = \
        lambda state: state.has("A Year's Supply Of Dynamite", player)

    world.get_entrance("Postal Way Station -> Chuck's House").access_rule = \
        lambda state: state.has("Postal Code Sheet", player)

    world.get_entrance("Roy Bean's House -> Ol' Granddad").access_rule = \
        lambda state: state.has("Mint Mint Jellybeans", player)

    world.get_entrance("Roy Bean's House -> Shroomcave").access_rule = \
        lambda state: (state.has("Mint Mint Jellybeans", player) and
                       state.has("Green Green Apple Jellybeans", player))

    world.get_entrance("Railroad Camp (West) -> Necromancer's Tower").access_rule = \
        lambda state: (state.has_group("Necromancer Clues", player, 5) and
                       state.can_reach_region("The Perfessor's House", player) and
                       state.has("Mycology, Yourcology", player))

    world.get_entrance("Railroad Camp (West) -> Frisco").access_rule = \
        lambda state: can_build_bridge(state, world)

    world.get_entrance("Frisco -> Wasco's Comedy Shack").access_rule = \
        lambda state: state.has("Comedy Flier", player)

    world.get_entrance("Dr. Morton's House -> Old Cave").access_rule = \
        lambda state: state.has("Interesting Rock", player)

    world.get_entrance("Map Region H -> Curious False Mountain").access_rule = \
        lambda state: state.has("El Vibrato Transponder", player)

    world.get_entrance("Miscellany -> Leatherworkery Crafting").access_rule = \
        lambda state: (state.has("Burned Leatherworking Manual", player) and
                       (state.has("A Portable Leatherwork Bench", player) or
                        state.can_reach_region("Hellstrom Ranch", player)))
    world.get_entrance("Miscellany -> Master Cookery Crafting").access_rule = \
        lambda state: (state.has("Beans Illustrated", player) and
                       (state.has("A Portable Arcane Oven", player) or
                        state.can_reach_region("The Great Garbanzo's Hideout", player)))

def set_location_rules(world: "WOLWorld") -> None:
    player = world.player
    options = world.options