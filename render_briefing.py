#!/usr/bin/env python3
"""Regenerate the static Briefing markup in index.html and archive.html from news.json.

Run from the repo root after every change to news.json:  python3 render_briefing.py
The script rewrites only the content between these markers (never edit it by hand):
  index.html:   <!-- BRIEFING:START --> … <!-- BRIEFING:END -->
                <!-- BRIEFING-LD:START --> … <!-- BRIEFING-LD:END -->
                <!-- BRIEFING-NOTE:START --> … <!-- BRIEFING-NOTE:END -->
  archive.html: <!-- ARCHIVE:START --> … <!-- ARCHIVE:END -->
The client-side JS re-renders the same data and stays in place as a fallback;
the static markup exists so crawlers that do not execute JavaScript (all major
AI crawlers) can read The Briefing.
"""
import json, re, html, sys

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def esc(s):
    return html.escape(str(s), quote=True)


def card(item):
    chip = '<span class="news-chip">%s</span>' % esc(item.get('chip', 'News'))
    if item.get('image'):
        art = ('<div class="news-art photo"><img src="%s" alt="%s" loading="lazy">%s</div>'
               % (esc(item['image']), esc(item.get('title', '')), chip))
    else:
        art = ('<div class="news-art %s">%s<span class="news-art-title">%s</span></div>'
               % (esc(item.get('art', 'yellow')), chip, esc(item.get('artTitle', ''))))
    credit = ('<span class="crediti">%s — </span>' % esc(item['credit'])) if item.get('credit') else ''
    body = ('<div class="news-body"><h3>%s</h3><p>%s%s</p>'
            '<div class="news-meta"><b>%s</b> · %s →</div></div>'
            % (esc(item.get('title', '')), credit, esc(item.get('summary', '')),
               esc(item.get('source', '')), esc(item.get('date', ''))))
    return ('<a class="news-card" href="%s" target="_blank" rel="noopener">%s%s</a>'
            % (esc(item.get('url', '#')), art, body))


def archive_item(item):
    chip = '<span class="chip">%s</span>' % esc(item.get('chip', 'News'))
    credit = ('<span style="font-style:italic;color:#a3a29a">%s — </span>'
              % esc(item['credit'])) if item.get('credit') else ''
    return ('<article class="item">%s<h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>'
            '<p>%s%s</p><div class="meta"><b>%s</b> · %s</div></article>'
            % (chip, esc(item.get('url', '#')), esc(item.get('title', '')),
               credit, esc(item.get('summary', '')),
               esc(item.get('source', '')), esc(item.get('date', ''))))


def replace_between(text, start, end, new_inner, path):
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        sys.exit('ERROR: markers %s…%s not found in %s' % (start, end, path))
    return pattern.sub(start + new_inner + end, text)


def main():
    data = json.load(open('news.json', encoding='utf-8'))
    items = data.get('items', [])
    if not items:
        sys.exit('ERROR: news.json has no items')

    # --- index.html ---
    front = items[:3]
    grid_html = '\n      ' + '\n      '.join(card(i) for i in front) + '\n    '
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "The Briefing — latest curated news on " + data.get('site', ''),
        "itemListElement": [
            {"@type": "ListItem", "position": n + 1,
             "name": i.get('title', ''), "url": i.get('url', '')}
            for n, i in enumerate(front)
        ],
    }
    ld_html = ('\n    <script type="application/ld+json">\n'
               + json.dumps(ld, ensure_ascii=False, indent=2)
               + '\n    </script>\n    ')
    latest = front[0].get('date', '')
    note = ('Curated by humanoid.guide · Latest briefing: %s · Sources linked on each story.'
            % esc(latest))

    idx = open('index.html', encoding='utf-8').read()
    idx = replace_between(idx, '<!-- BRIEFING:START -->', '<!-- BRIEFING:END -->', grid_html, 'index.html')
    idx = replace_between(idx, '<!-- BRIEFING-LD:START -->', '<!-- BRIEFING-LD:END -->', ld_html, 'index.html')
    idx = replace_between(idx, '<!-- BRIEFING-NOTE:START -->', '<!-- BRIEFING-NOTE:END -->', note, 'index.html')
    open('index.html', 'w', encoding='utf-8').write(idx)

    # --- archive.html ---
    ordered = sorted(items, key=lambda i: i.get('iso', ''), reverse=True)
    groups, order = {}, []
    for it in ordered:
        key = (it.get('iso', '') or '')[:7] or 'undated'
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(it)
    sections = []
    for key in order:
        parts = key.split('-')
        title = (MONTHS[int(parts[1]) - 1] + ' ' + parts[0]) if len(parts) == 2 else 'Undated'
        sections.append('<section class="month"><h2>%s</h2>%s</section>'
                        % (esc(title), ''.join(archive_item(i) for i in groups[key])))
    arch_html = '\n    ' + '\n    '.join(sections) + '\n  '

    arch = open('archive.html', encoding='utf-8').read()
    arch = replace_between(arch, '<!-- ARCHIVE:START -->', '<!-- ARCHIVE:END -->', arch_html, 'archive.html')
    open('archive.html', 'w', encoding='utf-8').write(arch)

    print('Static Briefing rendered: %d cards on front page, %d items in archive (latest: %s)'
          % (len(front), len(items), latest))


if __name__ == '__main__':
    main()
