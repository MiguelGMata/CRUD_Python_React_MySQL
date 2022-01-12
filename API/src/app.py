from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


from config import connexion

app = Flask(__name__)

#CORS(app, resources={r"(/todo/*": {"origins": "http://localhost"}})

mysql = connexion()

#-----------------------------------GET TOUTES LES TACHES ACCUEIL-----------------------------------------------
@cross_origin
@app.route('/todo/', methods=['GET'])
def Index():
    cur = mysql.cursor()
    cur.execute("SELECT * FROM taches")
    data = cur.fetchall()
    cur.close()
    print(data)
    return jsonify(data)
    
#-----------------------------------POST UNE TACHE-----------------------------------------------
@app.route('/todo/tache', methods=['POST'])
def creer_tâches():

            if request.method == 'POST':
                nom = request.form['nom']
                description = request.form['description']
                cur = mysql.cursor()
                cur.execute('INSERT INTO taches (nom, description) VALUES (%s,%s)', (nom, description))
                mysql.commit()
                return jsonify({'mensage': 'Tâches ajoutée'})#, redirect(url_for('Index'))     
            else:
                return jsonify({'mensage': 'Erreur'})

#---------------------------------------GET TOUTES LES TACHES-------------------------------------------
@app.route('/todo/taches', methods=['GET'])
def get_tâches():
    try:
        cur =  mysql.cursor()
        cur.execute("SELECT id, nom, description FROM taches") #On execute la requete 
        data = cur.fetchall() #response de mysql
        print(data)
        taches = []
        for file in data:
            tache = {'id': file[0], 'nom': file[1], 'description': file[2]}
            taches.append(tache)
        return jsonify({'Tâches': taches, 'mensage': "Liste de tâches.", 'exito': True})#retour de JSON avec la liste
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


#-----------------------------------------GET TACHE ID-----------------------------------------
@app.route('/todo/tache/<id>', methods=['GET'])
def get_tâche_id(id):
    try:
        data = get_tâche_id(id)
        cur = mysql.cursor()
        sql = "SELECT * FROM taches WHERE id ='{0}'".format(id)
        cur.execute(sql)
        data = cur.fetchone()
        if data != None:
            tache = {'id': data[0], 'nom': data[1], 'description': data[2]}
            return jsonify({'tache': tache, 'mensage': 'Tâche trouvée'})
        else:
            return jsonify({'mensage': 'Erreur, tâche non trouvée'})
    except Exception as ex:
        return jsonify({'mensage': 'Erreur'})

#------------------------------------------DELETE TACHE----------------------------------------
@app.route('/todo/tache/<id>', methods=['DELETE'])
def delete_tache_id(id):
    cur = mysql.cursor()
    cur.execute("DELETE FROM taches WHERE id = {0}".format(id))
    mysql.commit()
    return jsonify({'mensage': 'tâche effacée'})

#-----------------------------------------UPDATE TACHE-----------------------------------------
@app.route('/todo/tache/<id>', methods=['POST'])
def update_tache_id(id):
    try:
        if request.method =='POST':
            nom = request.form['nom']
            description = request.form['description']
            cur = mysql.cursor()
            cur.execute("""
                UPDATE taches 
                SET nom = %s, 
                description = %s
                WHERE id = %s
                """, ( nom, description, id))
            mysql.commit()
            return jsonify({'mensage': 'Tâches editée'})#, redirect(url_for('Index'))   
        else:
            return jsonify({'mensage': 'Erreur, tâche non trouvée'})
    except Exception as ex:
        return jsonify({'mensage': 'Erreur'})

#----------------------------PAGE ERREUR 404------------------------------------------------------
def page_erreur(error):
    return"<h1>Erreur 404, page non trouvée.</h1>", 404

if __name__ == '__main__':
    app.register_error_handler(404, page_erreur)
    app.run(port = 3000, debug = True)
