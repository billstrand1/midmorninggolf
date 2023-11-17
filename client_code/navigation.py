import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.users
import anvil.tables.query as q
from anvil.tables import app_tables
#--------- Import all components here:
from .Home.Components.ContactsComponent import ContactsComponent
from .Home.Components.HomeAnonComponent import HomeAnonComponent
from .Home.Components.HomeDetailsComponent import HomeDetailsComponent
from .Home.Components.ContactsComponent.EmailList import EmailList
from .Home.Components.HelpComponentLoggedIn import HelpComponentLoggedIn
from .Home.Components.HelpComponentLoggedOut import HelpComponentLoggedOut
# from .Home.Components.Birdies import Birdies

'''
Share the navigation module with the Component forms, (import navigation)
Then you can re-direct after a button/link push: navigation.go_home()

'''

#--------------------from data_access module--------------------
__user = None
def the_user():
#     print('the_user running')
    global __user
    if __user:
        return __user

#first time getting user
#     print('no user, must login and store in cache')
    __user = anvil.users.get_user()
    return __user
  
def logout():
  global __user
  __user = None
  anvil.users.logout()
#--------------------from navigation module--------------------
home_form = None

def get_form():
  '''
  In the Home form:
    self.base_title = self.label_title.text
    navigation.home_form = self
    navigation.go_home() 
  '''
  if home_form is None:
    raise Exception("You must set the home form first.")
  return home_form

#Update Active Nav State and Title (called from go_link and Home) 
#function name is the same (set_active_nav)
def set_active_nav(state):
  form = get_form()
  form.set_active_nav(state)  
  
def set_title(text):
  form = get_form()
  base_title = form.base_title
  
  if text:
    form.label_title.text = base_title + " - " + text
  else:
    form.label_title.text = base_title

def require_account():
#   print('require_account running')
  '''
  in functions that require an account, add the following:
  
  user = require_account()
  if not user:
    go_home()
    return
  
  '''
  user = the_user()
  if user: 
    return user

  user = anvil.users.login_with_form(allow_cancel=True)
  form = get_form()
  form.set_account_state(user) #logged in or not, sets button visibility
  return user

# ---------HOME---------------------------------      
# load_component is a function from the Home Form    
#Navigation and Form Loading based upon Log-in Status:

def go_home():
#   print('go_home')
  set_active_nav('home')
  set_title("")
  form = get_form()

  user = the_user()
   
  if user:
    form.load_component(HomeDetailsComponent())
  else:
    form.load_component(HomeAnonComponent())

# ---------CONTACTS-------------------------------- 
def go_contacts():
#   print('go_contacts')
  set_active_nav('contacts')
  set_title("Contacts")
  user = require_account()
  if not user:
    go_home()
    return
  form = get_form()
  form.load_component(ContactsComponent())
  
def go_email_list():
#   print('go_contacts')
  set_active_nav('contacts')
  set_title("Email List")
  
  user = require_account()
  if not user:
    go_home()
    return
  
  form = get_form()
  form.load_component(EmailList())  

def go_help():
#   print('go_help')
  set_active_nav('help')
  set_title("Help")
  form = get_form()

  user = the_user()
   
  if user:
    form.load_component(HelpComponentLoggedIn())
  else:
    form.load_component(HelpComponentLoggedOut())

def go_birdies():
#   print('go_contacts')
  set_active_nav('birdies')
  set_title("Birdies / Skins")
  
  user = require_account()
  if not user:
    go_home()
    return
  
  form = get_form()
  form.load_component(Birdies())  