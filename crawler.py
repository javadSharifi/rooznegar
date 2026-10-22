"""Crawl bahesab.ir calendar events (مناسبت‌ها) for 1404/01 .. 1406/12 into JSON.

Usage: python3 crawler.py [output.json]   (default: monasebat.json)
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from base64 import b64encode

URL = "https://www.bahesab.ir/cdn/time/Mpostcalendars/"
YEARS = (1404, 1405, 1406)
MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
          "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
FA_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
HOLIDAY_MARK = "«تعطیل»"


def _scramble(s, key):
    """Mirror of the site's Dy() obfuscation."""
    t = 5 + key % 9
    o = len(s)
    out = [""] * (2 * o)
    for r in range(o):
        out[2 * r] = s[(r + 3 * t) % o]
        out[2 * r + 1] = s[o - r - 1]
    return "".join(out)


def fetch_month(year, month):
    payload = b64encode(json.dumps({"y": 13 * year, "m": 19 * month},
                                   separators=(",", ":")).encode()).decode()
    body = urllib.parse.quote(_scramble(payload, year * month), safe="")
    req = urllib.request.Request(URL, data=body.encode(), headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bahesab.ir/time/calendar/",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode()


def parse_month(html, year, month):
    chunk = re.search(r'<p id="monasebat2".*?</p>', html, re.S)
    if not chunk:
        raise ValueError(f"no #monasebat2 for {year}/{month}")
    chunk = chunk.group(0)

    day_marks = list(re.finditer(r'<span class="M2( ho)?">([^<]+)</span>', chunk))
    days = []
    for i, mark in enumerate(day_marks):
        end = day_marks[i + 1].start() if i + 1 < len(day_marks) else len(chunk)
        segment = chunk[mark.end():end]
        day = int(mark.group(2).split()[0].translate(FA_DIGITS))

        events = []
        for piece in re.split(r"<[^>]+>", segment):
            # shortcut: titles are split on " - "; a title containing " - " would break
            for raw in re.split(r"\s+-\s+", piece):
                raw = raw.strip().lstrip("-").strip()
                if not raw:
                    continue
                holiday = HOLIDAY_MARK in raw
                title = " ".join(raw.replace(HOLIDAY_MARK, "").split())
                events.append({"title": title, "holiday": holiday})

        days.append({
            "day": day,
            "holiday": bool(mark.group(1)) or any(e["holiday"] for e in events),
            "events": events,
        })

    return {"year": year, "month": month, "month_name": MONTHS[month - 1], "days": days}


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "monasebat.json"
    result = []
    for year in YEARS:
        for month in range(1, 13):
            html = fetch_month(year, month)
            data = parse_month(html, year, month)
            result.append(data)
            print(f"{year}/{month:02d} {data['month_name']}: {len(data['days'])} روز", flush=True)
            time.sleep(0.4)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"-> {out_path} ({len(result)} ماه)")


if __name__ == "__main__":
    main()
