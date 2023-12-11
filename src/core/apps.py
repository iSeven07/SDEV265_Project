# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#          apps.py        #
# = = = = = = = = = = = = #

# This file is used by Django to configure the application
# and define various application-specific settings. 

from django.apps import AppConfig

# This is where we have configured core.signals which assists in creating
# user profiles when new users are created.
class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import core.signals 
