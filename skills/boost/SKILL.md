---
name: boost
description: "Use for any work with github.com/xgodev/boost or its subpackages — the modular Go microservice framework. Covers the boost.Start() boot sequence, wrapper/* (log, config, cache, publisher), bootstrap/* (function, middleware, Pub/Sub, NATS, Kafka adapters), extra/* (health, middleware, multiserver), fx/* modules, model/errors, and every factory/contrib/* integration (Echo, Resty, Pub/Sub, Mongo, Cassandra, Redis, Elasticsearch, Kafka, AWS, gRPC, gocloud.dev, Postgres/pgx, Oracle/godror, BigQuery, Firestore, BuntDB, MemDB, BigCache, FreeCache, Vault, Hystrix, Ants, NATS, Goka, CloudEvents, GCP API/gRPC composition, OTel, Datadog, Prometheus, fx, Cobra, GraphQL, K8s, FTP, HTTP/2, Zap/Zerolog/Logrus). Triggers on any import under github.com/xgodev/boost, on questions about boost initialization, wiring, or any component listed above, on writing or reviewing Go service code that uses boost, and on contributing a new component to the boost repo itself."
license: MIT
metadata:
  author: jpfaria
  version: "1.0.0"
allowed-tools: Read Edit Write Glob Grep Bash(go:*) Bash(golangci-lint:*) Bash(git:*) Agent
---

This skill indexes `github.com/xgodev/boost`. **This file is only the index — read the matching reference file(s) below before answering.** All paths are relative to this skill's directory (`skills/boost/`).

Each reference file may itself point to a `REQUIRED BACKGROUND` reference — follow that pointer too before answering. There are no intermediate category index files: every row below is one `Read` away from the actual content.

## Start here

| Topic | Reference |
|---|---|
| `boost.Start()` boot sequence | `references/start.md` |
| Typed error catalog (`model/errors`) | `references/model-errors.md` |
| Contributing a new component to `xgodev/boost` | `references/CONTRIBUTING.md` |

## Wrapper (`wrapper/*`)

| Topic | Reference |
|---|---|
| Cache wrapper | `references/wrapper/cache.md` |
| Config wrapper | `references/wrapper/config.md` |
| Log wrapper | `references/wrapper/log.md` |
| Log backends | `references/wrapper/log-backends.md` |
| Publisher wrapper | `references/wrapper/publisher.md` |

## Bootstrap (`bootstrap/*`)

| Topic | Reference |
|---|---|
| Function bootstrap (`function.New`, `Handler[T]`) | `references/bootstrap/function.md` |
| Middleware chain | `references/bootstrap/middleware.md` |
| Kafka adapter | `references/bootstrap/adapter-kafka.md` |
| NATS adapter | `references/bootstrap/adapter-nats.md` |
| Pub/Sub adapter | `references/bootstrap/adapter-pubsub.md` |

## Extra (`extra/*`)

| Topic | Reference |
|---|---|
| Health checks | `references/extra/health.md` |
| Extra middleware | `references/extra/middleware.md` |
| Multiserver | `references/extra/multiserver.md` |

## fx (`fx/*`)

| Topic | Reference |
|---|---|
| fx modules | `references/fx/modules.md` |
| Pluggable datastore | `references/fx/pluggable-datastore.md` |

## Factory (`factory/contrib/*`)

| Component | Reference |
|---|---|
| Ants (goroutine pool) | `references/factory/ants.md` |
| AWS | `references/factory/aws.md` |
| BigCache | `references/factory/bigcache.md` |
| BigQuery | `references/factory/bigquery.md` |
| BuntDB | `references/factory/buntdb.md` |
| Cassandra | `references/factory/cassandra.md` |
| CloudEvents | `references/factory/cloudevents.md` |
| Cobra | `references/factory/cobra.md` |
| Datadog | `references/factory/datadog.md` |
| Echo | `references/factory/echo.md` |
| Elasticsearch | `references/factory/elasticsearch.md` |
| Firestore | `references/factory/firestore.md` |
| FreeCache | `references/factory/freecache.md` |
| FTP | `references/factory/ftp.md` |
| fx (factory-level) | `references/factory/fx.md` |
| GCP API composition | `references/factory/gcp-api.md` |
| GCP gRPC composition | `references/factory/gcp-grpc.md` |
| gocloud.dev Pub/Sub | `references/factory/gocloud-pubsub.md` |
| Oracle (godror) | `references/factory/godror.md` |
| Goka | `references/factory/goka.md` |
| GraphQL | `references/factory/graphql.md` |
| gRPC | `references/factory/grpc.md` |
| Hystrix | `references/factory/hystrix.md` |
| K8s | `references/factory/k8s.md` |
| Kafka | `references/factory/kafka.md` |
| Logrus | `references/factory/logrus.md` |
| MemDB | `references/factory/memdb.md` |
| Mongo | `references/factory/mongo.md` |
| NATS | `references/factory/nats.md` |
| net/http2 | `references/factory/net-http2.md` |
| OTel | `references/factory/otel.md` |
| Postgres (pgx) | `references/factory/pgx.md` |
| Prometheus | `references/factory/prometheus.md` |
| Pub/Sub | `references/factory/pubsub.md` |
| Redis | `references/factory/redis.md` |
| Resty | `references/factory/resty.md` |
| Vault | `references/factory/vault.md` |
| Zap | `references/factory/zap.md` |
| Zerolog | `references/factory/zerolog.md` |

## Out of scope

`gqlgen-field-resolvers` is a separate skill in this plugin, not merged here — it documents `99designs/gqlgen`, not `xgodev/boost`.
