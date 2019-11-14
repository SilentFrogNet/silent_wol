import os

env = os.getenv('SWOL_ENV', 'dev')

if env == 'test':
    from .settings_test import *
else:
    from .settings_dev import *
