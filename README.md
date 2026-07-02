# boost-claude

Claude Code plugin distribution for **[github.com/xgodev/boost](https://github.com/xgodev/boost)** —
the modular Go service framework. This repo ships the `golang-boost` plugin: a
single `boost` entry skill with a flat, one-hop index into `references/*.md`
(one file per component), plus a standalone `gqlgen-field-resolvers` skill. Only
the entry skill's description loads at session start — every component's detail
loads on demand when Claude reads the matching reference file.

> The plugin documents `boost`, but it is **distributed from here**. The boost
> source code lives in [`xgodev/boost`](https://github.com/xgodev/boost); this
> repo holds only the Claude Code skills + plugin manifests.

## Install

```
/plugin marketplace add xgodev/boost-claude
/plugin install golang-boost@xgodev-boost
```

The marketplace is named `xgodev-boost` and the plugin is `golang-boost` — only
the `marketplace add` URL points here.

### Dependency

`golang-boost` depends on `quality-gate@xgodev-quality-gate` (pre-push
comparative gate). Add its marketplace first, otherwise the install resolves
the dependency as unsatisfied and disables the plugin:

```
/plugin marketplace add xgodev/quality-gate
```

## Migrating from `xgodev/boost`

The plugin used to be distributed from the `xgodev/boost` repository itself.
If you installed it the old way, remove it and re-add from here:

```
/plugin uninstall golang-boost@xgodev-boost
/plugin marketplace remove xgodev-boost
/plugin marketplace add xgodev/boost-claude
/plugin install golang-boost@xgodev-boost
```

## What's inside

```
.claude-plugin/
  plugin.json                # golang-boost manifest + quality-gate dependency
  marketplace.json           # marketplace "xgodev-boost", source "./"
skills/
  boost/
    SKILL.md                 # entry skill: flat index, one hop to every reference
    references/
      start.md, model-errors.md, CONTRIBUTING.md
      wrapper/{cache,config,log,log-backends,publisher}.md
      bootstrap/{function,middleware,adapter-kafka,adapter-nats,adapter-pubsub}.md
      extra/{health,middleware,multiserver}.md
      fx/{modules,pluggable-datastore}.md
      factory/{ants,aws,...,zerolog}.md   # one per factory/contrib/ component
  gqlgen-field-resolvers/    # standalone, unrelated to boost
```

Reference groups (each row in `skills/boost/SKILL.md`'s index links directly to
one of these — no intermediate category index files):

- `references/start.md` — boot sequence (`boost.Start()`).
- `references/wrapper/*` — log, config, cache, publisher.
- `references/model-errors.md` — typed error catalog.
- `references/factory/*` — one per `factory/contrib/` component (Echo, Resty,
  Pub/Sub, Mongo, Cassandra, Redis, Elasticsearch, Kafka, AWS, gRPC, OTel, …).
- `references/bootstrap/*`, `references/extra/*`, `references/fx/*` —
  bootstrap adapters, extra middleware/health/multiserver, fx modules.
- `references/CONTRIBUTING.md` — guide for contributing to boost itself.

Run `python3 scripts/verify_references.py` after editing any reference file —
it confirms every `references/....md` pointer in `skills/boost/` still
resolves.

## Maintenance

This plugin co-evolves with the boost framework but lives in a separate repo.
See [`CLAUDE.md`](./CLAUDE.md) for the sync rule: whenever a boost component
changes in `xgodev/boost`, the matching `boost-*` skill must be updated here in
a corresponding PR, with a `plugin.json` version bump.

## License

MIT — see [LICENSE](./LICENSE).
