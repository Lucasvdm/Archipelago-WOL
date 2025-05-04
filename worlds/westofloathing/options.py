from dataclasses import dataclass
from typing import Dict, Any
from Options import (DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections,
                     PerGameCommonOptions, OptionGroup, Visibility)

class EnableDLC(DefaultOnToggle):
    """
    To use this option, you must own the "Reckonin' at Gun Manor" DLC.
    """
    internal_name = "dlc_enabled"
    display_name = "Gun Manor DLC Enabled"

class RandomizeGunManorCoach(DefaultOnToggle):
    """
    Randomize the coach to access Gun Manor into the item pool.
    This has no effect if the Gun Manor DLC is disabled.
    """
    internal_name = "randomize_ghost_coach"
    display_name = "Randomize Gun Manor Coach"

class RandomizeGoblintongue(DefaultOnToggle):
    """
    Randomize the ability to speak Goblintongue into the item pool.
    If this is disabled, you will always be able to speak Goblintongue from the start.
    """
    internal_name = "randomize_goblintongue"
    display_name = "Randomize Goblintongue"

@dataclass
class WOLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool

    dlc_enabled: EnableDLC
    randomize_ghost_coach: RandomizeGunManorCoach
    randomize_goblintongue: RandomizeGoblintongue

wol_option_groups = [
    # OptionGroup("Logic Options", [
        
    # ])
]

wol_option_presets: Dict[str, Dict[str, Any]] = {
    
}