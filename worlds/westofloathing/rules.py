from typing import Dict, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import WOLWorld

def can_cook(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            state.has("Beans Illustrated", player) and
            (
             state.has("A Portable Arcane Oven", player) or
             state.can_reach_region("The Great Garbanzo's Hideout", player)
            )
           )

def saved_murray(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (state.can_reach_region("Lost Dutch Oven Mine", player) and
            has_stench_resistance(state, world) and
            (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player)) and
            state.has("El Vibrato Headband", player))

#Resistance buffs that apply to all types and aren't covered by an item category
#Clownwort pollen, Mirrorbeans, and Uncanny Presence
def has_common_resistance(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            (
             state.has("Desert Eatin' And Drinkin'", player) and #For foraging clownwort pollen
             (
              state.can_reach_region("Map Region C", player) or
              state.can_reach_region("Circus", player) or
              state.can_reach_region("Lazy-A Dude Ranch", player) or
              state.can_reach_region("Olive Garden's Homestead", player)
             )
            ) or
            can_cook(state, world) and saved_murray(state, world) or #Can cook Mirrorbeans at level 3
            state.has("Advanced Beancraft", player, 8)
            #Could get Uncanny Presence with fewer of these, 5 guarantees you have the option -
            #but you could still choose something else, so need all 8 to guarantee that you have the perk
           )

def has_stench_resistance(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return state.has_group("Stench Resistance", player) or has_common_resistance(state, world)

def has_hot_resistance(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            state.has_group("Hot Resistance", player) or
            state.can_reach_region("Roy Bean's House", player) or
            (
             state.can_reach_region("Soupstock Lode", player) and
             (state.has("Monkey Wrench", player) or state.has("Percussive Maintenance", player))
            ) or
            has_common_resistance(state, world) or
            (state.has("Varmint Skinnin' Knife", player) and state.can_reach_region("Map Region F", player))
            #Can also get it from Beer-Battered Hot Dogs but those are easily missable and would be a pain for logic
           )

def has_cold_resistance(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            state.has_group("Cold Resistance", player) or
            state.can_reach_region("Roy Bean's House", player) or
            has_common_resistance(state, world)
            #Can also get it from Beer-Battered Hot Dogs but those are easily missable and would be a pain for logic
           )

def has_elv_keystone_source(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            (
             state.can_reach_region("The Perfessor's House", player) and
             state.has("El Vibrato Transponder", player)
            ) or
            (
             state.can_reach_region("Lost Dutch Oven Mine", player) and
             has_stench_resistance(state, world) and
             (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player))
            ) or
            state.can_reach_region("Map Region D", player)
           )

def has_elv_battery_source(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            (
             state.can_reach_region("The Perfessor's House", player) and
             state.has("El Vibrato Transponder", player) and
             state.has("El Vibrato Device", player)
            ) or
            state.can_reach_region("Map Region D", player)
           )

def can_get_breadwood_lumber(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    if not state.can_reach_region("Breadwood", player): return False

    count = 1 #The cemetery quest is basically free, at least as far as AP logic goes
    count += (
              state.has("NE North Central Logging Permit", player) +
              state.has("Breadwood's Missing Mail", player) +
              state.has("Half A Ton Of Yeast", player) +
              state.has("Forty Loaves Of Bread", player) +
              state.has("Overdue Breadwood Book", player) +
              (state.has("Overdue Breadwood Book x5", player) and
               state.can_reach_region("Soupstock Lode", player) and
               (state.has("Monkey Wrench", player) or state.has("Percussive Maintenance", player)) #and
               #has_hot_resistance(state, world)) #This IS a requirement but basically short circuits because you can farm it in soupstock lode
              )
             )

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
    options = world.options

    world.get_entrance("Dirtwater -> Tony's Boots").access_rule = \
        lambda state: (state.can_reach_region("Fort of Darkness", player) and
                       state.has("A Bunch Of Really Small Guns", player))
    world.get_entrance("Dirtwater -> Murray's Curiosity & Bean").access_rule = \
        lambda state: saved_murray(state, world)
    world.get_entrance("Dirtwater -> Grady's Fine Leather Goods").access_rule = \
        lambda state: (state.can_reach_region("Danny's Tannery", player) and
                       state.has("Tannery Back Door Key", player) and
                       state.has("Tannery St. Rage Key", player))
    world.get_entrance("Dirtwater -> Alexandria's Bookstore").access_rule = \
        lambda state: (state.can_reach_region("Alexandria Ranch", player) and
                       state.has("Key-Shaped El Vibrato Device", player))

    world.get_entrance("Dirtwater -> The Perfessor's House").access_rule = \
        lambda state: state.has("Strange Stone Arrow", player)

    #Bounty regions don't really have any hard requirements - even for the ones that need items for the peaceful resolution,
    #you can always just kill 'em, so by default there's the option for basically free progression up to the pickle factory

    world.get_entrance("Silversmith's House -> The Silver Plater").access_rule = \
        lambda state: state.has("Locks And How To Pick Them", player)
    
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
        lambda state: can_cook(state, world)

    if options.dlc_enabled:
        world.get_entrance("Dirtwater -> Gun Manor").access_rule = \
            lambda state: state.has("Ghost Coach To Gun Manor", player)
        world.get_entrance("Gun Manor -> Gun Manor Carriage House").access_rule = \
            lambda state: (state.has("Gun Manor Carriage House Key", player) or
                           state.has("Locks And How To Pick Them", player))
        #By default can also use a can of kerosene + a match (both widely available), or the starting Beanslinger skill Lava Fava,
        #in place of the small blowtorch. But I'm not sure how to handle those things yet, and the blowtorch has no other purpose,
        #so for now I'll call it a hard requirement.
        world.get_entrance("Gun Manor First Floor -> Gun Manor Second Floor").access_rule = \
            lambda state: has_cold_resistance(state, world) and state.has("Small Blowtorch", player)
        world.get_entrance("Gun Manor Second Floor -> Gun Manor Third Floor").access_rule = \
            lambda state: state.has("Elevator Button", player)
        world.get_entrance("Gun Manor Billiards Room -> Gun Manor Belfry").access_rule = \
            lambda state: state.has("Attic-Opening Stick", player)

def set_location_rules(world: "WOLWorld") -> None:
    player = world.player
    options = world.options

    set_rule(world.get_location("Dirtwater Saloon - Bartender's Mini Piano"),
             lambda state: state.can_reach_region("Shaggy Dog Cave", player))
    set_rule(world.get_location("Dirtwater Saloon - Chef's Mail Key"),
             lambda state: (state.has("Shaker Of Saltpeter", player) and
                            state.has("Southeast-Western Murder Pepper", player)))
    set_rule(world.get_location("Dirtwater Saloon - Chef's Quest Complete"),
             lambda state: (state.has("Shaker Of Saltpeter", player) and
                            state.has("Southeast-Western Murder Pepper", player) and
                            state.has("Dave's Secret Sauce Recipe", player)))
    set_rule(world.get_location("Dirtwater Post Office - Postal Codes"),
             lambda state: state.can_reach_region("Postal Way Station", player))
    set_rule(world.get_location("Dirtwater Post Office - P.O. Box 114"),
             lambda state: state.has("Key To P.O. Box 114", player))
    set_rule(world.get_location("Dirtwater Post Office - P.O. Box 441"),
             lambda state: state.has("Key To P.O. Box 441", player))

    #TODO: Logic for shops' bonus items (have another shop to the right)

    set_rule(world.get_location("Shaggy Dog Cave - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Silversmith's House - Spittoon"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Silversmith's House - Safe"),
             lambda state: (state.has("Locks And How To Pick Them", player) and
                            state.has("Get Crackin': A Guide To Modern Safes", player)))
    set_rule(world.get_location("Silversmith's House - Shelf (Item 1)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Silversmith's House - Shelf (Item 2)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Danny's Tannery (St. Rage Shed) - Grady's Cowsbane Seeds"),
             lambda state: (state.has("Tannery Back Door Key", player) and
                            state.has("Tannery St. Rage Key", player)))
    set_rule(world.get_location("Stearns Ranch House - Lockbox"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Stearns Ranch Cellar - Safe"),
             lambda state: state.has("Get Crackin': A Guide To Modern Safes", player))
    set_rule(world.get_location("Snakepit Mine - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("The Daveyard - First Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("The Daveyard - Dave J's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("The Daveyard Mausoleum - The Skeleton of Dave B. Defeated"),
             lambda state: (state.has("Gore-Splattered Scroll", player) and
                            state.has("Human Ashes x2", player) and
                            state.has("Glass Sphere", player) and
                            state.has("Pickaxe", player))) #For mining stardust
    set_rule(world.get_location("Fort Cowardice Back Office - General Gob's Hat"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Cowardice Back Office - General Gob's Pistol"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Cowardice First Tent - Back-Right Footlocker"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Cowardice Math Tent - Safe"),
             lambda state: state.has("Get Crackin': A Guide To Modern Safes", player))
    set_rule(world.get_location("Gustavson Gulch - Deli Hut"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Gustavson Gulch Storage Hut - Secret Item"),
             lambda state: state.has("English-Goblintongue Dictionary", player))
    set_rule(world.get_location("Gustavson Gulch Treasure Cave - Bottom Chest (Item 1)"),
             lambda state: (state.has("Locks And How To Pick Them", player) and
                            (state.has("Gustavson Gulch Treasure Cave Key", player) or
                             state.has("Gustavson Gulch Treasure Cave Key (Spare)", player))))
    set_rule(world.get_location("Gustavson Gulch Treasure Cave - Bottom Chest (Item 2)"),
             lambda state: (state.has("Locks And How To Pick Them", player) and
                            (state.has("Gustavson Gulch Treasure Cave Key", player) or
                             state.has("Gustavson Gulch Treasure Cave Key (Spare)", player))))
    set_rule(world.get_location("Gustavson Gulch Treasure Cave - Middle Chest"),
             lambda state: (state.has("Gustavson Gulch Treasure Cave Key", player) or
                            state.has("Gustavson Gulch Treasure Cave Key (Spare)", player)))
    set_rule(world.get_location("Gustavson Gulch Destroyed - Dynamite Crate"),
             lambda state: (state.can_reach_region("Fort Alldead", player) and
                            state.has("Toy Skeletons", player)))
    set_rule(world.get_location("Railroad Camp (East) - Rock Monster's Remains (Dr. Morton's Quest)"),
             lambda state: state.can_reach_region("Frisco", player))
    set_rule(world.get_location("Kole Ridge Mine (Level 2) - Triangular Stones"),
             lambda state: (state.has("A Length Of Rope", player) and
                            state.has("Shovel", player) and
                            state.can_reach_region("Butterfield Ranch", player)))
    set_rule(world.get_location("Kole Ridge Mine (Level 2) - Bean-Iron Deposit"),
             lambda state: (state.has("A Length Of Rope", player) and
                            state.has("Beans Illustrated", player) and
                            state.has("Pickaxe", player)))
    set_rule(world.get_location("Kole Ridge Mine (Level 3) - Pick-Head"),
             lambda state: state.has("A Length Of Rope", player))
    set_rule(world.get_location("Butterfield Ranch Barn - Milk Shelf"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Butterfield Ranch Barn - Toybox"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Snake Spring - Temporal Rift"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Old Mission Catacombs - Cemented Skull Pile"),
             lambda state: state.has("Pickaxe", player))
    set_rule(world.get_location("Old Millinery - Office Safe"),
             lambda state: (state.has("Locks And How To Pick Them", player) and
                            state.has("Get Crackin': A Guide To Modern Safes", player)))
    set_rule(world.get_location("The Silver Plater - Plated Barbed Wire"),
             lambda state: state.has("Big Coil Of Barbed Wire", player))
    set_rule(world.get_location("Lost Dutch Oven Mine (Level 1) - Lockers (Item 1)"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Lost Dutch Oven Mine (Level 1) - Lockers (Item 2)"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Lost Dutch Oven Mine (Level 1) - Spittoon"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Lost Dutch Oven Mine (Pit) - Emerald Rock"),
             lambda state: (has_stench_resistance(state, world) and
                            (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player)) and
                            state.has("Pickaxe", player)))
    set_rule(world.get_location("El Vibrato Chamber (Lost Dutch Oven Mine) - Leftmost Box"),
             lambda state: (has_stench_resistance(state, world) and
                            (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player)) and
                            has_elv_keystone_source(state, world)))
    set_rule(world.get_location("El Vibrato Chamber (Lost Dutch Oven Mine) - Locked Box"),
             lambda state: (has_stench_resistance(state, world) and
                            (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player)) and
                            has_elv_keystone_source(state, world)))
    set_rule(world.get_location("El Vibrato Ruin - Cylinder"),
             lambda state: (has_stench_resistance(state, world) and
                            (state.has("Percussive Maintenance", player) or state.has("Can Of Oil", player)) and
                            has_elv_keystone_source(state, world) and
                            has_elv_battery_source(state, world)))