import abc
from typing import Iterable

class User(object):
    def __init__(self, id: str = None, slug: str = None, name: str = None, markdown: str = None, html: str = None):
        self.id = id
        self.name = name
        self.markdown = markdown
        self.html = html


class UserDAO(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, User: User) -> User:
        pass

    @abc.abstractmethod
    def update(self, User: User) -> User:
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[User]:
        pass

    @abc.abstractmethod
    def get_by_id(self, User_id: str) -> User:
        pass

class UserNotFound(Exception):
    pass