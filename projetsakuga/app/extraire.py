import requests
from bs4 import BeautifulSoup
import mysql.connector

headers = {'User-Agent': 'Mozilla/5.0'}

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Subaru.",
        database="video"
    )

def extract_video_url(post_id):
    url = f"https://www.sakugabooru.com/post/show/{post_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        highres_link = soup.find('a', id='highres')
        if highres_link and highres_link.get('href'):
            artiste_name, anime_title = extract_artiste_and_anime_info(soup)
            return highres_link['href'], artiste_name, anime_title
    else:
        print(f"Erreur HTTP {response.status_code} pour l'URL {url}")
    return None, None, None

def extract_artiste_and_anime_info(soup):
    artiste_tag = soup.find('li', class_='tag-type-artist')
    artiste_name = artiste_tag.find_all('a')[1].text.strip() if artiste_tag else None

    anime_tag = soup.find('li', class_='tag-type-copyright')
    anime_title = anime_tag.find_all('a')[1].text.strip() if anime_tag else None

    return artiste_name, anime_title

def manage_database_entries(conn, artiste_name, anime_title, video_url):
    cursor = conn.cursor()
    # Vérifiez d'abord si l'URL de la vidéo existe déjà dans la base de données
    cursor.execute('SELECT video_id FROM videos WHERE url = %s', (video_url,))
    if cursor.fetchone():
        print(f"URL déjà existante dans la base de données : {video_url}")
    else:
        if artiste_name is not None and anime_title is not None:
            artiste_id = manage_artiste(cursor, artiste_name, conn)
            anime_id = manage_anime(cursor, anime_title, conn)
            if artiste_id and anime_id:
                cursor.execute('INSERT INTO videos (url, artiste_id, anime_id) VALUES (%s, %s, %s)', (video_url, artiste_id, anime_id))
                conn.commit()
                print(f"URL insérée dans la base de données : {video_url}")
        else:
            print("Erreur : Nom d'artiste ou titre d'anime manquant.")
    cursor.close()


def manage_artiste(cursor, artiste_name, conn):
    cursor.execute('SELECT artiste_id FROM artistes WHERE nom_principal = %s', (artiste_name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO artistes (nom_principal) VALUES (%s)', (artiste_name,))
        conn.commit()  # Commit the transaction with the connection object
        artiste_id = cursor.lastrowid
        print(f"Nouvel artiste ajouté avec l'ID {artiste_id}: {artiste_name}")
        return artiste_id
    else:
        print(f"Artiste déjà existant récupéré avec l'ID {row[0]}: {artiste_name}")
    return row[0]

def insert_source(conn, source_url):
    cursor = conn.cursor()
    cursor.execute('SELECT source_id FROM sources WHERE url = %s', (source_url,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO sources (url) VALUES (%s)', (source_url,))
        conn.commit()
        return cursor.lastrowid
    return row[0]

def link_video_to_tags_and_source(conn, video_id, tags, source_url):
    source_id = insert_source(conn, source_url)
    if source_id:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO video_sources (video_id, source_id) VALUES (%s, %s)', (video_id, source_id))
        conn.commit()

    for tag in tags:
        tag_id = insert_tag(conn, tag)
        if tag_id:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO video_tags (video_id, tag_id) VALUES (%s, %s)', (video_id, tag_id))
            conn.commit()
def insert_tag(conn, tag_name):
    cursor = conn.cursor()
    cursor.execute('SELECT tag_id FROM tags WHERE nom = %s', (tag_name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO tags (nom) VALUES (%s)', (tag_name,))
        conn.commit()
        return cursor.lastrowid
    return row[0]

def manage_anime(cursor, anime_title, conn):
    cursor.execute('SELECT anime_id FROM animes WHERE titre_principal = %s', (anime_title,))
    row = cursor.fetchone()
    if not row:
        cursor.execute('INSERT INTO animes (titre_principal) VALUES (%s)', (anime_title,))
        conn.commit()  # Commit using the connection object
        anime_id = cursor.lastrowid
        print(f"Nouvel anime ajouté avec l'ID {anime_id}: {anime_title}")
        return anime_id
    else:
        print(f"Anime déjà existant récupéré avec l'ID {row[0]}: {anime_title}")
    return row[0]
def main():
    with connect_db() as conn:
        for post_id in range(605,606):
            video_url, artiste_name, anime_title = extract_video_url(post_id)
            if video_url:
                manage_database_entries(conn, artiste_name, anime_title, video_url)

if __name__ == "__main__":
    main()
