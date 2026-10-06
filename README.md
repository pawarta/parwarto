# PAWARTA — Javanese culture and news portal

A static site built with Bootstrap 5. `generate_blog.py` (content data in `blog_content.py`) creates 69 categories × 30 SEO articles, plus a sitemap for each category.

## Running it
- For GitHub Pages: `python3 generate_blog.py` writes into the repository root
- For Netlify: `python3 generate_blog.py --out dist --copy-static` (already set in netlify.toml)

## Roadmap
- Rewrite key articles by hand, add custom images for each category, and connect the newsletter.
