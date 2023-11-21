from ._anvil_designer import birthday_labelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class birthday_label(birthday_labelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.label_bday.visible = False
    print('calling get birthdays from client code')
    birthday_text = anvil.server.call('get_this_month_birthdays')
    if birthday_text:
      self.label_bday.visible = True
      self.label_bday.text = birthday_text