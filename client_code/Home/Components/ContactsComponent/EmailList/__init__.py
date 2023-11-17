from ._anvil_designer import EmailListTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import navigation

class EmailList(EmailListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    email_list_str = anvil.server.call('get_email_list')
    self.lbl_email.text = email_list_str  