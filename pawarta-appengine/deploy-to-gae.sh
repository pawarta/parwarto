#!/bin/bash
# Script ONE-STEP untuk generate + deploy PAWARTA ke App Engine
# Gunakan: bash deploy-to-gae.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ENGINE_DIR="$REPO_ROOT/pawarta-appengine"
GENERATOR_DIR="$APP_ENGINE_DIR/generator"
PROJECT_ID="${1:-pawarta}"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🚀 PAWARTA Deployment - Google Cloud App Engine"
echo "════════════════════════════════════════════════════════════"
echo ""

# COLOR CODES
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_step() { echo -e "${BLUE}➜${NC} $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠️ ${NC}$1"; }

# 1. CHECK GCLOUD
log_step "Checking gcloud CLI..."
if ! command -v gcloud &> /dev/null; then
    log_error "gcloud CLI not installed"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
log_success "gcloud CLI found: $(gcloud --version | head -1)"

# 2. CHECK PYTHON3
log_step "Checking Python3..."
if ! command -v python3 &> /dev/null; then
    log_error "Python3 not installed"
    exit 1
fi
log_success "Python3 found: $(python3 --version)"

# 3. VERIFY PROJECT STRUCTURE
log_step "Verifying project structure..."
if [ ! -f "$REPO_ROOT/generate_blog.py" ]; then
    log_error "generate_blog.py not found"
    exit 1
fi
if [ ! -f "$REPO_ROOT/blog_content.py" ]; then
    log_error "blog_content.py not found"
    exit 1
fi
if [ ! -f "$APP_ENGINE_DIR/main.py" ]; then
    log_error "main.py not found in pawarta-appengine/"
    exit 1
fi
if [ ! -f "$APP_ENGINE_DIR/app.yaml" ]; then
    log_error "app.yaml not found in pawarta-appengine/"
    exit 1
fi
log_success "All required files present"

# 4. AUTHENTICATE GCLOUD
log_step "Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    log_warning "Not authenticated. Opening login..."
    gcloud auth login
fi
CURRENT_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
log_success "Authenticated as: $CURRENT_ACCOUNT"

# 5. SET PROJECT
log_step "Setting project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID" 2>/dev/null || {
    log_error "Failed to set project. Check if project '$PROJECT_ID' exists."
    echo ""
    echo "Available projects:"
    gcloud projects list --format="value(project_id)" | head -10
    exit 1
}
log_success "Project set to: $(gcloud config get-value project)"

# 6. CLEAN OLD GENERATOR
log_step "Preparing generator folder..."
if [ -d "$GENERATOR_DIR" ]; then
    log_warning "Removing old generator folder..."
    rm -rf "$GENERATOR_DIR"
fi
mkdir -p "$GENERATOR_DIR"
log_success "Generator folder ready: $GENERATOR_DIR"

# 7. GENERATE STATIC SITE
log_step "Generating static site (this may take a minute)..."
cd "$REPO_ROOT"

SITE_URL="https://${PROJECT_ID}.appspot.com"
echo "   Site URL: $SITE_URL"

python3 generate_blog.py \
    --out "$GENERATOR_DIR" \
    --copy-static \
    --site-url "$SITE_URL" 2>&1 | tail -5

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    log_error "Failed to generate static site"
    exit 1
fi
log_success "Static site generated"

# 8. VERIFY GENERATOR CONTENTS
log_step "Verifying generator folder..."
if [ ! -f "$GENERATOR_DIR/index.html" ]; then
    log_error "index.html not found in generator folder"
    ls -la "$GENERATOR_DIR" | head -20
    exit 1
fi

FILE_COUNT=$(find "$GENERATOR_DIR" -type f | wc -l)
DIR_COUNT=$(find "$GENERATOR_DIR" -type d | wc -l)

log_success "Generator folder contains:"
echo "   Files: $FILE_COUNT"
echo "   Directories: $DIR_COUNT"

# Check important files
echo ""
echo "   Checking important files:"
for file in index.html assets/blog.css assets/blog.js search.json robots.txt sitemap.xml; do
    if [ -f "$GENERATOR_DIR/$file" ]; then
        SIZE=$(du -h "$GENERATOR_DIR/$file" | cut -f1)
        echo -e "      ${GREEN}✓${NC} $file ($SIZE)"
    else
        echo -e "      ${YELLOW}!${NC} $file (not found)"
    fi
done

# 9. VERIFY APP ENGINE FILES
log_step "Verifying App Engine configuration..."
cd "$APP_ENGINE_DIR"
echo "   app.yaml:"
cat app.yaml | sed 's/^/      /'
echo ""
echo "   requirements.txt:"
cat requirements.txt | sed 's/^/      /'

# 10. FINAL CONFIRMATION
echo ""
echo "════════════════════════════════════════════════════════════"
echo "📋 DEPLOYMENT SUMMARY"
echo "════════════════════════════════════════════════════════════"
echo "   Project ID: $PROJECT_ID"
echo "   Site URL: $SITE_URL"
echo "   Generator: $GENERATOR_DIR ($FILE_COUNT files)"
echo "   Status: ${GREEN}READY TO DEPLOY${NC}"
echo ""
read -p "Continue with deployment? (y/n) " -n 1 -r REPLY
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_warning "Deployment cancelled"
    exit 0
fi

# 11. DEPLOY TO APP ENGINE
echo ""
log_step "Deploying to Google Cloud App Engine..."
echo "   (This may take 2-5 minutes)"
echo ""

cd "$APP_ENGINE_DIR"
if gcloud app deploy --quiet --project="$PROJECT_ID"; then
    log_success "Deployment completed successfully!"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "🎉 DEPLOYMENT SUCCESS"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 Your site is now live at:"
    echo "   ${GREEN}https://${PROJECT_ID}.appspot.com${NC}"
    echo ""
    echo "📊 Useful commands:"
    echo "   • View logs:      gcloud app logs read -f"
    echo "   • Redeploy:       bash deploy-to-gae.sh"
    echo "   • Open in browser: gcloud app browse"
    echo ""
else
    log_error "Deployment failed"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check app.yaml syntax: gcloud app deploy --no-promote"
    echo "2. View error logs: gcloud app logs read"
    echo "3. Verify project settings: gcloud config list"
    echo ""
    exit 1
fi
