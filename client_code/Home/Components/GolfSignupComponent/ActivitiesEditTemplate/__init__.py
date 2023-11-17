from ._anvil_designer import ActivitiesEditTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import navigation

class ActivitiesEditTemplate(ActivitiesEditTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    print('ActivitiesEditTemplate opened')