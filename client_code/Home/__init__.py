from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users


# from .. import Globals
from .. import navigation
from . import Components
from .Components.ContactsComponent import ContactsComponent
from .Components.HomeAnonComponent import HomeAnonComponent
from .Components.HomeDetailsComponent import HomeDetailsComponent
from .Components.HelpComponentLoggedIn import HelpComponentLoggedIn
from .Components.HelpComponentLoggedOut import HelpComponentLoggedOut


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
# ------------------Comment out before cloning, run from data_functions Server Code
    # print('Calling for log-in')
    # anvil.server.call('force_debug_login')

    
    user = navigation.the_user()
    if user:
      print(f" User is {user['first_name']}")
      

    #------------------CREATE MENU LINKS, UPDATE BASED UPON 'FEATURES' TABLE
    #Create the Menu of Links, then update the navigation module


    # Home - Default ON
    self.link_home = Link(text='Home', icon='fa:home')
    self.menu_panel.add_component(self.link_home)
    self.link_home.set_event_handler('click', self.link_home_click)

    # Birdies / Skins
    # self.link_birdies = Link(text='Birdies / Skins', icon='fa:home')
    # self.menu_panel.add_component(self.link_birdies)
    # self.link_birdies.set_event_handler('click', self.link_birdies_click)
    
    #Contacts
    self.link_contacts = Link(text='Contacts', icon="fa:book")
    self.menu_panel.add_component(self.link_contacts)
    self.link_contacts.set_event_handler('click', self.link_contacts_click)

    #Help
    self.link_help = Link(text='Help', icon='fa:question-circle')
    self.menu_panel.add_component(self.link_help)
    self.link_help.set_event_handler('click', self.link_help_click)    
    
    #------------------Set the base title, will be concatenated with the Menu Item Title
    self.base_title = self.label_title.text #title of app on HOME - Design - label_title
    user = navigation.the_user()  #cache's the user info    
    self.set_account_state(user) #logged in or not, sets button visibility
        
    navigation.home_form = self
    navigation.go_home()
    
    form = navigation.get_form()   
    #Set Link Visibility based upon log-in  status
    #Leaving Home and Help visible
    if user:
      form.label_name.text = 'Hi ' + user['first_name'] + ', '
      self.link_contacts.visible = True
    else:
      self.link_contacts.visible = False




   
  #------------------FUNCTIONS BELOW:
  #------------------Set Active Nave State - called from navigation  
  def set_active_nav(self, state):
    self.link_home.role = 'selected' if state == 'home' else None
    # self.link_birdies.role = 'selected' if state == 'birdies' else None
    self.link_contacts.role = 'selected' if state == 'contacts' else None    
    # self.link_maps.role = 'selected' if state == 'maps' else None
    # self.link_activities.role = 'selected' if state == 'activities' else None
    # self.link_admin.role = 'selected' if state == 'admin' else None
    self.link_help.role = 'selected' if state == 'help' else None

  #------------------LOAD HOME CARD, CALLED FROM NAV MODULE  
  def load_component(self, cmpt):
     self.card_home.clear()
     self.card_home.add_component(cmpt)

  #------------------USER STATE FUNCTIONS, set button visibility
  def set_account_state(self, user):
      self.btn_logout.visible = user is not None
      self.btn_login.visible = user is None  #i.e. is NOT logged in
#       self.btn_register.visible = user is None 
#       self.btn_account.visible = user is not None #i.e. is logged in
      
  #------------------------------BUTTON CLICKS
  def btn_account_click(self, **event_args):
      print('Account button clicked, nothing to do yet....')
      navigation.go_home()
  
  def btn_logout_click(self, **event_args):
    print('Logout button clicked')
#     anvil.users.logout()
    navigation.logout()
    self.set_account_state(None) #logged in or not, sets button visibility
    self.label_name.text = ''
    self.label_name.visible = False
    self.link_contacts.visible = False 
    navigation.go_home()

  def btn_login_click(self, **event_args):
    user = anvil.users.login_with_form(allow_cancel=True)
    user = navigation.the_user()
    self.set_account_state(user)
    
    if user:
      self.label_name.text = f"Hi {user['first_name']},"
      self.label_name.visible = True
# #       self.link_activities.visible = True
      self.link_contacts.visible = True
      self.link_birdies.visible = True        
#       if user['admin']:
#         self.link_admin.visible = True
#       else: 
#         self.link_admin.visible = False    
      
    navigation.go_home()


        
  #------------------------------LINK CLICKS      
  def link_home_click(self, **event_args):
    navigation.go_home()
  
  def link_contacts_click(self, **event_args):
    navigation.go_contacts()

  def link_help_click(self, **event_args):
    navigation.go_help()
    
  def link_birdies_click(self, **event_args):
    navigation.go_birdies()
