from ._anvil_designer import AddOtherPlayersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AddOtherPlayers(AddOtherPlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('AddOtherPlayers called')
    #All Players
    
    
    all_groups = anvil.server.call('all_groups')
    group_3 = anvil.server.call('group_3')
    
    #has name, user link in list.
    list_of_names =  [(r["full_name"],r) for r in all_groups]
    
#     self.drop_down_names.items = [(r["full_name"],r) for r in app_tables.users.search(tables.order_by('full_name', ascending=True))]   

    self.drop_down_names.items = list_of_names
    

  def button_signup_player_click(self, **event_args):
    #Add selected player to tee time.
    player = self.drop_down_names.selected_value
    
    
    '''
  def button_add_player_click(self, **event_args):
    player = self.drop_down_names.selected_value
    event = self.drop_down_all_events.selected_value
    user = data_access.the_user()

    if not event:
      print('no event selected')
      alert(content="Please select an Event")
      return
      
    if not player:
      print('no player selected')
      alert(content="Please select a Player")
      return    
    '''

  