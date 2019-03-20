from dataclasses import dataclass


@dataclass
class User:
    name: str
    user_id: int
    just_joined: bool=True


a = User("x", 4)
print(a.name)
