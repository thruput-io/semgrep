from flask import Flask

app = Flask(__name__)

# ruleid: python-flask-debug-true
app.run(host="0.0.0.0", port=5000, debug=True)

# ruleid: python-flask-debug-true
app.config['DEBUG'] = True

# ruleid: python-flask-debug-true
app.debug = True

# ok: python-flask-debug-true
app.run(host="0.0.0.0", port=5000, debug=False)

# ok: python-flask-debug-true
app.run(host="0.0.0.0", port=5000)
