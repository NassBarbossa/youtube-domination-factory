"""Extract topic from video title and description using keyword matching."""
import re

# Ordered by priority — more specific patterns first
TOPIC_KEYWORDS = [
    ("claude-computer-use", ["claude computer use", "computer use claude", "claude controls", "computer use"]),
    ("claude-mythos", ["claude mythos", "mythos"]),
    ("claude-code", ["claude code", "claudecode"]),
    ("claude", ["claude ai", "anthropic claude"]),
    ("gpt", ["gpt-5", "gpt-4", "gpt5", "gpt4", "chatgpt", "openai gpt"]),
    ("gemini", ["gemini", "google gemini"]),
    ("grok", ["grok"]),
    ("vibe-coding", ["vibe coding", "vibecoding", "vibe code"]),
    ("ai-agents", ["ai agent", "ai agents", "autonomous agent", "agent ai"]),
    ("ai-tools", ["ai tool", "ai tools", "ai app", "ai apps"]),
    ("cursor", ["cursor ai", "cursor ide", "cursor editor"]),
    ("ai-business", ["ai business", "ai startup", "ai company", "ai money", "make money ai"]),
    ("ai-news", ["ai news", "ai update", "ai release", "just released", "just launched"]),
]


def extract_topic(title: str, description: str) -> str:
    """Extract topic from title + first 500 chars of description."""
    text = (title + " " + description[:500]).lower()
    for topic, keywords in TOPIC_KEYWORDS:
        for kw in keywords:
            if kw.lower() in text:
                return topic
    return "other"
