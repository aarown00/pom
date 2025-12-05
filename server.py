import os
from waitress import serve
from mabuhaypowers_pom.wsgi import application  

port = int(os.environ.get("PORT", 8080)) 

serve(application, host="0.0.0.0", port=port)
