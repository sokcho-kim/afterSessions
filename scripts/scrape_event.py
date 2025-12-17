import os
import argparse
import datetime
import json
import time
import re
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_image(page, src, output_path):
    try:
        # Use playwright's request logic or python's requests? 
        # Since we are in playwright, we can fetch via page context or just skip complex auth.
        # For simplicity in this script, we'll try to fetch using the page context (evaluate fetch)
        # or just ignore complex downloads and focus on easy ones.
        # Let's use simple saving if it's a data url, otherwise request.
        
        if src.startswith("data:"):
            # Skip data URIs for file download to keep it clean, or implement if needed.
            return False
            
        response = page.request.get(src)
        if response.status == 200:
            with open(output_path, "wb") as f:
                f.write(response.body())
            return True
    except Exception as e:
        print(f"Failed to download {src}: {e}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Scrape content from a URL.")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--date", required=True, help="Event date (YYYY-MM-DD)")
    parser.add_argument("--slug", required=True, help="Event slug")
    parser.add_argument("--title", help="Event title (optional)")
    parser.add_argument("--tags", help="Comma-separated tags (optional)")
    
    args = parser.parse_args()
    
    # Setup paths
    try:
        event_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be YYYY-MM-DD")
        return

    year = str(event_date.year)
    folder_name = f"{args.date}_{args.slug}"
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(root_dir, "raw", year, folder_name)
    images_dir = os.path.join(target_dir, "images")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        
    print(f"Starting scrape for {args.url} -> {target_dir}")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # Go to page
            page.goto(args.url, wait_until="networkidle", timeout=60000)
            
            # Wait a bit just in case
            time.sleep(2)
            
            # 1. Full Page Screenshot
            screenshot_path = os.path.join(target_dir, "screenshot.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Captured screenshot: {screenshot_path}")
            
            # 2. Extract Title
            page_title = page.title()
            print(f"Page Title: {page_title}")
            
            # 3. Save Original HTML
            html_content = page.content()
            with open(os.path.join(target_dir, "original.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
                
            # 4. Extract Text Content (Simple)
            # Try to find main article content if possible, else body
            content_text = page.evaluate("""() => {
                const article = document.querySelector('article') || document.querySelector('main') || document.body;
                return article.innerText;
            }""")
            
            with open(os.path.join(target_dir, "content.txt"), "w", encoding="utf-8") as f:
                f.write(content_text)
                
            # 5. Download Images (Top 10 meaningful images)
            img_elements = page.query_selector_all("img")
            count = 0
            image_meta_list = []
            
            for i, img in enumerate(img_elements):
                if count >= 10: break
                
                src = img.get_attribute("src")
                if not src: continue
                
                # Resolve relative URLs
                src = urljoin(args.url, src)
                
                # Simple filter: skip small icons often implied by keywords in name or dimensions (if we could check)
                # For now just try to download
                
                ext = os.path.splitext(urlparse(src).path)[1]
                if not ext or len(ext) > 5: ext = ".jpg" # Default fallback
                
                filename = f"image_{i:03d}{ext}"
                filepath = os.path.join(images_dir, filename)
                
                success = download_image(page, src, filepath)
                if success:
                    image_meta_list.append({"src": src, "local": filename})
                    count += 1
            
            print(f"Downloaded {count} images.")

            # 6. Save Metadata
            meta_data = {
                "url": args.url,
                "title_scraped": page_title,
                "title_arg": args.title,
                "date": args.date,
                "scraped_at": datetime.datetime.now().isoformat(),
                "tags": args.tags,
                "images": image_meta_list
            }
            
            with open(os.path.join(target_dir, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(meta_data, f, indent=2, ensure_ascii=False)
                
            # 7. Create/Append to agenda.txt (Placeholder)
            # If we didn't extract a clear agenda, just leave a placeholder or basic info
            with open(os.path.join(target_dir, "agenda.txt"), "w", encoding="utf-8") as f:
                f.write(f"Scraped source: {args.url}\n\nSee content.txt or screenshot.png for details.")
                
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
