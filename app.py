import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timezone
import time

app = Flask(__name__)

# API key config.py se load hogi
try:
    from config import YOUTUBE_API_KEY
    API_KEY = YOUTUBE_API_KEY
except ImportError:
    API_KEY = ""
    print("WARNING: config.py nahi mili! config.example.py ko config.py banao aur API key daalo.")

BASE = "https://www.googleapis.com/youtube/v3"

NICHES = [
    {
        "id": "pov_finance",
        "name": "POV Finance (Animated)",
        "icon": "💰",
        "color": "#22aa55",
        "desc": "2D animated money/finance POV stories — 2026 ka #1 hot niche",
        "start_advice": "Yeh 2026 ka #1 niche hai. Money Life POV ne 31 videos mein 8K subs liye. Format: 'You stop climbing corporate ladder — wealth takes off'. AI 2D animation (Vyond/Adobe Animate) + relatable financial story from POV perspective. Script ChatGPT se. Finance CPM = $10-20. US audience. 10-15 min videos.",
        "keywords": [
            "pov finance animated",
            "money life pov animated",
            "financial decisions animated story",
            "wealth animated pov channel",
        ]
    },
    {
        "id": "animated_myths",
        "name": "Animated Myths & Legends",
        "icon": "🏛️",
        "color": "#cc8800",
        "desc": "Myths animated — Kelevin style (282K subs, 1.7M views/video!)",
        "start_advice": "Kelevin ne 282K subs liye sirf myths animated karke — 1.7M views per video! Format: 'Ancient Myths That Turned Out to Be True'. Stickman ya 2D animation. Script ChatGPT se. ElevenLabs voice. Very low competition abhi — start karo!",
        "keywords": [
            "animated myths channel",
            "myths legends animated youtube",
            "ancient myths animated stories",
            "mythology animation explained",
        ]
    },
    {
        "id": "true_crime",
        "name": "True Crime (Faceless)",
        "icon": "🕵️",
        "color": "#884400",
        "desc": "Real crime cases narrated — top trending faceless niche 2026",
        "start_advice": "Sirf AI voice + stock footage chahiye. Real murder/mystery cases cover karo. Script ChatGPT se, narration ElevenLabs se. Har video ek case. US audience — CPM $8-15.",
        "keywords": [
            "true crime narration",
            "true crime mystery channel",
            "crime documentary narrated",
            "unsolved murder mystery channel",
        ]
    },
    {
        "id": "dark_history",
        "name": "Dark History & Mystery",
        "icon": "😱",
        "color": "#cc5500",
        "desc": "Dark history, unsolved mysteries — evergreen high-CPM niche",
        "start_advice": "History ke dark events cover karo. AI narration + stock footage. Invideo AI ya Pictory use karo. Har video ek event. 10-20 minute videos best hain.",
        "keywords": [
            "dark history narrated channel",
            "history mystery narration youtube",
            "dark secrets history documentary",
            "historical mysteries explained",
        ]
    },
    {
        "id": "horror_animated",
        "name": "Horror Stories (Faceless)",
        "icon": "👻",
        "color": "#9900cc",
        "desc": "Scary animated/narrated stories — millions of views, no face",
        "start_advice": "Real scary true stories animate ya narrate karo. ElevenLabs AI voice. Dark background + creepy music. Thumbnail mein monster zaroori. 10-20 min.",
        "keywords": [
            "horror story narrated channel",
            "scary true stories animated",
            "horror narration faceless youtube",
            "creepy stories animated channel",
        ]
    },
    {
        "id": "stickman",
        "name": "Stickman Animation",
        "icon": "🎭",
        "color": "#ff4444",
        "desc": "Stickman fights, battles & adventures — viral animation niche",
        "start_advice": "FlipaClip ya Stick Nodes se banao. Fight/battle scenes most viral hain. Kelevin jaisa travel/myth format bhi try karo. 5-15 min videos.",
        "keywords": [
            "stickman animation fight",
            "stick figure animation channel",
            "stickman adventure story youtube",
            "stickman travel animated",
        ]
    },
    {
        "id": "documentary_animated",
        "name": "Mini Documentary (Narrated)",
        "icon": "🌍",
        "color": "#006633",
        "desc": "Short narrated documentaries — premium high-CPM niche",
        "start_advice": "Stock footage + AI narration. History, nature, science topics. 10-20 min videos. Invideo AI ya Pictory use karo. US/UK audience target karo.",
        "keywords": [
            "mini documentary narrated channel",
            "documentary narration faceless youtube",
            "history documentary narrated channel",
            "educational documentary narration",
        ]
    },
    {
        "id": "science_animated",
        "name": "Science & Space (Animated)",
        "icon": "🔬",
        "color": "#0055cc",
        "desc": "Universe, science explained animated — highest retention content",
        "start_advice": "Space, physics topics cover karo. Simple animations + good script. 'What if' questions best viral hote hain. After Effects ya Manim use karo.",
        "keywords": [
            "science explained animated channel",
            "space universe narrated channel",
            "science documentary animation youtube",
            "what if science animated",
        ]
    },
    {
        "id": "reddit_animated",
        "name": "Reddit Stories (Animated)",
        "icon": "📖",
        "color": "#ff5500",
        "desc": "Reddit posts animated/narrated — easiest & most viral faceless",
        "start_advice": "Reddit AITA posts lo, animate ya narrate karo. Character ek avatar ho. AI voice + simple animation. Sabse easy faceless format hai.",
        "keywords": [
            "reddit stories narrated channel",
            "reddit reading channel youtube",
            "reddit animated stories channel",
            "storytime reddit animated",
        ]
    },
    {
        "id": "anime_recap",
        "name": "Anime Recap / Summary",
        "icon": "⚔️",
        "color": "#cc0066",
        "desc": "Anime episode recaps narrated — millions views, no face needed",
        "start_advice": "Popular anime clips edit karo + AI narration. Jujutsu Kaisen, AOT, One Piece se shuru karo. 10-20 min recap format.",
        "keywords": [
            "anime recap narrated channel",
            "anime summary explained youtube",
            "anime recap channel",
            "anime episode recap narration",
        ]
    },
    {
        "id": "kids_cartoon",
        "name": "Kids Animation (Faceless)",
        "icon": "🧒",
        "color": "#0088ff",
        "desc": "Kids cartoons & stories — billions of views worldwide",
        "start_advice": "Bright colors, simple moral story. Canva ya Toonly use karo. English mein banao. 5-10 min videos. Family-friendly = high CPM.",
        "keywords": [
            "kids cartoon animation channel",
            "animated stories for children youtube",
            "kids cartoon story channel",
            "children animation educational youtube",
        ]
    },
]


def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return str(n)


def is_latin_text(text):
    if not text: return True
    latin = sum(1 for c in text if ord(c) < 591)
    return (latin / len(text)) > 0.80


def find_channels_via_videos(keyword, published_after="2025-07-01T00:00:00Z"):
    """Search recent English long-form videos to find channel IDs"""
    try:
        r = requests.get(f"{BASE}/search", params={
            "part": "snippet", "q": keyword, "type": "video",
            "maxResults": 50, "order": "viewCount",
            "publishedAfter": published_after,
            "relevanceLanguage": "en",
            "regionCode": "US",
            "videoDuration": "long",
            "key": API_KEY
        }, timeout=12)
        data = r.json()
        if "error" in data:
            return [], data["error"].get("message", "")
        ids = []
        seen = set()
        for item in data.get("items", []):
            sn = item.get("snippet", {})
            title = sn.get("title", "")
            ch_id = sn.get("channelId", "")
            if ch_id and ch_id not in seen and is_latin_text(title):
                seen.add(ch_id)
                ids.append(ch_id)
        return ids, None
    except Exception as e:
        return [], str(e)


def search_channels_direct(keyword):
    """Directly search for English channels"""
    try:
        r = requests.get(f"{BASE}/search", params={
            "part": "snippet", "q": keyword, "type": "channel",
            "maxResults": 20, "order": "relevance",
            "relevanceLanguage": "en",
            "regionCode": "US",
            "key": API_KEY
        }, timeout=12)
        data = r.json()
        if "error" in data:
            return []
        return [i["id"]["channelId"] for i in data.get("items", []) if i.get("id", {}).get("channelId")]
    except:
        return []


LOW_CPM_COUNTRIES = {'IN','PK','BD','NG','PH','ID','VN','MM','ET','KE','GH','TZ','UG','SD','SO','NP','LK'}


def is_english_channel(title, country, default_lang):
    if country and country.upper() in LOW_CPM_COUNTRIES:
        return False
    if default_lang and not default_lang.lower().startswith('en'):
        return False
    if not is_latin_text(title):
        return False
    return True


def get_channels(ids, niche):
    if not ids: return []
    try:
        r = requests.get(f"{BASE}/channels", params={
            "part": "snippet,statistics",
            "id": ",".join(ids[:25]),
            "key": API_KEY
        }, timeout=12)
        data = r.json()
        out = []
        for item in data.get("items", []):
            sn = item.get("snippet", {})
            st = item.get("statistics", {})
            pub_str = sn.get("publishedAt", "")
            try:
                pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                if pub.year != 2026: continue
            except: continue

            title        = sn.get("title", "")
            country      = sn.get("country", "")
            default_lang = sn.get("defaultLanguage", "")

            if not is_english_channel(title, country, default_lang):
                continue

            subs  = int(st.get("subscriberCount", 0) or 0)
            views = int(st.get("viewCount", 0) or 0)
            vids  = int(st.get("videoCount", 0) or 0)
            if vids < 1: continue

            now   = datetime.now(timezone.utc)
            days  = max((now - pub).days, 1)
            score = min(100, int((subs/days)*0.7 + (views/days)*0.004 + vids*1.5))

            months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                      7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
            out.append({
                "id": item["id"],
                "title": title,
                "description": (sn.get("description") or "")[:120],
                "thumbnail": sn.get("thumbnails",{}).get("medium",{}).get("url",""),
                "country": country,
                "published": pub.strftime("%d %b %Y"),
                "month": months.get(pub.month,""),
                "month_num": pub.month,
                "days_old": days,
                "subs": subs,
                "subs_fmt": fmt(subs),
                "views_fmt": fmt(views),
                "videos": vids,
                "url": f"https://www.youtube.com/channel/{item['id']}",
                "growth_score": score,
                "niche_id": niche["id"],
                "niche": niche["name"],
                "niche_icon": niche["icon"],
                "niche_color": niche["color"],
            })
        return out
    except: return []


def competition_analysis(channels):
    if not channels:
        return {"level": "Unknown", "color": "#888", "msg": "Data nahi mili"}
    avg_subs = sum(c["subs"] for c in channels) / len(channels)
    max_subs = max(c["subs"] for c in channels)
    count    = len(channels)
    if max_subs > 500_000 or avg_subs > 50_000:
        return {"level": "High", "color": "#ff4444",
                "msg": f"Mushkil — {count} bade channels, avg {fmt(int(avg_subs))} subs"}
    elif max_subs > 100_000 or avg_subs > 10_000:
        return {"level": "Medium", "color": "#ffaa00",
                "msg": f"Moderate — {count} channels, avg {fmt(int(avg_subs))} subs"}
    else:
        return {"level": "Low", "color": "#00cc66",
                "msg": f"Abhi Start Karo — {count} channels, avg {fmt(int(avg_subs))} subs"}


@app.route("/")
def index():
    return render_template("index.html", niches=NICHES)


@app.route("/api/scan-niche")
def scan_niche():
    nid = request.args.get("id","")
    niche = next((n for n in NICHES if n["id"]==nid), None)
    if not niche: return jsonify({"error":"Niche not found"}), 404

    seen = set(); channels = []
    for kw in niche["keywords"]:
        ids, _ = find_channels_via_videos(kw)
        ids += search_channels_direct(kw)
        ids = list(dict.fromkeys(ids))
        for ch in get_channels(ids, niche):
            if ch["id"] not in seen:
                seen.add(ch["id"]); channels.append(ch)
        time.sleep(0.3)

    channels.sort(key=lambda x: x["growth_score"], reverse=True)
    comp = competition_analysis(channels)
    return jsonify({
        "niche": niche["name"],
        "icon": niche["icon"],
        "color": niche["color"],
        "advice": niche["start_advice"],
        "channels": channels,
        "total": len(channels),
        "competition": comp
    })


@app.route("/api/scan-all")
def scan_all():
    all_ch = []; seen = set(); by_niche = []

    for niche in NICHES:
        niche_chs = []
        for kw in niche["keywords"][:2]:
            ids, _ = find_channels_via_videos(kw)
            ids += search_channels_direct(kw)
            ids = list(dict.fromkeys(ids))
            for ch in get_channels(ids, niche):
                if ch["id"] not in seen:
                    seen.add(ch["id"]); niche_chs.append(ch); all_ch.append(ch)
            time.sleep(0.25)

        niche_chs.sort(key=lambda x: x["growth_score"], reverse=True)
        by_niche.append({
            "id": niche["id"],
            "name": niche["name"],
            "icon": niche["icon"],
            "color": niche["color"],
            "desc": niche["desc"],
            "advice": niche["start_advice"],
            "channels": niche_chs,
            "competition": competition_analysis(niche_chs)
        })

    all_ch.sort(key=lambda x: x["growth_score"], reverse=True)
    return jsonify({"total": len(all_ch), "channels": all_ch, "by_niche": by_niche})


@app.route("/api/search")
def search():
    q = request.args.get("q","").strip()
    if not q: return jsonify({"error":"Keyword daalo"}), 400
    dummy_niche = {"id":"custom","name":"Custom Search","icon":"🔍","color":"#888"}
    ids, _ = find_channels_via_videos(q)
    ids += search_channels_direct(q)
    ids = list(dict.fromkeys(ids))
    chs = get_channels(ids, dummy_niche)
    chs.sort(key=lambda x: x["growth_score"], reverse=True)
    return jsonify({"channels": chs, "total": len(chs)})


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  YouTube Niche Finder - READY")
    print("  Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
