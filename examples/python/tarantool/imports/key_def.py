from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def new(parts: List[types.KeyPartDef]) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def merge(left: int, right: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def validate_key(key_def: int, key: bytes) -> Tuple[bool, int]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def validate_full_key(key_def: int, key: bytes) -> Tuple[bool, int]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def compare(key_def: int, left: int, right: int) -> int:
    raise NotImplementedError

def compare_keys(key_def: int, left: int, right: int) -> int:
    raise NotImplementedError

def extract_key(key_def: int, tuple: int) -> int:
    raise NotImplementedError

def part_count(key_def: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def validate_tuple(key_def: int, tuple: int) -> bool:
    raise NotImplementedError

def dup(key_def: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def delete(key_def: int) -> None:
    raise NotImplementedError

def dump_parts(key_def: int) -> List[types.KeyPartDef]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

