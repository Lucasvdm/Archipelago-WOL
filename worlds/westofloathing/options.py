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

@dataclass
class WOLOptions(PerGameCommonOptions):
    dlc_enabled: EnableDLC

wol_option_groups = [
    OptionGroup("Logic Options", [
        
    ])
]

wol_option_presets: Dict[str, Dict[str, Any]] = {
    
}