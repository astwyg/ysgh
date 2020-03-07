import os
import sys
import site

# add python site packages, you can use virtualenvs also
site.addsitedir("C:\\workspace\\ysgh\\env\\Lib\\site-packages")

# Add the app's directory to the PYTHONPATH 
sys.path.append('C:\\workspace\\ysgh') 
sys.path.append('C:\\workspace\\ysgh\\webserver')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'webserver.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")  

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()