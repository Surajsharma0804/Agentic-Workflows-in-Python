from abc import ABC, abstractmethod
from typing import Dict, Any

class PluginBase(ABC):
    """
    Base interface for all task plugins.
    """

    name: str = "base"

    def __init__(self, params: Dict[str, Any], audit=None):
        self.params = params or {}
        self.audit = audit

    @abstractmethod
    def plan(self) -> list:
        """
        Return a list of planned atomic actions (for dry-run / UI).
        Each action is a dict describing 'action', 'target', 'data'...
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> dict:
        """
        Execute the task; return result dict with status and metadata.
        """
        raise NotImplementedError

    def rollback(self, result_meta: dict) -> dict:
        """
        Optional rollback if execute partially applied changes.
        """
        return {"status": "noop", "reason": "no rollback implemented"}
