import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#---------TO BE COMMENTED OUT BEFORE CLONING, called from Home

@anvil.server.callable
def force_debug_login():
  anvil.users.force_login(app_tables.users.get(email="jacklcarroll@verizon.net"))
  
# billstrand1@yahoo.com
#  reid.baker@sbcglobal.net
#        wbarnard96@aol.com
#        rbaumgarth@aol.com
#        rick@rickbesse.com
#  frank.broyles@utexas.edu
#  jacklcarroll@verizon.net
# vanhorn_davis@verizon.net
#   kent.fannon@verizon.net
#         cmfitzg@gmail.com
#    rcraighumphrey@msn.com
#   mkilanowski@verizon.net
#     billstrand1@yahoo.com
#    jimwickham@verizon.net
# dougwilliams9@hotmail.com