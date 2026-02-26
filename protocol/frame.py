from dataclasses import dataclass

@dataclass
class Frame:
    type: int
    message: str
    id: int
    id2: int | None = None
    length: int | None = None
    payload: str | None = None

    def to_json(self):  
        return {
            "type": self.type,
            "message": self.message,
            "id": self.id,
            "id2": self.id2,
            "length": len(self.payload) if self.payload is not None else None,
            "payload": self.payload
        }
