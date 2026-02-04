#!/usr/bin/env python3
"""
Batch fact checker for articles folder
Runs Google Fact Check on all article files
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add the fact-checker script directory to path
fact_checker_dir = Path("AI Act skills packages/AI Act package/fact-checker/scripts")
sys.path.insert(0, str(fact_checker_dir))

from google_fact_checker import fact_check

def process_articles(articles_dir="articles", output_dir="Output"):
    """Process all articles in the articles directory"""

    # Set API key
    api_key = "AIzaSyCCVJihaLR7_d4vQsgmY6OlATBwpryHKjU"
    os.environ['GOOGLE_FACT_CHECK_API_KEY'] = api_key

    articles_path = Path(articles_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Get all text files in articles directory
    article_files = sorted(articles_path.glob("Article_*.txt"))

    print(f"Found {len(article_files)} articles to process")

    results = []
    results.append("# FACT-CHECK BATCH RESULTS\n")
    results.append(f"**Total Articles Processed:** {len(article_files)}\n")
    results.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    results.append("---\n\n")

    for i, article_file in enumerate(article_files, 1):
        print(f"Processing {article_file.name} ({i}/{len(article_files)})...")

        # Read article content
        try:
            content = article_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  Error reading {article_file.name}: {e}")
            continue

        # Skip very short articles (likely section headers)
        if len(content.strip()) < 100:
            print(f"  Skipping {article_file.name} - too short")
            continue

        # Extract first meaningful claim (first 200 chars as context)
        claim = content.strip()[:500]

        # Run fact check
        print(f"  Checking claim...")
        fact_check_result = fact_check(claim)

        # Add to results
        results.append(f"## {article_file.name}\n\n")
        results.append(f"**Article Content Preview:**\n```\n{content.strip()[:300]}...\n```\n\n")
        results.append(f"**Fact Check Results:**\n")

        if fact_check_result.startswith("ERROR"):
            results.append(f"❌ {fact_check_result}\n\n")
        elif fact_check_result == "NO_RESULTS":
            results.append(f"ℹ️ No existing fact-checks found for this content\n\n")
        else:
            results.append(f"```\n{fact_check_result}\n```\n\n")

        results.append("---\n\n")

    # Write output report
    output_file = output_path / "FACT_CHECK_BATCH_RESULTS.md"
    output_file.write_text("".join(results), encoding='utf-8')

    print(f"\n✅ Fact-check complete!")
    print(f"Results saved to: {output_file}")

    return str(output_file)

if __name__ == "__main__":
    output_file = process_articles()
    print(f"\nView results: {output_file}")
