import feedparser
from datetime import datetime, timedelta, timezone
import pytz

IST = pytz.timezone("Asia/Kolkata")
now = datetime.now(IST)
cutoff = now - timedelta(hours=24)

PROFILE_SKILLS = {"sql", "python", "tableau", "data", "analytics", "mysql"}
LOCATIONS = {"madurai", "coimbatore", "trichy", "bangalore", "tamil nadu"}
AVOID = {"senior", "lead", "manager", "ml engineer", "unpaid"}

FEEDS = [
    "https://www.indeed.com/rss?q=Data+Analyst+Fresher&l=Tamil+Nadu",
    "https://www.indeed.com/rss?q=Junior+Data+Analyst&l=Bangalore",
    "https://www.indeed.com/rss?q=SQL+Analyst+Entry+Level&l=India"
]

results = []

for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)
    for e in feed.entries:
        if not hasattr(e, "published_parsed"):
            continue

        published = datetime(*e.published_parsed[:6], tzinfo=timezone.utc).astimezone(IST)
        if published < cutoff:
            continue

        title = e.title.lower()
        if any(bad in title for bad in AVOID):
            continue

        score = sum(skill in title for skill in PROFILE_SKILLS)

        results.append({
            "role": e.title,
            "company": e.get("source", {}).get("title", "Company"),
            "location": e.get("location", "Not specified"),
            "posted": e.published,
            "link": e.link,
            "score": score
        })

results = sorted(results, key=lambda x: x["score"], reverse=True)[:20]

print(f"\nRun time: {now.strftime('%Y-%m-%d %H:%M')} IST\n")

for r in results:
    print(f"{r['role']} — {r['company']}")
    print(f"Location: {r['location']}")
    print(f"Posted: {r['posted']}")
    print(f"Link: {r['link']}")
    print("Why it matches: Fresher-friendly data role with SQL/Python overlap\n")
