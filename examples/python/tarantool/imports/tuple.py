from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some



def new(format: int, data: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def ref(t: int) -> int:
    raise NotImplementedError

def unref(t: int) -> None:
    raise NotImplementedError

def field_count(t: int) -> int:
    raise NotImplementedError

def bsize(t: int) -> int:
    raise NotImplementedError

def to_buf(t: int) -> bytes:
    raise NotImplementedError

def format(t: int) -> int:
    raise NotImplementedError

def field(t: int, idx: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def field_by_path(path: str, index_base: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def update(t: int, expr: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def upsert(t: int, expr: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def validate(t: int, format: int) -> bool:
    raise NotImplementedError

