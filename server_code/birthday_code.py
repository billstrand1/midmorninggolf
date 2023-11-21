import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from anvil import *

'''
NOT MAKING GENERIC JUST YET, JUST SEE IF THE COMPONENT CAN BE USED
Requires the Users table to have the following fields:
birth_month - number
Name - text
birth_date - number

Test if no 'Birthday' field, just do date printout.

'''
@anvil.server.callable
def get_this_month_birthdays():
    print('get_birthdays_called')
    now_time = datetime.now()
    month = now_time.month
    month_text = now_time.strftime("%b")
    current_day = now_time.day
    year = now_time.year
#     return app_tables.users.search(tables.order_by("birth_date", ascending=True), birth_month=month)
    birthday_list = app_tables.users.search(tables.order_by("birth_date", ascending=True), birth_month=month)
    birthday_text = ''

    if birthday_list:
        birthday_text = 'Birthdays this month: \n'
        for player in birthday_list:
            if player['enabled']:               
                # print(f"{player['Name']}: {player['Birthday']}")
                age = year - player['Birthday'].year
                if current_day > player['Birthday'].day:
                  verb = 'turned'
                else: verb = 'will be'
                # print(f"{player['Name']} will be {age} on {month_text} {player['Birthday'].day}")
                birthday_text += f"{player['Name']} {verb} {age} on {month_text} {player['Birthday'].day}\n"

    print(birthday_text)
    return birthday_text
