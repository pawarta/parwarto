import os
import xml.etree.ElementTree as ET
from datetime import datetime


CATEGORIES = [
    "home", "market", "finance", "macro", "micro", "economy", "explainers",
    "manufacturing", "property", "health", "education", "lifestyle", "hospitality",
    "tech", "media", "smes", "luxury", "whos-who", "international", "local-resources",
    "politics", "culture", "science", "public-policy", "business", "news", "sports",
    "arts", "celebrities", "automotive", "commentary", "interview", "money",
    "perbankan", "belanja", "sharia", "football", "opinion", "video", "kisah",
    "index", "sejarah", "entrepreneur", "research", "photo", "olahraga",
    "selebritis", "country", "dki", "diy", "jabar", "jatim", "jateng", "aceh",
    "papua", "kalimantan", "sumatra", "sulawesi", "bali", "asia", "afrika",
    "australia", "rusia", "eropa", "amerika", "ai", "teknologi", "astronomi",
    "zodiak","matematika","ipa","ips","biologi","sejarah","fisika","bahasa indonesia","bahasa inggris","bahasa arab","bahasa jawa","sd","smp","sma","smk","d3","sarjana","tools","software","generator","ai","berita","gambar","penerbangan","lokal","mancanegara","maps"
]

TOTAL_ARTICLES_PER_CAT = 30

def get_html_template(title, category, content_body, canonical_url, meta_desc):
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - PAWARTA</title>

    <!-- Meta SEO & Verification -->
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="pawarta, {category}, warta jawa, berita jawa, honocoroko, aksara jawa, portal warta, pawarta github io">
    <meta name="robots" content="index, follow">
    <meta name="google-site-verification" content="IAcn_DcNzAkFuMAjiMDNMoUEMZV5oKau1XrJ4aDJlRc">
    <meta name="msvalidate.01" content="E9411F953448412F854C1FBA584B1383">
    
    <!-- Google AdSense -->
    <script async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9308517202792186"></script>
    <script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>

    <!-- Open Graph / Social Media Meta -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="https://pawarta.github.io/pawarta.jpg">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="article">

    <!-- Favicon & Icons -->
    <link rel="icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">
    <link rel="shortcut icon" href="https://pawarta.github.io/pawarta.ico" type="image/x-icon">

    <!-- Canonical & Hreflang Links -->
    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" href="https://pawarta.github.io/" hreflang="x-default">
    <link rel="alternate" href="https://pawarta.github.io/id/" hreflang="id">

    <!-- Stylesheets (Bootstrap 5, Icons, Animate.css, AOS) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
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
    <style>
        .rainbow-text {{ background: linear-gradient(45deg, #d4af37, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .honocoroko-title {{ font-family: serif; color: #d4af37; letter-spacing: 2px; }}
        .carousel-item {{ height: 350px; background-size: cover; background-position: center; }}
        .carousel-overlay {{ position: absolute; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.6); }}
    </style>
</head>
<body class="bg-light">

    <!-- Header & Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="https://pawarta.github.io/index.html">
                <img src="https://pawarta.github.io/pawarta.jpg" alt="Logo Pawarta" width="40" height="40" class="rounded-circle" onerror="this.src='https://placehold.co/40x40/d4af37/ffffff?text=P'">
                <div>
                    <span class="rainbow-text fs-4 fw-bold">PAWARTA</span>
                    <div style="font-size: 10px; color: #d4af37;">ꦥꦮꦂꦠ - Javanese Portal</div>
                </div>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item"><a class="nav-link active" href="https://pawarta.github.io/index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/market/index.html">Market</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/tech/index.html">Tech</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/news/index.html">News</a></li>
                    <li class="nav-item"><a class="nav-link" href="https://pawarta.github.io/culture/index.html">Culture</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container my-5">
        <div class="row">
            <!-- Article Body -->
            <div class="col-lg-8" data-aos="fade-up">
                <article class="bg-white p-4 p-md-5 rounded-4 shadow-sm border mb-4">
                    <span class="badge bg-warning text-dark mb-2 text-uppercase">{category}</span>
                    <h1 class="fw-bold mb-3">{title}</h1>
                    <div class="text-muted small mb-4">Diterbitake dening Redaksi PAWARTA | Tanggal: {datetime.now().strftime('%Y-%m-%d')} | ꦫꦲꦪꦸ</div>
                    
                    <!-- Featured Image -->
                    <div class="mb-4 text-center">
                        <img src="https://placehold.co/800x450/212529/d4af37?text={category.upper()}+PAWARTA" alt="{title} - Portal Warta Jawi" class="img-fluid rounded shadow-sm" onerror="this.src='https://placehold.co/800x450/212529/d4af37?text=PAWARTA'">
                    </div>

                    <!-- AdSense Banner -->
                    <div class="my-4 text-center">
                        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9308517202792186" data-ad-slot="8374036730" data-ad-format="auto" data-full-width-responsive="true"></ins>
                        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                    </div>

                    {content_body}

                    <!-- Social Share -->
                    <div class="card bg-light border-0 my-4 p-3 rounded-3">
                        <h5 class="fw-bold mb-2">Sebarkake Warta Menika:</h5>
                        <div class="d-flex gap-2">
                            <a href="#" class="btn btn-primary btn-sm"><i class="bi bi-facebook"></i> Facebook</a>
                            <a href="#" class="btn btn-info btn-sm text-white"><i class="bi bi-twitter"></i> Twitter</a>
                            <a href="#" class="btn btn-success btn-sm"><i class="bi bi-whatsapp"></i> WhatsApp</a>
                            <a href="#" class="btn btn-danger btn-sm"><i class="bi bi-envelope"></i> Email</a>
                        </div>
                    </div>

                    <!-- Contact Form Box -->
                    <div class="card border-warning my-4 p-4 shadow-sm">
                        <h4 class="fw-bold mb-3 text-warning">Kirim Tanggapan utawa Pitaken</h4>
                        <form onsubmit="event.preventDefault(); alert('Matur nuwun! Tanggapan panjenengan sampun katampi.');">
                            <div class="mb-3">
                                <label class="form-label">Asma Lengkap</label>
                                <input type="text" class="form-control" required placeholder="Sêkar / Budi...">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Alamat Email</label>
                                <input type="email" class="form-control" required placeholder="email@domain.com">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Pesen Panjenengan</label>
                                <textarea class="form-control" rows="3" required placeholder="Tulis irah-irah utawa pitaken..."></textarea>
                            </div>
                            <button type="submit" class="btn btn-warning fw-bold">Kirim Pesen</button>
                        </form>
                    </div>

                </article>
            </div>

            <!-- Sidebar -->
            <div class="col-lg-4">
                <!-- Popular Articles -->
                <div class="card shadow-sm border-0 mb-4 p-3">
                    <h5 class="fw-bold border-bottom pb-2 text-dark"><i class="bi bi-fire text-danger"></i> Artikel Populer</h5>
                    <ul class="list-unstyled mb-0 small">
                        <li class="mb-2 pb-2 border-bottom"><a href="artikel1.html" class="text-decoration-none text-dark fw-semibold">Pangembangan Teknologi Digital lan Kearifan Lokal Jawi Modern</a></li>
                        <li class="mb-2 pb-2 border-bottom"><a href="artikel2.html" class="text-decoration-none text-dark fw-semibold">Pewarisan Aksara Honocoroko ing Era Artificial Intelligence</a></li>
                        <li><a href="artikel3.html" class="text-decoration-none text-dark fw-semibold">Strategi Ekonomi Kreatif Digital tumrap UMKM Nusantara</a></li>
                    </ul>
                </div>

                <!-- Latest Articles -->
                <div class="card shadow-sm border-0 mb-4 p-3">
                    <h5 class="fw-bold border-bottom pb-2 text-dark"><i class="bi bi-clock text-primary"></i> Artikel Terbaru</h5>
                    <ul class="list-unstyled mb-0 small">
                        <li class="mb-2 pb-2 border-bottom"><a href="artikel15.html" class="text-decoration-none text-dark">Inovasi Kebudayaan lan Informasi Global 2026</a></li>
                        <li class="mb-2 pb-2 border-bottom"><a href="artikel16.html" class="text-decoration-none text-dark">Transformasi Kebijakan Publik Berbasis Digital</a></li>
                        <li><a href="artikel17.html" class="text-decoration-none text-dark">Eksplorasi Ruang Siber lan Keamanan Data Wilayah</a></li>
                    </ul>
                </div>

                <!-- Oldest Articles -->
                <div class="card shadow-sm border-0 mb-4 p-3">
                    <h5 class="fw-bold border-bottom pb-2 text-dark"><i class="bi bi-archive text-secondary"></i> Artikel Terlama & Arsip</h5>
                    <ul class="list-unstyled mb-0 small">
                        <li class="mb-2"><a href="artikel30.html" class="text-decoration-none text-muted">Arsip Sejarah Wiwitan Portal Pawarta</a></li>
                        <li class="mb-2"><a href="artikel29.html" class="text-decoration-none text-muted">Dokumentasi Awal Budaya Jawi Digital</a></li>
                    </ul>
                </div>

                <!-- Labels / Tags -->
                <div class="card shadow-sm border-0 mb-4 p-3">
                    <h5 class="fw-bold border-bottom pb-2 text-dark"><i class="bi bi-tags text-warning"></i> Label / Kategori</h5>
                    <div class="d-flex flex-wrap gap-1">
                        <a href="https://pawarta.github.io/tech/index.html" class="badge bg-secondary text-decoration-none">Tech</a>
                        <a href="https://pawarta.github.io/culture/index.html" class="badge bg-secondary text-decoration-none">Culture</a>
                        <a href="https://pawarta.github.io/market/index.html" class="badge bg-secondary text-decoration-none">Market</a>
                        <a href="https://pawarta.github.io/news/index.html" class="badge bg-secondary text-decoration-none">News</a>
                        <a href="https://pawarta.github.io/ai/index.html" class="badge bg-secondary text-decoration-none">AI</a>
                    </div>
                </div>

                <!-- AdSense Sidebar Banner -->
                <div class="card shadow-sm border-0 p-3 text-center">
                    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9308517202792186" data-ad-slot="8374036730" data-ad-format="auto"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="pt-5 pb-4 bg-dark text-white border-top border-warning">
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
                        <li><a href="https://pawarta.github.io/sitemap.html" class="text-decoration-none text-secondary">Sitemap HTML</a></li>
                        <li><a href="https://pawarta.github.io/sitemap.xml" class="text-decoration-none text-secondary">Sitemap XML</a></li>
                        <li><a href="https://pawarta.github.io/sitemap.txt" class="text-decoration-none text-secondary">Sitemap TXT</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-4">
                    <h6 class="text-white fw-bold mb-3">Informasi Aliran Data</h6>
                    <p class="small text-secondary mb-1">Nama Aliran: <strong>pawarta</strong></p>
                    <p class="small text-secondary mb-1">ID Pengukuran: <code class="text-warning">G-GN5PGKKM3T</code></p>
                    <p class="small text-secondary">URL: <a href="https://pawarta.github.io" target="_blank" class="text-warning">https://pawarta.github.io</a></p>
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
        AOS.init({{ duration: 1000, once: true }});
    </script>
</body>
</html>
"""

def generate_article_content(title, cat_name, index_num):
    return f"""
    <p class="lead fw-semibold text-secondary">Kagali warta lan informasi mendalam ngenani {title} ing kanal khusus {cat_name.upper()} Portal PAWARTA. Minangka sarana digital modheren, kita ngupayakake transparansi, kawruh wiyar, sarta tetep njunjung dhuwur kearifan lokal lan kabudayan Nusantara.</p>

    <!-- Table of Contents -->
    <div class="card bg-light border-0 p-3 mb-4 rounded-3">
        <h5 class="fw-bold text-dark mb-2"><i class="bi bi-list-nested"></i> Tabel Konten (Daftar Isi)</h5>
        <ul class="mb-0 small ps-3">
            <li><a href="#pendahuluan" class="text-decoration-none">1. Pambuka lan Latar Belakang {title}</a></li>
            <li><a href="#analisis" class="text-decoration-none">2. Analisis Komprehensif Sektor {cat_name}</a></li>
            <li><a href="#tabel-data" class="text-decoration-none">3. Tabel Statistik & Perkembangan Kinerja</a></li>
            <li><a href="#tantangan" class="text-decoration-none">4. Tantangan lan Peluang ing Era Digital Modern</a></li>
            <li><a href="#faq" class="text-decoration-none">5. Pitakonan Asring Ditakokake (FAQ)</a></li>
            <li><a href="#kesimpulan" class="text-decoration-none">6. Kesimpulan lan Pangajab</a></li>
        </ul>
    </div>

    <h2 id="pendahuluan" class="fw-bold mt-4 mb-3 text-dark">1. Pambuka lan Latar Belakang {title}</h2>
    <p>Perkembangan teknologi lan dinamika jaman ing taun 2026 nuntut saben sektor supaya luwih adaptif. Lumantar portal <strong>PAWARTA</strong> (<a href="https://pawarta.github.io/" target="_blank">pawarta.github.io</a>), informasi babagan {title} kababar kanthi luwih jero, akurat, sarta gampang diakses dening masarakat. Kanthi dhasar filosofi luhur sarta pedoman jurnalistik profesional, warta menika dipunrancang kanggo nyukupi kabetahan literasi digital panjenengan sedaya.</p>
    <p>Ing konteks modheren, aspek {cat_name} nduweni peran strategis tumrap panguripan bebrayan. Kathah owah-owahan ingkang kedadeyan, wiwit saking tingkat mikro nganti makrokosmos global. Bab menika mbuktekaken bilih kawruh lan informasi minangka kunci utama kemajuan bangsa ing kancah internasional.</p>

    <h2 id="analisis" class="fw-bold mt-4 mb-3 text-dark">2. Analisis Komprehensif Sektor {cat_name}</h2>
    <p>Nalika nggatekake dinamika {title}, wonten kathah babagan ingkang kedah dipunanalisis kanthi premati. Para pengamat lan pakar industri negesaken bilih sinergi antawisipun pamarentah, swasta, lan masyarakat dados pilar utama. Panduan lengkap saged dipuntingali lumantar <a href="https://pawarta.github.io/tech/index.html" target="_blank">Portal Teknologi Pawarta</a> saha referensi pendukung ing <a href="https://pawarta.github.io/market/index.html" target="_blank">Kanal Market & Finance</a>.</p>
    <p>Miturut riset lan observasi, panggunaan teknologi intelijen buatan (AI) saha otomatisasi sampun mlebu ing macem-macem lini. Mangga pirsani ulasan tambahan lumantar <a href="https://pawarta.github.io/ai/index.html" target="_blank">Kanal AI & Teknologi</a> sarta <a href="https://pawarta.github.io/research/index.html" target="_blank">Pusat Riset Nusantara</a> kanggo mangerteni tren paling anyar.</p>

    <!-- Table Content -->
    <h3 id="tabel-data" class="fw-bold mt-4 mb-3 text-dark">3. Tabel Statistik & Perkembangan Kinerja {cat_name}</h3>
    <div class="table-responsive my-3">
        <table class="table table-bordered table-striped">
            <thead class="table-dark">
                <tr>
                    <th>No</th>
                    <th>Indikator Utama</th>
                    <th>Taun 2024</th>
                    <th>Taun 2025</th>
                    <th>Proyeksi 2026</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>Tingkat Pertumbuhan Sektor {cat_name}</td>
                    <td>7.4%</td>
                    <td>8.9%</td>
                    <td>11.2%</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>Adopsi Digital & Sistem Modern</td>
                    <td>62%</td>
                    <td>78%</td>
                    <td>94%</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>Kepuasan Publik / Pengguna</td>
                    <td>81%</td>
                    <td>88%</td>
                    <td>95%</td>
                </tr>
            </tbody>
        </table>
    </div>

    <h2 id="tantangan" class="fw-bold mt-4 mb-3 text-dark">4. Tantangan lan Peluang ing Era Digital Modern</h2>
    <p>Sanadyan kathah kemajuan ingkang dipunraih, tantangan tetep wonten. Mulai saking masalah keamanan siber, literasi digital masyarakat, nganti fluktuasi ekonomi global. Nanging, peluang ingkang kabukak ugi tansah ageng tumrap sinten mawon ingkang siyap berinovasi.</p>
    <p>Kanthi maos artikel menika, para pamiarsa kaajab langkung wiyar wawasanipun. Kanggo sinau luwih jero babagan kabudayan lan kawruh sanesipun, mangga priksa <a href="https://pawarta.github.io/culture/index.html" target="_blank">Kanal Budaya Jawi</a> sarta <a href="https://pawarta.github.io/news/index.html" target="_blank">Kanal Warta Utama</a>.</p>

    <!-- External Links Section (7 links) -->
    <div class="card bg-light border-0 p-3 my-4 rounded-3">
        <h5 class="fw-bold text-dark mb-2"><i class="bi bi-globe"></i> Pranala Eksternal & Referensi Global</h5>
        <ul class="mb-0 small ps-3">
            <li><a href="https://www.wikipedia.org" target="_blank" rel="noopener noreferrer">1. Ensiklopedia Bebas Global (Wikipedia)</a></li>
            <li><a href="https://www.bbc.com" target="_blank" rel="noopener noreferrer">2. Jaringan Berita Internasional (BBC News)</a></li>
            <li><a href="https://www.reuters.com" target="_blank" rel="noopener noreferrer">3. Kantor Berita Finansial & Pasar Global (Reuters)</a></li>
            <li><a href="https://www.github.com" target="_blank" rel="noopener noreferrer">4. Platform Pengembangan Perangkat Lunak & Repositori (GitHub)</a></li>
            <li><a href="https://scholar.google.com" target="_blank" rel="noopener noreferrer">5. Mesin Pencari Literatur Akademik (Google Scholar)</a></li>
            <li><a href="https://www.w3.org" target="_blank" rel="noopener noreferrer">6. Konsorsium Standar Web Global (W3C)</a></li>
            <li><a href="https://www.un.org" target="_blank" rel="noopener noreferrer">7. Organisasi Internasional Perserikatan Bangsa-Bangsa (UN)</a></li>
        </ul>
    </div>

    <!-- FAQ Section -->
    <h2 id="faq" class="fw-bold mt-4 mb-3 text-dark">5. Pitakonan Asring Ditakokake (FAQ)</h2>
    <div class="accordion mb-4" id="faqAccordion">
        <div class="accordion-item">
            <h2 class="accordion-header" id="faqOne">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne">
                    Kapan artikel ngenani {title} menika dipunperbarui?
                </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                    Artikel lan data ing portal PAWARTA dipunperbarui saben dina selaras kaliyan dinamika warta lan informasi paling anyar ing taun 2026.
                </div>
            </div>
        </div>
        <div class="accordion-item">
            <h2 class="accordion-header" id="faqTwo">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo">
                    Kepiye carane ngirim saran utawa artikel menyang portal PAWARTA?
                </button>
            </h2>
            <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                <div class="accordion-body">
                    Panjenengan saged ngisi formulir kontak ingkang cumawis ing sisih ngandhap artikel menika utawa ngubungi redaksi liwat email resmi portal pawarta.github.io.
                </div>
            </div>
        </div>
    </div>

    <!-- Conclusion -->
    <h2 id="kesimpulan" class="fw-bold mt-4 mb-3 text-dark">6. Kesimpulan lan Pangajab</h2>
    <p>Minangka panutup, {title} ing kanal {cat_name} mbuktekaken bilih integrasi antawisipun informasi modheren lan kearifan lokal saged lumaku bebarengan kanthi selaras. Mugi-mugi pawarta menika maringi inspirasi, kawruh, lan manfaat ingkang ageng tumrap sedaya pamiarsa saking pundi mawon. <em>Rahayu sarwa rahajeng, salam budaya lan literasi digital!</em></p>
    """

def main():
    base_dir = "."
    
    # Track all URLs for sitemap generation
    all_urls = []

    print("=== Mlai Generate Direktori lan File PAWARTA ===")

    for cat in CATEGORIES:
        cat_path = os.path.join(base_dir, cat)
        os.makedirs(cat_path, exist_ok=True)
        print(f"Memproses Kategori: /{cat}")

        # 1. Generate Category Index (index.html)
        cat_index_title = f"Kanal {cat.capitalize()} - PAWARTA Portal"
        cat_index_desc = f"Kumpulan warta lan artikel pilihan babagan {cat} ing portal digital PAWARTA."
        cat_index_url = f"https://pawarta.github.io/{cat}/index.html"
        
        cat_index_body = f"""
        <h1 class="fw-bold mb-3">Kanal {cat.capitalize()}</h1>
        <p class="lead">Sugeng rawuh ing kaca utama kanal {cat}. Pirsani bagean artikel pilihan ing ngandhap menika.</p>
        <div class="list-group my-4">
        """
        for i in range(1, TOTAL_ARTICLES_PER_CAT + 1):
            cat_index_body += f'<a href="artikel{i}.html" class="list-group-item list-group-item-action">Artikel {i}: Kabar lan Analisis Pilihan {cat.capitalize()} Bagian {i}</a>\n'
        cat_index_body += "</div>"

        cat_index_html = get_html_template(cat_index_title, cat, cat_index_body, cat_index_url, cat_index_desc)
        with open(os.path.join(cat_path, "index.html"), "w", encoding="utf-8") as f:
            f.write(cat_index_html)
        all_urls.append(cat_index_url)

        # 2. Generate 30 Articles per Category
        for i in range(1, TOTAL_ARTICLES_PER_CAT + 1):
            art_title = f"Artikel {i} {cat.capitalize()} - Informasi Terbaru dan Terlengkap Tahun 2026"
            art_desc = f"Pembahasan komprehensif 3000 kata mengenai {cat} artikel ke-{i} di portal digital pawarta.github.io."
            art_url = f"https://pawarta.github.io/{cat}/artikel{i}.html"
            
            art_body = generate_article_content(art_title, cat, i)
            art_html = get_html_template(art_title, cat, art_body, art_url, art_desc)
            
            with open(os.path.join(cat_path, f"artikel{i}.html"), "w", encoding="utf-8") as f:
                f.write(art_html)
            all_urls.append(art_url)

        # 3. Generate Category sitemap.html
        sitemap_html_content = f"""<!DOCTYPE html>
<html lang="id">
<head><meta charset="UTF-8"><title>Sitemap {cat.capitalize()} - PAWARTA</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body class="container my-5">
    <h1 class="fw-bold mb-4">Sitemap Kanal {cat.capitalize()}</h1>
    <ul class="list-group">
        <li class="list-group-item"><a href="index.html">Index Kanal {cat}</a></li>
"""
        for i in range(1, TOTAL_ARTICLES_PER_CAT + 1):
            sitemap_html_content += f'        <li class="list-group-item"><a href="artikel{i}.html">Artikel {i} - {cat}</a></li>\n'
        sitemap_html_content += "    </ul></body></html>"
        
        with open(os.path.join(cat_path, "sitemap.html"), "w", encoding="utf-8") as f:
            f.write(sitemap_html_content)
        all_urls.append(f"https://pawarta.github.io/{cat}/sitemap.html")

        # 4. Generate Category sitemap.txt
        sitemap_txt_content = f"https://pawarta.github.io/{cat}/index.html\n"
        for i in range(1, TOTAL_ARTICLES_PER_CAT + 1):
            sitemap_txt_content += f"https://pawarta.github.io/{cat}/artikel{i}.html\n"
        
        with open(os.path.join(cat_path, "sitemap.txt"), "w", encoding="utf-8") as f:
            f.write(sitemap_txt_content)

        # 5. Generate Category sitemap.xml
        sitemap_xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        sitemap_xml_content += f'  <url><loc>https://pawarta.github.io/{cat}/index.html</loc></url>\n'
        for i in range(1, TOTAL_ARTICLES_PER_CAT + 1):
            sitemap_xml_content += f'  <url><loc>https://pawarta.github.io/{cat}/artikel{i}.html</loc></url>\n'
        sitemap_xml_content += '</urlset>'
        
        with open(os.path.join(cat_path, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap_xml_content)

    print("=== Proses Pembuatan File Selesai Kabeh! ===")

if __name__ == "__main__":
    main()
