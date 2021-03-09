from flask import Blueprint,request,jsonify
import DatabaseFiles.connection as connection
from VerifToken import verifyToken

beer_api = Blueprint('beer_api',__name__)

@beer_api.route('/beers', methods=['GET','POST'])
def beers() :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor = conn.cursor()
        if request.method=='GET':
            cursor.execute("SELECT * FROM beer")
            beers = [
                dict(id=row[0],name = row[1], percentageAlcohol=row[2], category=row[3])
                for row in cursor.fetchall()
            ]
            if beers is not None :
                cursor.close()
                conn.close()
                return jsonify(beers)
        if request.method=='POST':
            data = request.get_json()
            new_name = data['name']
            new_percentageAlcohol = data['percentageAlcohol']
            new_category = data['category']
            sql = """INSERT INTO beer (name,percentageAlcohol,category) VALUES (?,?,?) """
            cursor.execute(sql,(new_name,new_percentageAlcohol,new_category))
            conn.commit()
            cursor.close()
            conn.close()
            return f"Beer with the id {cursor.lastrowid} created successful"
    else :
        return "Your token is expired"


@beer_api.route('/beer/<int:id>',methods=['GET','PUT','DELETE'])
def single_beer(id):
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor = conn.cursor()
        beer = None
        if request.method == 'GET':
            cursor.execute("SELECT * FROM beer WHERE id =?",(int(id),))
            rows = cursor.fetchall()
            for r in rows :
                beer = r
            if beer is not None :
                cursor.close()
                conn.close()
                return jsonify(beer),200
            else :
                cursor.close()
                conn.close()
                return "Something wrong",404
        if request.method == 'PUT' :
            sql = """UPDATE beer
                    SET name = ?,
                        percentageAlcohol=?,
                        category=?
                    WHERE id=? """
            data = request.get_json()
            name= data["name"]
            percentageAlcohol = data["percentageAlcohol"]
            category = data["category"]
            updated_beer = {
                'id':id,
                'name' : name,
                'percentageAlcohol' : percentageAlcohol,
                'category' : category
            }
            cursor.execute(sql,(name,percentageAlcohol,category,int(id)))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(updated_beer)

        if request.method == 'DELETE':
            sql = """ DELETE FROM beer WHERE id=? """
            cursor.execute(sql,(int(id),))
            conn.commit()
            cursor.close()
            conn.close()
            return "Beer with the id {} has been deleted".format(id),200
    else :
        return "Your token is expired"