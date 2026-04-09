class FinalAnswerTool:
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {
        "answer": {"type": "any", "description": "The final answer to the problem"}
    }
    output_type = "any"

    def __call__(self, answer):
        return answer


class VisitWebpageTool:
    name = "visit_webpage"
    description = "Visits a webpage at the given url and reads its content as a markdown string."
    inputs = {
        "url": {
            "type": "string",
            "description": "The url of the webpage to visit.",
        }
    }
    output_type = "string"

    def __init__(self, max_output_length: int = 40000):
        self.max_output_length = max_output_length

    def __call__(self, url: str) -> str:
        try:
            import re
            import requests
            from markdownify import markdownify
            from requests.exceptions import RequestException
            from smolagents.utils import truncate_content
        except ImportError as e:
            raise ImportError(
                "Install: pip install markdownify requests"
            ) from e

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            markdown_content = markdownify(response.text).strip()
            markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

            return truncate_content(markdown_content, self.max_output_length)

        except requests.exceptions.Timeout:
            return "Timeout error"
        except RequestException as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


class DuckDuckGoSearchTool:
    name = "web_search"
    description = "Performs a DuckDuckGo search"
    inputs = {
        "query": {"type": "string", "description": "Search query"}
    }
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        self.max_results = max_results
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "Install: pip install duckduckgo-search"
            ) from e
        self.ddgs = DDGS(**kwargs)

    def __call__(self, query: str) -> str:
        results = self.ddgs.text(query, max_results=self.max_results)

        if len(results) == 0:
            return "No results found"

        postprocessed_results = [
            f"[{result['title']}]({result['href']})\n{result['body']}"
            for result in results
        ]

        return "## Search Results\n\n" + "\n\n".join(postprocessed_results)


class TavilySearchTool:
    name = "tavily_search"
    description = "Performs a Tavily search"
    inputs = {
        "query": {"type": "string", "description": "Search query"}
    }
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        self.max_results = max_results
        try:
            from tavily import TavilyClient
        except ImportError as e:
            raise ImportError(
                "Install: pip install tavily"
            ) from e

        self.tavily = TavilyClient(**kwargs)

    def __call__(self, query: str) -> str:
        results = self.tavily.search(query, max_results=self.max_results)["results"]

        if len(results) == 0:
            return "No results found"

        postprocessed_results = [
            f"[{result['title']}]({result['url']})\n{result['content']}"
            for result in results
        ]

        return "## Search Results\n\n" + "\n\n".join(postprocessed_results)