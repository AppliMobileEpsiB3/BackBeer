from flask import Flask
from Api.BeerApi import beer_api
from Api.SearchApi import search_api
from Api.FavoriteApi import favorite_api

app=Flask(__name__)

app.register_blueprint(beer_api)
app.register_blueprint(search_api)
app.register_blueprint(favorite_api)

if __name__ =='__main__' :
    app.run()