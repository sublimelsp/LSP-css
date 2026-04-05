from __future__ import annotations

from typing import List

from LSP.plugin import Notification
from typing_extensions import TypeAlias

FilePath: TypeAlias = str


class CustomDataChangedNotification:
    Type = "css/customDataChanged"
    Params: TypeAlias = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])
