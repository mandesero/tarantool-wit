from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def new(message: str, type: str, code: int) -> types.BoxError:
    raise NotImplementedError

def set(err: types.BoxError) -> None:
    raise NotImplementedError

def last() -> Optional[types.BoxError]:
    raise NotImplementedError

def clear() -> None:
    raise NotImplementedError

def to_string(err: types.BoxError) -> str:
    raise NotImplementedError

