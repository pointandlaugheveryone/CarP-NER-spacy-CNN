import json
from typing import List


class Label:
    start: int
    end: int
    label: str
    value: str

    def __init__(self, start: int, end: int, label: str, value:str): 
        self.start = start
        self.end = end
        self.label = label
        self.value = value

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "label": self.label,
            "value":self.value
        }



class Document:
    content: str
    labels: List[Label]
    source_doc_id: int 
    '''
    source_doc_id used for debugging
    raw data is collected in individual text files, later split into sequences
    '''
    def __init__(self,source_doc_id:int, content: str, labels: List[Label]): 
        self.source_doc_id= source_doc_id
        self.content = content
        self.labels = labels

    def to_dict(self) -> dict:
        return {
            "source_doc_id":self.source_doc_id,
            "content": self.content,
            "labels": [a.to_dict() for a in self.labels],
        }
