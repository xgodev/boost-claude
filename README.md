# boost-claude

Claude Code plugin distribution for **[github.com/xgodev/boost](https://github.com/xgodev/boost)** —
the modular Go service framework. This repo ships the `golang-boost` plugin: one
skill per boost component (58 total), so Claude loads only what the current task
needs.

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
  plugin.json        # golang-boost manifest + quality-gate dependency
  marketplace.json   # marketplace "xgodev-boost", source "./"
skills/              # 58 skills: boost-* (one per component) + gqlgen-field-resolvers
```

Skill families:

- `boost-start` — boot sequence (`boost.Start()`).
- `boost-wrapper-*` — log, config, cache, publisher.
- `boost-model-errors` — typed error catalog.
- `boost-factory-*` — one per `factory/contrib/` component (Echo, Resty,
  Pub/Sub, Mongo, Cassandra, Redis, Elasticsearch, Kafka, AWS, gRPC, OTel, …).
- `boost-bootstrap-*`, `boost-extra-*`, `boost-fx-*` — bootstrap adapters,
  extra middleware/health/multiserver, fx modules.
- `boost-maintainer` — guide for contributing to boost itself.

## Maintenance

This plugin co-evolves with the boost framework but lives in a separate repo.
See [`CLAUDE.md`](./CLAUDE.md) for the sync rule: whenever a boost component
changes in `xgodev/boost`, the matching `boost-*` skill must be updated here in
a corresponding PR, with a `plugin.json` version bump.

## License

MIT — see [LICENSE](./LICENSE).
