from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from typing import Type

class SearchInput(BaseModel):
    query: str = Field(description="Requête de recherche")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Recherche des informations récentes sur le web. "
        "Utilise pour trouver des actualités IA, des articles, des tendances."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=5,
                region="fr-fr"
            ))
        
        if not results:
            return "Aucun résultat trouvé."
        
        formatted = []
        for r in results:
            formatted.append(
                f"**{r['title']}**\n{r['body']}\nSource: {r['href']}\n"
            )
        return "\n---\n".join(formatted)