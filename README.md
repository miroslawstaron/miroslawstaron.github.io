# Miroslaw Staron Personal Website

This repository contains the source for `https://miroslawstaron.github.io/`.

The site is a personal academic website built on top of the HTML5 UP "Editorial" template and then customized with additional static pages, Reveal.js slide pages, course material, and writing resources.

## What This Site Contains

The site currently includes:

- A homepage with profile information and books.
- Course pages for PhD-level material.
- A writing advice page for students.
- A standalone Reveal.js publications page.
- A standalone Reveal.js hallucinations/reports page.

Everything is static HTML, CSS, JavaScript, images, and PDFs. There is no build step required for normal edits.

## Main Pages

- `index.html`
  - Main homepage.
  - Contains the profile intro, books section, and the sidebar menu.

- `generic.html`
  - PhD course page for Action Research in Software Engineering.

- `phd-course-measurement.html`
  - PhD course page for Software Development Measurement Programs.

- `writing-advice.html`
  - Curated advice page for academic writing in software engineering.
  - Includes a table of contents, section anchors, curated external links, and writing tips.

- `pubs.html`
  - Standalone Reveal.js slide deck with selected publications from 2025 and 2026.
  - Uses `styles.css` for local styling.

- `hallucinations.html`
  - Standalone Reveal.js slide deck linking to unpublished reports and AI-generated material.
  - Uses `styles.css` for local styling.

## Supporting Files

- `styles.css`
  - Shared stylesheet for the standalone Reveal.js pages (`pubs.html` and `hallucinations.html`).
  - If the layout of those pages looks wrong, this is the first file to check.

- `hallucinations/`
  - Stores PDF files linked from `hallucinations.html`.

- `images/`
  - Site images used by the homepage and other standard pages.

- `assets/css/main.css`
  - Main stylesheet for the HTML5 UP site layout.

- `assets/js/`
  - Template JavaScript used by the site layout and sidebar behavior.

- `README.txt`
  - Original template readme from HTML5 UP.

## How the Site Is Organized

There are effectively two page types:

1. Standard site pages
   - Examples: `index.html`, `generic.html`, `phd-course-measurement.html`, `writing-advice.html`
   - These use the HTML5 UP structure with:
     - `#wrapper`
     - `#main`
     - `#sidebar`
     - shared sidebar navigation

2. Standalone Reveal.js pages
   - Examples: `pubs.html`, `hallucinations.html`
   - These are separate full-page slide experiences.
   - They do not use the normal sidebar layout.
   - They include Reveal.js from CDN and use `styles.css`.

## How To Edit Existing Pages

### Standard site pages

For pages like `index.html` or `writing-advice.html`:

- Edit the page HTML directly.
- If you change the sidebar menu, make the same change in all standard pages that contain the shared menu.
- If you add external links, prefer:
  - `target="_blank"`
  - `rel="noreferrer"`

### Reveal.js pages

For pages like `pubs.html` and `hallucinations.html`:

- Edit the HTML page directly.
- Update content in the JavaScript data arrays if the slides are generated programmatically.
- Update `styles.css` if you need layout, spacing, typography, or responsive fixes.

## How To Add a New Standard Page

Use this when adding a normal content page with the site sidebar.

1. Copy an existing standard page such as `generic.html` or `writing-advice.html`.
2. Rename it to the new page name, for example `new-page.html`.
3. Update:
   - page `<title>`
   - main header `<h1>`
   - body content
4. Add a link to the sidebar menu in all standard pages that should expose it.
5. If the page should be reachable from the homepage, add a visible link there as well.

## How To Add a New Reveal.js Page

Use this when adding another slide-based standalone page similar to `pubs.html`.

1. Copy `pubs.html` or `hallucinations.html`.
2. Rename it, for example `new-slides.html`.
3. Update:
   - page `<title>`
   - hero slide text
   - slide data in the JavaScript block
   - back link at the top of the page
4. Reuse `styles.css` unless the new slide deck truly needs a different look.
5. Add a link to the page from the appropriate menu location in the standard pages.

## How To Add Downloadable Files

For documents such as PDFs:

1. Create a dedicated subfolder if needed, for example `reports/` or `hallucinations/`.
2. Copy the files into that folder.
3. Link to them using relative paths, for example:
   - `reports/my-paper.pdf`
4. If the files are referenced from a Reveal page, update the page's JavaScript data array.

## Menu Maintenance

The sidebar menu is duplicated across multiple standard pages. That means menu updates are manual.

When adding or renaming a menu item, update at least:

- `index.html`
- `generic.html`
- `phd-course-measurement.html`
- `writing-advice.html`

If you forget one page, the site will feel inconsistent.

## Styling Notes

- `assets/css/main.css` controls the standard website look.
- `styles.css` controls the standalone Reveal pages.
- If a Reveal intro slide looks too large or too narrow, check:
  - `.hero-compact`
  - `.publication-slide`
  - `.summary-slide`
  - `.detail-grid`

## Deployment

The site is published through GitHub Pages from the `main` branch of this repository.

Typical workflow:

1. Edit files locally.
2. Review with `git status`.
3. Commit changes.
4. Push to `main`.
5. Wait for GitHub Pages to publish the update.

## Suggested Future Improvements

- Move duplicated sidebar markup into a templating workflow if the site grows further.
- Add a dedicated landing page for publications instead of only a Reveal deck.
- Add a short README section for image sizing and preferred asset formats.
- Consider a local link checker if the writing-advice page continues to grow.

## Copyright

Unless otherwise stated, the original content of this website is copyright Miroslaw Staron.

This includes, for example:

- text content written for the site
- curated academic resources and page structure
- custom standalone Reveal.js pages and their content
- locally added PDFs and supporting materials where ownership permits publication

Third-party template and library assets remain under their own licenses.

## Template Credits

This site is based on the "Editorial" template by HTML5 UP.

Editorial by HTML5 UP  
`html5up.net` | `@ajlkn`  
Free for personal and commercial use under the CCA 3.0 license (`html5up.net/license`)

Say hello to Editorial, a blog/magazine-ish template built around a toggleable "locking"
sidebar and an accordion-style menu.

Demo images courtesy of Unsplash, a collection of CC0/public-domain images.

AJ  
`aj@lkn.io` | `@ajlkn`

### Original Template Credits

- Demo Images: Unsplash (`unsplash.com`)
- Icons: Font Awesome (`fontawesome.io`)
- Other:
  - jQuery (`jquery.com`)
  - Responsive Tools (`github.com/ajlkn/responsive-tools`)
