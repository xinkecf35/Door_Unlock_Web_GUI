from door_api import create_app
import yaml


if __name__ == '__main__':
    # load config from yaml file
    with open('config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)
    print(type(config))
    app = create_app(config)
    app.run()
