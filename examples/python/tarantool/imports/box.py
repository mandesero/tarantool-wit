from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def schema_version() -> int:
    raise NotImplementedError

def space_by_name(name: str) -> types.Space:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def index_by_name(name: str, index_base: int) -> types.Index:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def insert(space: types.Space, tup: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def replace(space: types.Space, tup: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def truncate(space: types.Space) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def delete(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def update(index: types.Index, key: bytes, ops: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def upsert(index: types.Index, tup: bytes, ops: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

