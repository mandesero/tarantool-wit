from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def current() -> types.Session:
    raise NotImplementedError

def iproto_send(session: types.Session, header: bytes, body: bytes) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def id(session: types.Session) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def exists() -> bool:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def get_peer(session: types.Session) -> types.Peer:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def sync() -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def user() -> str:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def type(session: types.Session) -> str:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def su(session: types.Session, user: str) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def uid(session: types.Session) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def euid(session: types.Session) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def get_storage(session: types.Session) -> List[Tuple[str, str]]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

