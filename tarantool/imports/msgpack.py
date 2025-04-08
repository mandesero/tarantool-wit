from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some



def encode(data: bytes) -> bytes:
    """
    Encodes a JSON-like structure into MsgPack format.
    * `data` is a byte array containing a valid UTF-8 encoded JSON string.
    
    Raises: `tarantool.types.Err(tarantool.imports.types.MsgpackError)`
    """
    raise NotImplementedError

def decode(data: bytes) -> bytes:
    """
    Decodes a MsgPack-encoded byte array back into a JSON-like structure.
    * `data` is a byte array containing data encoded in MessagePack format.
    
    Raises: `tarantool.types.Err(tarantool.imports.types.MsgpackError)`
    """
    raise NotImplementedError

