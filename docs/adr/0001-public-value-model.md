# ADR 0001: Public value and ownership model

Status: accepted for `tarantool:tarantool@0.2.0`.

## Context

A WIT contract crosses a trust and address-space boundary. Guest components
cannot safely dereference Tarantool pointers, and a numeric value that happens
to contain a host address has no portable meaning in the Component Model.
Public types also need explicit rules for ownership, absence, and copied data
so that hosts and language bindings implement the same behavior.

The contract represents four different kinds of data: catalog identifiers,
copied values, opaque host objects, and guest-owned traversal state. Treating
all four as integers or byte arrays loses the distinctions required for safe
lifetime management.

## Decision

### Catalog and context identifiers are records

Objects that Tarantool addresses by stable numeric IDs use small records.
`space` contains a space ID, `index` contains its space and index IDs,
`sequence` contains a sequence ID, and `session` contains a session ID. These
records are values: copying one does not allocate host state or transfer
ownership.

A guest may obtain these records from lookup functions or construct them from
IDs supplied by application configuration. The host validates that an ID
exists when an operation uses it. An unknown ID produces `box-error`; it is not
a forged memory reference.

### MessagePack and tuple fields are copied values

`msgpack-value` is exactly one complete MessagePack object encoded as
`list<u8>`. The byte sequence contains no trailing object. Functions may
further require a specific top-level shape: tuples, keys, and update
expressions are arrays, while IPROTO headers and bodies are maps.

Bytes returned by the host are copied into guest-owned memory. `tuple-field`
is an alias of `msgpack-value`, so a field remains valid independently of the
tuple from which it was read. No pointer into Tarantool tuple memory crosses
the component boundary.

### Opaque host objects use instance-scoped handles

`box-tuple`, `key-def`, and `tuple-format` are records containing opaque
host-issued handles. A handle is an identifier resolved through host-managed
state; it is never a native pointer. The host rejects unknown, stale, forged,
or cross-instance handles.

Returned handles own one reference unless the function documentation states
otherwise. Passing a handle to a function borrows it for that call. Copying
the record creates an alias, not another ownership reference. `retain`
acquires an additional reference where supported, and `release` consumes one
owned reference. The final release invalidates every remaining alias, so using
or releasing such an alias traps as a contract violation.

The host does not reuse handle values during a component instance's lifetime.
Destroying the instance releases all handles still registered to it. These
rules prevent one guest from guessing or reusing another guest's host state.

### Iterators are WIT resources

Index and tuple iterators are guest-owned state with a bounded lifetime. They
use WIT resources so generated bindings can tie cleanup to resource disposal.
Dropping an index iterator releases its native iterator state. A tuple
iterator retains the tuple it traverses and releases that reference when the
resource is dropped.

Spaces, indexes, sequences, and sessions are not resources because the guest
does not own the underlying Tarantool object. Turning their IDs into resources
would add host table entries and destructors without representing real guest
ownership.

### Absence and failure are distinct

`option<T>` represents a normal missing value, including an unsuccessful
lookup, an absent tuple or field, and iterator exhaustion. `result<T,
box-error>` represents validation or operation failure. Functions combine the
two as `result<option<T>, box-error>` when both outcomes are possible.

Validation functions return `ok(())` for valid input and `err(box-error)` for
invalid input. They do not return booleans because validation failures retain
Tarantool's diagnostic code and message.

### Error codes remain open

`error-code` is the raw `u32` reported by Tarantool. It is not a WIT enum,
because WIT enums are closed while Tarantool can add error codes. Consumers
compare codes they recognize and preserve unknown values. `box-error` also
copies the message, error type, and optional source location supplied by the
host.

## Consequences

Host implementations need an instance-local handle registry and deterministic
cleanup. Guest libraries need to release owned handles and must not synthesize
handle values. Copied MessagePack values cost an allocation and copy, but they
remain portable and valid after the originating host object is released.

The contract does not prescribe the host's internal table, pointer, or
reference-count implementation. It specifies only observable validity,
ownership, and cleanup behavior.

## Rejected alternatives

Native addresses encoded as `u64` were rejected because they expose host
memory and are meaningless outside the producing process. Making every
Tarantool object a WIT resource was rejected because catalog objects are owned
by Tarantool rather than the guest. Copying complete tuples for every operation
was rejected because tuple identity and reference-counted operations are part
of the API; individual fields remain copied values.
