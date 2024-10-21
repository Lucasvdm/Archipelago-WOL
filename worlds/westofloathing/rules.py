from typing import Dict, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import WOLWorld

def can_leatherwork(state: CollectionState, world: "WOLWorld") -> bool:
    player = world.player

    return (
            state.has("Burnt Leatherworking Manual", player) and
            (
             state.has("A Portable Leatherwork Bench", player) or
             state.can_reach_region("Hellstrom Ranch", player)
            ) and
            state.has("Varmint Skinnin' Knife", player) #Not technically a requirement for everything but reasonable to expect
           )

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

    world.get_entrance("Circus -> Circus (Inside)").access_rule = \
        lambda state: state.has("Circus Ticket", player)
    
    world.get_entrance("Railroad Camp (East) -> Railroad Camp (West)").access_rule = \
        lambda state: state.has("A Year's Supply Of Dynamite", player)

    world.get_entrance("Alexandria Ranch -> Alexandria Ranch Vault").access_rule = \
        lambda state: (state.can_reach_region("Fort Treason", player) and
                       state.has("Fort Treason Ballistics Chart", player) and
                       state.has("Artillery Targeting Flare", player) and
                       state.has("Demi-Culverin Cannonball", player))

    world.get_entrance("Jumbleneck Mine -> Jumbleneck Mine (Inside)").access_rule = \
        lambda state: (state.has("Jumbleneck Mine Elevator Key", player) or
                       state.has("Locks And How To Pick Them", player))

    world.get_entrance("Curious Abandoned Well -> Curious Abandoned Well Facility").access_rule = \
        lambda state: (state.has("A Length Of Rope", player) and
                       state.can_reach_location("El Vibrato Ruin - Cylinder", player) and
                       state.has("El Vibrato Cylinder", player)) #What if you've only gotten one and used it somewhere else?

    world.get_entrance("Postal Way Station -> Chuck's House").access_rule = \
        lambda state: state.has("Postal Code Sheet", player)

    world.get_entrance("Roy Bean's House -> Ol' Granddad").access_rule = \
        lambda state: state.has("Mint Mint Jellybeans", player)

    world.get_entrance("Roy Bean's House -> Shroomcave").access_rule = \
        lambda state: (state.has("Mint Mint Jellybeans", player) and
                       state.has("Green Green Apple Jellybeans", player))

    world.get_entrance("Madness Maw Mine -> El Vibrato Outpost (MMM)").access_rule = \
        lambda state: (state.has("El Vibrato Transponder", player) and
                       state.has("Pickaxe", player))

    world.get_entrance("Railroad Camp (West) -> Necromancer's Tower").access_rule = \
        lambda state: (state.has_group("Necromancer Clues", player, 5) and
                       state.can_reach_region("The Perfessor's House", player) and
                       state.has("Mycology, Yourcology", player))

    world.get_entrance("Railroad Camp (West) -> Frisco").access_rule = \
        lambda state: can_build_bridge(state, world)

    world.get_entrance("Frisco -> Wasco's Comedy Shack").access_rule = \
        lambda state: state.has("Comedy Flier", player)

    world.get_entrance("Abandoned Mine -> Abandoned Mine (Inside)").access_rule = \
        lambda state: ((state.has("Can Of Oil", player) and state.has("Monkey Wrench", player)) or
                       state.has("Percussive Maintenance", player))

    world.get_entrance("Dr. Morton's House -> Old Cave").access_rule = \
        lambda state: state.has("Interesting Rock", player)

    world.get_entrance("Map Region H -> Curious False Mountain").access_rule = \
        lambda state: state.has("El Vibrato Transponder", player)

    world.get_entrance("Deepest Delve Mine -> Deepest Delve Mine (Elevator Fixed)").access_rule = \
        lambda state: ((state.has("Can Of Kerosene", player) and state.has("Gas Cap", player)) or
                       state.has("Percussive Maintenance", player))

    world.get_entrance("Miscellany -> Leatherworkery Crafting").access_rule = \
        lambda state: can_leatherwork(state, world)
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
    set_rule(world.get_location("Lost Dutch Oven Mine - Sluice"),
             lambda state: state.can_reach_region("Snakepit Mine", player))
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
    set_rule(world.get_location("Fort Alldead - Trash Can"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Fort Alldead Barracks - Bottom-Right Footlocker"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Lazy-A Dude Ranch - Dreads Dude Hat Trade"),
             lambda state: state.has("Old Patrol Cap", player))
    set_rule(world.get_location("Lazy-A Dude Ranch - Cowsbane Harvest"),
             lambda state: (state.has("Packet Of Cowsbane Seeds", player) and
                            state.has("Silver-Plated Barbed Wire", player)))
    set_rule(world.get_location("Abandoned Pickle Factory - Puzzle Solved"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Humming Cave - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Circus - Slide Whistle Reward"),
             lambda state: state.has("Slide Whistle", player))
    set_rule(world.get_location("Circus Kid - Lucky Cap Trade"),
             lambda state: state.has("Balloon", player))
    set_rule(world.get_location("Circus - Survived the Main Act"),
             lambda state: state.has("Circus Show Ticket", player))
    set_rule(world.get_location("Circus - Barnaby Bob's Safe"),
             lambda state: (state.can_reach_region("Fort Alldead", player) and
                            state.has("Toy Skeletons", player)))
    set_rule(world.get_location("Ghostwood - Ghost Cactus"),
             lambda state: state.has("Ghostwood Visitor's Permit", player))
    set_rule(world.get_location("Ghostwood - Sharpened Pencil"),
             lambda state: state.has("Ghost Pencil", player))
    set_rule(world.get_location("Ghostwood Town Hall - Issued ID"),
             lambda state: state.has("Sharpened Ghost Pencil", player))
    set_rule(world.get_location("Ghostwood Office Supply - Stapler"),
             lambda state: state.has("Ghostwood Visitor's ID", player))
    set_rule(world.get_location("Ghostwood Jail - Stapled Report"),
             lambda state: state.has("Ghost Stapler", player))
    set_rule(world.get_location("Ghostwood Stable - Got IDDTF"),
             lambda state: state.has("Breadwood Logging Report", player))
    set_rule(world.get_location("Ghostwood Salooooon - Staple Remover"),
             lambda state: state.has("Breadwood Logging Report Folder", player))
    set_rule(world.get_location("Ghostwood Town Hall - The Final Form"),
             lambda state: state.has("Ghost Staple Remover", player))
    set_rule(world.get_location("Ghostwood Town Hall - Permit Finally Processed"),
             lambda state: state.has("Breadwood Logging Permit Forms", player))
    set_rule(world.get_location("Ghostwood Salooooon - Whiskey Bottle"),
             lambda state: state.has("Ghostwood Visitor's ID", player))
    set_rule(world.get_location("Soupstock Lode (Level 1) - Workbench Toolbox (Item 1)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Soupstock Lode (Level 1) - Workbench Toolbox (Item 2)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Soupstock Lode (Level 1) - Bean-Iron Deposit (Bottom Left)"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("El Vibrato Chamber (Soupstock Lode) - Chest"),
             lambda state: ((state.has("Percussive Maintenance", player) or state.has("Monkey Wrench", player)) and
                            state.has("Pickaxe", player) and
                            state.has("El Vibrato Transponder", player) and
                            has_elv_keystone_source(state, world)))
    set_rule(world.get_location("Fort Memoriam Barracks - Trash Pile"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Alexandria Ranch Vault - Glass Case (Right)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Alexandria Ranch Vault - Glass Case (Middle)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Alexandria Ranch Vault - Glass Case (Left)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Curly's Cairn - Under the Cairn"),
             lambda state: state.has("Curly's Compass", player))
    set_rule(world.get_location("Roy Bean's House - Honey Bean"),
             lambda state: state.can_reach_region("Frisco", player))
    set_rule(world.get_location("Jelly Bean Thieves' Hideout - Crate Beside Bed"),
             lambda state: state.has("Crowbar", player))
    set_rule(world.get_location("Shroomcave - First Magic Mushroom"),
             lambda state: (state.has("Mycology, Yourcology", player) and
                            state.has("Mushroom Plucking Pliers", player)))
    set_rule(world.get_location("Shroomcave - Second Magic Mushroom"),
             lambda state: (state.has("Mycology, Yourcology", player) and
                            state.has("Mushroom Plucking Pliers", player)))
    set_rule(world.get_location("Shroomcave - Third Magic Mushroom"),
             lambda state: (state.has("Mycology, Yourcology", player) and
                            state.has("Mushroom Plucking Pliers", player)))
    set_rule(world.get_location("Shroomcave (Hidden Lounge) - Lava Lamp"),
             lambda state: (state.has("Lactarius Dirtihippica mushroom x4", player) and
                            state.can_reach_region("Fort of Darkness", player))) #To trade for Dirtihippica extract
    set_rule(world.get_location("Shroomcave (Hidden Lounge) - Jellybean Jar"),
             lambda state: (state.has("Lactarius Dirtihippica mushroom x4", player) and
                            state.can_reach_region("Fort of Darkness", player))) #To trade for Dirtihippica extract
    set_rule(world.get_location("Fort of Darkness (First Tent) - Free Mushroom"),
             lambda state: state.has("Mind Your Meat", player))
    set_rule(world.get_location("Fort of Darkness (Fifth Tent) - Gun Safe"),
             lambda state: state.has("Get Crackin': A Guide To Modern Safes", player))
    set_rule(world.get_location("Fort of Darkness - Temporal Rift"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Fort Treason Barracks - Top-Left Footlocker"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Treason Barracks - Top-Right Footlocker (Item 1)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Treason Barracks - Top-Right Footlocker (Item 2)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Fort Treason Barracks - Bottom-Right Footlocker"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Jumbleneck Mine - Grease Barrel"),
             lambda state: state.has("Paper Bag", player))
    set_rule(world.get_location("Jumbleneck Mine Foreman's Office - Safe (Item 1)"),
             lambda state: (state.has("Silver-Toothed Skull", player) or
                            state.has("Get Crackin': A Guide To Modern Safes", player)))
    set_rule(world.get_location("Jumbleneck Mine Foreman's Office - Safe (Item 2)"),
             lambda state: (state.has("Silver-Toothed Skull", player) or
                            state.has("Get Crackin': A Guide To Modern Safes", player)))
    set_rule(world.get_location("Jumbleneck Mine (Left Tunnel) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Jumbleneck Mine (Right Tunnel) - Idol"),
             lambda state: (state.has("Unstable Stick Of Dynamite", player) and
                            state.has("Bag Of Grease", player)))
    set_rule(world.get_location("Curious Abandoned Well Facility (Secondary Storage) - Top Chest"),
             lambda state: has_elv_keystone_source(state, world))
    set_rule(world.get_location("Curious Abandoned Well Facility (Secondary Storage) - Bottom Chest"),
             lambda state: has_elv_keystone_source(state, world))
    set_rule(world.get_location("Reboot Hill (Plot 1) - Wise Ol' Jed Marmot's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 1) - Big Bob Hurlingham's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 2) - Dink 'Scotch' Terkinson's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 2) - Fred Deeks' Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 2) - Annette Jangle's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 2) - Fancy Tomb (Middle)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Reboot Hill (Plot 2) - Fancy Tomb (Right)"),
             lambda state: state.has("Get Crackin': A Guide To Modern Safes", player))
    set_rule(world.get_location("Reboot Hill (Plot 3) - Paulette Tootsbury's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("Reboot Hill (Plot 3) - Outhouse"),
             lambda state: has_stench_resistance(state, world))
    set_rule(world.get_location("Reboot Hill (Plot 3) - Stanrietta Minkleston's Grave"),
             lambda state: state.has("Shovel", player))
    set_rule(world.get_location("ReBoot Hill - Tontine Treasure Chest"),
             lambda state: (state.has("Key Fragment 1", player) and
                            state.has("Key Fragment 2", player) and
                            state.has("Key Fragment 3", player)))
    set_rule(world.get_location("The West Pole - Leftmost Cairn (Dr. Morton's Quest)"),
             lambda state: state.can_reach_region("Frisco", player))
    set_rule(world.get_location("Temporal Nexus - Camaro"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Temporal Nexus - Stagecoach"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Temporal Nexus - Robot"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Temporal Nexus - Jawbone"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("The Great Garbanzo's Hideout - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Buffalo Pile (Sleeping Quarters) - Left Footlocker (Item 1)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Buffalo Pile (Sleeping Quarters) - Left Footlocker (Item 2)"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Buffalo Pile (Sleeping Quarters) - Right Footlocker"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Buffalo Pile Locker Key", player)))
    set_rule(world.get_location("Madness Maw Mine (Level 2) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Madness Maw Mine (Curly's Cave) - Nightstand"),
             lambda state: state.has("Curly's Auto-Gyrotheodolite", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Madness Maw Mine (Curly's Cave) - Pie Safe"),
             lambda state: state.has("Curly's Auto-Gyrotheodolite", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Madness Maw Mine (Level 4) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Kellogg Ranch (Main Building) - Loose Floorboard"),
             lambda state: state.has("Crowbar", player))
    set_rule(world.get_location("Kellogg Ranch (Office) - Animal Skeleton"),
             lambda state: state.can_reach_region("Petting Cemetery", player))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - First Locker (Item 1)"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - First Locker (Item 2)"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - Second Locker"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - Fourth Locker"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - Fifth Locker"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - Sixth Locker (Item 1)"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Dormitory) - Sixth Locker (Item 2)"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Kitchen) - Dough Baked"),
             lambda state: state.has("Bag Of Mixed Grain", player))
    set_rule(world.get_location("Kellogg Ranch (Barn) - Barbed Wire"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Kellogg Ranch (Barn) - Grain Pile"),
             lambda state: (state.has("Locks And How To Pick Them", player) or
                            state.has("Kellogg Ranch Keyring", player)))
    set_rule(world.get_location("Fort Unnecessary - Time Portal"),
             lambda state: state.has("Key-Shaped El Vibrato Device", player))
    set_rule(world.get_location("Abandoned Mine - Drywasher"),
             lambda state: state.can_reach_region("Snakepit Mine", player))
    set_rule(world.get_location("Abandoned Mine (Inside) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Abandoned Mine (Side Tunnel 1) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Abandoned Mine (Side Tunnel 2) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Abandoned Mine (Side Tunnel 2) - Drilling Machine"),
             lambda state: (state.can_reach_region("Frisco", player) and
                            state.can_reach_region("Dr. Morton's House", player) and
                            state.has("Interesting Rock", player) and
                            state.has("Weird Rock Sample", player)))
    set_rule(world.get_location("El Vibrato Storage Room - Card Table (Item 1)"),
             lambda state: state.has("El Vibrato Transponder", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("El Vibrato Storage Room - Card Table (Item 2)"),
             lambda state: state.has("El Vibrato Transponder", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("El Vibrato Storage Room - Cylinder"),
             lambda state: state.has("El Vibrato Transponder", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("Morton's Quarry (Tiny Diverticulum) - Hex Puzzle"),
             lambda state: (state.can_reach_region("Frisco", player) and
                            state.can_reach_region("Dr. Morton's House", player) and
                            state.has("Interesting Rock", player) and
                            state.has("Weird Rock Sample", player) and
                            state.has("High-Tech Drill Bit", player)))
    set_rule(world.get_location("Morton's Quarry - Dr. Morton's Quest Completion"),
             lambda state: (state.can_reach_region("Frisco", player) and
                            state.can_reach_region("Dr. Morton's House", player) and
                            state.has("Interesting Rock", player) and
                            state.has("Weird Rock Sample", player) and
                            state.has("High-Tech Drill Bit", player)))
    set_rule(world.get_location("Jeweler's Cabin - Coal"),
             lambda state: state.has("Superdense Coal", player))
    set_rule(world.get_location("Jeweler's Cabin - Sapphire"),
             lambda state: state.has("Cool Sapphire", player))
    set_rule(world.get_location("Jeweler's Cabin - Cowseye"),
             lambda state: state.has("Cowseye", player))
    set_rule(world.get_location("Jeweler's Cabin - Diamond"),
             lambda state: state.has("Massive Diamond", player))
    set_rule(world.get_location("Jeweler's Cabin - Emerald"),
             lambda state: state.has("Effluvious Emerald", player))
    set_rule(world.get_location("Jeweler's Cabin - Ruby"),
             lambda state: state.has("Unbreakable Ruby", player))
    set_rule(world.get_location("Jeweler's Cabin - Silicon"),
             lambda state: state.has("Strange Silvery Crystal", player))
    set_rule(world.get_location("Jeweler's Cabin - Diorite"),
             lambda state: state.has("Polished Diorite", player))
    set_rule(world.get_location("Jeweler's Cabin - Spectacles"),
             lambda state: state.can_reach_region("Fort Unnecessary", player))
    set_rule(world.get_location("El Vibrato Chamber (Curious False Mountain) - Chronokey Fabrication"),
             lambda state: state.has("El Vibrato Cylinder", player))
    set_rule(world.get_location("Alamo Rent-A-Mule - Rented a Mule"),
             lambda state: state.can_reach_region("Fort Unnecessary", player))
    set_rule(world.get_location("Curious Flat Plain - Garbage Return"),
             lambda state: state.has("El Vibrato Cylinder", player))
    set_rule(world.get_location("Deepest Delve Mine (Alt Entrance) - Bean-Iron Deposit"),
             lambda state: state.has("Beans Illustrated", player) and state.has("Pickaxe", player))
    set_rule(world.get_location("El Vibrato Control Center - El Vibrato Quest Completion"),
             lambda state: (state.has("Pickaxe", player) and
                            state.has("El Vibrato Cross", player) and
                            state.can_reach_region("Curious False Mountain", player) and
                            state.can_reach_region("Curious Flat Plain", player) and
                            state.has("El Vibrato Cylinder", player, 2)))
    set_rule(world.get_location("Halloway's Hideaway - Half of Curly's Map"),
             lambda state: (state.has("Left Half Of Curly's Map", player) and
                            state.has("Halloway's Pin", player)))
    set_rule(world.get_location("Halloway's Hideaway - X Marks the Spot"),
             lambda state: (state.has("Left Half Of Curly's Map", player) and
                            state.has("Right Half Of Curly's Map", player) and
                            state.has("Shovel", player)))

    set_rule(world.get_location("Random Encounter (Region A) - Murder Pepper"),
             lambda state: state.has("Shaker Of Saltpeter", player))

    set_rule(world.get_location("Rufus' Gifts - Gift 1"),
             lambda state: state.has("Blank Postcard", player))
    set_rule(world.get_location("Rufus' Gifts - Gift 2"),
             lambda state: state.has("Blank Postcard", player, 2))
    set_rule(world.get_location("Rufus' Gifts - Gift 3"),
             lambda state: state.has("Blank Postcard", player, 3))
    set_rule(world.get_location("Rufus' Gifts - Gift 4"),
             lambda state: state.has("Blank Postcard", player, 4))
    set_rule(world.get_location("Rufus' Gifts - Gift 5"),
             lambda state: state.has("Blank Postcard", player, 5))
    set_rule(world.get_location("Opened Charred Locket"),
             lambda state: state.has("Locks And How To Pick Them", player))
    set_rule(world.get_location("Magic-Infused Leaf Crafting - 3 Leaves"),
             lambda state: state.can_reach_region("Gun Manor Hedge Maze", player))
    set_rule(world.get_location("Magic-Infused Leaf Crafting - 5 Leaves"),
             lambda state: state.can_reach_region("Gun Manor Hedge Maze", player))
    set_rule(world.get_location("Magic-Infused Leaf Crafting - 7 Leaves"),
             lambda state: state.can_reach_region("Gun Manor Hedge Maze", player))
    set_rule(world.get_location("Spider Part Crafting - 4 Piles"),
             lambda state: state.can_reach_region("Gun Manor Cellar", player))
    set_rule(world.get_location("Spider Part Crafting - 6 Piles"),
             lambda state: state.can_reach_region("Gun Manor Cellar", player))
    set_rule(world.get_location("Spider Part Crafting - 8 Piles"),
             lambda state: state.can_reach_region("Gun Manor Cellar", player))

    #Same deal here as with the El Vibrato cylinders, not sure yet how to track which checks you've used the
    #unique nuggets for since there are multiple options per -- requiring one then 2 then 3 isn't right but works for now
    set_rule(world.get_location("Master Cookery Crafting - Level 1 (Item 1)"),
             lambda state: state.has("Bean-Iron Nugget", player))
    set_rule(world.get_location("Master Cookery Crafting - Level 1 (Item 2)"),
             lambda state: state.has("Bean-Iron Nugget", player, 2))
    set_rule(world.get_location("Master Cookery Crafting - Level 1 (Item 3)"),
             lambda state: state.has("Bean-Iron Nugget", player, 3))
    set_rule(world.get_location("Master Cookery Crafting - Level 2 (Item 1)"),
             lambda state: state.has("Dense Bean-Iron Nugget", player))
    set_rule(world.get_location("Master Cookery Crafting - Level 2 (Item 2)"),
             lambda state: state.has("Dense Bean-Iron Nugget", player, 2))
    set_rule(world.get_location("Master Cookery Crafting - Level 2 (Item 3)"),
             lambda state: state.has("Dense Bean-Iron Nugget", player, 3))
    set_rule(world.get_location("Master Cookery Crafting - Level 3 (Item 1)"),
             lambda state: state.has("Delicate Bean-Iron Nugget", player))
    set_rule(world.get_location("Master Cookery Crafting - Level 3 (Item 2)"),
             lambda state: state.has("Delicate Bean-Iron Nugget", player, 2))
    set_rule(world.get_location("Master Cookery Crafting - Level 3 (Item 3)"),
             lambda state: state.has("Delicate Bean-Iron Nugget", player, 3))

    if options.dlc_enabled:
        set_rule(world.get_location("Desert House - Macready's Grave"),
             lambda state: (state.has("Basics Of Gun law", player) and
                            state.has("Duel Law", player) and
                            state.has("1878 Nautical Almanac", player)))

        set_rule(world.get_location("Back of Gun Manor - Compost Heap"),
             lambda state: has_stench_resistance(state, world))
        set_rule(world.get_location("Gun Manor Carriage House - Lathe"),
             lambda state: state.has("Wobbly Billiards Cue", player))
        set_rule(world.get_location("Gun Manor Visitor Center - Photo"),
             lambda state: (state.has("Basics Of Gun law", player) and
                            state.has("Duel Law", player) and
                            state.has("1878 Nautical Almanac", player) and
                            state.has("Shovel", player) and
                            state.has("Macready's Pocketwatch", player)))
        set_rule(world.get_location("Gun Manor Visitor Center - SouvenIRS Stand"),
             lambda state: (state.can_reach_region("Mr. Gun's Manliness Room", player) and
                            state.has("Shower Curtain", player)))
        set_rule(world.get_location("Gun Manor Laboratory - Workbench"),
             lambda state: (state.has("Wad Of Stuffing", player) and
                            state.has("1.2337\" Diameter Tin Can", player)))
        set_rule(world.get_location("Gun Manor Laboratory - Workbench"),
             lambda state: state.has("Mrs. Gun's Blueprint", player))
        set_rule(world.get_location("Gun Manor Parlor - Sofa Cushions (Murdered Chili)"),
             lambda state: (state.can_reach_region("Gun Manor Dining Room", player) and
                            state.has("Chili Sin Pistoles", player)))
        set_rule(world.get_location("Gun Manor Kitchen - Spice Rack"),
             lambda state: state.can_reach_region("Gun Manor Dining Room", player))
        set_rule(world.get_location("Gun Manor Parlor - Sofa Cushions (Murdered Chili)"),
             lambda state: (state.can_reach_region("Gun Manor Dining Room", player) and
                            state.can_reach_region("Gun Manor Library", player) and
                            state.has("Chili Spices", player) and
                            state.has("A Pile Of Loose Chili Beans", player)))
        set_rule(world.get_location("Gun Manor Larder - Right Shelf"),
             lambda state: state.can_reach_region("Gun Manor Laboratory", player))
        set_rule(world.get_location("Gun Manor Library - Fun Law Returned"),
             lambda state: state.has("Fun Law: Rules For Parlor Games", player))
        set_rule(world.get_location("Gun Manor Library - Duelling Banjos Returned"),
             lambda state: state.has("Duelling Banjos", player))
        set_rule(world.get_location("Gun Manor Art Gallery - Clock Noon Objection"),
             lambda state: (state.has("Basics Of Gun law", player) and
                            state.has("Duel Law", player)))
        set_rule(world.get_location("Gun Manor Art Gallery - Lawyer Quest Completion"),
             lambda state: (state.has("Basics Of Gun law", player) and
                            state.has("Duel Law", player) and
                            state.has("1878 Nautical Almanac", player) and
                            state.has("Shovel", player) and
                            state.has("Macready's Pocketwatch", player)))