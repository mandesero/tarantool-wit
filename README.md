# Tarantool WIT definitions

This repository contains WIT definition for Tarantool DBMS.

## Interface overview

Each WIT file in the `wit/` directory mirrors a Tarantool module or
structure. The table below shows the correspondence between the WIT
interfaces and Tarantool APIs.

| WIT file | Tarantool interface |
| -------- | ------------------- |
| `box-tuple.wit` | [`box.tuple`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_tuple/) / `box_tuple_t` |
| `error.wit` | [`box.error`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_error/) |
| `index.wit` | [`box.index`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_index/) |
| `key-def.wit` | `box.key_def` C API |
| `metrics.wit`     | Module for metrics (currently provides only `uptime`) |
| `msgpack.wit` | [`msgpack`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/msgpack/) module |
| `sequence.wit` | [`box.sequence`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_sequence/) |
| `session.wit` | [`box.session`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_session/) |
| `say.wit` | [`log`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/log/) module / `say_*` macros |
| `ttbox.wit` | General `box` helpers (`space:insert`, `index:update`, …) |
| `tuple-format.wit` | [`box.tuple.format`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_tuple/#lua-function.box_tuple_format) |
| `txn.wit` | [`box.txn`](https://www.tarantool.io/en/doc/latest/reference/reference_capi/txn/) |
| `types.wit` | Common Tarantool types (`box_error_t`, `box_tuple_t`, …) |

## Architecture Decision Record

Aside from enums, we opted to express every Tarantool type as either
record, resource or type alias. Choice of an expressing entity for each
type might seem arbitrary, but they are all aligned with the following
ideas:

Resource is an entity that lives outside of a WASM component. That means
its whole lifecycle is managed entirely by the embedder. These entities are
explicitly created and destroyed by the embedder on command from a WASM
component. Resource entities, unlike records, can have methods.

We made a decision to use resource semantics only for the iterators. One
might argue that the same semantics should apply to the spaces, indexes and
other types, since they are all handled by Tarantool and not by a WASM
component. That is a valid point, but a key difference between a space and
an iterator in regard to the ownesrhip semantics is that space is
manipulated by a `space_id` and is owned by Tarantool, while an iterator
is owned by an application and is manipulated directly.

Resource semantics also requires every resource to be freed after use,
which makes no sense for spaces or indexes, because we would have to free
a reference. Yet still, it makes perfect sense for iterators.

Final thing for consideration is object notation and methods. That feature
off resources looks very appealing to use for other Tarantool types, but it
has a few downsides to it. Every resource must be stored within a resource
table on the embedder side, and removed from there after free. Some of
our target languages have a notion of destructor and some of them don't.
That, in turn, results in making the user responsible for freeing the
resources from the resource table which is inconvenient, makes no sense in
comparison to Lua and leads to memory leaks.

With that in mind, the decision is to sacrifice methods in favor of
preserving the logic and memory safety.

Opaque host objects that are not WIT resources are represented by
host-issued handles. A handle is an identifier resolved by the host, never a
native address. Consumers must not construct or modify handle values. Hosts
must reject unknown and stale handles rather than interpret them as pointers.

Handles are scoped to the component instance that created them and must not
be reused during that instance's lifetime. Copying a handle value creates an
alias, not a new ownership reference. Unless a function explicitly documents
otherwise, each returned handle owns one reference and must be released with
the public `unref` or `delete` function from the corresponding WIT interface.
These are interface functions, not methods on the handle records. The final
release invalidates every alias. Double release and use of forged, stale, or
cross-instance handles are contract violations and trap. Destroying a
component instance releases all handles that remain live in that instance.
Handle parameters are borrowed for the duration of a call unless the function
explicitly documents ownership transfer or retention.

Values that do not require host-side identity, such as an individual tuple
field, are copied across the component boundary. Native pointers and other
host memory addresses are never part of the public WIT contract.

MessagePack data uses the shared
`tarantool:tarantool/types::msgpack-value` alias. Each value is exactly one
complete MessagePack object with no trailing bytes. Tuple and key inputs are
arrays; update expressions are arrays of operation arrays; tuple fields may
contain any MessagePack value. A missing tuple or field is `none`, while
malformed input and failed operations are `box-error` values.

`tarantool:tarantool/types::error-code` is the raw unsigned numeric code
reported by Tarantool, not a closed enum. Consumers should compare only codes
they understand and retain a fallback for unknown values. The contract does
not define a separate error category: `error-type`, `message`, and optional
source location preserve the metadata supplied by the host without freezing
Tarantool's evolving error set.

## Adding Tarantool WIT Interfaces

### Dependencies

Make sure you have [wkg](https://github.com/bytecodealliance/wasm-pkg-tools) installed:

```bash
cargo install wkg
```

### 1. Manual (local) usage

1. **Clone the `tarantool-wit` repository:**

   ```bash
   git clone https://github.com/mandesero/tarantool-wit.git
   ```

   You should now have a directory named `tarantool-wit/` containing a `wit/` subfolder
   with all the Tarantool WIT files.

2. **Create or edit `wkg.toml` in your own project to point at that local `wit/` folder:**

   ```toml
   [overrides]
   "tarantool:tarantool" = { path = "<path-to>/tarantool-wit/wit" }
   ```

   Replace `<path-to>/tarantool-wit/wit` with the relative (or absolute) path
   where you cloned `tarantool-wit/wit`.

3. **Fetch the interface into your project:**

   ```bash
   wkg wit fetch
   ```

   After this command completes, you’ll see `wit/deps/tarantool/tarantool@<version>.wasm`
   (and any other dependencies) checked out under `wit/deps/`.


### 2. Fetching the published interface from GHCR

1. **Edit your global (or per-project) `wkg` config** so that all `tarantool:tarantool`
requests resolve to GHCR. Run:

   ```bash
   wkg config --edit
   ```

   This will open your `$WKG_CONFIG_FILE` (usually `~/.config/wasm-pkg/config.toml`) in your
   default editor. Add the following section (or merge it with existing settings):

   ```toml
   [package_registry_overrides]
   "tarantool:tarantool" = { registry = "ghcr.io", metadata = { preferredProtocol = "oci", oci = { registry = "ghcr.io", namespacePrefix = "mandesero/" } } }
   ```

2. **Run `wkg wit fetch` in your project:**

   ```bash
   wkg wit fetch
   ```

   Now any `include tarantool:tarantool@<version>` in your `wit/world.wit` will be pulled from
   `ghcr.io/mandesero/tarantool/tarantool:<version>`, and placed under `wit/deps/` automatically.

### Example `wit/world.wit`

In your `wit/world.wit`, just reference the Tarantool sequence or other types as usual. For example:

```wit
package docs:adder@0.1.0;

world my-world {
  include tarantool:tarantool/types@0.1.2;
  // other includes/exports
}
```

With either the **manual override** (step 1) or the **registry override** (step 2), `wkg wit fetch` will
pull in exactly that `tarantool:tarantool@0.1.2` interface.

## Generating bindings
```sh
$ componentize-py --wit-path /path/to/repo --world tarantool bindings /output/dir
$ wit-bindgen c-sharp --runtime native-aot /path/to/repo

$ wit-bindgen
Usage: wit-bindgen <COMMAND>

Commands:
  markdown    This generator outputs a Markdown file describing an interface
  moonbit     Generates bindings for MoonBit guest modules
  rust        Generates bindings for Rust guest modules
  c           Generates bindings for C/CPP guest modules
  teavm-java  Generates bindings for TeaVM-based Java guest modules
  tiny-go     Generates bindings for TinyGo-based Go guest modules
  c-sharp     Generates bindings for C# guest modules
  help        Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version

```

## Useful links
[Introduction to component model.](https://component-model.bytecodealliance.org/introduction.html)
[Resource table docs.](https://docs.rs/wasmtime/latest/wasmtime/component/struct.ResourceTable.html)
