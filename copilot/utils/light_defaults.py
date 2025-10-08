# Light Configuration Defaults
# Based on data model specifications for three-point lighting setup

LIGHT_DEFAULTS = {
    'KEY': {
        'power_watts': 100,
        'color_temperature': 5600,  # Daylight balanced
        'size': 1.0,
        'horizontal_angle': 45,     # 45 degrees from front
        'vertical_angle': 30,       # 30 degrees elevation
        'distance_multiplier': 3.0,
        'light_type': 'AREA'
    },
    'FILL': {
        'power_watts': 30,          # Softer than key
        'color_temperature': 5600,
        'size': 2.0,                # Larger for softer shadows
        'horizontal_angle': -45,    # Opposite side from key
        'vertical_angle': 15,       # Lower than key
        'distance_multiplier': 3.5,
        'light_type': 'AREA'
    },
    'RIM': {
        'power_watts': 80,          # Strong for edge definition
        'color_temperature': 6500,  # Slightly cooler
        'size': 0.5,                # Smaller for sharper rim
        'horizontal_angle': 135,    # Behind and to side
        'vertical_angle': 45,       # Higher for rim effect
        'distance_multiplier': 2.5,
        'light_type': 'AREA'
    }
}

# Collection naming convention
COLLECTION_NAME_PREFIX = "ThreePointRig"

# Empty object naming for track-to target
TARGET_EMPTY_NAME = "LightTarget"

# Light naming conventions
LIGHT_NAMES = {
    'KEY': 'Key_Light',
    'FILL': 'Fill_Light', 
    'RIM': 'Rim_Light'
}