# API guide

The examples use WIT names and compact pseudocode. `mp(value)` means one
complete MessagePack encoding of `value`, `?` unwraps a successful `result`,
and `defer` schedules cleanup. Language generators adapt kebab-case names to
their native naming convention.

## `types`

The `types` interface defines shared values. Catalog identifiers are plain
records and may be copied. Opaque handles must come from host functions.

```text
primary = index { space-id: 512, id: 0 }
configured_sequence = sequence { id: 1 }

# Invalid: handle values are host-issued, not guest-generated.
tuple = box-tuple { handle: 42 }
```

`msgpack-value` and `tuple-field` own their bytes in guest memory. A function
that requires an array or map rejects a valid MessagePack scalar of the wrong
shape.

## `database`

The database interface resolves spaces and indexes and performs tuple-changing
operations. Lookups return `none` when the named object does not exist.

```text
space = database.space-by-name("users")?
if space is none:
    return "users space is not configured"
space = space.value

primary = database.index-by-name(space, "primary")?
if primary is none:
    return "primary index is not configured"
primary = primary.value

tuple = database.insert(space, mp([1, "Alice"]))?
defer box-tuple.release(tuple)

updated = database.update(primary, mp([1]), mp([["=", 1, "Alicia"]]))?
if updated is some:
    defer box-tuple.release(updated.value)
```

`insert` and `replace` always return an owned tuple handle on success.
`update` and `delete` return `none` when no tuple matches. `upsert` and
`truncate` return `ok(())` and no tuple value.

## `index`

Index reads use MessagePack arrays as keys. An empty array selects the
unbounded prefix accepted by operations such as `min`, `max`, and scans.

```text
tuple = index.get(primary, mp([1]))?
if tuple is some:
    defer box-tuple.release(tuple.value)

scan = index.iterator.new(primary, iterator-type.greater-than-or-equal, mp([1]))?
while item = scan.next()?:
    consume(box-tuple.to-bytes(item)?)
    box-tuple.release(item)
drop(scan)
```

Iterator exhaustion is `ok(none)`. Malformed keys and Tarantool failures are
`err(box-error)`. Dropping the iterator releases its host traversal state.

## `box-tuple`

Tuple construction, updates, and upserts return owned handles. Copied fields
and serialized tuple bytes remain valid after the handle is released.

```text
tuple = box-tuple.new(mp([1, {"name": "Alice"}]))?
field = box-tuple.field-by-path(tuple, "[1].name")?
bytes = box-tuple.to-bytes(tuple)?
box-tuple.release(tuple)

if field is some:
    print(msgpack.to-json(field.value)?)
persist(bytes)
```

Path array indexes are zero-based. `retain` is required before treating an
alias as another owned reference. Releasing the final reference invalidates
all aliases.

The tuple iterator retains its source tuple until the resource is dropped:

```text
tuple = box-tuple.new(mp([10, 20, 30]))?
fields = box-tuple.iterator.new(tuple)?
box-tuple.release(tuple)

while field = fields.next()?:
    consume(field)
drop(fields)
```

## `key-def`

A key definition describes tuple fields used for validation, extraction, and
comparison. Each handle returned by `new`, `duplicate`, or `merge` is owned.

```text
parts = [key-part {
    field-no: 0,
    field-type: field-type.unsigned,
    collation: none,
    path: none,
    flags: {},
}]

definition = key-def.new(parts)?
defer key-def.release(definition)
tuple = box-tuple.new(mp([1, "Alice"]))?
defer box-tuple.release(tuple)
key-def.validate-full-key(definition, mp([1]))?
key = key-def.extract-key(definition, tuple)?
```

`validate-key` accepts a prefix; `validate-full-key` requires exactly one
value per key part. Validation failure is `err(box-error)`, not `ok(false)`.

## `tuple-format`

Tuple formats own references independently of the key definitions used to
create them.

```text
parts = [key-part {
    field-no: 0,
    field-type: field-type.unsigned,
    collation: none,
    path: none,
    flags: {},
}]

definition = key-def.new(parts)?
defer key-def.release(definition)
format = tuple-format.new([definition])?
defer tuple-format.release(format)

tuple = box-tuple.new(mp([1, "Alice"]))?
defer box-tuple.release(tuple)
box-tuple.validate(tuple, format)?
```

`default` also returns an owned handle. Use `retain` only when creating an
additional owned reference to the same format.

## `msgpack`

The conversion interface is intended for JSON-compatible values. It does not
provide a general MessagePack codec because MessagePack extensions, binary
values, and non-string map keys have no lossless JSON representation.

```text
encoded = msgpack.from-json("{\"id\":1,\"active\":true}")?
json = msgpack.to-json(encoded)?
```

The returned JSON text is not canonical. Do not compare it byte-for-byte for
semantic equality.

## `error`

Errors are copied records. The numeric code is open-ended and must not be
exhaustively matched without a fallback.

```text
err = error.new-with-location(1234, "invalid request", some("guest.wasm"), some(17))
error.set(err)

if current = error.last():
    log.write(log-level.error, error.to-string(current), none)
error.clear()
```

The last-error slot belongs to the current host execution context. Clearing it
does not mutate copies already held by the guest.

## `transaction`

Transaction state is associated with the current Tarantool execution context.
Callers must finish every successful `begin` with `commit` or `rollback`.

```text
transaction.begin()?
result = database.upsert(primary, mp([1, 0, 1]), mp([["+", 2, 1]]))

if result is err:
    transaction.rollback()?
    return result.error

transaction.make-synchronous()
transaction.commit()?
```

`id` and `isolation` return `none` outside a transaction. Calling
`make-synchronous` makes commit wait for configured synchronous-replication
acknowledgements; it does not mean an unconditional local disk flush.

## `sequence`

The WIT API operates on an existing sequence ID; sequence creation remains a
Tarantool schema operation.

```text
orders = sequence { id: 1 }
next_id = sequence.next(orders)?
current_id = sequence.current(orders)?
assert(next_id == current_id)
```

`current` fails until the sequence has been advanced or set. `reset` restores
the initial state, after which `current` fails again until another value is
assigned.

## `session`

Session IDs identify Tarantool client or execution contexts. IPROTO packets
require MessagePack maps for both header and body.

```text
caller = session.current()
session.iproto-send(caller, mp({0x00: 0x80}), some(mp({0x30: []})))?
session.broadcast("cache.invalidate", "{space_id = 512}")?
```

The broadcast value is a Lua expression string, not JSON. Invalid expressions
return `box-error`. Callers must treat the value as code and must not
interpolate untrusted text into the expression.

## `log`

Logging exposes only levels that return to the guest. Fatal and
errno-dependent helpers are deliberately absent.

```text
context = log-context { file: "rules.py", line: 42 }
log.write(log-level.info, "rule evaluation started", some(context))
```

Guest libraries may provide formatting and level-specific wrappers without
expanding the host contract.

## `metrics`

The metrics interface currently exposes Tarantool instance uptime:

```text
started_seconds_ago = metrics.uptime()
```

The floating-point value may include fractional seconds.
