from __future__ import annotations

from typing import List

from LSP.plugin import Notification

FilePath = str


class CustomDataChangedNotification:
    Type = "css/customDataChanged"
    Params = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])
