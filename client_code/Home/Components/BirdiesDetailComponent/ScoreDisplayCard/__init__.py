from ._anvil_designer import ScoreDisplayCardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ScoreDisplayCard(ScoreDisplayCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def edit_score_click(self, **event_args):
    score_copy = dict(list(self.item))
    if alert(content=ScoreEditCard(item=score_copy), title="Update Score Info",
             large=True, buttons=[("Save", True), ("Cancel", False)]):
      
      #validation:
      if score_copy['birdies'] == None:
        print('birdies = None')
        score_copy['birdies'] = 0

      if score_copy['skins'] == None:
        print('skins = None')
        score_copy['skins'] = 0

      anvil.server.call('update_score', self.item, score_copy)
      message = f"Update recorded, thanks !" #{current_user['first_name']}!"
      n = Notification(message)
      n.show()
       # Refresh articles to show the changes on the Homepage
      self.refresh_data_bindings()
      self.parent.raise_event('x-update-scores')
      self.parent.raise_event('x-update-labels')
    # Any code you write here will run when the form opens.

  def delete_score_button_click(self, **event_args):
       # Get the user to confirm if they wish to delete the article
    # If they confirm, raise the 'x-delete-article' event on self.parent (which is the articles_panel on our Homepage)
    if confirm(f"Are you sure you want to delete this entry, {self.item['player']['first_name']} ?"):
      self.parent.raise_event('x-delete-score', score=self.item)






