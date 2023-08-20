import json


class MockResponse:
    def __init__(self, text: str, status: int):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def json(self):
        return json.loads(self._text)

    async def __aexit__(self, exc_type, exc, tb):  # type: ignore
        pass

    async def __aenter__(self):
        return self
