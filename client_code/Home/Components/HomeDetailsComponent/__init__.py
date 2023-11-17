from ._anvil_designer import HomeDetailsComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import navigation
from ..GolfSignupComponent import GolfSignupComponent


class HomeDetailsComponent(HomeDetailsComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # self.label_travel_entry.text = None
    self.label_activities.text = None
    self.label_activities_detail.text = None
    
    #Name Label on the Main Form
    user = navigation.the_user()
    form = navigation.get_form()    
    if user:
      form.label_name.text = 'Hi ' + user['first_name'] + ', '


    
    #----Get Couple's Activities Info,.
    # if user['spouse']:
    #   spouse = user['spouse']
    spouse = None
      
    activities_message_1, activities_message_2 = anvil.server.call('get_user_or_spouse_activities_str', user, spouse)
    self.label_activities.text = activities_message_1
    self.label_activities_detail.text = activities_message_2
#     btn.remove_from_parent()
    self.tee_times_card.add_component(GolfSignupComponent())

      
    
    # Any code you write here will run before the form opens.


