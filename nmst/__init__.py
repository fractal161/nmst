"""
Nestris Match Statistics Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utility functions to manipulate the **CTM Masters Match Statistics** database,
maintained by aGameScout, Marfram, and HydrantDude.

:license: MIT, see LICENSE for more details.
"""

from .config import config
from .load import update_db, load_as_df, load_as_list
