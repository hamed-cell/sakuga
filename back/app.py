from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  # Importez le module CORS
from flask import request



app = Flask(__name__)
CORS(app)
# Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Subaru.'  # Remplacez par votre mot de passe
app.config['MYSQL_DB'] = 'video'

mysql = MySQL(app)

@app.route('/get_videos')
def get_videos():
    page = request.args.get('page', default=1, type=int)
    per_page = 10  # Nombre de vidéos par page
    offset = (page - 1) * per_page  # Calcul du décalage

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videos LIMIT %s, %s", (offset, per_page))
    videos = cur.fetchall()
    cur.close()

    return jsonify(videos)

@app.route('/get_video_details')
def get_video_details():
    video_id = request.args.get('id')  # Récupération de l'ID de la vidéo depuis les paramètres de requête
    cur = mysql.connection.cursor()
    
    # Requête SQL avec jointure pour récupérer les détails de la vidéo, de l'artiste, et de l'anime
    query = """
    SELECT v.video_id, v.url, a.nom as artiste_nom, an.titre as anime_titre, an.description as anime_description
    FROM videos v
    JOIN artistes a ON v.artiste_id = a.artiste_id
    JOIN animes an ON v.anime_id = an.anime_id
    WHERE v.video_id = %s;
    """
    cur.execute(query, (video_id,))
    video_details = cur.fetchone()
    cur.close()
    
    if video_details:
        # Convertir les détails de la vidéo en un dictionnaire (si nécessaire) et les retourner
        return jsonify({
            'title': video_details[3],  # Titre de l'anime
            'video_url': video_details[1],  # URL de la vidéo
            'artist': video_details[2],  # Nom de l'artiste
            'anime': video_details[3],  # Titre de l'anime
            'description': video_details[4]  # Description de l'anime
        })
    else:
        # Retourner une réponse d'erreur si aucune vidéo n'est trouvée
        return 'Video not found', 404



if __name__ == '__main__':
    app.run(debug=True)