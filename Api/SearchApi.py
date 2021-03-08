from flask import Blueprint,request,jsonify
import DatabaseFiles.connection as connection

search_api = Blueprint('search_api',__name__)

@search_api.route('/search/<string:name>',methods=['GET'])
def search(name):
    conn = connection.db_connection()
    cursor= conn.cursor()
    if request.method=='GET' :
        cursor.execute("SELECT * FROM beer where name = ?",(str(name),))
        rows = cursor.fetchall()
        if(len(rows)>0) :
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
        else :
            cursor.close()
            conn.close()
            return "Something wrong",404