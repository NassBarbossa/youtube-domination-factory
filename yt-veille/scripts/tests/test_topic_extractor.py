from topic_extractor import extract_topic, TOPIC_KEYWORDS

def test_extract_topic_claude_code():
    assert extract_topic("Claude Code Full Course 4 Hours", "Learn Claude Code...") == "claude-code"

def test_extract_topic_computer_use():
    assert extract_topic("Claude Can Now Control Your Computer", "Computer use demo...") == "claude-computer-use"

def test_extract_topic_vibe_coding():
    assert extract_topic("I Built an App with Vibe Coding", "VibeCoding is the new way...") == "vibe-coding"

def test_extract_topic_ai_agents():
    assert extract_topic("AI Agents Will Replace Your Team", "Autonomous AI agent...") == "ai-agents"

def test_extract_topic_gpt():
    assert extract_topic("GPT-5 Just Changed Everything", "OpenAI released GPT-5...") == "gpt"

def test_extract_topic_from_description_when_title_is_vague():
    assert extract_topic("This Changes Everything", "I tested Claude Code and...") == "claude-code"

def test_extract_topic_unknown():
    assert extract_topic("My Morning Routine", "I wake up at 5am...") == "other"

def test_extract_topic_case_insensitive():
    assert extract_topic("CLAUDE CODE is AMAZING", "") == "claude-code"

def test_extract_topic_priority():
    """Claude Computer Use should match before generic Claude Code."""
    assert extract_topic("Claude Computer Use Demo", "Claude Code controls screen") == "claude-computer-use"
