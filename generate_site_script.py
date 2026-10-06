 import os

categories = [
    "Market", "Finance", "Macro", "Micro", "Economy", "Explainers", "Manufacturing",
    "Property", "Health", "Education", "Lifestyle", "Hospitality", "Tech", "Media",
    "Smes", "Luxury", "Whos_Who", "International", "Local_Resources", "Politics",
    "Culture", "Science", "Public_Policy", "Business", "News", "Sports", "Arts",
    "Celebrities", "Automotive", "Commentary", "Interview", "Money", "perbankan",
    "belanja", "Sharia", "Football", "Opinion", "Video", "kisah", "Index",
    "Sejarah", "Entrepreneur", "Research", "Photo", "olahraga", "selebritis",
    "country", "dki", "diy", "jabar", "jatim", "jateng", "aceh", "papua",
    "kalimantan", "sumatra", "sulawesi", "bali", "asia", "afrika", "australia",
    "rusia", "eropa", "amerika", "ai", "teknologi", "astronomi", "zodiak", "maps"
]

print(f"Generating site structure for {len(categories)} categories, 30 articles each...")

for cat in categories:
    cat_slug = cat.lower()
    cat_dir = os.path.join("pawarta_site", cat_slug)
    os.makedirs(cat_dir, exist_ok=True)
    
    articles = []
    for i in range(1, 31):
        filename = f"artikel{i}.html"
        articles.append((filename, f"Artikel {i} Babagan {cat} Modheren lan Kabudayan Jawi"))
        
        art_content = f"""<!DOCTYPE html>
<html lang="jv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Artikel {i} {cat} - PAWARTA Portal Warta Jawi</title>
<meta name="description" content="Warta lan informasi lengkap babagan {cat} artikel {i} kanthi sudut pandang budaya Jawi modheren lan analisis jero tuwin SEO akurat.">
<meta name="keywords" content="pawarta, {cat_slug}, warta jawa, artikel {i}, honocoroko">
<meta name="robots" content="index, follow">
<meta name="google-site-verification" content="IAcn_DcNzAkFuMAjiMDNMoUEMZV5oKau1XrJ4aDJlRc">
<meta name="msvalidate.01" content="E9411F953448412F854C1FBA584B1383">
<link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
<link rel="canonical" href="https://pawarta.github.io/{cat_slug}/artikel{i}.html">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GN5PGKKM3T"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-GN5PGKKM3T');
</script>
<style>
.rainbow-text {{ background: linear-gradient(45deg, #d4af37, #ff6b6b, #48dbfb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
body {{ background-color: #f8f9fa; color: #333; }}
</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container">
        <a class="navbar-brand d-flex align-items-center gap-2" href="https://pawarta.github.io/index.html">
            <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta" width="40" height="40" class="rounded-circle">
            <div>
                <span class="rainbow-text fs-4 fw-bold">PAWARTA</span>
                <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - Javanese Portal</div>
            </div>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/index.html">Home</a></li>
                <li class="nav-item"><a class="nav-link active" href="index.html">{cat}</a></li>
                <li class="nav-item"><a class="nav-link" href="sitemap.html">Sitemap</a></li>
            </ul>
        </div>
    </div>
</nav>

<div class="container my-5">
    <div class="row">
        <div class="col-lg-8">
            <article class="bg-white p-4 p-md-5 rounded-4 shadow-sm border">
                <h1 class="fw-bold mb-3 text-dark">Artikel {i}: Perkembangan Tumrap {cat} ing Era Digital Lan Kearifan Lokal</h1>
                <div class="text-muted small mb-4">
                    <span><i class="bi bi-calendar"></i> 6 Oktober 2026</span> | 
                    <span><i class="bi bi-folder"></i> {cat}</span> | 
                    <span><i class="bi bi-person"></i> Redaksi PAWARTA</span>
                </div>
                
                <img src="https://pawarta.github.io/img/{cat_slug}-{i}.jpeg" alt="Ilustrasi {cat} Artikel {i} PAWARTA Portal Warta Jawi" class="img-fluid rounded mb-4 shadow-sm w-100" style="max-height: 400px; object-fit: cover;">
                
                <h2 class="h4 fw-bold mt-4 mb-3">Pambuka Tumrap Kawontenan {cat}</h2>
                <p>Ing era modern niki, peranan <strong>{cat}</strong> sanget wigati tumrap kemajuan masyarakat sarta pembangunan ekonomi digital. PAWARTA minangka portal warta terkemuka nyajiaken analisis mendalam babagan dinamika lan tantangan kang diadhepi dening para pelaku ing sektor {cat} sakmenika.</p>
                <p>Kanthi nggabungaken filosofi luhur Jawi lan teknologi informasi mutakhir, kawruh babagan {cat} dados langkung gampang diakses dening masyarakat luas saking maneka kalangan.</p>

                <h2 class="h4 fw-bold mt-4 mb-3">Analisis Komprehensif Sarta Tabel Data {cat}</h2>
                <p>Kanggo langkung mangertos babagan tren lan statistik {cat}, ing ngandhap punika katampilaken tabel ringkesan data performa sarta indikator utama:</p>
                
                <div class="table-responsive my-4">
                    <table class="table table-striped table-bordered align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th>No</th>
                                <th>Indikator {cat}</th>
                                <th>Target 2026</th>
                                <th>Pencapaian</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>Pertumbuhan Sektoral</td>
                                <td>85%</td>
                                <td>88.5%</td>
                                <td class="text-success fw-bold">Optimal</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>Adopsi Teknologi Digital</td>
                                <td>90%</td>
                                <td>92.1%</td>
                                <td class="text-success fw-bold">Unggul</td>
                            </tr>
                            <tr>
                                <td>3</td>
                                <td>Pemberdayaan Komunitas</td>
                                <td>75%</td>
                                <td>79.4%</td>
                                <td class="text-primary fw-bold">Stabil</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <h3 class="h5 fw-bold mt-4 mb-2">Tantangan Lan Solusi Strategis</h3>
                <p>Maneka tantangan mesthi wonten ing saben pangembanganing {cat}. Nanging, kanthi komitmen sesarengan lan inovasi tanpa wates, sedaya kendala saged dipun lampahi kanthi sae.</p>

                <!-- AdSense Banner -->
                <div class="my-4 p-3 bg-light border rounded text-center">
                    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9308517202792186" crossorigin="anonymous"></script>
                    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9308517202792186" data-ad-slot="8374036730" data-ad-format="auto" data-full-width-responsive="true"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>

                <h3 class="h5 fw-bold mt-4 mb-2">Pitakonan Asring Dipun Lajengaken (FAQ)</h3>
                <div class="accordion mb-4" id="faqAccordion{i}">
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne{i}">
                      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne{i}">
                        Kados pundi cara ngetrapaken strategi {cat} ing era digital?
                      </button>
                    </h2>
                    <div id="collapseOne{i}" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion{i}">
                      <div class="accordion-body">
                        Penerapan strategi {cat} mbutuhaken adaptasi teknologi, pemahaman pasar, sarta konsistensi nindakaken kearifan lokal.
                      </div>
                    </div>
                  </div>
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="headingTwo{i}">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo{i}">
                        Punapa kauntungan utami saking pengembangan sektor {cat}?
                      </button>
                    </h2>
                    <div id="collapseTwo{i}" class="accordion-collapse collapse" data-bs-parent="#faqAccordion{i}">
                      <div class="accordion-body">
                        Kauntungan utaminipun inggih punika peningkatan efisiensi, perluasan jaringan, lan kesejahteraan masyarakat ingkang langkung merata.
                      </div>
                    </div>
                  </div>
                </div>

                <h3 class="h5 fw-bold mt-4 mb-2">Kesimpulan</h3>
                <p>Kesimpulanipun, {cat} artikel {i} niki maringi gambaran bilih kemajuan zaman kedah dipun selarasaken kaliyan nilai-nilai budaya lan integritas ingkang luhur.</p>

                <!-- Internal & External Links Section -->
                <div class="mt-4 p-3 bg-white border rounded">
                    <h6 class="fw-bold">Pranala Internal (7 Internal Links):</h6>
                    <ul class="small mb-3">
                        <li><a href="index.html">1. Indeks Kategori {cat}</a></li>
                        <li><a href="artikel1.html">2. Artikel Utama {cat} 1</a></li>
                        <li><a href="artikel2.html">3. Artikel Terkait {cat} 2</a></li>
                        <li><a href="artikel3.html">4. Artikel Pilihan {cat} 3</a></li>
                        <li><a href="sitemap.html">5. Sitemap Pawarta</a></li>
                        <li><a href="https://pawarta.github.io/index.html">6. Halaman Utama Pawarta</a></li>
                        <li><a href="https://pawarta.github.io/tools/ai/index.html">7. Eksplorasi AI Pawarta</a></li>
                    </ul>
                    <h6 class="fw-bold">Pranala Eksternal (7 External Links):</h6>
                    <ul class="small mb-0">
                        <li><a href="https://www.wikipedia.org" target="_blank" rel="noopener">1. Wikipedia Ensiklopedia Global</a></li>
                        <li><a href="https://www.github.com" target="_blank" rel="noopener">2. GitHub Platform Kolaborasi</a></li>
                        <li><a href="https://www.google.com" target="_blank" rel="noopener">3. Google Mesin Pencari</a></li>
                        <li><a href="https://www.reuters.com" target="_blank" rel="noopener">4. Reuters Berita Internasional</a></li>
                        <li><a href="https://www.bbc.com" target="_blank" rel="noopener">5. BBC News Global</a></li>
                        <li><a href="https://www.cnn.com" target="_blank" rel="noopener">6. CNN International</a></li>
                        <li><a href="https://getbootstrap.com" target="_blank" rel="noopener">7. Bootstrap Framework CSS</a></li>
                    </ul>
                </div>

                <!-- Social Media Share -->
                <div class="mt-4 p-3 bg-light rounded text-center">
                    <span class="fw-bold me-2">Sebar Warta Niki:</span>
                    <a href="https://facebook.com/sharer/sharer.php?u=https://pawarta.github.io/{cat_slug}/artikel{i}.html" target="_blank" class="btn btn-primary btn-sm me-1"><i class="bi bi-facebook"></i> Facebook</a>
                    <a href="https://twitter.com/intent/tweet?url=https://pawarta.github.io/{cat_slug}/artikel{i}.html" target="_blank" class="btn btn-info btn-sm text-white me-1"><i class="bi bi-twitter"></i> Twitter</a>
                    <a href="https://api.whatsapp.com/send?text=Waca%20Artikel%20Menarik%20https://pawarta.github.io/{cat_slug}/artikel{i}.html" target="_blank" class="btn btn-success btn-sm"><i class="bi bi-whatsapp"></i> WhatsApp</a>
                </div>

                <!-- Contact Form Section -->
                <div class="mt-5 p-4 bg-white border rounded shadow-sm">
                    <h4 class="fw-bold mb-3">Kirim Komentar / Pitakenan</h4>
                    <form action="#" method="POST">
                        <div class="mb-3">
                            <label class="form-label">Asma Lengkap</label>
                            <input type="text" class="form-control" placeholder="Asma panjenengan..." required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Alamat Email</label>
                            <input type="email" class="form-control" placeholder="email@domain.com" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pesen / Tanggapan</label>
                            <textarea class="form-control" rows="3" placeholder="Tulis pesen panjenengan ing mriki..." required></textarea>
                        </div>
                        <button type="submit" class="btn btn-warning fw-bold">Kirim Pesen</button>
                    </form>
                </div>

            </article>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4 mt-4 mt-lg-0">
            <!-- News Artikel -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">Warta Pilihan ({cat})</div>
                <ul class="list-group list-group-flush small">
                    <li class="list-group-item"><a href="artikel1.html" class="text-decoration-none text-dark">Perkembangan Anyar Tumrap {cat} Tahun 2026</a></li>
                    <li class="list-group-item"><a href="artikel2.html" class="text-decoration-none text-dark">Strategi Ngadhepi Tantangan Global ing {cat}</a></li>
                    <li class="list-group-item"><a href="artikel3.html" class="text-decoration-none text-dark">Kolaborasi Budaya lan Teknologi ing Sektor {cat}</a></li>
                </ul>
            </div>

            <!-- Artikel Popular -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-warning text-dark fw-bold">Artikel Populer</div>
                <ul class="list-group list-group-flush small">
                    <li class="list-group-item"><a href="artikel5.html" class="text-decoration-none text-dark">Top 10 Tren {cat} Paling Anyar</a></li>
                    <li class="list-group-item"><a href="artikel12.html" class="text-decoration-none text-dark">Panduan Lengkap Ngembangaken {cat}</a></li>
                    <li class="list-group-item"><a href="artikel18.html" class="text-decoration-none text-dark">Wawancara Eksklusif Pakar {cat}</a></li>
                </ul>
            </div>

            <!-- Artikel Terbaru -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">Artikel Terbaru</div>
                <ul class="list-group list-group-flush small">
                    <li class="list-group-item"><a href="artikel30.html" class="text-decoration-none text-dark">Inovasi Terkini {cat} Minggu Niki</a></li>
                    <li class="list-group-item"><a href="artikel29.html" class="text-decoration-none text-dark">Cathetan Penting Babagan {cat}</a></li>
                    <li class="list-group-item"><a href="artikel28.html" class="text-decoration-none text-dark">Refleksi Budaya lan {cat} Modern</a></li>
                </ul>
            </div>

            <!-- Artikel Terlama -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-secondary text-white fw-bold">Arsip / Artikel Terlama</div>
                <ul class="list-group list-group-flush small">
                    <li class="list-group-item"><a href="artikel1.html" class="text-decoration-none text-dark">Sajarah Awal Mula {cat} ing Nusantara</a></li>
                    <li class="list-group-item"><a href="artikel2.html" class="text-decoration-none text-dark">Evolusi Sektor {cat} Dekade Kepungkur</a></li>
                </ul>
            </div>

            <!-- Labels / Tags -->
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">Label / Kategori</div>
                <div class="card-body">
                    <span class="badge bg-secondary mb-1">{cat}</span>
                    <span class="badge bg-secondary mb-1">Warta Jawi</span>
                    <span class="badge bg-secondary mb-1">Honocoroko</span>
                    <span class="badge bg-secondary mb-1">Digital</span>
                    <span class="badge bg-secondary mb-1">Ekonomi</span>
                </div>
            </div>
        </div>
    </div>
</div>

<footer class="pt-5 pb-4 border-top border-warning bg-dark text-white mt-5">
<div class="container text-center text-md-start">
<div class="row">
<div class="col-md-4 mb-4">
<h5 class="text-white fw-bold mb-3"><span class="rainbow-text">PAWARTA</span></h5>
<p class="small text-secondary">Portal warta digital inovatif kang nyawijiake kabudayan Jawi, aksara Honocoroko, lan teknologi informasi modheren ing donya maya.</p>
<div class="fs-4 text-warning">ꦫꦲꦪꦸ ꦫꦲꦪꦸ ꦫꦲꦪꦸ</div>
</div>
<div class="col-md-4 mb-4">
<h6 class="text-white fw-bold mb-3">Pranala Kaca</h6>
<ul class="list-unstyled small">
<li><a href="https://pawarta.github.io/index.html" class="text-decoration-none text-secondary">Beranda / Index</a></li>
<li><a href="sitemap.html" class="text-decoration-none text-secondary">Sitemap HTML</a></li>
<li><a href="sitemap.xml" class="text-decoration-none text-secondary">Sitemap XML</a></li>
</ul>
</div>
<div class="col-md-4 mb-4">
<h6 class="text-white fw-bold mb-3">Informasi Aliran Data</h6>
<p class="small text-secondary mb-1">Nama Aliran: <strong>pawarta</strong></p>
<p class="small text-secondary mb-1">ID Pengukuran: <code class="text-warning">G-GN5PGKKM3T</code></p>
<p class="small text-secondary">URL: <a href="https://pawarta.github.io" class="text-warning text-decoration-none">https://pawarta.github.io</a></p>
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
        with open(os.path.join(cat_dir, filename), "w", encoding="utf-8") as f:
            f.write(art_content)
            
    # Index for Category
    index_content = f"""<!DOCTYPE html>
<html lang="jv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kategori {cat} - PAWARTA Portal Warta Jawi</title>
<meta name="description" content="Arsip lengkap 30 artikel pilihan babagan {cat} ing portal warta digital PAWARTA.">
<link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
<link rel="canonical" href="https://pawarta.github.io/{cat_slug}/index.html">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<style>
.rainbow-text {{ background: linear-gradient(45deg, #d4af37, #ff6b6b, #48dbfb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
body {{ background-color: #f8f9fa; color: #333; }}
</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container">
        <a class="navbar-brand d-flex align-items-center gap-2" href="https://pawarta.github.io/index.html">
            <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta" width="40" height="40" class="rounded-circle">
            <div>
                <span class="rainbow-text fs-4 fw-bold">PAWARTA</span>
                <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - Javanese Portal</div>
            </div>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/index.html">Home</a></li>
                <li class="nav-item"><a class="nav-link active" href="index.html">{cat}</a></li>
                <li class="nav-item"><a class="nav-link" href="sitemap.html">Sitemap</a></li>
            </ul>
        </div>
    </div>
</nav>

<div class="container my-5">
    <div class="text-center mb-5">
        <h1 class="fw-bold rainbow-text display-5">Kategori: {cat}</h1>
        <p class="lead text-muted">Kempalan 30 artikel pilihan lan warta paling anyar babagan {cat}</p>
    </div>

    <div class="row row-cols-1 row-cols-md-3 g-4">
"""
    for fname, ftitle in articles:
        index_content += f"""
        <div class="col">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body">
                    <h5 class="card-title fw-bold"><a href="{fname}" class="text-decoration-none text-dark">{ftitle}</a></h5>
                    <p class="card-text small text-muted">Waca katrangan lengkap lan analisis mendalam tumrap {cat} ugi perkembanganipun...</p>
                </div>
                <div class="card-footer bg-white border-0 pb-3">
                    <a href="{fname}" class="btn btn-outline-warning btn-sm fw-bold">Waca Selengkapnya</a>
                </div>
            </div>
        </div>
        """
    index_content += f"""
    </div>
</div>

<footer class="pt-5 pb-4 border-top border-warning bg-dark text-white mt-5">
<div class="container text-center text-md-start">
<div class="row">
<div class="col-md-4 mb-4">
<h5 class="text-white fw-bold mb-3"><span class="rainbow-text">PAWARTA</span></h5>
<p class="small text-secondary">Portal warta digital inovatif kang nyawijiake kabudayan Jawi, aksara Honocoroko, lan teknologi informasi modheren ing donya maya.</p>
<div class="fs-4 text-warning">ꦫꦲꦪꦸ ꦫꦲꦪꦸ ꦫꦲꦪꦸ</div>
</div>
<div class="col-md-4 mb-4">
<h6 class="text-white fw-bold mb-3">Pranala Kaca</h6>
<ul class="list-unstyled small">
<li><a href="https://pawarta.github.io/index.html" class="text-decoration-none text-secondary">Beranda / Index</a></li>
<li><a href="sitemap.html" class="text-decoration-none text-secondary">Sitemap HTML</a></li>
<li><a href="sitemap.xml" class="text-decoration-none text-secondary">Sitemap XML</a></li>
</ul>
</div>
<div class="col-md-4 mb-4">
<h6 class="text-white fw-bold mb-3">Informasi Aliran Data</h6>
<p class="small text-secondary mb-1">Nama Aliran: <strong>pawarta</strong></p>
<p class="small text-secondary mb-1">ID Pengukuran: <code class="text-warning">G-GN5PGKKM3T</code></p>
<p class="small text-secondary">URL: <a href="https://pawarta.github.io" class="text-warning text-decoration-none">https://pawarta.github.io</a></p>
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
</body>
</html>
"""
    with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_content)

    # Sitemap HTML
    sitemap_html = f"""<!DOCTYPE html>
<html lang="jv">
<head>
<meta charset="UTF-8">
<title>Sitemap {cat} - PAWARTA</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container my-5">
    <h1 class="fw-bold mb-4">Sitemap Kategori: {cat}</h1>
    <ul class="list-group">
        <li class="list-group-item"><a href="index.html">Index {cat}</a></li>
"""
    for fname, ftitle in articles:
        sitemap_html += f'        <li class="list-group-item"><a href="{fname}">{ftitle}</a></li>\n'
    sitemap_html += """    </ul>
</div>
</body>
</html>
"""
    with open(os.path.join(cat_dir, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_html)

    # Sitemap XML
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://pawarta.github.io/{cat_slug}/index.html</loc>
        <changefreq>daily</changefreq>
    </url>
"""
    for fname, _ in articles:
        sitemap_xml += f"""    <url>
        <loc>https://pawarta.github.io/{cat_slug}/{fname}</loc>
        <changefreq>weekly</changefreq>
    </url>
"""
    sitemap_xml += "</urlset>"
    with open(os.path.join(cat_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    # Sitemap TXT
    sitemap_txt = f"https://pawarta.github.io/{cat_slug}/index.html\n"
    for fname, _ in articles:
        sitemap_txt += f"https://pawarta.github.io/{cat_slug}/{fname}\n"
    with open(os.path.join(cat_dir, "sitemap.txt"), "w", encoding="utf-8") as f:
        f.write(sitemap_txt)

print("Kabeh file direktori, indeks, sitemap, lan 30 artikel saben kategori wis sukses digawe ing folder 'pawarta_site'!")

