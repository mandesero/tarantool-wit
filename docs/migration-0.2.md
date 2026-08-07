# Migrating from 0.1.x to 0.2.0

Version `0.2.0` is a new compatibility baseline. Regenerate bindings and update
both host implementations and guest components; changing only the dependency
version is not sufficient.

## Package and world

The package remains `tarantool:tarantool` and the aggregate world is now
`guest`:

```wit
world my-component {
  include tarantool:tarantool/guest@0.2.0;
}
```

Components may continue to import individual interfaces instead of including
the aggregate world.

## Interface names

The general `ttbox` interface is now `database`. The `say` interface is now
`log`, and `txn` is now `transaction`. The logging interface exposes one
`write` function; level-specific helpers belong in guest libraries. Fatal and
errno-dependent logging operations are not part of the 0.2.0 contract, and
`log-context.filename` is now `log-context.file`.

## Function and resource names

Tuple and tuple-format reference operations use `retain` and `release`.
Key-definition destruction uses `release`. Tuple serialization is
`box-tuple.to-bytes`, tuple size is `box-tuple.byte-size`, index size is
`index.memory-size`, and index cardinality is `index.tuple-count`.
`key-def.dup` is now `key-def.duplicate`.

MessagePack conversion functions are now `msgpack.from-json` and
`msgpack.to-json` instead of `encode` and `decode`. JSON crosses the component
boundary as a WIT `string`; MessagePack crosses it as `msgpack-value`.

`box-tuple.compare-with-key` now returns `result<s32, box-error>` so comparison
failures are preserved. `session.iproto-send` now accepts
`option<msgpack-value>` for the body; pass `none` to omit it.

Both index and tuple iterator resources are named `iterator` within their own
interfaces. Their static constructor is `new`. Generated bindings distinguish
them by the fully qualified interface path.

Transaction functions no longer repeat the interface name: use `id`,
`isolation`, `set-isolation`, and `make-synchronous`. `id` and `isolation`
return `none` when there is no active transaction. The redundant `txn`
boolean function was removed; test whether `id` is `some` instead.

## Types and enum cases

Space, index, and sequence IDs are `u32`; session and transaction IDs are
`u64`. Schema versions are `u32`, and nonnegative sizes and counts use unsigned
types. The unused `index.index-base` field was removed, and tuple JSON-path
lookups always use zero-based array indexes. `field-by-path` no longer accepts
an index-base argument.

Enum cases no longer repeat their type prefixes. Examples include
`log-level.info`, `iterator-type.equal`, and
`transaction-isolation.read-committed`. Hosts must map the cases explicitly to
the corresponding Tarantool constants rather than relying on generated Rust
variant names.

## MessagePack, fields, and absence

Every `msgpack-value` contains one complete object with no trailing bytes.
Tuple and key arguments are MessagePack arrays; update expressions are arrays
of operation arrays; IPROTO headers and bodies are maps. Tuple fields are
copied MessagePack bytes rather than native addresses. The unsafe
`decode-from-raw-ptr` operation was removed.

Lookups and iteration use `option<T>` for normal absence. APIs that can also
fail use `result<option<T>, box-error>`. Update guest code that previously
treated a missing tuple, field, or end-of-iteration as an error. Validation
functions now return `ok(())` or `err(box-error)` instead of discarding
diagnostics in a boolean.

## Handles and ownership

`box-tuple`, `key-def`, and `tuple-format` contain opaque `handle` values
instead of native pointers. Guests must obtain handles from the host, must not
construct them, and must release every owned reference. Handle values are
scoped to one component instance and become invalid after their final release.
`box-tuple.retain` no longer exposes the native reference-count return value.

## Errors

`error-code` is now an open `u32` value rather than a closed enum. Preserve
unknown codes and use the copied `error-type`, `message`, `file`, and `line`
fields for diagnostics. Code that exhaustively matches the old enum needs a
fallback branch.

## Migration checklist

Regenerate language bindings, update canonical interface names, replace renamed
functions and enum cases, adapt signed IDs and sentinel values, map normal
absence to options, implement the handle registry and release operations, and
rerun component contract tests against the `guest@0.2.0` world.
