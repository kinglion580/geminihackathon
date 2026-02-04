#!/usr/bin/env python3
"""
Merge Skills Script
===================
Merges all skills from multiple directories into a single /skills folder.
For duplicate skills, selects the best version based on:
1. Content completeness (file size, number of sections)
2. Has supporting files (scripts, modules, examples)
3. More recent modifications
"""

import os
import re
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import yaml

BASE_DIR = Path(__file__).parent
TARGET_DIR = BASE_DIR / "skills"

# Source directories to scan
SOURCE_DIRS = [
    BASE_DIR / "AI Act skills packages",
    BASE_DIR / "skills",
    BASE_DIR / "Risks packages",
]


@dataclass
class SkillInfo:
    """Information about a skill"""
    name: str
    path: Path
    description: str = ""
    content_size: int = 0
    num_sections: int = 0
    has_scripts: bool = False
    has_modules: bool = False
    has_examples: bool = False
    num_supporting_files: int = 0
    score: int = 0

    def calculate_score(self):
        """Calculate quality score for this skill version"""
        self.score = 0

        # Content size (larger = more comprehensive)
        self.score += min(self.content_size // 1000, 20)  # Max 20 points

        # Number of sections
        self.score += min(self.num_sections * 2, 20)  # Max 20 points

        # Supporting files
        if self.has_scripts:
            self.score += 15
        if self.has_modules:
            self.score += 15
        if self.has_examples:
            self.score += 10

        # Additional supporting files
        self.score += min(self.num_supporting_files * 2, 20)  # Max 20 points

        return self.score


def parse_skill_file(skill_file: Path) -> Optional[SkillInfo]:
    """Parse a SKILL.md file and extract metadata"""
    try:
        content = skill_file.read_text(encoding='utf-8')

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            return None

        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        name = frontmatter.get('name', '')

        if not name:
            return None

        # Get skill directory
        skill_dir = skill_file.parent

        # Count supporting files
        has_scripts = (skill_dir / "scripts").exists() or (skill_dir / "script").exists()
        has_modules = (skill_dir / "modules").exists()
        has_examples = (skill_dir / "examples").exists() or (skill_dir / "example").exists()

        # Count all files in directory
        num_supporting_files = sum(1 for _ in skill_dir.rglob("*") if _.is_file() and _.name != "SKILL.md")

        # Count sections in content
        num_sections = len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE))

        skill_info = SkillInfo(
            name=name,
            path=skill_dir,
            description=frontmatter.get('description', ''),
            content_size=len(content),
            num_sections=num_sections,
            has_scripts=has_scripts,
            has_modules=has_modules,
            has_examples=has_examples,
            num_supporting_files=num_supporting_files,
        )

        skill_info.calculate_score()
        return skill_info

    except Exception as e:
        print(f"Warning: Could not parse {skill_file}: {e}")
        return None


def discover_all_skills() -> Dict[str, List[SkillInfo]]:
    """Discover all skills from all source directories"""
    skills_by_name: Dict[str, List[SkillInfo]] = {}

    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            print(f"Skipping non-existent directory: {source_dir}")
            continue

        print(f"\nScanning: {source_dir}")

        for skill_file in source_dir.rglob("SKILL.md"):
            # Skip nested duplicates in explaining-code folder
            if "explaining-code" in str(skill_file):
                continue

            skill_info = parse_skill_file(skill_file)
            if skill_info:
                if skill_info.name not in skills_by_name:
                    skills_by_name[skill_info.name] = []
                skills_by_name[skill_info.name].append(skill_info)

    return skills_by_name


def select_best_skill(skill_versions: List[SkillInfo]) -> SkillInfo:
    """Select the best version of a skill"""
    if len(skill_versions) == 1:
        return skill_versions[0]

    # Sort by score (descending)
    sorted_versions = sorted(skill_versions, key=lambda s: s.score, reverse=True)
    return sorted_versions[0]


def merge_skills(dry_run: bool = True):
    """Merge all skills into target directory"""
    print("=" * 80)
    print("SKILLS MERGE TOOL")
    print("=" * 80)

    # Discover all skills
    all_skills = discover_all_skills()

    print(f"\n\nFound {len(all_skills)} unique skill names")

    # Analyze duplicates
    duplicates = {name: versions for name, versions in all_skills.items() if len(versions) > 1}
    print(f"Found {len(duplicates)} skills with duplicates")

    # Report
    print("\n" + "=" * 80)
    print("DUPLICATE ANALYSIS")
    print("=" * 80)

    merge_plan: List[Tuple[str, SkillInfo, List[SkillInfo]]] = []

    for name in sorted(all_skills.keys()):
        versions = all_skills[name]
        best = select_best_skill(versions)

        if len(versions) > 1:
            print(f"\n{name} ({len(versions)} versions):")
            for v in sorted(versions, key=lambda s: s.score, reverse=True):
                marker = "✓ BEST" if v == best else "  skip"
                print(f"  {marker} | Score: {v.score:3d} | Size: {v.content_size:6d} | "
                      f"Files: {v.num_supporting_files:2d} | {v.path}")

        merge_plan.append((name, best, versions))

    # Summary
    print("\n" + "=" * 80)
    print("MERGE PLAN SUMMARY")
    print("=" * 80)
    print(f"Total unique skills: {len(merge_plan)}")
    print(f"Skills with duplicates: {len(duplicates)}")

    if dry_run:
        print("\n[DRY RUN] No changes made. Run with --execute to perform merge.")
        return merge_plan

    # Execute merge
    print("\n" + "=" * 80)
    print("EXECUTING MERGE")
    print("=" * 80)

    # Create clean target structure
    merged_count = 0

    for name, best, all_versions in merge_plan:
        target_path = TARGET_DIR / name

        # Skip if already the best version in target location
        if best.path == target_path:
            print(f"✓ {name} - Already in correct location")
            continue

        # Remove existing versions in target if they exist
        if target_path.exists():
            # Check if it's a numbered version folder
            existing_numbered = [d for d in TARGET_DIR.glob(f"{name}-*") if d.is_dir()]
            for numbered in existing_numbered:
                if numbered != best.path:
                    print(f"  Removing duplicate: {numbered}")
                    if not dry_run:
                        shutil.rmtree(numbered)

        # Copy best version to target
        print(f"✓ {name} - Copying from {best.path}")
        if not dry_run:
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.copytree(best.path, target_path)

        merged_count += 1

    print(f"\nMerged {merged_count} skills")

    # Clean up numbered duplicates
    print("\n" + "=" * 80)
    print("CLEANING UP DUPLICATES")
    print("=" * 80)

    # Find all numbered folders like skill-name-2, skill-name-3
    for skill_dir in TARGET_DIR.iterdir():
        if skill_dir.is_dir():
            # Check if this is a numbered version
            match = re.match(r'^(.+)-(\d+)$', skill_dir.name)
            if match:
                base_name = match.group(1)
                # Check if base version exists
                base_path = TARGET_DIR / base_name
                if base_path.exists():
                    print(f"  Removing numbered duplicate: {skill_dir.name}")
                    if not dry_run:
                        shutil.rmtree(skill_dir)

    return merge_plan


def main():
    import sys

    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("\n" + "!" * 80)
        print("DRY RUN MODE - No changes will be made")
        print("Run with --execute to perform actual merge")
        print("!" * 80)

    merge_skills(dry_run=dry_run)

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)


if __name__ == "__main__":
    main()
