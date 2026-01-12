"""
Alethia Orchestration Package

Provides runtime orchestration for the Alethia Protocol.

Modules included:
- alethia_runtime: Core runtime engine that manages data flow, context evaluation,
  trust scoring, and entropy application.

This __init__.py exposes the primary orchestration class for integration
with Sentenial-X agents, export guards, and higher-level workflows.
"""

from .alethia_runtime import AlethiaRuntime

__all__ = [
    "AlethiaRuntime"
]
