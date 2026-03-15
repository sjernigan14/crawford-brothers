#!/usr/bin/env python3
"""
Script to add sameAs property to Restaurant schema JSON-LD blocks in HTML files.
"""

import json
import re
import sys
from pathlib import Path
from typing import Tuple, Optional, Dict, Any


# Files to modify
TARGET_FILES = [
    "blog-restaurants-near-carter-finley-stadium.html",
    "blog-valentines-day-dinner-cary-nc.html",
    "blog-new-years-eve-dinner-cary-nc.html",
    "blog-restaurants-near-lenovo-center-raleigh.html",
    "blog-restaurants-near-umstead-hotel-cary.html",
    "blog-restaurants-near-rdu-airport.html",
    "blog-mothers-day-restaurant-cary-nc.html",
    "blog-fathers-day-steakhouse-cary-nc.html",
    "blog-crawford-hospitality-restaurants-raleigh.html",
]

SAMEAS_DATA = [
    "https://www.instagram.com/crawfordbrosnc/",
    "https://www.facebook.com/crawfordbrothersteak",
    "https://crawfordbrotherssteakhouse.com/"
]


def find_json_ld_blocks(html_content: str) -> list[Tuple[int, int, str]]:
    """
    Find all JSON-LD script blocks in HTML content.
    Returns list of tuples: (start_pos, end_pos, content)
    """
    blocks = []
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'

    for match in re.finditer(pattern, html_content, re.DOTALL | re.IGNORECASE):
        start = match.start()
        end = match.end()
        content = match.group(1).strip()
        blocks.append((start, end, content))

    return blocks


def find_restaurant_schema(blocks: list[Tuple[int, int, str]]) -> Optional[Tuple[int, int, Dict[str, Any]]]:
    """
    Find and return the Restaurant schema from JSON-LD blocks.
    Returns tuple: (start_pos, end_pos, parsed_json)
    """
    for start, end, content in blocks:
        try:
            data = json.loads(content)

            # Handle array of schemas
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Restaurant":
                        return (start, end, data)
            # Handle single schema
            elif isinstance(data, dict) and data.get("@type") == "Restaurant":
                return (start, end, data)
        except json.JSONDecodeError as e:
            # Skip malformed JSON
            continue

    return None


def fix_malformed_json_ld(blocks: list[Tuple[int, int, str]]) -> list[Tuple[int, int, str]]:
    """
    Fix malformed JSON-LD blocks (missing @type, etc).
    Returns corrected list of blocks.
    """
    corrected_blocks = []

    for start, end, content in blocks:
        try:
            data = json.loads(content)

            # Check if it's an array with items missing @type
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "@type" not in item:
                        # Try to infer type from content
                        if "name" in item and "@context" in item:
                            item["@type"] = "Thing"
            # Check single schema
            elif isinstance(data, dict) and "@type" not in data:
                if "@context" in data:
                    data["@type"] = "Thing"

            # Re-serialize
            corrected_content = json.dumps(data, indent=2)
            corrected_blocks.append((start, end, corrected_content))
        except json.JSONDecodeError:
            # Keep original if can't fix
            corrected_blocks.append((start, end, content))

    return corrected_blocks


def add_sameas_to_restaurant(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add sameAs property to Restaurant schema data.
    """
    # If it's an array, find and modify the Restaurant item
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("@type") == "Restaurant":
                if "sameAs" not in item:
                    item["sameAs"] = SAMEAS_DATA
        return data
    # If it's a single schema
    elif isinstance(data, dict) and data.get("@type") == "Restaurant":
        if "sameAs" not in data:
            data["sameAs"] = SAMEAS_DATA
        return data

    return data


def process_file(file_path: Path) -> Tuple[bool, str]:
    """
    Process a single HTML file to add sameAs to Restaurant schema.
    Returns tuple: (success, message)
    """
    if not file_path.exists():
        return False, f"File not found: {file_path}"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Find all JSON-LD blocks
        blocks = find_json_ld_blocks(html_content)

        if not blocks:
            return False, f"No JSON-LD blocks found in {file_path.name}"

        # For Mother's Day file, fix malformed JSON-LD
        if "mothers-day" in file_path.name:
            blocks = fix_malformed_json_ld(blocks)

        # Find Restaurant schema
        result = find_restaurant_schema(blocks)

        if not result:
            return False, f"No Restaurant schema found in {file_path.name}"

        start, end, data = result

        # Check if sameAs already exists
        already_has_sameas = False
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("@type") == "Restaurant":
                    if "sameAs" in item:
                        already_has_sameas = True
        else:
            if "sameAs" in data:
                already_has_sameas = True

        if already_has_sameas:
            return True, f"Already has sameAs: {file_path.name}"

        # Add sameAs property
        modified_data = add_sameas_to_restaurant(data)

        # Re-serialize JSON
        modified_json = json.dumps(modified_data, indent=2)

        # Reconstruct the script tag
        original_block = html_content[start:end]
        new_block = original_block[:original_block.find('>')+1] + modified_json + '</script>'

        # Replace in HTML
        new_html_content = html_content[:start] + new_block + html_content[end:]

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)

        return True, f"✓ Modified: {file_path.name}"

    except json.JSONDecodeError as e:
        return False, f"JSON parsing error in {file_path.name}: {e}"
    except Exception as e:
        return False, f"Error processing {file_path.name}: {e}"


def main():
    """Main function"""
    # Get directory from command line or use current directory
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path.cwd()

    print(f"Processing HTML files in: {directory}\n")

    success_count = 0
    error_count = 0

    for filename in TARGET_FILES:
        file_path = directory / filename
        success, message = process_file(file_path)

        print(message)

        if success:
            success_count += 1
        else:
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Results: {success_count} successful, {error_count} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
