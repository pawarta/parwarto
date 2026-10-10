import os
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

# Mengatur agar folder utama pencarian HTML berada di folder generator tempat berkas dibuat
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATOR_DIR = os.path.join(BASE_DIR, 'generator')

# 1. Rute untuk Halaman Utama (index.html)
@app.route('/')
@app.route('/index.html')
def index():
    if os.path.exists(os.path.join(GENERATOR_DIR, 'index.html')):
        return send_from_directory(GENERATOR_DIR, 'index.html')
    return "Selamat Datang di PAWARTA. Silakan jalankan script generator terlebih dahulu.", 200

# 2. Rute otomatis untuk membaca artikel berdasarkan kategori
# Contoh akses: ://pawarta.appspot.com
@app.route('/<category>/<filename>')
def serve_articles(category, filename):
    category_path = os.path.join(GENERATOR_DIR, category)
    
    # Memastikan file target benar-benar ada di dalam folder kategori
    if os.path.exists(os.path.join(category_path, filename)):
        return send_from_directory(category_path, filename)
    else:
        abort(404)

# 3. Rute darurat jika ada pemanggilan file root asset seperti pawarta.ico atau contact.html
@app.route('/<filename>')
def serve_root_files(filename):
    if os.path.exists(os.path.join(GENERATOR_DIR, filename)):
        return send_from_directory(GENERATOR_DIR, filename)
    abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
