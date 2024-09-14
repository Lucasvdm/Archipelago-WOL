from dataclasses import dataclass
from typing import Dict, Any
from Options import (DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections,
                     PerGameCommonOptions, OptionGroup, Visibility)

class TempOption(DefaultOnToggle):
    internal_name = "temp_option"
    display_name = "Temp Option"

@dataclass
class WOLOptions(PerGameCommonOptions):
    temp_option: TempOption

wol_option_groups = [
    OptionGroup("Logic Options", [
        
    ])
]

wol_option_presets: Dict[str, Dict[str, Any]] = {
    
}