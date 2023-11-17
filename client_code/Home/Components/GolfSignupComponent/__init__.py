from ._anvil_designer import GolfSignupComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import navigation
# from .... import Globals
from .ActivitiesAddTemplate import ActivitiesAddTemplate

class GolfSignupComponent(GolfSignupComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    user = navigation.the_user()
    form = navigation.get_form()
    if user:
      form.label_name.text = 'Hi ' + user['first_name'] + ', '

    #Team 1: All Days
    #Team 2: All Days
    #Team 3: Weekend Only
    self.refresh_data_bindings()
    self.repeating_panel_activites.items = self.get_correct_tee_times_for_team()
    

  def get_correct_tee_times_for_team(self, **event_args ):
    user = navigation.the_user()
    if user['ladies_golf_team'] == 3:
      print(f" Team 3") 
      saturday_only_activities = anvil.server.call('get_all_future_activities_saturday')
      return saturday_only_activities
    else:
      print('Team 1 or 2')      
      future_golf = anvil.server.call('get_all_future_activities')
      return future_golf

  #------------------------WORKING ON EDIT / DELETE / REFRESH-------------
  def refresh_activities(self, **event_args):
    print('refresh_activities called')
    #update should be done in server code:  CANNOT RUN GLOBALS IN SERVER CODE.
    self.refresh_data_bindings()
    self.repeating_panel_activites.items = self.get_correct_tee_times_for_team()
 

  def button_add_click(self, **event_args):
    print('GolfSignupComponent button_add_click called')    
    form = navigation.get_form()
    form.load_component(ActivitiesAddTemplate())
    print('Exiting Button Add Click')
   
    

  def button_1_click(self, **event_args):
    navigation.go_home()

