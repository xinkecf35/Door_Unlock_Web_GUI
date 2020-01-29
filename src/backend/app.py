import sys

import yaml

from door_api import create_app

if __name__ == '__main__':
    # load config from yaml file
    try:
        with open('config.yaml', 'r') as configFile:
            config = yaml.safe_load(configFile)
    except OSError:
        print('Missing config file for flask app')
        # exit with no such file
        sys.exit(-2)
    app = create_app(config)
    app.run()
