from flask import Flask
from ApiFiles.BeerApi import beer_api
from ApiFiles.SearchApi import search_api
from ApiFiles.FavoriteApi import favorite_api

app=Flask(__name__)

app.register_blueprint(beer_api)
app.register_blueprint(search_api)
app.register_blueprint(favorite_api)

if __name__ =='__main__' :
    app.run()