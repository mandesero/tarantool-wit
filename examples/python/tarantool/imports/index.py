from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def len(index: types.Index) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def bsize(index: types.Index) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def random(index: types.Index, rnd: int) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def get(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def min(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def max(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def count(iter_type: types.IteratorType, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def unique(index: types.Index) -> bool:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def get_type(index: types.Index) -> types.IndexType:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def parts(index: types.Index) -> List[types.KeyPartDef]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def pairs(index: types.Index, opts: types.PairsOpts) -> types.Iterator:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def select(index: types.Index, key: bytes, opts: types.SelectOpts) -> List[int]:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def update(index: types.Index, key: bytes, ops: List[types.UpdateOp]) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def delete(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def alter(index: types.Index, unique: bool, parts: List[types.KeyPartDef]) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def drop(index: types.Index) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def rename(index: types.Index, new_name: str) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def stat(index: types.Index) -> types.IndexStat:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def compact(index: types.Index) -> None:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def tuple_pos(index: types.Index, key: bytes) -> int:
    """
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

