from natsugash import app
import os

# app.run(host='127.0.0.1', port=8080, debug=True)
port = int(os.environ.get('PORT'))
print(os.environ.get('PORT'))
app.run(port=port)
