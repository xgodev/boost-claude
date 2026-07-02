**REQUIRED BACKGROUND:** `references/start.md`, `references/factory/echo.md` (typical mount point).

> This factory wraps **`graphql-go/graphql`** (code-first). If your service uses
> **gqlgen** (schema-first + Federation 2) instead, see `gqlgen-field-resolvers`
> for the resolver / model-binding / DataLoader patterns — a different library.

```go
import (
    gqlfact "github.com/xgodev/boost/factory/contrib/graphql-go/graphql/v0"
    "github.com/graphql-go/graphql"
)

schema, _ := graphql.NewSchema(graphql.SchemaConfig{ /* ... */ })

h := gqlfact.NewHandler(&schema)

srv.POST("/graphql", echo.WrapHandler(h))
srv.GET("/graphql",  echo.WrapHandler(h))   // for GraphiQL
```

Use `NewHandlerWithConfig` when you need GraphiQL playground, query introspection toggles, or custom request parsers.

## Red flags

| Red flag | Fix |
|---|---|
| `handler.New(...)` from `graphql-go/handler` directly | `gqlfact.NewHandler(&schema)` |
| Schema constructed per request | Build once at startup |
| GraphQL errors leaking 500s through the Echo error_handler | Map them explicitly via the GraphQL formatter; don't return them as Go errors |
