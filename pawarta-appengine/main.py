import os
from pathlib import Path
from flask import Flask, abort, render_template_string, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATOR_DIR = os.path.join(BASE_DIR, 'generator')

ERROR_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body class="d-flex flex-column justify-content-center align-items-center min-vh-100 bg-light">
    <div class="text-center">
        <h1 class="display-1 fw-bold text-danger">{{ code }}</h1>
        <h2 class="mb-4">{{ message }}</h2>
        <p class="text-muted mb-4">{{ details }}</p>
        <a href="/" class="btn btn-primary btn-lg">Kembali ke Halaman Utama</a>
    </div>
</body>
</html>
"""


def safe_file_path(rel_path: str) -> str | None:
    """Return rel_path if it stays inside generator dir."""
    generator_root = os.path.abspath(GENERATOR_DIR)
    candidate = os.path.abspath(os.path.join(generator_root, rel_path))
    if os.path.commonpath([generator_root, candidate]) != generator_root:
        return None
    return rel_path


def file_exists(rel_path: str) -> bool:
    safe_rel = safe_file_path(rel_path)
    if not safe_rel:
        return False
    full_path = os.path.join(GENERATOR_DIR, safe_rel)
    return os.path.isfile(full_path)


def send_generated_file(rel_path: str):
    safe_rel = safe_file_path(rel_path)
    if not safe_rel or not file_exists(safe_rel):
        abort(404)
    return send_from_directory(GENERATOR_DIR, safe_rel)


@app.route('/')
@app.route('/index.html')
def index():
    if file_exists('index.html'):
        return send_generated_file('index.html')
    return (
        "Selamat Datang di PAWARTA. Silakan jalankan script generator terlebih dahulu.",
        202,
    )


@app.route('/<category>/index.html')
@app.route('/<category>/')
def category_index(category):
    path = f"{category}/index.html"
    if file_exists(path):
        return send_generated_file(path)
    abort(404)


@app.route('/<category>/artikel<int:num>.html')
def category_article(category, num):
    path = f"{category}/artikel{num}.html"
    if file_exists(path):
        return send_generated_file(path)
    abort(404)


@app.route('/<category>/sitemap.html')
def category_sitemap_html(category):
    path = f"{category}/sitemap.html"
    if file_exists(path):
        return send_generated_file(path)
    abort(404)


@app.route('/<category>/sitemap.xml')
def category_sitemap_xml(category):
    path = f"{category}/sitemap.xml"
    if file_exists(path):
        return send_generated_file(path), 200, {'Content-Type': 'application/xml'}
    abort(404)


@app.route('/<category>/sitemap.txt')
def category_sitemap_txt(category):
    path = f"{category}/sitemap.txt"
    if file_exists(path):
        return send_generated_file(path), 200, {'Content-Type': 'text/plain'}
    abort(404)


@app.route('/<filename>')
def serve_root_files(filename):
    if file_exists(filename):
        return send_generated_file(filename)

    if filename == 'robots.txt' and file_exists('robots.txt'):
        return send_generated_file('robots.txt'), 200, {'Content-Type': 'text/plain'}

    if filename == 'sitemap.xml' and file_exists('sitemap.xml'):
        return send_generated_file('sitemap.xml'), 200, {'Content-Type': 'application/xml'}

    if filename == 'search.json' and file_exists('search.json'):
        return send_generated_file('search.json'), 200, {'Content-Type': 'application/json'}

    if filename.endswith('.css'):
        asset = f'assets/{filename}'
        if file_exists(asset):
            return send_generated_file(asset), 200, {'Content-Type': 'text/css'}

    if filename.endswith('.js'):
        asset = f'assets/{filename}'
        if file_exists(asset):
            return send_generated_file(asset), 200, {'Content-Type': 'application/javascript'}

    abort(404)


@app.route('/assets/<path:filepath>')
def serve_assets(filepath):
    asset = f'assets/{filepath}'
    if file_exists(asset):
        return send_generated_file(asset)
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template_string(
        ERROR_HTML,
        code=404,
        title='Halaman Tidak Ditemukan',
        message='Halaman yang Anda cari tidak ditemukan',
        details='Folder generator mungkin masih kosong. Jalankan generate_blog.py terlebih dahulu.',
    ), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template_string(
        ERROR_HTML,
        code=500,
        title='Error Server',
        message='Terjadi kesalahan pada server',
        details=str(error),
    ), 500


if __name__ == '__main__':
    print(f"Generator directory: {GENERATOR_DIR}")
    print(f"Generator exists: {os.path.exists(GENERATOR_DIR)}")
    app.run(host='127.0.0.1', port=8080, debug=False)
