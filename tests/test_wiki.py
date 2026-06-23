import pytest
from src.agents.researcher import ResearcherSwarm, LiveEvent
from src.agents.editor import AutonomousEditor, WikiArticle

@pytest.mark.asyncio
async def test_wiki_pipeline_verified():
    researcher = ResearcherSwarm()
    editor = AutonomousEditor()
    
    event = LiveEvent(
        event_id="EVT-001",
        headline="AGI Achieved Internally",
        sources=["TechCrunch", "Reuters"],
        credibility_score=0.9
    )
    
    article = WikiArticle(
        title="AGI",
        content="AGI is theoretical.",
        last_updated="old",
        revision_history=[]
    )
    
    report = await researcher.cross_reference(event)
    assert report.is_verified is True
    
    updated = await editor.update_article(report, article)
    assert "Breaking Update" in updated.content

@pytest.mark.asyncio
async def test_wiki_pipeline_unverified():
    researcher = ResearcherSwarm()
    editor = AutonomousEditor()
    
    event = LiveEvent(
        event_id="EVT-002",
        headline="Aliens Use Python",
        sources=["Reddit"],
        credibility_score=0.2
    )
    
    article = WikiArticle(
        title="Python",
        content="Python is a programming language.",
        last_updated="old",
        revision_history=[]
    )
    
    report = await researcher.cross_reference(event)
    assert report.is_verified is False
    
    updated = await editor.update_article(report, article)
    assert "Unverified Claims" in updated.content
