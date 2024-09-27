import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from crewai import Agent, Task
from urllib.parse import urlparse

class BrowserTools():

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        try:
            if not urlparse(website).scheme:
                return f"Invalid URL: {website}. Please provide a valid URL including the scheme (e.g., https://)"
            # Send a GET request to the website
            response = requests.get(website, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from paragraphs, headings, and other relevant tags
            content = ' '.join([element.get_text(strip=True) for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])])
            
            # Split content into chunks of 8000 characters
            content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            
            summaries = []
            for chunk in content_chunks:
                agent = Agent(
                    role='Principal Researcher',
                    goal='Do amazing research and summaries based on the content you are working with',
                    backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                    allow_delegation=False)
                task = Task(
                    agent=agent,
                    description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
                )
                summary = task.execute()
                summaries.append(summary)
            return "\n\n".join(summaries)
        except requests.RequestException as e:
            return f"An error occurred while scraping the website: {str(e)}"