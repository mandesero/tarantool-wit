from typing import TypeVar, Generic, Union, Optional, Protocol, Tuple, List, Any, Self
from types import TracebackType
from enum import Flag, Enum, auto
from dataclasses import dataclass
from abc import abstractmethod
import weakref

from ..types import Result, Ok, Err, Some


class BoxTuple:
    
    def __init__(self, data: bytes) -> None:
        """
        Create new tuple.
        * data must represent a valid messagepack array
        * using unsafe tarantool::tuple::Tuple::from_slice(data: &[u8]) -> Tuple
        """
        raise NotImplementedError

    def to_vec(self) -> bytes:
        """
        tarantool::tuple::Tuple::to_vec(&self) -> Vec<u8>
        Get tuple contents as a vector of raw bytes.
        Returns tuple bytes in msgpack encoding.
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


class Index:
    
    def __init__(self, space_id: int, index_id: int) -> None:
        """
        unsafe tarantool::index::Index::from_ids_unchecked(space_id: SpaceId, index_id: IndexId) -> Index
        * IDs must be valid tarantool space/index id.
        * Only use this function with ids acquired from tarantool in some way, e.g. from lua code.
        """
        raise NotImplementedError

    def id(self) -> int:
        """
        tarantool::index::Index::id(&self) -> u32
        Return id of this index.
        """
        raise NotImplementedError
    def space_id(self) -> int:
        """
        tarantool::index::Index::id(&self) -> u32
        Return the space id of this index.
        """
        raise NotImplementedError
    def delete(self, key: bytes) -> BoxTuple:
        """
        tarantool::index::Index::delete<K>(&self, key: &K) -> Result<Option<Tuple>, Error>
        Delete a tuple identified by a key.
        * `key` must represent a valid messagepack array
        * using unsafe tarantool::tuple::Tuple::from_slice(data: &[u8]) -> Tuple
        * to convert key: msgpack-data (=list<u8>) to key: &K
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def update(self, key: bytes, ops: bytes) -> BoxTuple:
        """
        unsafe tarantool::index::Index::update_raw(&self, key: &[u8], ops: &[u8]) -> Result<Option<Tuple>, Error>
        Update a tuple.
        * `key` must represent a valid messagepack array
        * `ops` must be a slice of valid msgpack arrays.
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def upsert(self, value: bytes, ops: bytes) -> BoxTuple:
        """
        unsafe tarantool::index::Index::upsert_raw(&self, value: &[u8], ops: &[u8]) -> Result<(), Error>
        Execute an UPSERT request. Will try to insert tuple. Update if already exists.
        * `value` must represent a valid messagepack array
        * `ops` must be a valid msgpack array of msgpack arrays.
        
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


class Space:
    
    def __init__(self, id: int) -> None:
        """
        unsafe fn tarantool::space::Space::from_id_unchecked(id: SpaceId) -> Space
        * ID must be a valid tarantool space id.
        * Only use this function with ids acquired from tarantool in some way, e.g. from lua code.
        """
        raise NotImplementedError

    @classmethod
    def find(cls, name: str) -> Self:
        """
        tarantool::space::Space::find(name: &str) -> Option<Space>
        Find space by name.
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def id(self) -> int:
        """
        tarantool::space::Space::id(&self) -> SpaceId
        Get space ID.
        """
        raise NotImplementedError
    def index(self, name: str) -> Index:
        """
        tarantool::space::Space::index(&self, name: &str) -> Option<Index>
        Find index by name.
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def insert(self, value: bytes) -> BoxTuple:
        """
        tarantool::space::Space::insert<T>(&self, value: &T) -> Result<Tuple, Error>
        Insert a value into a space. Returns a new tuple.
        * `data` must represent a valid messagepack array
        * using unsafe tarantool::tuple::Tuple::from_slice(data: &[u8]) -> Tuple
        * to convert value: msgpack-data (=list<u8>) to value: &K
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def replace(self, value: bytes) -> BoxTuple:
        """
        tarantool::space::Space::replace<T>(&self, value: &T) -> Result<Tuple, Error>
        Insert a value into a space. If a tuple with the same primary key already exists, it is replaced with a new one.
        Returns a new tuple.
        * `data` must represent a valid messagepack array
        * using unsafe tarantool::tuple::Tuple::from_slice(data: &[u8]) -> Tuple
        * to convert value: msgpack-data (=list<u8>) to value: &K
        
        Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
        """
        raise NotImplementedError
    def truncate(self) -> None:
        """
        tarantool::space::Space::truncate(&self) -> Result<(), Error>
        Deletes all tuples.
        
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



def schema_version() -> int:
    """
    C API: uint64_t box_schema_version(void)
    Get the database schema version.
    """
    raise NotImplementedError

def space_id_by_name(name: str) -> int:
    """
    tarantool::space::Space::find(name: &str) -> Option<Space>
    Get space ID.
    
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

def index_id_by_name(space_id: int, name: str) -> int:
    """
    unsafe tarantool::index::Index::from_ids_unchecked(space_id: SpaceId, index_id: IndexId) -> Index
    * IDs must be valid tarantool space/index id.
    * Only use this function with ids acquired from tarantool in some way, e.g. from lua code.
    
    Raises: `tarantool.types.Err(tarantool.imports.types.BoxError)`
    """
    raise NotImplementedError

