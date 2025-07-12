from abc import ABC, abstractmethod

class IParser(ABC):
    @abstractmethod
    def __init__(self, url: str) -> None: ...
    @abstractmethod
    def parse(self) -> list[dict[str, str]]: ...

    '''
        Current parsing result:
        dict[str, dict[str, str]]
        
        {
            'product1': {
                'field1': 'value1',
                'field2': 'value2',
                'field3': 'value3'
            },
            'product2': { ... }
        }
    '''
