from flask import Blueprint,request,jsonify
import DatabaseFiles.connection as connection
from VerifToken import verifyToken


favorite_api = Blueprint('favorite_api',__name__)


@favorite_api.route('/favorite/<int:user_id>',methods=['GET'])
def beer_by_user(user_id) :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='GET' :
            cursor.execute("SELECT * FROM beer WHERE id in (SELECT beer_id from beerlist where user_id=?)",(str(user_id),))
            beers = [
                dict(id=row[0],name = row[1], percentageAlcohol=row[2], category=row[3])
                for row in cursor.fetchall()
            ]
            cursor.close()
            conn.close()
            return jsonify(beers)
    else :
        return "Your token is expired"

@favorite_api.route('/favorite',methods=['POST'])
def favorite():
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='POST' :
            data = request.get_json()
            beer_id=data['beer_id']
            user_id = data['user_id']
            sqllist = """INSERT INTO beerlist (user_id,beer_id) VALUES (?,?) """
            cursor.execute(sqllist,(user_id,beer_id))
            conn.commit()
            cursor.close()
            conn.close()
            return f"Beer {beer_id} add to your favlist"
    else :
        return "Your token is expired"

@favorite_api.route('/favorite/<int:beer_id>/<int:user_id>',methods=['DELETE'])
def remove_from_favorite(beer_id,user_id):
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='DELETE' :
            sqllist = """DELETE FROM beerlist where user_id = ? and beer_id=? """
            cursor.execute(sqllist,(int(user_id),int(beer_id)))
            conn.commit()
            cursor.close()
            conn.close()
            return f"Beer {beer_id} remove from your favlist"
    else :
        return "Your token is expired"