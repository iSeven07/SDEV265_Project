# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#      admin.py           #
# = = = = = = = = = = = = #

# This is where models are registered for use in the admin panel.
# When a model is registered in the admin panel, you can modify the
# database items from there.


from django.contrib import admin
from .models import Recipe, Profile, Ingredient

# Recipe Builder Models
admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(Ingredient)
