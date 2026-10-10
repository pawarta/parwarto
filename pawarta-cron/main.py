import functions_framework
import random
from google.cloud import storage

# Kategori dan Gambar dari skrip asli Anda
CATEGORIES = ["market", "finance", "macro", "culture", "ai", "teknologi", "sejarah"] # potong pendek untuk contoh
COMMON_IMAGES = [
    "https://github.io",
    "https://github.io",
    "https://github.io"
]

# Ganti dengan nama Bucket Cloud Storage yang Anda buat di GCP
BUCKET_NAME = "nama-bucket-pawarta-anda" 

def generate_html_content(category, file_num):
    img_url = random.choice(COMMON_IMAGES)
    cat_upper = category.upper()
    
    # Potongan kode HTML template Anda
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>PAWARTA - {cat_upper} - Artikel {file_num}</title>
    <!-- Favicon & Icons -->
    <link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
    <link rel="shortcut icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
    <link rel="icon" href="https://pawarta.github.io/pawarta.jpg" type="image/x-icon">
    <link rel="shortcut icon" href="https://pawarta.github.io/pawarta.png" type="image/x-icon">

    <!-- Canonical & Hreflang Links -->
    <link rel="canonical" href="https://pawarta.github.io/">
    <link rel="alternate" href="https://pawarta.github.io/en-us/" hreflang="en-us">
    <link rel="alternate" href="https://pawarta.github.io/en/" hreflang="en">
    <link rel="alternate" href="https://pawarta.github.io/es/" hreflang="es">
    <link rel="alternate" href="https://pawarta.github.io/" hreflang="x-default">
    <link rel="alternate" hreflang="fr" href="https://pawarta.github.io/fr/">
    <link rel="alternate" hreflang="de" href="https://pawarta.github.io/de/">
    <link rel="alternate" hreflang="th" href="https://pawarta.github.io/th/">
    <link rel="alternate" hreflang="id" href="https://pawarta.github.io/id/">

    <!-- Stylesheets (Bootstrap 5, Icons, Animate.css) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

    <!-- AMP Auto Ads -->
    <script async custom-element="amp-auto-ads" src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js"></script>

    <!-- Google AdSense -->
    <script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9308517202792186"></script>

    <!-- Google tag (gtag.js) - GA4 ID: G-GN5PGKKM3T -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GN5PGKKM3T"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-GN5PGKKM3T');
    </script>



    <!-- Custom CSS -->
    <style>
        :root {
            --primary-jawa: #2c1d0c;
            --accent-gold: #d4af37;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #fcf8f2;
            color: #333;
            overflow-x: hidden;
        }

        @keyframes rainbowGlow {
            0% { color: #ff0000; }
            14% { color: #ff7f00; }
            28% { color: #ffff00; }
            42% { color: #00ff00; }
            57% { color: #0000ff; }
            71% { color: #4b0082; }
            85% { color: #9400d3; }
            100% { color: #ff0000; }
        }

        @keyframes rainbowBg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .rainbow-text {
            animation: rainbowGlow 6s infinite linear;
            font-weight: bold;
        }

        .rainbow-badge {
            background: linear-gradient(270deg, #ff416c, #ff4b2b, #f12711, #f5af19, #00b09b, #96c93d);
            background-size: 400% 400%;
            animation: rainbowBg 10s ease infinite;
            color: white;
        }

        .navbar-brand img {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            border: 2px solid var(--accent-gold);
        }

        .carousel-item {
            height: 550px;
            background-size: cover;
            background-position: center;
            position: relative;
        }

        .carousel-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.55);
        }

        .carousel-caption {
            bottom: 20%;
        }

        .honocoroko-title {
            font-size: 2.5rem;
            letter-spacing: 2px;
            color: var(--accent-gold);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }

        footer {
            background-color: var(--primary-jawa);
            color: #d1c7bd;
        }

        footer a {
            color: #d4af37;
            text-decoration: none;
        }

        footer a:hover {
            color: #fff;
            text-decoration: underline;
        }
    </style>
</head>
<body>

    <!-- Header & Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="https://pawarta.github.io/index.html" target="_blank" rel="noopener noreferrer">
                <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta">
                <div>
                    <span class="rainbow-text fs-4">PAWARTA</span>
                    <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - Javanese Portal</div>
                </div>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav align-items-center gap-3">
                    <li class="nav-item"><a class="nav-link active" href="https://pawarta.github.io/" target="_blank" rel="noopener noreferrer">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/about.html" target="_blank" rel="noopener noreferrer">Babagan (About)</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/sitemap.html" target="_blank" rel="noopener noreferrer">Sitemap</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/contact.html" target="_blank" rel="noopener noreferrer">Kontak</a></li>
                    <li class="nav-item">
                        <a href="https://pawarta.github.io/choices.html" target="_blank" rel="noopener noreferrer" class="btn btn-sm rainbow-badge px-3 py-1">Pilihan Warta</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Responsive Slider Section -->
    <div id="pawartaSlider" class="carousel slide carousel-fade shadow" data-bs-ride="carousel">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#pawartaSlider" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#pawartaSlider" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#pawartaSlider" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div class="carousel-inner">
            <!-- Slide 1 -->
            <div class="carousel-item active" style="background-image: url('https://pawarta.github.io/img/bahasa-jawa.jpeg');">
                <div class="carousel-overlay"></div>
                <div class="carousel-caption text-center animate__animated animate__fadeInDown">
                    <h2 class="honocoroko-title">ꦲꦏ꧀ꦱꦫꦗꦮꦭꦸꦩꦶꦤꦲꦶꦤꦫ</h2>
                    <h1 class="display-4 fw-bold text-white mb-3">Sugeng Rawuh ing <span class="rainbow-text">PAWARTA</span></h1>
                    <p class="lead text-light">Pusat warta digital modheren kanthi dhasar budaya lan kearifan lokal Jawi.</p>
                    <a href="#artikels" class="btn btn-warning btn-lg fw-bold mt-2 shadow">Miwiti Warta</a>
                </div>
            </div>
            <!-- Slide 2 -->
            <div class="carousel-item" style="background-image: url('https://pawarta.github.io/img/ai.jpeg');">
                <div class="carousel-overlay"></div>
                <div class="carousel-caption text-center animate__animated animate__fadeInDown">
                    <h2 class="honocoroko-title">ꦠꦼꦏ꧀ꦤꦺꦴꦭꦺꦴꦒꦶꦭꦤ꧀ꦄꦆ</h2>
                    <h1 class="display-4 fw-bold text-white mb-3">Transformasi Digital & AI</h1>
                    <p class="lead text-light">Nyambungake tradhisi luhur karo intelijen buatan (AI) lan teknologi masa depan.</p>
                    <a href="https://pawarta.github.io/tools/ai/index.html" target="_blank" rel="noopener noreferrer" class="btn btn-outline-light btn-lg fw-bold mt-2">Jlentrehake AI</a>
                </div>
            </div>
            <!-- Slide 3 -->
            <div class="carousel-item" style="background-image: url('https://pawarta.github.io/img/3d.jpeg');">
                <div class="carousel-overlay"></div>
                <div class="carousel-caption text-center animate__animated animate__fadeInDown">
                    <h2 class="honocoroko-title">ꦏꦧꦸꦢꦪꦤ꧀ꦤꦸꦱꦤ꧀ꦠꦫ</h2>
                    <h1 class="display-4 fw-bold text-white mb-3">Karya Seni 3D lan Visual</h1>
                    <p class="lead text-light">Eksplorasi estetika visual digital modern kanthi sentuhan budaya nusantara.</p>
                    <a href="https://pawarta.github.io/tools/3d/index.html" target="_blank" rel="noopener noreferrer" class="btn btn-warning btn-lg fw-bold mt-2 shadow">Waca Selengkapnya</a>
                </div>
            </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#pawartaSlider" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Sadurunge</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#pawartaSlider" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Sabanjure</span>
        </button>
    </div>
<h1>Transformasi Modern {cat_upper} - Artikel {file_num}</h1>
<p>Kearifan lokal dadi dhasar utama pangembangan sektor {category}...</p>

<!-- Widget Iklan / AdSense Placeholder -->
                <div class="card shadow-sm border-0 mb-4 rounded-4 text-center p-3 bg-light">
                    <div class="small text-muted mb-2">--- Ruang Iklan / Google AdSense ---</div>
                    <ins class="adsbygoogle"
                         style="display:block"
                         data-ad-client="ca-pub-9308517202792186"
                         data-ad-slot="auto"
                         data-ad-format="auto"
                         data-full-width-responsive="true"></ins>
                    <script>
                         (adsbygoogle = window.adsbygoogle || []).push({});
                    </script>
                </div>

                <!-- Navigasi kaca pendukung & Tools -->
                <div class="card shadow-sm border-0 rounded-4 mb-4">
                    <div class="card-header bg-dark text-white fw-bold">
                        <i class="bi bi-link-45deg"></i> Pranala Penting
                    </div>
                    <div class="list-group list-group-flush rounded-bottom">
                        <a href="https://pawarta.github.io/" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Portal Utama (Home)</a>
                        <a href="https://pawarta.github.io/about.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Babagan Kami (About)</a>
                        <a href="https://pawarta.github.io/contact.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Hubungi Kami (Contact)</a>
                        <a href="https://pawarta.github.io/privacy.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Kebijakan Privasi (Privacy)</a>
                        <a href="https://pawarta.github.io/terms.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Syarat & Ketentuan (Terms)</a>
                        <a href="https://pawarta.github.io/disclaimer.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Penyangkalan (Disclaimer)</a>
                        <a href="https://pawarta.github.io/license.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Lisensi (License)</a>
                        <a href="https://pawarta.github.io/LICENSE" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">File LICENSE</a>
                        <a href="https://pawarta.github.io/gdpr.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Kepatuhan GDPR</a>
                        <a href="https://pawarta.github.io/choices.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Pilihan Pengguna</a>
                        <a href="https://pawarta.github.io/sitemap.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Sitemap Website</a>
                    </div>
                </div>

                <!-- Tools & Utilities -->
                <div class="card shadow-sm border-0 rounded-4">
                    <div class="card-header rainbow-badge text-white fw-bold">
                        <i class="bi bi-tools"></i> Pilihan Tools & Layanan
                    </div>
                    <div class="list-group list-group-flush rounded-bottom small">
                        <a href="https://pawarta.github.io/tools/3d/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">3D Viewer Tool</a>
                        <a href="https://pawarta.github.io/tools/IP/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">IP Lookup Tool</a>
                        <a href="https://pawarta.github.io/tools/ai/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">AI Assistant Tool</a>
                        <a href="https://pawarta.github.io/tools/bahasa-jawa/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Penerjemah Bahasa Jawa</a>
                        <a href="https://pawarta.github.io/tools/calendar/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Kalender Jawa / Weton</a>
                        <a href="https://pawarta.github.io/tools/macapat/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Tembang Macapat</a>
                        <a href="https://pawarta.github.io/tools/maps/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Peta Lokasi</a>
                        <a href="https://pawarta.github.io/tools/qr/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">QR Code Generator/Scanner</a>
                        <a href="https://pawarta.github.io/tools/quran/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Al-Quran Digital</a>
                        <a href="https://pawarta.github.io/tools/search/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Pencarian Lanjutan</a>
                        <a href="https://pawarta.github.io/tools/tts/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Text-to-Speech (TTS)</a>
                        <a href="https://pawarta.github.io/tools/voice/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Voice Recognition</a>
                        <a href="https://pawarta.github.io/tools/wa/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">WhatsApp Direct Tool</a>
                        <a href="https://pawarta.github.io/tools/wayang/index.html" target="_blank" rel="noopener noreferrer" class="list-group-item list-group-item-action">Katalog Wayang Kulit</a>
                    </div>
                </div>

            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="pt-5 pb-4 border-top border-warning">
        <div class="container text-center text-md-start">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <h5 class="text-white fw-bold mb-3"><span class="rainbow-text">PAWARTA</span></h5>
                    <p class="small text-secondary">Portal warta digital inovatif kang nyawijiake kabudayan Jawi, aksara Honocoroko, lan teknologi informasi modheren ing donya maya.</p>
                    <div class="fs-4 text-warning">
                        ꦫꦲꦪꦸ ꦫꦲꦪꦸ ꦫꦲꦪꦸ
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <h6 class="text-white fw-bold mb-3">Pranala Kaca</h6>
                    <ul class="list-unstyled small">
                        <li><a href="https://pawarta.github.io/index.html" target="_blank" rel="noopener noreferrer">Beranda / Index</a></li>
                        <li><a href="https://pawarta.github.io/about.html" target="_blank" rel="noopener noreferrer">Tentang Kami</a></li>
                        <li><a href="https://pawarta.github.io/contact.html" target="_blank" rel="noopener noreferrer">Kontak</a></li>
                        <li><a href="https://pawarta.github.io/privacy.html" target="_blank" rel="noopener noreferrer">Kebijakan Privasi</a></li>
                        <li><a href="https://pawarta.github.io/terms.html" target="_blank" rel="noopener noreferrer">Syarat & Ketentuan</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-4">
                    <h6 class="text-white fw-bold mb-3">Informasi Aliran Data</h6>
                    <p class="small text-secondary mb-1">Nama Aliran: <strong>pawarta</strong></p>
                    <p class="small text-secondary mb-1">ID Pengukuran: <code class="text-warning">G-GN5PGKKM3T</code></p>
                    <p class="small text-secondary">URL: <a href="https://pawarta.github.io" target="_blank" rel="noopener noreferrer">https://pawarta.github.io</a></p>
                </div>
            </div>
            <hr class="border-secondary">
            <div class="row text-center small text-secondary">
                <div class="col-md-12">
                    <p class="mb-0">&copy; 2026 PAWARTA (pawarta.github.io). Hak Cipta Dilindungi Undang-Undang. Kinarya kanti katresnan tumrap Budaya Jawi.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS & AOS Animation Script -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        // Initialize AOS (Animate on Scroll)
        AOS.init({
            duration: 1000,
            once: true
        });
    </script>

</body>
</html>"""

@functions_framework.http
def trigger_generator(request):
    """Fungsi utama yang akan dipicu oleh Cloud Scheduler"""
    try:
        # Inisialisasi Cloud Storage Client
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        # Melakukan perulangan otomatis untuk membuat artikel
        for category in CATEGORIES:
            # Contoh: membuat 5 artikel per kategori setiap cron berjalan
            for i in range(1, 6): 
                html_content = generate_html_content(category, i)
                
                # Menentukan lokasi path file di Cloud Storage (misal: market/artikel1.html)
                blob_path = f"{category}/artikel{i}.html"
                blob = bucket.blob(blob_path)
                
                # Mengunggah konten HTML dengan Content-Type yang benar agar bisa dibuka sebagai halaman web
                blob.upload_from_string(html_content, content_type='text/html')
                
        return "Otomatisasi pembaruan artikel PAWARTA Berhasil!", 200
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}", 500
