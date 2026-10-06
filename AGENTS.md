# AGENTS
- A static site. The Netlify build runs `generate_blog.py` and puts its output in `dist/`. Do not commit the generated pages.
- `blog_content.py`: categories, topic groups, external references and sentence templates. `generate_blog.py`: layout (head, navbar, sidebar, footer), pages and sitemaps.
- Randomness is seeded per article, so the output is the same on every run. The site URL comes from the `SITE_URL` or `URL` environment variable.
- If `img/blog/<group>.jpg` is missing, pages fall back to the images in `img/`.
- The contact form uses Netlify Forms (`kontak-pawarta`) with an AJAX POST to `/`.
