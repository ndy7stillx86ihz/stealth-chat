from abc import ABC, abstractmethod
from typing import Any, Optional


class IEventListener(ABC):
    @abstractmethod
    def update(self, d: Optional[Any]) -> None: pass
