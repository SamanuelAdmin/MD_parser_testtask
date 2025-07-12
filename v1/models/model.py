from dataclasses import dataclass

@dataclass
class Product:
    url: str | None = None
    name: str | None = None
    description: str | None = None
    calories: str | None = None
    fats: str | None = None
    carbs: str | None = None
    proteins: str | None = None
    unsaturated_fats: str | None = None
    sugar: str | None = None
    salt: str | None = None
    portion: str | None = None

    def __str__(self):
        return f'{self.name}  {self.url}'