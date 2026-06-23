from pydantic import BaseModel
import asyncio
from src.agents.researcher import ResearchReport

class WikiArticle(BaseModel):
    title: str
    content: str
    last_updated: str
    revision_history: list[str]

class AutonomousEditor:
    def __init__(self):
        self.name = "Wiki Markdown Editor"

    async def update_article(self, report: ResearchReport, current_article: WikiArticle) -> WikiArticle:
        await asyncio.sleep(0.05) # Simulate LLM rewriting content
        
        if not report.is_verified:
            # If not verified, append to a "Rumors" section instead of main body
            new_content = current_article.content + f"\n\n## Unverified Claims\n- {report.fact_checked_summary}"
        else:
            # If verified, rewrite main body
            new_content = f"## Breaking Update\n{report.fact_checked_summary}\n\n{current_article.content}"
            
        current_article.revision_history.append(f"Auto-update based on event {report.event_id}")
        
        return WikiArticle(
            title=current_article.title,
            content=new_content,
            last_updated="Just now",
            revision_history=current_article.revision_history
        )
