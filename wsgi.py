"""
This file is for running the application under dotCloud. The script mast be
called wsgy.py and it must export a single variable called application.
"""

import sys
sys.path.append('/home/dotcloud/current')
from webapp import app as application
