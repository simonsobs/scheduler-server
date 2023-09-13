from .basic import config as basic_config
from .flex import config as flex_config

CONFIGS = {
    'basic': basic_config,
    'flex': flex_config
}
def get_default_config(name):
    return CONFIGS.get(name, {})