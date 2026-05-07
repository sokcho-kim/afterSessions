import argparse
import json
import os
import re
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


DEFAULT_URL = "https://www.aiexpo.co.kr/home/v6.php?s=36"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
GENERIC_TEXTS = {
    "HOME",
    "참관객",
    "참가기업 디렉토리",
    "Image",
    "AI EXPO KOREA 사무국",
}
DETAIL_SECTION_LABELS = [
    "회사 및 주요 서비스 소개",
    "전시 제품 및 서비스 소개",
    "제품별 적용 분야 및 실제 적용 사례",
]


def fetch_html(url: str, timeout: int = 30) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    content = response.content
    head = content[:2048].lower()

    if b"charset=euc-kr" in head or b"charset=\"euc-kr\"" in head:
        return content.decode("euc-kr", errors="replace")
    if b"charset=cp949" in head or b"charset=\"cp949\"" in head:
        return content.decode("cp949", errors="replace")

    encoding = response.apparent_encoding or response.encoding or "utf-8"
    return content.decode(encoding, errors="replace")


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value


def get_stripped_lines(node: Tag) -> List[str]:
    lines = []
    for text in node.stripped_strings:
        cleaned = clean_text(text)
        if cleaned and cleaned not in GENERIC_TEXTS:
            lines.append(cleaned)
    return lines


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def is_probable_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_probable_address(value: str) -> bool:
    prefixes = (
        "서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종",
        "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
    )
    return value.startswith(prefixes)


def get_cnum_from_url(url: str) -> Optional[str]:
    parsed = urlparse(url)
    cnum = parse_qs(parsed.query).get("cnum")
    return cnum[0] if cnum else None


def find_container(anchor: Tag) -> Tag:
    current = anchor
    while current.parent and isinstance(current.parent, Tag):
        current = current.parent
        lines = get_stripped_lines(current)
        if len(lines) >= 4 and len(" ".join(lines)) >= 40:
            return current
    return anchor.parent if isinstance(anchor.parent, Tag) else anchor


def extract_labeled_values(lines: List[str], label: str) -> List[str]:
    values: List[str] = []
    for index, line in enumerate(lines):
        if line == label:
            for candidate in lines[index + 1:]:
                if candidate in {"품목구분", "카테고리"} or candidate in DETAIL_SECTION_LABELS:
                    break
                if candidate in {"Platinum", "Gold", "Silver", "Bronze"}:
                    values.append(candidate)
                    continue
                values.append(candidate)
            break
    return values


def guess_summary_fields(lines: List[str], detail_url: str, anchor: Tag) -> Dict[str, object]:
    company_name = clean_text(anchor.get_text(" ", strip=True))
    if not company_name:
        for line in lines:
            if line not in {"품목구분", "카테고리"} and not is_probable_url(line):
                company_name = line
                break

    english_name = ""
    for line in lines:
        if line == company_name or line in {"품목구분", "카테고리"}:
            continue
        if re.search(r"[A-Za-z]", line):
            english_name = line
            break

    item_types = []
    categories = []
    sponsor_level = ""

    if "품목구분" in lines:
        for candidate in lines[lines.index("품목구분") + 1:]:
            if candidate == "카테고리":
                break
            if candidate in {"Platinum", "Gold", "Silver", "Bronze"}:
                sponsor_level = candidate
                continue
            item_types.append(candidate)

    if "카테고리" in lines:
        for candidate in lines[lines.index("카테고리") + 1:]:
            if candidate in {"Platinum", "Gold", "Silver", "Bronze"}:
                sponsor_level = candidate
                continue
            if candidate in DETAIL_SECTION_LABELS:
                break
            categories.append(candidate)

    if not sponsor_level:
        for line in lines:
            if line in {"Platinum", "Gold", "Silver", "Bronze"}:
                sponsor_level = line
                break

    return {
        "cnum": get_cnum_from_url(detail_url),
        "company_name": company_name,
        "english_name": english_name,
        "item_types": dedupe_keep_order(item_types),
        "categories": dedupe_keep_order(categories),
        "sponsor_level": sponsor_level,
        "detail_url": detail_url,
    }


def parse_list_page(html: str, base_url: str) -> List[Dict[str, object]]:
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen_urls = set()

    for box in soup.select("div.v6_item_box"):
        onclick = box.get("onclick", "")
        match = re.search(r"v6_view\.php\?s=\d+&cnum=\d+", onclick)
        if not match:
            continue
        detail_url = urljoin(base_url, match.group(0))
        if detail_url in seen_urls:
            continue
        seen_urls.add(detail_url)

        company_name = clean_text(
            box.select_one(".v6_item_sangho").get_text(" ", strip=True)
        ) if box.select_one(".v6_item_sangho") else ""

        desc_nodes = box.select(".v6_item_desc")
        item_types = []
        categories = []

        if desc_nodes:
            item_type_text = clean_text(desc_nodes[0].get_text(" ", strip=True))
            if item_type_text:
                item_types.append(item_type_text)

        if len(desc_nodes) >= 2:
            for line in get_stripped_lines(desc_nodes[1]):
                normalized = clean_text(line.replace("·", "").strip())
                if normalized:
                    categories.append(normalized)

        sponsor_level = ""
        sponsor_node = box.select_one(".v6_spon_tag")
        if sponsor_node:
            sponsor_level = clean_text(sponsor_node.get_text(" ", strip=True))

        lines = dedupe_keep_order(get_stripped_lines(box))
        summary = guess_summary_fields(lines, detail_url, box)
        summary["company_name"] = company_name or summary.get("company_name", "")
        summary["item_types"] = dedupe_keep_order(item_types or list(summary.get("item_types", [])))
        summary["categories"] = dedupe_keep_order(categories or list(summary.get("categories", [])))
        summary["sponsor_level"] = sponsor_level or summary.get("sponsor_level", "")
        results.append(summary)

    return results


def extract_section_map(lines: List[str]) -> Dict[str, str]:
    section_map: Dict[str, str] = {}
    label_positions = [index for index, line in enumerate(lines) if line in DETAIL_SECTION_LABELS]

    for pos_index, start in enumerate(label_positions):
        label = lines[start]
        end = label_positions[pos_index + 1] if pos_index + 1 < len(label_positions) else len(lines)
        body_lines = [line for line in lines[start + 1:end] if line not in DETAIL_SECTION_LABELS]
        section_map[label] = "\n".join(body_lines).strip()

    return section_map


def parse_detail_page(html: str, detail_url: str) -> Dict[str, object]:
    soup = BeautifulSoup(html, "html.parser")
    lines = dedupe_keep_order(get_stripped_lines(soup))

    company_name = clean_text(
        soup.select_one(".v6_view_sangho").get_text(" ", strip=True)
    ) if soup.select_one(".v6_view_sangho") else ""
    english_name = clean_text(
        soup.select_one(".v6_view_sangho_2").get_text(" ", strip=True)
    ) if soup.select_one(".v6_view_sangho_2") else ""

    item_types: List[str] = []
    item_node = soup.select_one(".v6_view_pummok_1 .v6_view_desc")
    if item_node:
        item_types = dedupe_keep_order(get_stripped_lines(item_node))

    categories: List[str] = []
    category_node = soup.select_one(".v6_view_pummok_2 .v6_view_desc")
    if category_node:
        categories = [
            clean_text(line.replace("·", "").strip())
            for line in get_stripped_lines(category_node)
            if clean_text(line.replace("·", "").strip())
        ]

    website = ""
    homepage_link = soup.select_one(".v6_view_desc a[href]")
    if homepage_link:
        website = clean_text(homepage_link.get("href", ""))

    address = ""
    address_icon = soup.select_one("img[src*='icon_place_pin']")
    if address_icon:
        address_container = address_icon.find_parent("div", class_="v6_view_desc")
        if address_container:
            address = clean_text(address_container.get_text(" ", strip=True))

    section_map: Dict[str, str] = {}
    section_titles = soup.select(".v6_view_title_2")
    for title_node in section_titles:
        label = clean_text(title_node.get_text(" ", strip=True))
        content_node = title_node.find_next_sibling("div", class_="v6_view_desc_2")
        if label and content_node:
            section_map[label] = clean_text(content_node.get_text("\n", strip=True))

    external_links = []
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "").strip()
        absolute = urljoin(detail_url, href)
        if absolute.startswith("http") and "aiexpo.co.kr" not in urlparse(absolute).netloc:
            external_links.append(absolute)
    external_links = dedupe_keep_order(external_links)
    if not website and external_links:
        website = external_links[0]

    return {
        "company_name": company_name,
        "english_name": english_name,
        "item_types": dedupe_keep_order(item_types),
        "categories": dedupe_keep_order(categories),
        "website": website,
        "address": address,
        "company_intro": section_map.get("회사 및 주요 서비스 소개", ""),
        "products_and_services": section_map.get("전시 제품 및 서비스 소개", ""),
        "use_cases": section_map.get("제품별 적용 분야 및 실제 적용 사례", ""),
        "external_links": external_links,
    }


def write_json(path: str, payload: object) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)


def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def merge_records(summary: Dict[str, object], detail: Dict[str, object]) -> Dict[str, object]:
    merged = dict(summary)
    merged.update({key: value for key, value in detail.items() if value})

    if summary.get("company_name") and detail.get("company_name"):
        merged["company_name_list"] = dedupe_keep_order(
            [summary["company_name"], detail["company_name"]]
        )

    merged["item_types"] = dedupe_keep_order(
        list(summary.get("item_types", [])) + list(detail.get("item_types", []))
    )
    merged["categories"] = dedupe_keep_order(
        list(summary.get("categories", [])) + list(detail.get("categories", []))
    )
    return merged


def scrape_exhibitors(list_url: str, output_dir: str, limit: Optional[int] = None) -> Dict[str, object]:
    ensure_directory(output_dir)

    list_html = fetch_html(list_url)
    with open(os.path.join(output_dir, "directory.html"), "w", encoding="utf-8") as file:
        file.write(list_html)

    summaries = parse_list_page(list_html, list_url)
    if limit is not None:
        summaries = summaries[:limit]

    exhibitors = []
    detail_dir = os.path.join(output_dir, "details")
    ensure_directory(detail_dir)

    for index, summary in enumerate(summaries, start=1):
        detail_url = summary["detail_url"]
        print(f"[{index}/{len(summaries)}] Fetching {detail_url}")
        detail_html = fetch_html(detail_url)

        cnum = summary.get("cnum") or f"row_{index:03d}"
        detail_html_path = os.path.join(detail_dir, f"{cnum}.html")
        with open(detail_html_path, "w", encoding="utf-8") as file:
            file.write(detail_html)

        detail = parse_detail_page(detail_html, detail_url)
        exhibitors.append(merge_records(summary, detail))

    result = {
        "source_url": list_url,
        "count": len(exhibitors),
        "exhibitors": exhibitors,
    }
    write_json(os.path.join(output_dir, "exhibitors.json"), result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape exhibitor directory pages into JSON.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Directory URL")
    parser.add_argument(
        "--output-dir",
        default=os.path.join("raw", "2026", "2026-05-06_ai-expo-korea-2026", "exhibitors"),
        help="Output directory for HTML and JSON files",
    )
    parser.add_argument("--limit", type=int, help="Limit number of exhibitors for a quick run")
    args = parser.parse_args()

    result = scrape_exhibitors(args.url, args.output_dir, args.limit)
    print(f"Saved {result['count']} exhibitors to {args.output_dir}")


if __name__ == "__main__":
    main()
