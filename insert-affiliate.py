"""
Batch insert AffiliateBanner component into genapick blog posts and static pages.
Blog posts: insert after first <h2> paragraph
Static pages: insert after first paragraph
"""
import os, re

blog_dir = "D:\\Project\\genaipick\\src\\pages\\blog"
static_pages = [
    "D:\\Project\\genaipick\\src\\pages\\about.astro",
    "D:\\Project\\genaipick\\src\\pages\\index.astro",
]

import_stmt = "import AffiliateBanner from '../components/AffiliateBanner.astro';"
blog_import_stmt = "import AffiliateBanner from '../../components/AffiliateBanner.astro';"
compact_component = '  <AffiliateBanner variant="compact" />\n\n'

count_blog = 0

for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith(".astro") or fname == "index.astro":
        continue
    fpath = os.path.join(blog_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    changed = False
    
    # Add import if not present
    if blog_import_stmt not in content:
        fm_closing = content.find('\n---\n', content.find('---\n') + 4)
        if fm_closing > 0:
            insert_pos = content.rfind('\n', 0, fm_closing) + 1
            content = content[:insert_pos] + '\n' + blog_import_stmt + content[insert_pos:]
            changed = True
    
    # Find the first <h2> tag and insert after it + its paragraph content
    if compact_component.strip() not in content:
        # Find first </h2> - insert after the paragraph that follows it
        first_h2_end = content.find('</h2>')
        if first_h2_end > 0:
            # Find the end of the next paragraph (</p>) after the h2
            after_h2 = content[first_h2_end:]
            next_p_end = after_h2.find('</p>')
            if next_p_end > 0:
                insert_at = first_h2_end + next_p_end + 4  # after </p>
                content = content[:insert_at] + '\n\n' + compact_component + content[insert_at:]
                changed = True
    
    if changed:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        count_blog += 1
        print(f"  UPDATED blog: {fname}")

# Static pages
count_static = 0
for fpath in static_pages:
    if not os.path.exists(fpath):
        continue
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    changed = False
    
    if import_stmt not in content:
        fm_closing = content.find('\n---\n', content.find('---\n') + 4)
        if fm_closing > 0:
            insert_pos = content.rfind('\n', 0, fm_closing) + 1
            content = content[:insert_pos] + '\n' + import_stmt + content[insert_pos:]
            changed = True
    
    if compact_component.strip() not in content:
        # Find first <p> after the closing frontmatter content block, insert after it
        first_p_end = content.find('</p>')
        if first_p_end > 0:
            content = content[:first_p_end+4] + '\n\n' + compact_component + content[first_p_end+4:]
            changed = True
    
    if changed:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        count_static += 1
        print(f"  UPDATED static: {fname}")

print(f"\nDone: {count_blog} blog posts + {count_static} static pages updated")
