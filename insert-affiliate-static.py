"""
Insert AffiliateBanner into remaining genaipick static pages.
"""
import os

static_files = [
    "D:\\Project\\genaipick\\src\\pages\\contact.astro",
    "D:\\Project\\genaipick\\src\\pages\\privacy.astro",
    "D:\\Project\\genaipick\\src\\pages\\terms.astro",
    "D:\\Project\\genaipick\\src\\pages\\author.astro",
]

import_stmt = "import AffiliateBanner from '../components/AffiliateBanner.astro';"
component_tag = '<AffiliateBanner variant="compact" />'
count = 0

for fpath in static_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if component_tag in content:
        continue
    
    changed = False
    
    # Add import
    if import_stmt not in content:
        fm_close = content.find('\n---\n', content.find('---\n') + 4)
        if fm_close > 0:
            insert_pos = content.rfind('\n', 0, fm_close) + 1
            content = content[:insert_pos] + '\n' + import_stmt + content[insert_pos:]
            changed = True
    
    # Insert after first </p> (first paragraph end) that's after the frontmatter
    # Make sure we're past the frontmatter
    fm_end = content.find('\n---\n', content.find('---\n') + 4)
    if fm_end < 0:
        continue
    fm_end += 5  # past the closing ---\n
    
    # Find first </p> after frontmatter
    search_from = fm_end
    first_p_end = content.find('</p>', search_from)
    if first_p_end > 0:
        # Insert after </p>\n or </p>\n\n
        insert_at = first_p_end + 4  # after </p>
        # Skip any following whitespace/newlines
        content = content[:insert_at] + '\n\n  ' + component_tag + '\n\n' + content[insert_at:]
        changed = True
    
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"  UPDATED: {os.path.basename(fpath)}")

print(f"\nDone: {count} static pages updated")
