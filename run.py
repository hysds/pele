import os
from pele import app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'production')
    app.run(host="0.0.0.0", port=8878, debug=True)
