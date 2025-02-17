from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some
from ..imports import types


def say(level: types.LogLevel, msg: str) -> None:
    raise NotImplementedError

def say_error(msg: str) -> None:
    raise NotImplementedError

def say_crit(msg: str) -> None:
    raise NotImplementedError

def say_warn(msg: str) -> None:
    raise NotImplementedError

def say_info(msg: str) -> None:
    raise NotImplementedError

def say_verbose(msg: str) -> None:
    raise NotImplementedError

def say_debug(msg: str) -> None:
    raise NotImplementedError

def say_syserror(msg: str) -> None:
    raise NotImplementedError

