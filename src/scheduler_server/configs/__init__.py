from .basic import config as basic_config
from .flex import config as flex_config
from .sat import config_satp1

CONFIGS = {
    'basic': basic_config,
    'flex': flex_config,
    'satp1': config_satp1,
}
def get_config(preset):
    if preset not in CONFIGS:
        raise ValueError(f'Unknown config preset {preset}')
    return CONFIGS[preset] 