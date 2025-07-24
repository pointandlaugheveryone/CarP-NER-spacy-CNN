from typing import List


class Label:
    def __init__(self, start: int, end: int, label: str, value: str):
        self.start = start
        self.end = end
        self.label = label
        self.value = value

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "label": self.label,
            "value": self.value,
        }

    @staticmethod
    def from_dict(data: dict):
        return Label(
            start=data["start"],
            end=data["end"],
            label=data["label"],
            value=data["value"],
        )


class Document:
    def __init__(self, name: int, content: str, labels: List[dict]):
        self.name = name
        self.content = content
        self.labels = [Label.from_dict(label) for label in labels]

    def to_dict(self):
        return {
            "id": self.name,
            "content": self.content,
            "labels": [label.to_dict() for label in self.labels],
        }

    @staticmethod
    def from_dict(data: dict):
        return Document(
            name=data["name"],
            content=data["content"],
            labels=data["labels"],
        )



