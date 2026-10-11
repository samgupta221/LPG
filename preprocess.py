import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

    enriched_posts = []

    for post in posts:
        metadata = extract_metadata(post["text"])

        # FIX: safer dict merge
        post_with_metadata = {**post, **metadata}
        enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post.get("tags", [])

        # FIX: safe mapping (prevents KeyError)
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post["tags"] = list(new_tags)

    # FIX: avoid crash if path is None
    if processed_file_path:
        with open(processed_file_path, "w", encoding="utf-8") as outfile:
            json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    template = """
    You are given a LinkedIn post. Extract:

    1. line_count (integer)
    2. language (English or Hinglish)
    3. tags (max 2 items)

    Return ONLY valid JSON.

    Post:
    {post}
    """

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = chain.invoke({"post": post})

    json_parser = JsonOutputParser()

    try:
        return json_parser.parse(response.content)
    except Exception:
        # FIX: fallback cleaning for LLM messy output
        cleaned = response.content.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)


def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post.get("tags", []))

    unique_tags_list = ", ".join(unique_tags)

    template = """
    You will get a list of tags.

    Merge similar tags into unified categories.

    Rules:
    1. Merge similar meaning tags
    2. Use Title Case
    3. Return ONLY JSON mapping original -> unified

    Example:
    {"Jobseekers": "Job Search", "Job Hunting": "Job Search"}

    Tags:
    {tags}
    """

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = chain.invoke({"tags": unique_tags_list})

    json_parser = JsonOutputParser()

    try:
        return json_parser.parse(response.content)
    except Exception:
        cleaned = response.content.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")