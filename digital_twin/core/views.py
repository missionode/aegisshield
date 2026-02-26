from django.shortcuts import render
import requests
import random

def index(request):
    return render(request, 'core/index.html')

def features(request):
    return render(request, 'core/features.html')

def blog(request):
    # Wikipedia API Endpoint
    url = "https://en.wikipedia.org/w/api.php"
    
    # Search for "houseplant care" to get relevant articles
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": "houseplant care",
        "prop": "pageimages|extracts",
        "piprop": "thumbnail",
        "pithumbsize": 600,
        "exintro": 1,
        "explaintext": 1,
        "gsrlimit": 15, # Fetch more to filter out bad ones
        "format": "json"
    }
    
    headers = {
        "User-Agent": "PlantDoctor/1.0 (https://plantdoctor.example.com; contact@plantdoctor.example.com)"
    }
    
    articles = []
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        for page_id, page_data in pages.items():
            title = page_data.get("title", "")
            
            # Filter out irrelevant pages
            if "company" in title.lower() or "list of" in title.lower():
                continue
                
            summary = page_data.get("extract", "")
            # Truncate summary
            if len(summary) > 150:
                summary = summary[:150] + "..."
                
            image_url = page_data.get("thumbnail", {}).get("source")
            
            # Fallback image if no thumbnail
            if not image_url:
                image_url = "https://images.unsplash.com/photo-1463320726281-696a485928c7?q=80&w=2070&auto=format&fit=crop"
            
            articles.append({
                "title": title,
                "summary": summary,
                "image_url": image_url,
                "link": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                "author": "Wikipedia Contributors",
                "date": "Recently Updated"
            })
            
    except Exception as e:
        print(f"Error fetching blog articles: {e}")
        # Fallback content
        articles = [
            {
                "title": "Houseplant Care 101",
                "summary": "Learn the basics of taking care of your indoor garden.",
                "image_url": "https://images.unsplash.com/photo-1463320726281-696a485928c7?q=80&w=2070&auto=format&fit=crop",
                "link": "#",
                "author": "Plant Doctor",
                "date": "Today"
            }
        ]

    # Shuffle and pick top 10
    random.shuffle(articles)
    articles = articles[:10]

    return render(request, 'core/blog.html', {'articles': articles})

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')