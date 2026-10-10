#!/bin/bash
# Script GENERATE halaman statis PAWARTA sebelum deploy
# Gunakan: bash generate-site.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ENGINE_DIR="$REPO_ROOT/pawarta-appengine"
GENERATOR_DIR="$APP_ENGINE_DIR/generator"

echo "════════════════════════════════════════════════════════════"
echo "PAWARTA - Generator Situs Statis"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📂 Direktori:"
echo "   Repo Root: $REPO_ROOT"
echo "   App Engine: $APP_ENGINE_DIR"
echo "   Generator: $GENERATOR_DIR"
echo ""

# 1. Cek prasyarat
echo "🔍 Step 1: Cek prasyarat..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 tidak terinstall"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"
echo ""

# 2. Cek generate_blog.py ada
echo "📋 Step 2: Cek file generate_blog.py..."
if [ ! -f "$REPO_ROOT/generate_blog.py" ]; then
    echo "❌ Error: generate_blog.py tidak ditemukan di root repo"
    exit 1
fi

if [ ! -f "$REPO_ROOT/blog_content.py" ]; then
    echo "❌ Error: blog_content.py tidak ditemukan di root repo"
    exit 1
fi

echo "✅ File generator ada"
echo ""

# 3. Hapus folder lama kalau ada
echo "🧹 Step 3: Persiapkan folder generator..."
if [ -d "$GENERATOR_DIR" ]; then
    echo "   Menghapus folder generator lama..."
    rm -rf "$GENERATOR_DIR"
fi

mkdir -p "$GENERATOR_DIR"
echo "✅ Folder generator siap"
echo ""

# 4. Generate situs
echo "⚙️  Step 4: Generate situs statis (ini akan butuh beberapa detik)..."
cd "$REPO_ROOT"

# URL untuk situs App Engine
SITE_URL="https://pawarta.appspot.com"

python3 generate_blog.py \
    --out "$GENERATOR_DIR" \
    --copy-static \
    --site-url "$SITE_URL"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Generate BERHASIL!"
else
    echo ""
    echo "❌ Generate GAGAL - cek error di atas"
    exit 1
fi
echo ""

# 5. Verifikasi hasil
echo "📊 Step 5: Verifikasi hasil generate..."
if [ ! -f "$GENERATOR_DIR/index.html" ]; then
    echo "❌ Error: index.html tidak ada di generator folder"
    exit 1
fi

file_count=$(find "$GENERATOR_DIR" -type f | wc -l)
dir_count=$(find "$GENERATOR_DIR" -type d | wc -l)

echo "✅ Generator folder berisi:"
echo "   - File: $file_count"
echo "   - Folder: $dir_count"
echo ""

# Cek file penting
important_files=(
    "index.html"
    "assets/blog.css"
    "assets/blog.js"
    "search.json"
    "robots.txt"
    "sitemap.xml"
)

echo "   File penting:"
for file in "${important_files[@]}"; do
    if [ -f "$GENERATOR_DIR/$file" ]; then
        size=$(du -h "$GENERATOR_DIR/$file" | cut -f1)
        echo "      ✅ $file ($size)"
    else
        echo "      ⚠️  $file (TIDAK ADA)"
    fi
done
echo ""

# 6. Cek folder kategori
echo "   Folder kategori (sample):"
category_count=$(find "$GENERATOR_DIR" -maxdepth 1 -type d -name "[a-z]*" | wc -l)
echo "      Ditemukan: $category_count folder kategori"
sample_categories=$(find "$GENERATOR_DIR" -maxdepth 1 -type d -name "[a-z]*" | head -5 | xargs -I {} basename {})
echo "      Contoh: $sample_categories"
echo ""

# 7. Summary
echo "════════════════════════════════════════════════════════════"
echo "✅ GENERATE BERHASIL - SIAP UNTUK DEPLOY"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📂 Folder generator di:"
echo "   $GENERATOR_DIR"
echo ""
echo "🚀 Langkah berikutnya:"
echo "   1. Cek file dengan: ls -la $GENERATOR_DIR | head"
echo "   2. Deploy dengan: bash pawarta-appengine/deploy-to-gae.sh"
echo ""
