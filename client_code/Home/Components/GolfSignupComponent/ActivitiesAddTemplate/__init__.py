from ._anvil_designer import ActivitiesAddTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import navigation
from ..... import Globals
# from ..GolfTemplate import GolfTemplate
from ..AddOtherPlayers import AddOtherPlayers

from datetime import datetime
from datetime import date

class ActivitiesAddTemplate(ActivitiesAddTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def button_cancel_click(self, **event_args):
    navigation.go_home()


from datetime import datetime
from datetime import date
'''
Problem with New activity not showing up in summary, need to Update Globals somehow.
Also - check for 0:00 Time as an error
Also - check for more than one Category selected

'''

class ActivitiesAddTemplate(ActivitiesAddTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.activity_user = navigation.the_user()

    self.activity_title = ''
    self.activity_comments = ''
    self.activity_date_picker = None
    self.check_box_golf = None
    self.check_box_meals = None
    self.check_box_other = None
    today = date.today()
    self.input_activity_date_picker.min_date = today
    self.drop_down_course.selected_value = None
  
#added function
  def link_signup_click(self, activity,**event_args):
    print('self.link_signup_click called')
    #add participant to sign-up list
    user = navigation.the_user()
  
    # if user['spouse']:
    #   spouse = user['spouse']
    spouse = None  

#  FROM ACTIVITY SERVER CODE
    either_user_or_spouse = app_tables.participation.search(activity=activity, participant=q.any_of(user, spouse))
    if len(either_user_or_spouse) > 0:
      print('either_user_or_spouse > 0 ACTIVITY CLIENT')
      if user['spouse'] == None:
        print('Single person already signed up')
        message = "You have already signed up for this Tee Time." 
        alert(message)
        return  
      
      print('Couple already signed up')
      message = "You or your spouse have already signed up for one or both of you, please delete and re-sign up if you'd like to make a change."
      alert(message)
      return

    sign_up_name = f"{user['first_name']} {user['last_name'][0]}"     
      
    signup_message = f"Enter comments here."    
    t = TextBox(placeholder=signup_message, type="text")
    title = f"{sign_up_name}, if you have any comments please enter them below, then Save."
    result = alert(title=title, content=t,
#                title="Activity Sign-Up",
             large=True,
             buttons=[("Cancel", False), ("Save", True)])
    
    if result:  #changed self.item to activity:      
      print(f"The user chose {sign_up_name}")
      comment = t.text
      date_time = activity['act_date_time']
      message = anvil.server.call('add_participant', activity, user, sign_up_name, spouse, date_time, comment)  
      alert(message)

    #To add another player from AddTeeTime, after creator signs up...., later...
    #------------------Code from Ringerbook:
    
    '''
L A T E R:
    
    c = confirm("Would you like to sign up another player?")
    if c:
      add_form = AddOtherPlayers()
      
      date_of_golf = activity['act_date_time'].strftime("%a %b %d '%y")
      print(f"signing up other for {date_of_golf} tee time.")
      title = f"Sign up another player for the {date_of_golf} {activity['activity']} {activity['course']} tee time"
      result = alert(title=title, content=add_form,
#                title="Activity Sign-Up",
             large=True,
             buttons=[("Cancel", False), ("Save", True)])
#       pass
    
'''   
    navigation.go_home()
    
  def button_add_activity_click(self, **event_args):
    self.label_error_msg.visible = False
    self.input_check_box_golf.checked = True
    
    error = self.sync_data()
    if error:
      self.label_error_msg.text = error
      self.label_error_msg.visible = True      
      return

#     print(f" ActivitiesAdd: time = {self.input_activity_date_picker.date.time()}")
    
    message, new_activity = anvil.server.call('add_activity', self.input_activity_title.text, 
                             self.input_activity_comments.text,
                             self.input_activity_date_picker.date,
                             self.input_check_box_golf.checked,
                             self.input_check_box_meals.checked, 
                             self.input_check_box_other.checked,
                             self.activity_user,
                              self.drop_down_course.selected_value)
    alert(content=message)


#TESTING:
    c = confirm("Would you like to sign up for this tee time?")
    if c:
      print('executing link_signup_click from GolfTemplate')
      self.link_signup_click(new_activity)
      
    navigation.go_home()
  
  def sync_data(self):
    if not self.input_activity_date_picker.date:
      return "Please select a Date"

    if not self.drop_down_course.selected_value:
      return "Please select the Course"
    
    if not self.input_activity_title.text:
      return "Please enter the Tee Time"
 
    return None
 

  def button_cancel_click(self, **event_args):
    navigation.go_home()

