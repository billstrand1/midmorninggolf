from ._anvil_designer import ContactsComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import navigation

class ContactsComponent(ContactsComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    user = navigation.the_user()
    print(f"getting {user['first_name']} from Contacts")
    form = navigation.get_form()
    
    if user:
      form.label_name.text = 'Hi ' + user['first_name'] + ', '

    self.contact_panel.items = anvil.server.call('get_directory')
    

  def btn_get_email_list_click(self, **event_args):
      navigation.go_email_list()