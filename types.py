from LSP.plugin import Notification
from LSP.plugin.core.typing import List


FilePath = str


class CustomDataChangedNotification:
    Type = 'css/customDataChanged'
    Params = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])
