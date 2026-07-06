import os, re

blog_dir = "D:\\Project\\genaipick\\src\\pages\\blog"

# The author byline to insert
author_block = '''<div class="blog-meta">
  <span class="author">By <a href="https://lusdaily.com" target="_blank" rel="noopener">Lao Lu</a></span>
  <span class="sep">·</span>
  <span>Also on <a href="https://lusdaily.com" target="_blank" rel="noopener">lusdaily.com</a></span>
</div>'''

fixes = 0
skipped = 0

for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith(".astro") or fname == "index.astro":
        continue
    
    fpath = os.path.join(blog_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Case 1: Already has blog-meta - fix the author name
    if 'blog-meta' in content:
        old_author = '<span class="author">By <a href="https://www.linkedin.com/in/shenlu-ulysis6/" target="_blank" rel="noopener">Lu Shen</a></span>'
        new_author = '<span class="author">By <a href="https://lusdaily.com" target="_blank" rel="noopener">Lao Lu</a></span>'
        if old_author in content:
            content = content.replace(old_author, new_author)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"FIXED (existing): {fname}")
            fixes += 1
        else:
            print(f"SKIP (has blog-meta but different author): {fname}")
            skipped += 1
        continue
    
    # Case 2: No blog-meta yet - add it after </h1>
    # Find the first </h1> (which is the article title)
    h1_match = re.search(r'^(.*)</h1>\s*$', content, re.MULTILINE)
    if h1_match:
        line = h1_match.group(0)
        indent = re.match(r'^(\s*)', line).group(1) or ""
        # Indent the block to match
        indented_block = "\n".join(indent + l if l.strip() else l for l in author_block.split("\n"))
        
        content = content.replace(line, line + "\n" + indented_block)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"ADDED: {fname}")
        fixes += 1
    else:
        print(f"SKIP (no h1): {fname}")
        skipped += 1

print(f"\nDone: {fixes} files updated, {skipped} skipped")
