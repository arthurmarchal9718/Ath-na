from flask import Flask, request, jsonify, send_from_directory
import os

# Création de l'application Flask
app = Flask(__name__)

# Dossier pour les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_media():
    if 'media' not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    media = request.files['media']
    if media:
        allowed_extensions = {'mp4', 'webm', 'ogg', 'jpeg', 'png', 'gif'}
        ext = media.filename.split('.')[-1].lower()

        if ext not in allowed_extensions:
            return jsonify({"error": "Type de fichier non autorisé"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, media.filename)
        media.save(filepath)
        return jsonify({"message": "Fichier téléchargé avec succès!", "filename": media.filename}), 200

    return jsonify({"error": "Échec du téléchargement du fichier"}), 500

@app.route('/media/<filename>')
def get_media(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/media')
def list_media():
    files = os.listdir(UPLOAD_FOLDER)
    media_list = []
    for file in files:
        ext = file.split('.')[-1].lower()
        if ext in ['mp4', 'webm', 'ogg', 'jpeg', 'png', 'gif']:
            media_list.append({
                "filename": file,
                "type": "video" if ext in ['mp4', 'webm', 'ogg'] else "image"
            })
    return jsonify(media_list)

if __name__ == '__main__':
    app.run(debug=True)
