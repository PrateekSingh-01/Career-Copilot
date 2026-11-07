from duckduckgo_search import DDGS
from typing import List, Dict

# ==============================
# REAL COURSE SEARCH
# ==============================

def search_real_courses(query: str, max_results: int = 10) -> List[Dict]:
    courses = []

    allowed_domains = [
        "coursera.org",
        "udemy.com",
        "nptel.ac.in",
        "edx.org",
        "freecodecamp.org"
    ]

    garbage_keywords = [
        "forum", "movie", "game", "adventure",
        "angiography", "medical", "reddit",
        "知乎", "论坛", "torrent", "pdf"
    ]

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            url = r.get("href", "")
            title = r.get("title", "").lower()

            # Whitelist trusted learning platforms
            if not any(domain in url for domain in allowed_domains):
                continue

            # Filter garbage titles
            if any(g in title for g in garbage_keywords):
                continue

            courses.append({
                "name": r.get("title", "Unknown Course"),
                "provider": url.split("/")[2].replace("www.", ""),
                "difficulty": "Unknown",
                "url": url,
                "ai_score": 0.0
            })

    return courses


# ==============================
# AI COURSE RECOMMENDER
# ==============================

def recommend_live_courses(weak_areas: List[str]) -> List[Dict]:
    all_courses = []

    skill_map = {
        "DSA": "data structures algorithms",
        "ML": "machine learning",
        "Python": "python programming",
        "Web": "web development",
        "Consistency": "time management productivity"
    }

    for skill in weak_areas:
        search_term = skill_map.get(skill, skill)
        query = f"{search_term} online course"
        results = search_real_courses(query, max_results=12)

        for c in results:
            c["ai_score"] += 1
            all_courses.append(c)

    # Fallback if web search fails
    if not all_courses:
        return [
            {
                "name": "Python for Everybody",
                "provider": "coursera.org",
                "difficulty": "Beginner",
                "url": "https://www.coursera.org/specializations/python",
                "ai_score": 2
            },
            {
                "name": "Machine Learning Specialization",
                "provider": "coursera.org",
                "difficulty": "Intermediate",
                "url": "https://www.coursera.org/specializations/machine-learning-introduction",
                "ai_score": 2
            },
            {
                "name": "Data Structures in Python",
                "provider": "udemy.com",
                "difficulty": "Intermediate",
                "url": "https://www.udemy.com/course/data-structures-and-algorithms-in-python",
                "ai_score": 2
            },
            {
                "name": "Full Stack Web Development",
                "provider": "coursera.org",
                "difficulty": "Intermediate",
                "url": "https://www.coursera.org/specializations/full-stack-react",
                "ai_score": 2
            }
        ]

    # Deduplicate by name
    unique = {c["name"]: c for c in all_courses}
    final = list(unique.values())

    # Rank by AI relevance score
    final.sort(key=lambda x: x["ai_score"], reverse=True)

    return final[:5]


# ==============================
# REAL INTERNSHIP SEARCH
# ==============================

def search_real_internships(query: str, max_results: int = 10) -> List[Dict]:
    jobs = []

    trusted_domains = [
        "internshala.com",
        "linkedin.com",
        "indeed.com",
        "naukri.com",
        "glassdoor.com"
    ]

    scam_keywords = [
        "pay", "registration fee", "training fee", "deposit",
        "whatsapp", "telegram", "guaranteed",
        "crypto", "mlm", "forex"
    ]

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            url = r.get("href", "")
            title = r.get("title", "").lower()
            snippet = r.get("body", "").lower()

            # Trust filter
            if not any(domain in url for domain in trusted_domains):
                continue

            # Scam keyword filter
            if any(word in snippet for word in scam_keywords):
                continue

            jobs.append({
                "title": r.get("title", "Internship"),
                "company": "Unknown Company",
                "domain": query.split()[0],
                "salary": 0,
                "location": "Remote",
                "url": url,
                "ai_score": 0
            })

    return jobs


# ==============================
# AI INTERNSHIP RECOMMENDER
# ==============================

def recommend_live_internships(weak_areas: List[str]) -> List[Dict]:
    all_jobs = []

    skill_map = {
        "DSA": "software internship",
        "ML": "machine learning internship",
        "Python": "python developer internship",
        "Web": "web development internship"
    }

    for skill in weak_areas:
        search_term = skill_map.get(skill, skill)
        query = f"{search_term} site:internshala.com OR site:linkedin.com OR site:indeed.com"
        results = search_real_internships(query, max_results=12)

        for job in results:
            job["ai_score"] += 1
            all_jobs.append(job)

    # Fallback if no jobs found
    if not all_jobs:
        return [
            {
                "title": "Python Intern",
                "company": "ABC Tech",
                "domain": "Python",
                "salary": 15000,
                "location": "Remote",
                "url": "https://internshala.com",
                "ai_score": 2
            },
            {
                "title": "ML Intern",
                "company": "NeuralLabs",
                "domain": "ML",
                "salary": 20000,
                "location": "Remote",
                "url": "https://internshala.com",
                "ai_score": 2
            },
            {
                "title": "Web Developer Intern",
                "company": "WebWorks",
                "domain": "Web",
                "salary": 18000,
                "location": "Delhi",
                "url": "https://internshala.com",
                "ai_score": 2
            }
        ]

    # Deduplicate by job title
    unique = {j["title"]: j for j in all_jobs}
    final = list(unique.values())

    # Rank by AI score
    final.sort(key=lambda x: x["ai_score"], reverse=True)

    return final[:5]
