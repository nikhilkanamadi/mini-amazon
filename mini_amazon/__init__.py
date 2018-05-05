from flask import Flask

app = Flask('mini-amazon',
            static_folder='./mini_amazon/static',
            static_url_path='',
            template_folder='./mini_amazon/templates')

from mini_amazon import views, api
