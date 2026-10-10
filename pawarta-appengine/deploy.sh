#!/bin/bash
# Script deploy PAWARTA ke Google Cloud App Engine
# Gunakan: bash deploy.sh [project-id]
# Contoh: bash deploy.sh pawarta

set -e  # Exit kalau ada error

PROJECT_ID="${1:-pawarta}"
REGION="${2:-asia-southeast2}"
APP_ENGINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$APP_ENGINE_DIR")"

echo "════════════════════════════════════════════════════════════"
echo "PAWARTA Deployment Script untuk Google Cloud App Engine"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 Konfigurasi:"
echo "   Project ID: $PROJECT_ID"
echo "   Region: $REGION"
echo "   App Engine Dir: $APP_ENGINE_DIR"
echo "   Repo Root: $REPO_ROOT"
echo ""

# 1. Check prerequisites
echo "🔍 Step 1: Cek prasyarat..."
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI tidak terinstall"
    echo "   Install dari: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 tidak terinstall"
    exit 1
fi

echo "✅ gcloud dan Python3 sudah terinstall"
echo ""

# 2. Validate gcloud auth
echo "🔑 Step 2: Cek autentikasi Google Cloud..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "⚠️  Belum login. Silakan login:"
    gcloud auth login
fi
echo "✅ Sudah terautentikasi"
echo ""

# 3. Set project
echo "🎯 Step 3: Set project Google Cloud..."
gcloud config set project "$PROJECT_ID"
gcloud config set compute/region "$REGION"
echo "✅ Project: $(gcloud config get-value project)"
echo ""

# 4. Generate static site
echo "🔨 Step 4: Generate situs statis ke generator folder..."
cd "$REPO_ROOT"
python3 generate_blog.py --out "$APP_ENGINE_DIR/generator" --copy-static
if [ $? -eq 0 ]; then
    echo "✅ Situs statis berhasil dihasilkan"
else
    echo "❌ Error saat generate situs"
    exit 1
fi
echo ""

# 5. Verify generator folder
echo "📂 Step 5: Verifikasi folder generator..."
if [ ! -d "$APP_ENGINE_DIR/generator" ]; then
    echo "❌ Error: Folder generator tidak ada"
    exit 1
fi

file_count=$(find "$APP_ENGINE_DIR/generator" -type f | wc -l)
echo "✅ Folder generator ada dengan $file_count file"
ls -lah "$APP_ENGINE_DIR/generator" | head -10
echo ""

# 6. Test Flask locally (optional)
echo "🧪 Step 6: Test Flask app lokal (optional)..."
read -p "   Jalankan test Flask lokal? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$APP_ENGINE_DIR"
    python3 -m pip install -q -r requirements.txt
    echo "   Starting Flask server pada http://127.0.0.1:8080 (tekan Ctrl+C untuk stop)"
    timeout 10 python3 main.py || true
    echo "✅ Test Flask selesai"
else
    echo "⏭️  Skip test Flask"
fi
echo ""

# 7. Check App Engine readiness
echo "🔐 Step 7: Cek kesiapan App Engine..."
cd "$APP_ENGINE_DIR"

if [ ! -f "app.yaml" ]; then
    echo "❌ Error: app.yaml tidak ditemukan"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py tidak ditemukan"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt tidak ditemukan"
    exit 1
fi

echo "✅ Semua file konfigurasi sudah ada"
echo ""
echo "   app.yaml:"
cat app.yaml | head -3
echo ""
echo "   requirements.txt:"
cat requirements.txt
echo ""

# 8. Final confirmation
echo "════════════════════════════════════════════════════════════"
echo "🚀 SIAP UNTUK DEPLOY"
echo "════════════════════════════════════════════════════════════"
echo ""
read -p "Lanjutkan deploy ke $PROJECT_ID? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment dibatalkan"
    exit 0
fi
echo ""

# 9. Deploy
echo "⚡ Step 8: Deploy ke Google Cloud App Engine..."
cd "$APP_ENGINE_DIR"
gcloud app deploy --quiet --project="$PROJECT_ID"

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "✅ DEPLOYMENT BERHASIL!"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 Situs Anda tersedia di:"
    echo "   https://$PROJECT_ID.appspot.com"
    echo ""
    echo "📊 Lihat logs:"
    echo "   gcloud app logs read -f"
    echo ""
    echo "🔄 Redeploy di masa depan:"
    echo "   bash deploy.sh $PROJECT_ID"
    echo ""
else
    echo ""
    echo "❌ Deployment GAGAL"
    echo "Silakan cek error di atas"
    exit 1
fi
