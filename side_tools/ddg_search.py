from duckduckgo_search import DDGS

def website_content_search_agent(inputs):
    """Fetch company information using DuckDuckGo search."""
    query = f"{inputs['company']} site:{inputs['company_website']}"
    
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)  # Fetch top 3 search results
    
    if results:
        extracted_info = "\n".join([f"{res['title']}: {res['body']}" for res in results])
    else:
        extracted_info = "No relevant company information found."

    return extracted_info
