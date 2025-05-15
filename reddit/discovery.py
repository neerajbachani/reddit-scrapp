# reddit/discovery.py
from openai import OpenAI
import json
from config.config_loader import get_config
from utils.logger import setup_logger

log = setup_logger()
config = get_config()
PROMPT_PATH = "gpt/prompts/community_discovery.txt"

client = OpenAI()

def load_discovery_prompt_template():
    """Load the community discovery prompt template from file."""
    try:
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log.error(f"Error loading community discovery prompt template: {str(e)}")
        return (
            "Based on the following Reddit post summaries, suggest a ranked list of 12 relevant subreddits "
            "with pain points Cronlytic could solve. Respond in JSON format."
        )

DISCOVERY_PROMPT_TEMPLATE = load_discovery_prompt_template()

def build_discovery_prompt(top_post_summaries: list[str]) -> list:
    """Builds the GPT prompt for discovering adjacent subreddits using template."""
    joined = "\n".join(f"- {summary}" for summary in top_post_summaries)
    prompt_content = DISCOVERY_PROMPT_TEMPLATE.replace("{SUMMARIES}", joined)

    return [
        {"role": "system", "content": "You are an expert in developer marketing and community discovery."},
        {"role": "user", "content": prompt_content}
    ]

def discover_adjacent_subreddits(summaries: list[str], model: str = None) -> list:
    """Uses GPT-4.1 (from config) to suggest exploratory subreddits."""
    model = model or config["openai"].get("model_deep", "gpt-4.1")
    log.info(f"Running discovery with {len(summaries)} post summaries using model: {model}")
    
    prompt = build_discovery_prompt(summaries)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=0.3
        )
        content = response.choices[0].message.content
        log.debug(f"Discovery API response: {content[:200]}...")

        suggestions = json.loads(content)
        if not isinstance(suggestions, list):
            log.error("GPT response is not a list. Skipping.")
            return []

        valid_suggestions = [
            item for item in suggestions
            if isinstance(item, dict) and "subreddit" in item
        ]

        # Remove already-known subreddits
        primary_set = {sub.lower() for sub in config["subreddits"]["primary"]}
        filtered = [s for s in valid_suggestions if s["subreddit"].lower() not in primary_set]

        if not filtered:
            log.warning("No valid *new* subreddit suggestions found in GPT response.")
            return []

        return filtered[:config["subreddits"]["exploratory_limit"]]

    except json.JSONDecodeError as je:
        log.error(f"Failed to parse GPT discovery response as JSON: {str(je)}")
        return []
    except Exception as e:
        log.error(f"Error in discovery process: {str(e)}")
        return []