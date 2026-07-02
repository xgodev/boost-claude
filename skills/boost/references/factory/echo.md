**REQUIRED BACKGROUND:**
- `references/start.md` — `boost.Start()` first.
- `references/wrapper/log.md` — request logger via context.
- `references/model-errors.md` — handler errors are typed and routed by `error_handler`.

## Canonical `main.go`

```go
package main

import (
    "context"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/xgodev/boost"
    echoserver "github.com/xgodev/boost/factory/contrib/labstack/echo/v4"
    "github.com/xgodev/boost/factory/contrib/labstack/echo/v4/plugins/extra/error_handler"
    logplugin "github.com/xgodev/boost/factory/contrib/labstack/echo/v4/plugins/local/wrapper/log"
    restresponse "github.com/xgodev/boost/factory/contrib/labstack/echo/v4/plugins/local/model/restresponse"
    recoverplugin "github.com/xgodev/boost/factory/contrib/labstack/echo/v4/plugins/native/recover"
    "github.com/xgodev/boost/factory/contrib/labstack/echo/v4/plugins/native/requestid"
    "github.com/xgodev/boost/wrapper/log"
)

func main() {
    boost.Start()

    ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
    defer cancel()

    srv, err := echoserver.NewServer(ctx,
        recoverplugin.Register, // panics → 500, no process death
        requestid.Register,     // X-Request-ID propagation
        logplugin.Register,     // request access log via boost logger
        restresponse.Register,  // sets Type=REST so error_handler emits JSON
        error_handler.Register, // model/errors → HTTP status mapping
    )
    if err != nil {
        log.FromContext(ctx).WithError(err).Fatal("failed to build echo server")
    }

    srv.GET("/health", healthHandler)
    srv.POST("/orders", orderHandler.Create)

    go srv.Serve(ctx)
    <-ctx.Done()

    shutdownCtx, cancelShutdown := context.WithTimeout(context.Background(), 15*time.Second)
    defer cancelShutdown()
    srv.Shutdown(shutdownCtx)
}
```

## Required plugin set

| Plugin | Purpose | Skip when |
|---|---|---|
| `native/recover` | Panic → 500 | Never |
| `native/requestid` | X-Request-ID | Never |
| `local/wrapper/log` | Access log via boost logger | Never |
| `local/model/restresponse` | Sets `Type=REST` for `error_handler` JSON mode | Never (REST APIs) |
| `extra/error_handler` | Maps errors to HTTP status + JSON envelope via `model/errors.Classify` | Never |
| `native/cors` | Browser clients | Internal-only services |
| `native/gzip` | Response compression | gRPC / streaming |

## Plugin order constraint

`restresponse.Register` MUST come before `error_handler.Register`. Reason: the error handler picks `ErrorHandlerJSON` only when the server has `Type=REST` set on it. Without `restresponse` first, you get `ErrorHandlerString` (text/plain) — production symptom: 4xx/5xx responses come back as `"some error"` text instead of the JSON envelope clients expect.

## Graceful shutdown

```go
ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer cancel()

go srv.Serve(ctx)        // blocking; goroutine so we can react to ctx.Done()
<-ctx.Done()

shutdownCtx, _ := context.WithTimeout(context.Background(), 15*time.Second)
srv.Shutdown(shutdownCtx) // bounded drain with FRESH ctx
```

Use a fresh context for `Shutdown` — passing the cancelled parent makes it return immediately.

## Observability plugins

`echoserver.NewServer(ctx, plugins ...Plugin)` also accepts vendor plugins — if the service uses one of these vendors, add the matching plugin here, not a hand-rolled Echo middleware:

| Vendor | Import | Usage |
|---|---|---|
| Datadog | `.../factory/contrib/labstack/echo/v4/plugins/contrib/datadog/dd-trace-go/v1` | `echoserver.NewServer(ctx, ..., datadog.Register)` (or `datadog.NewDatadog(opts...).Register`) |
| OpenTelemetry | `.../factory/contrib/labstack/echo/v4/plugins/contrib/go.opentelemetry.io/contrib/v0` | `echoserver.NewServer(ctx, ..., otelecho.Register)` (or `NewOtelEcho(opts...).Register`) |
| Prometheus | `.../factory/contrib/labstack/echo/v4/plugins/contrib/prometheus/client_golang/v1` | `echoserver.NewServer(ctx, ..., prometheus.Register)` (or `NewPrometheus().Register`) |

Other available (non-observability) plugins live under the same `plugins/` tree: `native/bodydump`, `native/bodylimit`, `native/cors`, `native/gzip`, `contrib/bytedance/sonic` and `contrib/goccy/go-json` (JSON codec swaps), `contrib/hiko1129/echo-pprof` (profiling), `contrib/swaggo/echo-swagger` (docs UI). Same `Register` pattern as the required set above.

## Custom error → status, or ignore

The handler resolves status via `model/errors.Classify`. To make a non-boost
error return a specific status (or be ignored / treated as 200), register it at
boot — it works for HTTP and gRPC at once. See `references/model-errors.md`
(`Register`/`RegisterMatch`/`Ignore`); don't add cases to the handler by hand.

## Red flags

| Red flag | Fix |
|---|---|
| `echo.New()` directly | `echoserver.NewServer(ctx, ...)` |
| `error_handler.Register` before `restresponse.Register` | Reorder |
| `srv.Serve(ctx)` called inline (not in a goroutine) followed by `<-ctx.Done()` | Wrap `Serve` in a goroutine |
| `echo.NewHTTPError(...)` in a handler | Return `bootsterrors.<Type>(err, "...")` (see `references/model-errors.md`) |
| `Shutdown(ctx)` reusing the cancelled parent context | Use a fresh `context.WithTimeout` |
