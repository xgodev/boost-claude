# boost-claude

Claude Code plugin distribution for **[github.com/xgodev/boost](https://github.com/xgodev/boost)** —
the modular Go service framework. This repo ships the `golang-boost` plugin: a
single `boost` entry skill whose small top-level index expands, group by group,
into `references/*.md` (down to a domain file for `factory/*`, since it alone
covers 39 components). Only the entry skill's tiny index loads on every trigger —
every deeper file loads on demand only when the question actually needs it.

> The plugin documents `boost`, but it is **distributed from here**. The boost
> source code lives in [`xgodev/boost`](https://github.com/xgodev/boost); this
> repo holds only the Claude Code skills + plugin manifests.

## Install

`golang-boost` is distributed through the single `xgodev-plugins` marketplace,
hosted in [`xgodev/claude-plugin`](https://github.com/xgodev/claude-plugin) —
this repo is the plugin source the marketplace points at:

```
/plugin marketplace add xgodev/claude-plugin
/plugin install golang-boost@xgodev-plugins
```

### Dependency

`golang-boost` depends on `quality-gate` (pre-push comparative gate). It lives
in the same `xgodev-plugins` marketplace, so the install resolves it
automatically — no extra step.

## Migrating from the `xgodev-boost` marketplace

Until plugin 0.15.0 this repo was its own marketplace (`xgodev-boost`), and
before that the plugin shipped from `xgodev/boost` itself. Both are retired in
favor of the single `xgodev-plugins` marketplace. If you installed either old
way, remove and re-add:

```
/plugin uninstall golang-boost@xgodev-boost
/plugin marketplace remove xgodev-boost
/plugin marketplace remove xgodev-quality-gate
/plugin marketplace add xgodev/claude-plugin
/plugin install golang-boost@xgodev-plugins
```

(Skip any `marketplace remove` for a marketplace you never added.)

## What's inside

```
.claude-plugin/
  plugin.json                # golang-boost manifest + quality-gate dependency
skills/
  boost/
    SKILL.md                 # entry skill: 8 top-level contexts, ~25 lines
    references/
      start.md, model-errors.md, CONTRIBUTING.md   # inline in the index, no hop
      wrapper.md      -> wrapper/{cache,config,log,log-backends,publisher}.md
      bootstrap.md     -> bootstrap/{function,middleware,adapter-kafka,adapter-nats,adapter-pubsub}.md
      extra.md         -> extra/{health,middleware,multiserver}.md
      fx.md            -> fx/{modules,pluggable-datastore}.md
      factory.md       -> factory/{database,messaging,http,observability,infra}.md
                            -> factory/{ants,aws,...,zerolog}.md   # 39 leaves
```

Navigation depth matches group size: root essentials sit inline in `SKILL.md`
(no hop), the four small groups (wrapper/bootstrap/extra/fx) are one hop away,
and `factory/*` — which alone accounts for 39 of the 58 leaf files — is grouped
by domain first, so a factory question is two hops (context → domain → leaf)
instead of loading a 39-row table every time any factory topic comes up.

- `references/start.md` — boot sequence (`boost.Start()`).
- `references/model-errors.md` — typed error catalog.
- `references/CONTRIBUTING.md` — guide for contributing to boost itself.
- `references/wrapper.md` — log, config, cache, publisher.
- `references/bootstrap.md` — function bootstrap, middleware, Kafka/NATS/Pub-Sub adapters.
- `references/extra.md` — health, extra middleware, multiserver.
- `references/fx.md` — fx modules, pluggable datastore.
- `references/factory.md` — database, messaging, HTTP/RPC, observability, cloud/infra domains, each expanding into its own leaves (Echo, Resty, Mongo, Cassandra, Redis, Kafka, AWS, gRPC, OTel, …).

Run `python3 scripts/verify_references.py` after editing any reference file —
it confirms every `references/....md` pointer in `skills/boost/` still
resolves.

## Maintenance

This plugin co-evolves with the boost framework but lives in a separate repo.
See [`CLAUDE.md`](./CLAUDE.md) for the sync rule: whenever a boost component
changes in `xgodev/boost`, the matching reference file (under `skills/boost/references/`)
must be updated here in a corresponding PR, with a `plugin.json` version bump.

## License

MIT — see [LICENSE](./LICENSE).
