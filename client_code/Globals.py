import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users


print('running Globals....')
# print('nothing to do in Globals')
# all_future_activities, future_golf, future_dinners, future_other = anvil.server.call('get_all_future_activities')
print('globals checking for past activities')
past_activities = anvil.server.call('get_past_activities')
print(f"globals, past_activities size = {len(past_activities)}")
if len(past_activities) > 0:
  for activity in past_activities:
    anvil.server.call('delete_activity', activity)
# all_past_activities = anvil.server.call('get_past_activities')

'''
Working on Development version.

.strftime("%a %b %d '%y")  #day, month, day, 'year


.strftime("%a %b %d '%y, %I:%M %p")  adds time am/pm
.strftime("%a %b %d '%y, %-I:%M %p")  removes leading zero on Hours


'''

'''
Need to filter by Team #:

self.drop_down_names.items = [(r["full_name"],r) for r in app_tables.users.search(tables.order_by('full_name', ascending=True))]   


   
#     if user['ladies_golf_team'] == 3:
#       print(f" Team 3") 
#       saturday_only_activities = anvil.server.call('get_all_future_activities_saturday')
#       self.repeating_panel_activites.items = saturday_only_activities
#     else:
#       print('Team 1 or 2')      
#       future_golf = anvil.server.call('get_all_future_activities')
#       self.repeating_panel_activites.items = future_golf      
    #Old: 
#     if user['ladies_golf_team'] == 1:
#       print(f" Team 1")      
# #       Globals.future_golf = anvil.server.call('get_all_future_activities')
# #       self.repeating_panel_activites.items = Globals.future_golf 
#       future_golf = anvil.server.call('get_all_future_activities')
#       self.repeating_panel_activites.items = future_golf 

#     else:
#       print('Team 2')
#       weekday_only_activities = anvil.server.call('get_all_future_activities_weekday')
#       self.repeating_panel_activites.items = weekday_only_activities     


'''