from app import app

@app.route('/')
def hompage():
   return 'Home page'
