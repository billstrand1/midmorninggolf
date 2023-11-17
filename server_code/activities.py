import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from datetime import date
import pandas as pd
# from . import Globals

'''
FOR ACTIVITIES EDIT:

1.  Done: NEED TO REQUIRE LOG-IN
2.  DONE: IF USER or spouse IS OWNER OF ACTIVITY, LET THEM EDIT/DELETE
3.  DONE: IF USER IF ADMIN, LET THEM EDIT/DELETE

'''
#------------------Return groups for Golf signup:
@anvil.server.callable
def all_groups():
  return app_tables.users.search(
    tables.order_by('full_name', ascending=True), ladies_golf=True)

@anvil.server.callable
def group_3(): 
  return  app_tables.users.search(
    tables.order_by('full_name', ascending=True), ladies_golf_team=3)


#-----------------ACTIVITIES FUNCTIONS (PARTICIPATION BELOW)-----------------
# @anvil.server.callable
def update_activity(activity, activity_dict):
  activity.update(**activity_dict)

@anvil.server.callable
def get_all_future_activities_saturday():
  print('activities: get_all_future_activities_saturday called')
#   print(f"week_day = {week_day}")
  all_future_activities_saturday = app_tables.activities.search(
    tables.order_by("act_date_time", ascending=True), act_date_time=q.greater_than_or_equal_to(date.today()), week_day=5)  
  return all_future_activities_saturday

@anvil.server.callable
def get_all_future_activities(): 
  future_golf = app_tables.activities.search(
    tables.order_by("act_date_time", ascending=True),
    golf=True, act_date_time=q.greater_than_or_equal_to(date.today()))
  return future_golf

  
#-------------------------------TESTING---------------------------------------
@anvil.server.callable
def get_all_future_activities_weekday(): 
  print('activities: get_all_future_activities_weekday called')
  all_future_activities_weekday = app_tables.activities.search(
    tables.order_by("act_date_time", ascending=True), act_date_time=q.greater_than_or_equal_to(date.today()), week_day=q.less_than(5))
  
  return all_future_activities_weekday
    #, (act_date_time.weekday() < 5))
  
  
@anvil.server.callable
def get_past_activities():  
  #Used to delete past activities / participants from DT
  print('activities: get_past_activities called')
  return app_tables.activities.search(
    tables.order_by("act_date_time", ascending=True), act_date_time=q.less_than(date.today()))


@anvil.server.callable
def add_activity(activity_title, activity_comments,
                 input_activity_date_picker,input_check_box_golf,
                 input_check_box_meals, input_check_box_other,
                 activity_user, course):
  print('activities: add_activity called')
  
  tee_time_info = activity_title
  
  weekday = input_activity_date_picker.weekday()
  print(f"Adding activity weekday # {weekday}")
  
  if weekday < 5 and activity_user['ladies_golf_team'] == 3:
    print('Team 3, not adding a weekday tee time')
    return 'Sorry, you can only create Saturday tee times'
  
  new_activity = app_tables.activities.add_row(activity=tee_time_info, comments=activity_comments,act_date_time=input_activity_date_picker,
                               golf=input_check_box_golf, dinner=input_check_box_meals, other=input_check_box_other,
                               owner=activity_user, week_day=weekday, course=course)
  return 'Tee time created, thanks', new_activity

@anvil.server.callable
def delete_activity(activity):
    print('delete activity called')
    participants_in_activity = get_participants_in_activity(activity)
    if len(participants_in_activity) > 0:
      print('deleting participants')
      for participant in participants_in_activity:
        if app_tables.participation.has_row(participant):
          participant.delete()
        else:
          raise Exception("Participant does not exist") 
    if app_tables.activities.has_row(activity):
      print('activities: delete_activity called')
      activity.delete()
    else:
      raise Exception("Activity does not exist")
#       activity.delete()
#     Globals.all_activities, Globals.future_golf, Globals.future_dinners, Globals.future_other = get_all_future_activities()

#billstrand1@yahoo.com
#'act_date_time': datetime.datetime(2023, 7, 17, 9, 0, tzinfo=<anvil.tz.tzoffset (-5.0 hour offset)>)  Need to get the offset fixed
@anvil.server.callable
def edit_activity(activity, activity_dict):
    if app_tables.activities.has_row(activity):
      print('activities: edit_activity called')
      activity.update(**activity_dict)  
      
      #Need to update Participation date / time also:
      print(f"Activity Updated, dict date= {activity_dict['act_date_time']}")
      new_date = activity_dict['act_date_time']
      participants_results = app_tables.participation.search(activity=activity)
      for participant in participants_results:
        print(f"Changing date for {participant['participant']['first_name']} ")
#         participant['participation_date_time'] = new_date
        participant['participation_date_time'] = activity_dict['act_date_time']
      
    else:
      raise Exception("Activity does not exist")
#     Globals.all_activities, Globals.future_golf, Globals.future_dinners, Globals.future_other = get_all_future_activities()

#------------------------ACTIVITY PARTICIPANTS----------------------- 
@anvil.server.callable
def get_participants_in_activity(activity):
  participants_results = app_tables.participation.search(activity=activity)
  print(f"Number of participants = {len(participants_results)}")
  return participants_results

@anvil.server.callable
def delete_signup(participant):
#   print(f"deleting participant: {participant['participant']['couple_name']}")
  participant.delete()
  
@anvil.server.callable  
def add_participant(activity, participant, sign_up_name, spouse, date_time, comment):
  
  app_tables.participation.add_row(activity=activity, participant=participant, sign_up_name=sign_up_name, participation_date_time=date_time, comment=comment)

  if '&' in sign_up_name:
    message = f"{sign_up_name} have been signed up."
  else:
    message = f"{sign_up_name} has been signed up."
  return message



#. From HomeDetails:
@anvil.server.callable  
def get_user_or_spouse_activities_str(user, spouse): 
  #Returns 2 messages to display on the HomeDetail page
# 
#   return 'Message 1', 'Message 2'
    either_user_or_spouse_activities = app_tables.participation.search(
      tables.order_by("participation_date_time", ascending=True), 
      participant=q.any_of(user, spouse))
    if len(either_user_or_spouse_activities) > 0:
      print('either_user_or_spouse_activities > 0 in ACTIVITIES: CLIENT CODE')
      message_activities = 'You have signed up for the following Tee Times.  If you must cancel the day of golf, please text your group.'
    else:
      message_activities = 'You have not signed up for any Tee Times.'
      
    message_activities_detail = ''
    
# Need to format time, then display the activities in order of date.
# Also need to delete 'participation' before deleting 'activities'
# Also need to do FUTURE activities only.

    users_activities = []
    date_list = []
    name_list = []
    activity_list = []
    comment_list = []
    for activity in either_user_or_spouse_activities:
      #go thru participation table and pull out activities
      act_date_time = activity['activity']['act_date_time']
      #revise to just date
      act_date_time_str = act_date_time.strftime("%a %b %d '%y") + ' | '
#       act_date_time_str = act_date_time.strftime("%a %b %d '%y, %-I:%M %p") + ' | '

      activity_name = activity['activity']['course'] + ' @ ' + activity['activity']['activity'] + ' | '
      sign_up_name = activity['sign_up_name'] + ' | '
      comment = activity['comment']
#       users_activities += [act_date_time_str, activity_name, sign_up_name]
      date_list.append(act_date_time_str)
      name_list.append(sign_up_name)
      activity_list.append(activity_name)
      comment_list.append(comment)
#     print(users_activities)  
    
    activities_df = pd.DataFrame({'Name': name_list, 'Date': date_list, 'Tee Times': activity_list, 'Your Comment': comment_list})
    if len(activities_df) > 0:
      message_activities_detail = activities_df.to_string(index=False, justify='center', col_space=14)
  
    return message_activities, message_activities_detail
#     self.label_activities_detail.text = users_activities
      
    
                                   
