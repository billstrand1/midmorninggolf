from ._anvil_designer import GolfTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import navigation
from ..ActivitiesAddTemplate import ActivitiesAddTemplate
from ..ActivitiesEditTemplate import ActivitiesEditTemplate

#Same as Future Activities Signup Component

class GolfTemplate(GolfTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    #Name Label on the Main Form
    user = navigation.the_user()
    form = navigation.get_form()
    if user:
      form.label_name.text = 'Hi ' + user['first_name'] + ', '
      
    owner_of_activity = self.item['owner']
    print(f"Owner: {owner_of_activity['first_name']}")
    if owner_of_activity == user:
      self.link_delete.visible = True
      self.link_edit.visible = True    
    if user['email'] == 'billstrand1@yahoo.com':
      self.link_delete.visible = True
      self.link_edit.visible = True
    if user['email'] == 'jacklcarroll@verizon.net':
      self.link_delete.visible = True
      self.link_edit.visible = True      
      
#Here's where I need to break down the queries to only golf....
#Also need to work on the priviledges for sign-up / viewing.
#Add a "Create Tee Time button here also"

    self.repeating_panel_participants.items = anvil.server.call('get_participants_in_activity', self.item)
    self.repeating_panel_participants.set_event_handler('x-update-panel', self.update_panel)

  def update_panel(self, **event_args):
    print('update_panel called')
    self.refresh_data_bindings()
    self.repeating_panel_participants.items = anvil.server.call('get_participants_in_activity', self.item)
    

  def link_signup_click(self, **event_args):
    print('self.link_signup_click called')
    #add participant to sign-up list
    user = navigation.the_user()
  
    # if user['spouse']:
    #   spouse = user['spouse']
    spouse = None  

#  FROM ACTIVITY SERVER CODE
    either_user_or_spouse = app_tables.participation.search(activity=self.item, participant=q.any_of(user, spouse))
    if len(either_user_or_spouse) > 0:
      print('either_user_or_spouse > 0 ACTIVITY CLIENT')
      # if user['spouse'] == None:
      #   print('Single person already signed up')
      #   message = "You have already signed up for this Tee Time." 
      #   alert(message)
      #   return  
      
      # print('Couple already signed up')
      # message = "You or your spouse have already signed up for one or both of you, please delete and re-sign up if you'd like to make a change."
      message = "You have already signed up, please delete and re-sign up if you'd like to change your comments."

      alert(message)
      return

    signup_name = user['signup_name'] #f"{user['first_name']} {user['last_name'][0]}"
      
      
    signup_message = f"Enter comments here."    
    t = TextBox(placeholder=signup_message, type="text")
#     t = TextBox(placeholder=signup_message, type="text")
    title = f"{signup_name}, if you have any comments please enter them below, then Save."
#     result = alert(title=title, content=t,
   
    result = alert(title=title, content=t,
#                title="Activity Sign-Up",
             large=True,
             buttons=[("Cancel", False), ("Save", True)])
              
    if result:
      print(f"The user chose {signup_name}")
      comment = t.text
      date_time = self.item['act_date_time']
      message = anvil.server.call('add_participant', self.item, user, signup_name, spouse, date_time, comment)  
      alert(message)

    navigation.go_home()
#     self.refresh_data_bindings()
#     self.update_panel()

# Work On - Edit Activity, Delete Activity
  def link_edit_click(self, **event_args):
    activity_dict = dict(list(self.item))
    user = navigation.the_user()
    print('GolfTemplate link_edit_click called')
    print('activity dict:')
    print(activity_dict)
    
    if alert(content=ActivitiesEditTemplate(item=activity_dict), title="Update Activity Info",
             large=True, buttons=[("Save", True), ("Cancel", False)]):      
      anvil.server.call('edit_activity', self.item, activity_dict)
      self.parent.raise_event('x-edit-activity', activity=activity_dict)
      
#       anvil.server.call('update_score', self.item, activity_copy)
    message = f"Update recorded, thanks {user['first_name']}!"
    n = Notification(message)
    n.show()
    self.refresh_data_bindings()
    self.update_panel()    

  def link_delete_click(self, **event_args):
    print('GolfTemplate link_delete_click called')
    user = navigation.the_user()
    if confirm(f"Are you sure you want to delete this tee time, {user['first_name']}, it will also delete the sign-ups (if any) for this tee time."):
#       self.parent.raise_event('x-delete-activity', activity=self.item)
      self.delete_activity(self.item)
    navigation.go_home()

  def delete_activity(self, activity, **event_args):
    print('GolfSignupComponent delete_activity called')
    anvil.server.call('delete_activity', activity)
    navigation.go_home()
  