from ._anvil_designer import HelpComponentLoggedOutTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import navigation

class HelpComponentLoggedOut(HelpComponentLoggedOutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
class HelpComponentLoggedOut(HelpComponentLoggedOutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
    #     user = data_access.the_user()
#     print(user['first_name'])
    form = navigation.get_form()
    
#     if user is None:
#       current_user = anvil.users.login_with_form()
      
#     self.name_label.text = (user['first_name'] + ' ' + user['last_name'])
#     self.email_label.text = user['email']
    
  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Set 'name' to the text in the 'name_box'
    name = self.name_box.text
    # Set 'email' to the text in the 'email_box'
    email = self.email_box.text
    # Set 'feedback' to the text in the 'feedback_box'
    comment = self.comment_area.text
    anvil.server.call('add_comment', name, email, comment)
    Notification("Question / Comment submitted, Thank you.\n  I'll reply shortly.").show()
    navigation.go_home()
