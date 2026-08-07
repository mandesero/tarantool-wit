# Tarantool WIT definitions

This repository publishes the Component Model contract for guest components
that call Tarantool APIs. The current package is
`tarantool:tarantool@0.2.0`.

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
| `log.wit` | [`log`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/log/) module / `say_*` C API |
| `database.wit` | General `box` operations (`insert`, `update`, …) |
| `tuple-format.wit` | [`box.tuple.format`](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_tuple/#lua-function.box_tuple_format) |
| `transaction.wit` | [`box.txn`](https://www.tarantool.io/en/doc/latest/reference/reference_capi/txn/) |
| `types.wit` | Common Tarantool types (`box_error_t`, `box_tuple_t`, …) |

## Package and world structure

The public package is `tarantool:tarantool@0.2.0`. Its `guest` world is a
convenience aggregate containing all general-purpose host interfaces. Each
interface remains independently importable, so components should import only
the interfaces they need when they do not require the complete API.

The package identity and interface purposes are stable within the `0.2.x`
line. Breaking changes to interface signatures or aggregate-world membership
require a new minor version while the package is below `1.0.0`. Patch releases
are reserved for compatible fixes. Consumer-specific exports and runtime
implementation details are not part of the aggregate world.

Version `0.2.0` is a new compatibility baseline: all public WIT declarations
use `@since(version = 0.2.0)`, and no source compatibility with `0.1.x` is
implied.

## Documentation

Starting with `0.2.0`, the
[versioned generated API reference](https://mandesero.github.io/tarantool-wit/)
is published with every stable release. Prerelease tags do not update Pages or
the `latest` alias. The [API guide](docs/api.md) describes
MessagePack shapes, return semantics,
ownership, and a short example for every interface. The
[public value model ADR](docs/adr/0001-public-value-model.md) defines the trust
boundary and explains the choice between ID records, copied values, opaque
handles, and WIT resources. Existing consumers should follow the
[0.2.0 migration guide](docs/migration-0.2.md).

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

   References to `tarantool:tarantool` in your `wit/world.wit` will be pulled
   from `ghcr.io/mandesero/tarantool/tarantool:<version>` and placed under
   `wit/deps/` automatically.

### Example `wit/world.wit`

Include the aggregate world when the component needs the complete API:

```wit
package docs:adder@0.1.0;

world my-world {
  include tarantool:tarantool/guest@0.2.0;
}
```

Import individual interfaces instead when a smaller contract is preferable:

```wit
package docs:sequence-user@0.1.0;

world my-world {
  import tarantool:tarantool/sequence@0.2.0;
}
```

With either the **manual override** (step 1) or the **registry override**
(step 2), `wkg wit fetch` pulls in the referenced
`tarantool:tarantool@0.2.0` package.

## Generating bindings

Select the `guest` world when a generator requires an explicit world name.
For example:

```sh
componentize-py --wit-path /path/to/repo --world guest bindings /output/dir
wit-bindgen rust --world guest /path/to/repo/wit
wit-bindgen c-sharp --runtime native-aot --world guest /path/to/repo/wit
```

## Validating changes

CI builds and validates the encoded WIT package, generates Markdown API
documentation and Rust bindings, and uploads them with a semantic contract diff
against the latest `v*` release. Run the core checks locally with:

```sh
wkg wit build -d wit -o /tmp/tarantool-tarantool.wasm
wasm-tools validate /tmp/tarantool-tarantool.wasm
wit-bindgen markdown --world guest --out-dir /tmp/tarantool-wit-docs wit
wit-bindgen rust --world guest --out-dir /tmp/tarantool-wit-rust wit
scripts/report-contract-changes.sh /tmp/tarantool-wit-contract-changes.md
```

Release tags must use `v<version>` and exactly match the package version in all
WIT files. The publish workflow runs the complete contract validation workflow
and verifies the tag ref and version before uploading an artifact. After the
stable OCI package is published and signed, the workflow deploys generated
HTML and Markdown documentation to versioned GitHub Pages paths and updates
`latest`.

## Useful links

- [Introduction to the Component Model](https://component-model.bytecodealliance.org/introduction.html)
- [WIT worlds](https://component-model.bytecodealliance.org/design/worlds.html)
- [Wasmtime resource tables](https://docs.rs/wasmtime/latest/wasmtime/component/struct.ResourceTable.html)
