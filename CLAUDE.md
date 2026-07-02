# boost-claude — Claude Code

Distribution repo for the **`golang-boost`** Claude Code plugin. This repo holds
**only** the skills + plugin manifests. The framework source it documents lives
in [`xgodev/boost`](https://github.com/xgodev/boost).

```
.claude-plugin/
  plugin.json        # golang-boost manifest + quality-gate dependency
  marketplace.json   # marketplace "xgodev-boost", source "./"
skills/
  boost/              # entry skill: flat index (SKILL.md) + references/*.md per component
  gqlgen-field-resolvers/
```

## Iron Laws — NUNCA violar

1. **Skill é markdown autocontido.** Cada `SKILL.md` cita o boost como *import
   path Go* (`github.com/xgodev/boost/...`) dentro de exemplos — nunca como
   caminho de arquivo deste repo. Não dependa de ter o source do boost ao lado.
2. **Sync com o boost é manual e obrigatório.** Mudou um componente em
   `xgodev/boost` (`factory/`, `wrapper/`, `bootstrap/`, `extra/`, `fx/`,
   `model/errors`) → abrir PR **aqui** atualizando o `references/<grupo>/<nome>.md`
   correspondente em `skills/boost/references/`. Componente novo no boost →
   reference novo aqui, mais uma linha no índice de `skills/boost/SKILL.md`. Sem
   o PR aqui, a doc fica defasada. (Antes do split, isso era um PR único no
   boost; agora são dois repos — a disciplina substitui o acoplamento.)
3. **Bump de versão a cada mudança de conteúdo.** Mudou qualquer `SKILL.md` ou
   manifest → subir `version` em `.claude-plugin/plugin.json` **e** a `version`
   do plugin em `.claude-plugin/marketplace.json`. Sem bump, o auto-update não
   reconhece a mudança.
4. **Nomes são contrato.** `name` do plugin (`golang-boost`) e `name` do
   marketplace (`xgodev-boost`) não mudam sem migração documentada — quebram
   `/plugin install` e referências externas (umbrella `xgodev/claude-plugin`).
5. **`source: "./"`** no `marketplace.json` — a raiz deste repo é o plugin.

### Red flags — PARAR e reportar

- Componente do boost alterado sem o `references/*.md` correspondente atualizado aqui, ou sem entrada no índice de `skills/boost/SKILL.md`
- Mudança de skill/manifest sem bump de versão
- `SKILL.md` referenciando caminho de arquivo local em vez de import path Go
- Rename de `golang-boost` / `xgodev-boost` sem nota de migração

## Editar/criar skills

Autorar ou editar **qualquer** `SKILL.md` é um gate: usar a skill
`superpowers:writing-skills` (TDD de skill — baseline com subagent ANTES) antes
de escrever a primeira linha. Para o padrão de adicionar um componente novo
(novo `references/<grupo>/<nome>.md` + linha no índice), ver
`skills/boost/references/CONTRIBUTING.md`.

Cada skill segue o frontmatter padrão (`name`, `description`, `license`,
`metadata.version`, `allowed-tools`) e o bloco **REQUIRED BACKGROUND** que faz
cross-reference entre skills (carrega só o necessário).

## Distribuição

```
/plugin marketplace add xgodev/boost-claude
/plugin install golang-boost@xgodev-boost
```

Dependência puxada automaticamente: `quality-gate@xgodev-quality-gate`
(pré-requisito: `/plugin marketplace add xgodev/quality-gate` antes do install).

O umbrella `xgodev/claude-plugin` (marketplace `xgodev`) re-lista este plugin
como `boost@xgodev` — ao mover o repo, o `source` lá precisa apontar para
`xgodev/boost-claude`. Esse ajuste é em outro repo, fora daqui.

## Regras gerais

- `gofmt`/`goimports` não se aplicam (sem código Go aqui), mas exemplos dentro
  das skills devem compilar conceitualmente e seguir as Iron Laws do boost.
- Documentação é parte da tarefa: mudou comportamento de um componente →
  atualizar o `references/*.md` correspondente e, se preciso, o README.
- Para o fluxo de contribuição (issue, branch, PR) ver
  [`docs/development/gitflow.md` no boost](https://github.com/xgodev/boost/blob/main/docs/development/gitflow.md).
