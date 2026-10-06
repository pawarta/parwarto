import os
import random

# Dhaptar sedaya kategori (lengkap saking panyuwunan)
CATEGORIES = [
    "market", "finance", "macro", "micro", "economy", "explainers", "manufacturing",
    "property", "health", "education", "lifestyle", "hospitality", "tech", "media",
    "smes", "luxury", "whos-who", "international", "local-resources", "politics",
    "culture", "science", "public-policy", "business", "news", "sports", "arts",
    "celebrities", "automotive", "commentary", "interview", "money", "perbankan",
    "belanja", "sharia", "football", "opinion", "video", "kisah", "index", "sejarah",
    "entrepreneur", "research", "photo", "olahraga", "selebritis", "country", "dki",
    "diy", "jabar", "jatim", "jateng", "aceh", "papua", "kalimantan", "sumatra",
    "sulawesi", "bali", "asia", "afrika", "australia", "rusia", "eropa", "amerika",
    "ai", "teknologi", "astronomi", "zodiak", "maps"
]

COMMON_IMAGES = [
    "https://pawarta.github.io/img/bahasa-jawa.jpeg",
    "https://pawarta.github.io/img/ai.jpeg",
    "https://pawarta.github.io/img/3d.jpeg"
]

def generate_html_content(category, title_suffix, file_num):
    img_url = random.choice(COMMON_IMAGES)
    cat_upper = category.upper()
    
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PAWARTA - {cat_upper} - Artikel {file_num} & Kabudayan Jawi Modern</title>

<!-- Meta SEO & Verification -->
<meta name="description" content="Pawarta minangka portal warta digital kategori {category} - informasi modheren, lan pelestarian kabudayan Jawi sarta aksara Honocoroko ing era digital.">
<meta name="keywords" content="pawarta, warta jawa, {category}, berita jawa, honocoroko, aksara jawa, portal warta">
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="IAcn_DcNzAkFuMAjiMDNMoUEMZV5oKau1XrJ4aDJlRc">
<meta name="msvalidate.01" content="E9411F953448412F854C1FBA584B1383">

<!-- Google AdSense -->
<script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9308517202792186"></script>

<!-- Open Graph / Social Media Meta -->
<meta property="og:title" content="PAWARTA - {cat_upper} - Artikel {file_num}">
<meta property="og:description" content="Pusat informasi warta digital lan kabudayan kategori {category} kanthi nuansa Jawi modern.">
<meta property="og:image" content="{img_url}">
<meta property="og:url" content="https://pawarta.github.io/{category}/artikel{file_num}.html">
<meta property="og:type" content="article">

<!-- Favicon & Icons -->
<link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

<!-- Google tag (gtag.js) - GA4 ID: G-GN5PGKKM3T -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GN5PGKKM3T"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GN5PGKKM3T');
</script>
</head>
<body class="bg-light">

<!-- Header & Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container">
        <a class="navbar-brand d-flex align-items-center gap-2" href="https://pawarta.github.io/index.html">
            <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta" width="40" height="40" class="rounded-circle">
            <div>
                <span class="fs-4 text-warning fw-bold">PAWARTA</span>
                <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - {cat_upper} Portal</div>
            </div>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/index.html">Home</a></li>
                <li class="nav-item"><a class="nav-link active" href="https://pawarta.github.io/{category}/index.html">{cat_upper}</a></li>
                <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/contact.html">Contact</a></li>
            </ul>
        </div>
    </div>
</nav>

<!-- Main Content Area -->
<main id="artikels" class="container my-5">
    <div class="row">
        <!-- Article Content -->
        <div class="col-lg-8" data-aos="fade-up">
            <article class="bg-white p-4 p-md-5 rounded-4 shadow-sm border">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="https://pawarta.github.io/index.html">Home</a></li>
                        <li class="breadcrumb-item"><a href="https://pawarta.github.io/{category}/index.html">{cat_upper}</a></li>
                        <li class="breadcrumb-item active" aria-current="page">Artikel {file_num}</li>
                    </ol>
                </nav>

                <h1 class="fw-bold mb-3 text-dark">Transformasi & Inovasi Modern {cat_upper}: Warta Penting Artikel {file_num}</h1>
                <div class="text-muted small mb-4">
                    <i class="bi bi-calendar"></i> Dipublikasikaken ing 2026 | <i class="bi bi-tag"></i> Kategori: {cat_upper}
                </div>

                <!-- Google AdSense Banner -->
                <div class="my-4 text-center">
                    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9308517202792186" data-ad-slot="8374036730" data-ad-format="auto" data-full-width-responsive="true"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>

                <!-- Featured Image -->
                <div class="mb-4 text-center">
                    <img src="{img_url}" class="img-fluid rounded shadow-sm" alt="Ilustrasi Artikel {cat_upper} {file_num} Pawarta Jawi">
                    <p class="text-muted small mt-2">Gambar 1: Ilustrasi pendukung warta {cat_upper} ing era digital modern.</p>
                </div>

                <h2 class="h4 fw-bold mt-4">1. Pambuka Tumrap Pangembangan {cat_upper}</h2>
                <p>Ing jaman globalisasi lan digitalisasi menika, babagan {category} ngalami ewah-ewahan ingkang luar biasa cepat. Masyarakat Jawi sarta Nusantara kedah tanggap lan nyelarasaken antawisipun kearifan lokal lan kemajuan teknologi modheren. Artikel menika ngupas tuntas kanthi komprehensif babagan dinamika lan strategi ngadhepi tantangan global.</p>

                <h3 class="h5 fw-bold mt-3">1.1 Peran Strategis Kearifan Lokal</h3>
                <p>Kearifan lokal dadi dhasar utawi pondasi utama supados pangembangan sektor {category} boten ilang arah. Nilai luhur budaya Jawi tansah dados panutan ing saben pelaksanaane.</p>

                <h2 class="h4 fw-bold mt-4">2. Analisis Data lan Tabel Perbandingan</h2>
                <p>Berikut ing ngandhap punika tabel ringkesan data sarta statistik babagan perkembangan {category} ing taun punika:</p>
                
                <div class="table-responsive my-3">
                    <table class="table table-bordered table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th>No</th>
                                <th>Parameter Analisis</th>
                                <th>Statistik / Capaian</th>
                                <th>Keterangan</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>Tingkat Pertumbuhan</td>
                                <td>88.5%</td>
                                <td>Sangat Positif</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>Adopsi Teknologi</td>
                                <td>94.2%</td>
                                <td>Terintegrasi AI</td>
                            </tr>
                            <tr>
                                <td>3</td>
                                <td>Kepuasan Publik</td>
                                <td>91.0%</td>
                                <td>Standar Internasional</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <h2 class="h4 fw-bold mt-4">3. Pranala Penting (Internal & Eksternal Link)</h2>
                <p>Kanggo nambah wawasan, mangga pirsani pranala internal lan eksternal ing ngandhap menika:</p>
                <ul>
                    <li><a href="https://pawarta.github.io/{category}/artikel1.html">Pranala Internal 1: Warta Utama {cat_upper}</a></li>
                    <li><a href="https://pawarta.github.io/{category}/artikel2.html">Pranala Internal 2: Panduan Lengkap {cat_upper}</a></li>
                    <li><a href="https://pawarta.github.io/{category}/artikel3.html">Pranala Internal 3: Analisis Mendalam {cat_upper}</a></li>
                    <li><a href="https://pawarta.github.io/index.html">Pranala Internal 4: Halaman Utama Pawarta</a></li>
                    <li><a href="https://pawarta.github.io/contact.html">Pranala Internal 5: Hubungi Kami</a></li>
                    <li><a href="https://pawarta.github.io/ai/index.html">Pranala Internal 6: Teknologi AI Terkini</a></li>
                    <li><a href="https://pawarta.github.io/culture/index.html">Pranala Internal 7: Kabudayan Nusantara</a></li>
                    <li><a href="https://www.wikipedia.org" target="_blank" rel="nofollow">Pranala Eksternal 1: Ensiklopedia Global</a></li>
                    <li><a href="https://www.bbc.com" target="_blank" rel="nofollow">Pranala Eksternal 2: Berita Internasional</a></li>
                    <li><a href="https://www.reuters.com" target="_blank" rel="nofollow">Pranala Eksternal 3: Riset Pasar Global</a></li>
                    <li><a href="https://github.com" target="_blank" rel="nofollow">Pranala Eksternal 4: Platform Pengembang</a></li>
                    <li><a href="https://www.google.com" target="_blank" rel="nofollow">Pranala Eksternal 5: Mesin Pencari Utama</a></li>
                    <li><a href="https://www.w3.org" target="_blank" rel="nofollow">Pranala Eksternal 6: Standar Web Internasional</a></li>
                    <li><a href="https://www.python.org" target="_blank" rel="nofollow">Pranala Eksternal 7: Dokumentasi Pemrograman</a></li>
                </ul>

                <h2 class="h4 fw-bold mt-4">4. Pitakonan Sering (FAQ)</h2>
                <div class="accordion" id="faqAccordion">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne">
                                Punapa kauntungan utama saking program {category} menika?
                            </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                            <div class="accordion-body">
                                Program menika nyediakake akses informasi sing transparan, cepet, lan adhedhasar data akurat tumrap masyarakat.
                            </div>
                        </div>
                    </div>
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingTwo">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo">
                                Kados pundi cara nggabungaken teknologi lan kabudayan Jawi?
                            </button>
                        </h2>
                        <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                            <div class="accordion-body">
                                Kanthi nggunakake platform digital modern, aksara lan nilai-nilai luhur Jawi saged diwanuhake marang generasi mudha global.
                            </div>
                        </div>
                    </div>
                </div>

                <h2 class="h4 fw-bold mt-4">5. Kesimpulan</h2>
                <p>Pungkasane, kemajuan ing sektor {category} kedah tansah diiringi semangat gotong royong lan njaga jati diri budaya bangsa. Mugi-mugi artikel menika bermanfaat tumrap para pamaos sedaya.</p>

                <!-- Social Share & Contact Form Section -->
                <hr class="my-4">
                <div class="bg-light p-3 rounded border">
                    <h5 class="fw-bold mb-3"><i class="bi bi-share"></i> Bagikan Warta Menika</h5>
                    <a href="#" class="btn btn-primary btn-sm me-2 mb-2"><i class="bi bi-facebook"></i> Facebook</a>
                    <a href="#" class="btn btn-info btn-sm text-white me-2 mb-2"><i class="bi bi-twitter"></i> Twitter</a>
                    <a href="#" class="btn btn-success btn-sm me-2 mb-2"><i class="bi bi-whatsapp"></i> WhatsApp</a>
                </div>

                <div class="mt-4 p-3 bg-white rounded border">
                    <h5 class="fw-bold mb-3"><i class="bi bi-envelope"></i> Kirim Komentar / Kontak Kami</h5>
                    <form>
                        <div class="mb-3">
                            <label class="form-label">Asma Panjenengan</label>
                            <input type="text" class="form-control" placeholder="Tulis asma...">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pesan / Tanggapan</label>
                            <textarea class="form-control" rows="3" placeholder="Tulis tanggapan..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-warning fw-bold">Kirim Pesan</button>
                    </form>
                </div>
            </article>
        </div>

        <!-- Sidebar Widgets -->
        <div class="col-lg-4 mt-4 mt-lg-0">
            <!-- News / Popular Articles Widget -->
            <div class="card mb-4 shadow-sm border-0">
                <div class="card-header bg-dark text-white fw-bold">Warta Popular & Terbaru</div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item"><a href="https://pawarta.github.io/{category}/artikel1.html" class="text-decoration-none">Artikel Popular 1: Perkembangan {cat_upper}</a></li>
                    <li class="list-group-item"><a href="https://pawarta.github.io/{category}/artikel2.html" class="text-decoration-none">Artikel Terbaru 2: Tren Digital 2026</a></li>
                    <li class="list-group-item"><a href="https://pawarta.github.io/{category}/artikel3.html" class="text-decoration-none">Artikel Terlama 3: Arsip Sejarah {cat_upper}</a></li>
                </ul>
            </div>

            <!-- Label & Archive Widget -->
            <div class="card mb-4 shadow-sm border-0">
                <div class="card-header bg-warning text-dark fw-bold">Label & Archive</div>
                <div class="card-body">
                    <span class="badge bg-secondary mb-1">Jawa Modern</span>
                    <span class="badge bg-secondary mb-1">{cat_upper}</span>
                    <span class="badge bg-secondary mb-1">Honocoroko</span>
                    <span class="badge bg-secondary mb-1">Arsip 2026</span>
                </div>
            </div>

            <!-- AdSense Sidebar Banner -->
            <div class="card shadow-sm border-0 text-center p-2">
                <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9308517202792186" data-ad-slot="8374036730" data-ad-format="auto" data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
            </div>
        </div>
    </div>
</main>

<!-- Footer -->
<footer class="pt-5 pb-4 border-top border-warning bg-dark text-white">
    <div class="container text-center text-md-start">
        <div class="row">
            <div class="col-md-4 mb-4">
                <h5 class="text-white fw-bold mb-3"><span class="text-warning">PAWARTA</span></h5>
                <p class="small text-secondary">Portal warta digital inovatif kang nyawijiake kabudayan Jawi, aksara Honocoroko, lan teknologi informasi modheren ing donya maya.</p>
                <div class="fs-4 text-warning">ꦫꦲꦪꦸ ꦫꦲꦪꦸ ꦫꦲꦪꦸ</div>
            </div>
            <div class="col-md-4 mb-4">
                <h6 class="text-white fw-bold mb-3">Pranala Kaca</h6>
                <ul class="list-unstyled small">
                    <li><a href="https://pawarta.github.io/index.html" class="text-secondary text-decoration-none">Beranda / Index</a></li>
                    <li><a href="https://pawarta.github.io/about.html" class="text-secondary text-decoration-none">Tentang Kami</a></li>
                    <li><a href="https://pawarta.github.io/contact.html" class="text-secondary text-decoration-none">Kontak</a></li>
                </ul>
            </div>
            <div class="col-md-4 mb-4">
                <h6 class="text-white fw-bold mb-3">Informasi Aliran Data</h6>
                <p class="small text-secondary mb-1">Nama Aliran: <strong>pawarta</strong></p>
                <p class="small text-secondary mb-1">ID Pengukuran: <code class="text-warning">G-GN5PGKKM3T</code></p>
                <p class="small text-secondary">URL: <a href="https://pawarta.github.io" class="text-warning">https://pawarta.github.io</a></p>
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

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script>AOS.init({{ duration: 1000, once: true }});</script>
</body>
</html>
"""
    return html

def generate_index_content(category):
    cat_upper = category.upper()
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PAWARTA - Kategori {cat_upper}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="https://pawarta.github.io/index.html">PAWARTA - {cat_upper}</a>
  </div>
</nav>
<div class="container my-5">
    <h1 class="fw-bold mb-4">Daftar Artikel Kategori: {cat_upper}</h1>
    <p class="lead">Sugeng rawuh ing kaca arsip kategori {category}. Pirsani dhaptar 30 artikel pilihan ing ngandhap menika:</p>
    <div class="list-group mb-4">
""" + "".join([f'        <a href="artikel{i}.html" class="list-group-item list-group-item-action">Artikel {i} - Warta Pilihan {cat_upper}</a>\n' for i in range(1, 31)]) + f"""    </div>
    <a href="sitemap.html" class="btn btn-dark">Sitemap HTML</a>
    <a href="sitemap.xml" class="btn btn-secondary">Sitemap XML</a>
</div>
</body>
</html>
"""

def generate_sitemap_html(category):
    return f"<!DOCTYPE html><html><head><title>Sitemap {category}</title></head><body><h1>Sitemap {category}</h1><ul>" + "".join([f'<li><a href="artikel{i}.html">Artikel {i}</a></li>' for i in range(1, 31)]) + "</ul></body></html>"

def generate_sitemap_xml(category):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for i in range(1, 31):
        xml += f'  <url><loc>https://pawarta.github.io/{category}/artikel{i}.html</loc></url>\n'
    xml += '</urlset>'
    return xml

def generate_sitemap_txt(category):
    return "\n".join([f"https://pawarta.github.io/{category}/artikel{i}.html" for i in range(1, 31)])

def main():
    for cat in CATEGORIES:
        os.makedirs(cat, exist_ok=True)
        # Nggawe 30 artikel saben kategori
        for i in range(1, 31):
            with open(f"{cat}/artikel{i}.html", "w", encoding="utf-8") as f:
                f.write(generate_html_content(cat, f"Artikel {i}", i))
        
        # Nggawe file index lan sitemap
        with open(f"{cat}/index.html", "w", encoding="utf-8") as f:
            f.write(generate_index_content(cat))
        with open(f"{cat}/sitemap.html", "w", encoding="utf-8") as f:
            f.write(generate_sitemap_html(cat))
        with open(f"{cat}/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(generate_sitemap_xml(cat))
        with open(f"{cat}/sitemap.txt", "w", encoding="utf-8") as f:
            f.write(generate_sitemap_txt(cat))
        print(f"Kategori '{cat}' rampung 30 artikel.")

if __name__ == "__main__":
    main()
