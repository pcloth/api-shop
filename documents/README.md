# api-shop 文档项目

文档使用 VuePress 2，要求 Node.js 20 或更高版本，并通过 pnpm 锁定依赖。

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm run docs:dev
```

构建静态站点：

```bash
pnpm run docs:build
```

输出位于 `docs/.vuepress/dist`。`docs/` 是文档源码；仓库根目录的 `/docs` 是历史构建产物，更新源码后应通过构建流程重新生成，不要直接手工修改 HTML。
