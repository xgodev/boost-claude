**REQUIRED BACKGROUND:**
- `references/start.md` — `boost.Start()` first.
- `references/factory/echo.md` — endpoints typically attach to the Echo server.

## Liveness vs readiness — keep them separate

| Endpoint | Answers | Fails when |
|---|---|---|
| `/livez` (or `/health`) | "Is the process alive?" | Process should be killed and restarted |
| `/readyz` | "Should I receive traffic right now?" | A downstream is unhealthy; don't pull this pod from rotation, just stop sending requests |

Cascading failure mode to avoid: a transient downstream blip flips `/health` to 500, Kubernetes kills the pod, the new pod hits the same downstream, gets killed, replicas churn → total outage from a recoverable hiccup. Liveness probes must NOT depend on downstream state.

## Wiring

```go
import (
    "github.com/xgodev/boost/extra/health"
)

// Liveness: cheap, deterministic, no downstream calls.
srv.GET("/livez", func(c echo.Context) error {
    return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
})

// Readiness: checks every registered downstream checker.
checkers := []health.Checker{
    health.NewDBChecker(db),
    health.NewPubSubChecker(pb),
    health.NewRedisChecker(redisClient),
}
srv.GET("/readyz", health.AggregateHandler(checkers...))
```

Each checker implements:

```go
type Checker interface {
    Name() string
    Check(ctx context.Context) error
}
```

A nil error from every checker → 200; any error → 503 with the failing checker's name in the response.

## Implementation tips

- **Bound the timeout** on each checker (`context.WithTimeout`) so a hung downstream doesn't hang the readiness response.
- **Cache the result** for a few seconds if checkers are expensive (DB ping, full Redis round-trip) — Kubernetes typically polls every 10s, you don't need fresh data per request.
- **Don't include the publisher** in liveness — publishing to a downed Pub/Sub topic should not kill the pod.

## Red flags

| Red flag | Fix |
|---|---|
| Liveness probe runs downstream checks (DB, Redis, Pub/Sub) | Move downstream checks to readiness; liveness stays static |
| Single `/health` endpoint serving both probes | Split into `/livez` (static) and `/readyz` (dependency-aware) |
| Checker without a context timeout | Wrap with `context.WithTimeout(ctx, 2*time.Second)` |
| Aggregator returns 200 even when one checker failed | Use `health.AggregateHandler` (any failure → 503) |
| Health endpoint reads `os.Getenv("HEALTHY")` to flip state | Reflect actual state from real checkers; don't gate via env |
