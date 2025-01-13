from abc import ABC, abstractmethod
from typing import Any, Optional


class IEventListener(ABC):
    @abstractmethod
    def update(self,e: 'Event',  d: Optional[Any]) -> None: pass
