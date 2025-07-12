from abc import ABC, abstractmethod

if __name__ == '__main__': from model import Product
else: from .model import Product


class CRUD_Interface(ABC):
    @abstractmethod
    def create(self, p: Product) -> bool: ...
    @abstractmethod
    def read(self, id_: int) -> Product: ...
    @abstractmethod
    def update(self, id_: int, product: Product) -> bool: ...
    @abstractmethod
    def delete(self, id_: int) -> bool: ...


class OnMemoryDatabase(CRUD_Interface):
    __obj = None

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)

        return cls.__obj

    def __init__(self):
        self._objects: list[Product] = []

    def create(self, p: Product) -> bool:
        self._objects.append(p)
        return True

    def read(self, id_: int):
        return self._objects[id_]

    # USELESS
    def update(self, id_: int, product: Product) -> bool: ...

    def delete(self, id_: int) -> bool:
        try:
            self._objects.remove(id_)
            return True
        except ValueError: return False

    def isEmpty(self) -> bool:
        return len(self._objects) == 0

    def findByName(self, name: str) -> Product | None:
        for p in self._objects:
            if p.name == name: return p
        return None

    def getAll(self) -> list[Product]:
        return self._objects