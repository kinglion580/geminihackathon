"""
Governance AI Agent - Python Implementation Package

A comprehensive AI governance agent with access to all skills in /skills folder.
Provides end-to-end guidance on building compliant, safe, ethical, and robust
AI systems.
"""

from .governance_agent import (
    GovernanceAIAgent,
    AgentConfig,
    SkillMetadata
)

__version__ = "1.0.0"
__author__ = "AI Act Skills Packages"
__all__ = [
    "GovernanceAIAgent",
    "AgentConfig",
    "SkillMetadata"
]
