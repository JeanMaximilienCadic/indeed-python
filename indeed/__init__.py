from gnutools.utils import RecNamespace
import yaml


def load_config(file="/FileStore/indeed/config.yml"):
    conf = yaml.load(open(file, "r"), Loader=yaml.FullLoader)
    ns = RecNamespace(conf)
    return ns


cfg = load_config()

__version__ = "0.0.1"


