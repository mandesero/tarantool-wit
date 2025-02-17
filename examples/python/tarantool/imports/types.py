"""
* Architecture Decision Record for the Tarantool WIT definitions.
 *
 * Aside from enums, we opted to express every Tarantool type as either
 * record, resource or type alias. Choice of an expressing entity for each
 * type might seem arbitrary, but they are all aligned with the following
 * ideas:
 *
 * Resource is an entity that lives outside of a WASM component. That means
 * its whole lifecycle is managed entirely by the embedder. These entities are
 * explicitly created and destroyed by the embedder on command from a WASM
 * component. Resource entities, unlike records, can have methods.
 *
 * We made a decision to use resource semantics only for the iterators. One
 * might argue that the same semantics should apply to the spaces, indexes and
 * other types, since they are all handled by Tarantool and not by a WASM
 * component. That is a valid point, but a key difference between a space and
 * an iterator in regard to the ownesrhip semantics is that space is
 * manipulated by a `space_id` and is owned by Tarantool, while an iterator
 * is owned by an application and is manipulated directly.
 *
 * Resource semantics also requires every resource to be freed after use,
 * which makes no sense for spaces or indexes, because we would have to free
 * a reference. Yet still, it makes perfect sense for iterators.
 *
 * Final thing for consideration is object notation and methods. That feature
 * off resources looks very appealing to use for other Tarantool types, but it
 * has a few downsides to it. Every resource must be stored within a resource
 * table on the embedder side, and removed from there after free. Some of
 * our target languages have a notion of destructor and some of them don't.
 * That, in turn, results in making the user responsible for freeing the
 * resources from the resource table which is inconvenient, makes no sense in
 * comparison to Lua and leads to memory leaks.
 *
 * With that in mind, the decision is to sacrifice methods in favor of
 * preserving the logic and memory safety.
 *
 * Finally, we have type aliases. These are chosen for types that are
 * represented on the WASM side as opaque references. Unlike in records,
 * there is no generally useful underlying primitive to extract (like
 * `index_id`, for example), so we just wrap this reference into a nicely
 * named type.
"""
from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some


class LogLevel(Enum):
    S_FATAL = 0
    S_SYSERROR = 1
    S_ERROR = 2
    S_CRIT = 3
    S_WARN = 4
    S_INFO = 5
    S_VERBOSE = 6
    S_DEBUG = 7

class IteratorType(Enum):
    ITER_EQ = 0
    ITER_REQ = 1
    ITER_ALL = 2
    ITER_LT = 3
    ITER_LE = 4
    ITER_GE = 5
    ITER_GT = 6
    ITER_BITS_ALL_SET = 7
    ITER_BITS_ANY_SET = 8
    ITER_BITS_ALL_NOT_SET = 9
    ITER_OVERLAPS = 10
    ITER_NEIGHBOR = 11
    ITER_NP = 12
    ITER_PP = 13

class TxnIsolationLevel(Enum):
    TXN_ISOLATION_DEFAULT = 0
    TXN_ISOLATION_READ_COMMITTED = 1
    TXN_ISOLATION_READ_CONFIRMED = 2
    TXN_ISOLATION_BEST_EFFORT = 3
    TXN_ISOLATION_LINEARIZABLE = 4

class IndexType(Enum):
    TREE = 0
    HASH = 1
    BITSET = 2
    RTREE = 3

class KeyPartFlags(Flag):
    IS_NULLABLE = auto()
    EXCLUDE_NULL = auto()


@dataclass
class FieldIdentifier_Number:
    value: int


@dataclass
class FieldIdentifier_Name:
    value: str


FieldIdentifier = Union[FieldIdentifier_Number, FieldIdentifier_Name]


@dataclass
class KeyPartDef:
    field: FieldIdentifier
    field_type: str
    collation: Optional[str]
    path: Optional[str]
    flags: KeyPartFlags

@dataclass
class BoxError:
    message: str
    type: str
    code: int
    payload: Optional[List[Tuple[str, str]]]
    file: Optional[str]
    line: Optional[int]

@dataclass
class Index:
    id: int
    space_id: int
    index_base: int

@dataclass
class Sequence:
    id: int

@dataclass
class Space:
    id: int

@dataclass
class SequenceOptions:
    start: int
    increment: int
    min: int
    max: int
    cycle: bool

@dataclass
class Peer:
    host: str
    port: int

@dataclass
class Session:
    id: int

@dataclass
class SelectOpts:
    iterator: Optional[IteratorType]
    limit: Optional[int]
    offset: Optional[int]
    after: Optional[int]
    fetch_pos: Optional[bool]

@dataclass
class PairsOpts:
    key: Optional[bytes]
    iterator: Optional[IteratorType]
    after: Optional[int]

@dataclass
class UpdateOp:
    field_no: int
    op: str
    operand: bytes

@dataclass
class IndexStat:
    bsize: int
    len: int

class Iterator:
    
    @classmethod
    def new_iterator(cls, index: Index, iterator_type: IteratorType, key: bytes) -> Self:
        """
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def next(self) -> int:
        """
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def __enter__(self) -> Self:
        """Returns self"""
        return self
                                
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        """
        Release this resource.
        """
        raise NotImplementedError


class TupleIterator:
    
    @classmethod
    def new_tuple_iterator(cls, tuple: int) -> Self:
        """
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def position(self) -> int:
        raise NotImplementedError
    def rewind(self) -> None:
        raise NotImplementedError
    def seek(self, pos: int) -> int:
        """
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def next(self) -> int:
        """
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def __enter__(self) -> Self:
        """Returns self"""
        return self
                                
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        """
        Release this resource.
        """
        raise NotImplementedError



