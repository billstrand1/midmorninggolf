import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
# from datetime import datetime
# from datetime import date

#---------CONTACTS--------------------------------  
@anvil.server.callable  
def get_email_list():
  all_users = app_tables.users.search(tables.order_by("last_name", ascending=True), enabled=True)
  email_list = []
  for user in all_users:
    email_list.append(user['email'])
  email_df = pd.DataFrame(email_list)
  email_str = email_df.to_string(index=False, header=False)  #header=False removes the lead '0'
  return email_str

@anvil.server.callable
def get_directory():  #gets all contacts
  all_players = app_tables.users.search(
    tables.order_by("last_name", ascending=True), enabled=True)

#   for player in all_players:
#     if player['ladies_golf_team'] == 2:
#       print (player['full_name'])
  return all_players