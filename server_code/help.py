import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime


@anvil.server.callable
def add_comment(name, email, comments):
  print(f"Name: {name}, email: {email}, comments: {comments}")
  app_tables.comments.add_row(
    name=name, 
    email=email, 
    comments=comments, 
    created=datetime.now()
  )
  emails = ['billstrand1@yahoo.com', 'billstrand1@gmail.com', 'bill.strand@live.com']
  # Send yourself an email each time feedback is submitted
#   anvil.email.send(to="billstrand1@yahoo.com", # Change this to your email address!
  anvil.email.send(to=emails, # Change this to your email address!
                   subject=f"Question from {name}",
                   text=f""" Question from:  \n\n Name: {name}\n Email address: {email} \nComments: {comments} """)

  