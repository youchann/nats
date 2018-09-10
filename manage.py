from natsugash import app
import os

# app.run(host='127.0.0.1', port=8080, debug=True)
port = int(os.environ.get('PORT', 5000))
app.run(port=port)
