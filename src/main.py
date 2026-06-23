from fastapi import FastAPI
from src.agents.researcher import ResearcherSwarm, LiveEvent
from src.agents.editor import AutonomousEditor, WikiArticle

app = FastAPI(title="Living Wikipedia", version="1.0.0")
researcher = ResearcherSwarm()
editor = AutonomousEditor()

# In-memory mock database
db = {
    "AI_Safety": WikiArticle(
        title="AI Safety",
        content="Artificial Intelligence safety is an interdisciplinary field.",
        last_updated="2026-01-01",
        revision_history=["Initial human creation"]
    )
}

@app.post("/webhook/event")
async def process_live_event(event: LiveEvent, target_article: str):
    """
    Ingests a live event (e.g. from Twitter), fact-checks it, and rewrites the target Wiki article.
    """
    if target_article not in db:
        return {"error": "Article not found"}
        
    report = await researcher.cross_reference(event)
    updated_article = await editor.update_article(report, db[target_article])
    
    db[target_article] = updated_article
    return updated_article

@app.get("/article/{title}")
def get_article(title: str):
    return db.get(title, {"error": "Not found"})
