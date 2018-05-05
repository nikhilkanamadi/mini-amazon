from mini_amazon import app
import json

if __name__ == '__main__':
    config = json.load(open("./config.json", "r"))
    app.run(host=config["host"], port=config["port"], debug=True, threaded=True)
