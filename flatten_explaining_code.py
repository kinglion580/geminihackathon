#!/usr/bin/env python3
"""
Flatten skills from skills/explaining-code/ to skills/
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SKILLS_DIR = PROJECT_ROOT / "skills"
EXPLAINING_CODE_DIR = SKILLS_DIR / "explaining-code"

def get_existing_skills():
    """Get set of existing skill names in skills/"""
    existing = set()
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and item.name != "explaining-code":
            existing.add(item.name)
    return existing

def flatten_skills():
    """Flatten all skills from explaining-code to skills/"""
    existing = get_existing_skills()
    print(f"Existing skills in skills/: {len(existing)}")

    # Find all SKILL.md files in explaining-code
    skill_files = list(EXPLAINING_CODE_DIR.rglob("SKILL.md"))
    print(f"Skills found in explaining-code/: {len(skill_files)}")

    copied = 0
    skipped = 0

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        skill_name = skill_dir.name

        # Check if already exists
        if skill_name in existing:
            # Find unique name
            counter = 2
            while f"{skill_name}-{counter}" in existing:
                counter += 1
            new_name = f"{skill_name}-{counter}"
        else:
            new_name = skill_name

        dest = SKILLS_DIR / new_name

        if dest.exists():
            print(f"⏭️  Skip (exists): {skill_name}")
            skipped += 1
            continue

        try:
            shutil.copytree(skill_dir, dest)
            existing.add(new_name)
            copied += 1
            if new_name != skill_name:
                print(f"✅ {skill_name} -> {new_name}")
            else:
                print(f"✅ {skill_name}")
        except Exception as e:
            print(f"❌ Error copying {skill_name}: {e}")

    print(f"\n=== SUMMARY ===")
    print(f"Copied: {copied}")
    print(f"Skipped: {skipped}")
    print(f"Total skills in skills/: {len(existing)}")

if __name__ == "__main__":
    flatten_skills()
