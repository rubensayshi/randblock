import logging, sys
from randblock.application import create_app

# ensure all error traces are send to the logs
logging.basicConfig(stream=sys.stderr)

app = create_app()

if __name__ == '__main__':
    print "run?"
    app.run('0.0.0.0', 5000)