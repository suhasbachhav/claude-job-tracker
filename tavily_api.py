#!/usr/bin/env python3
"""
Tavily Search API Script
Easily configurable search queries and API key from .env
"""

import requests
import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION - Edit these variables
# ============================================================================

API_KEY = os.getenv("TAVILY_API_KEY", "")
SEARCH_QUERY = "Who is Suhas Bachhav"

# Optional: Advanced search parameters
ADVANCED_PARAMS = {
    "max_results": 5,  # Number of results to return (1-20)
    "include_images": False,  # Include images in results
    "include_answer": True,  # Include direct answer if available
    "include_raw_content": False,  # Include raw page content
}

# ============================================================================
# TAVILY API
# ============================================================================

def search_tavily(query: str, api_key: str, **kwargs) -> Dict[str, Any]:
    """
    Search using Tavily API.

    Args:
        query: Search query string
        api_key: Tavily API key
        **kwargs: Additional parameters (max_results, include_images, etc.)

    Returns:
        Dictionary with search results
    """
    url = "https://api.tavily.com/search"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": query,
        **kwargs,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def display_results(results: Dict[str, Any]) -> None:
    """Pretty print search results."""
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return

    print("\n" + "=" * 80)
    print(f"📌 Query: {results.get('query', 'N/A')}")
    print("=" * 80)

    # Display answer if available
    if results.get("answer"):
        print(f"\n💡 Answer:\n{results['answer']}\n")

    # Display follow-up questions if available
    if results.get("follow_up_questions"):
        print("🔗 Follow-up Questions:")
        for q in results["follow_up_questions"]:
            print(f"  • {q}")
        print()

    # Display search results
    search_results = results.get("results", [])
    if search_results:
        print(f"🔍 Search Results ({len(search_results)} results):\n")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('url', 'N/A')}")
            print(f"   Score: {result.get('score', 'N/A'):.2%}")
            print(f"   Content: {result.get('content', 'No content')[:200]}...")
            print()
    else:
        print("No results found.")

    print("=" * 80 + "\n")


def main():
    """Main execution."""
    if not API_KEY:
        print("❌ Error: TAVILY_API_KEY not found in .env file")
        print("Please add TAVILY_API_KEY to .env file and try again.")
        return

    print("\n🚀 Tavily Search API")
    print("-" * 80)
    print(f"Query: {SEARCH_QUERY}")
    print(f"API Key: {API_KEY[:20]}...")
    print("-" * 80)

    # Perform search
    print("\n⏳ Searching...")
    results = search_tavily(SEARCH_QUERY, API_KEY, **ADVANCED_PARAMS)

    # Display results
    display_results(results)

    # Print raw JSON for debugging (optional)
    if False:  # Set to True to see raw JSON
        print("\n📋 Raw JSON Response:")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
