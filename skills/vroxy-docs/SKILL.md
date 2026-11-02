---
name: vroxy-docs
description: Manage a vroxy workspace's knowledge-base docs — the articles the support bot answers from — over `vroxy docs`. Applies when asked to list, show, create, edit, publish, unpublish or delete KB docs.
---

# vroxy-docs

Knowledge-base docs are what the workspace's support bot answers from.
Edit them through the CLI rather than shelling into the database.

```bash
vroxy docs <workspace> list --q "refund"          # loose search, title + body
vroxy docs <workspace> list --status published    # or draft
vroxy docs <workspace> show <doc>                 # hashid from list
vroxy docs <workspace> create "Title" --body "…"  # --body - reads stdin, --file reads a file
vroxy docs <workspace> edit <doc> --title "…" --body "…"
vroxy docs <workspace> publish <doc>              # or unpublish
vroxy docs <workspace> delete <doc>
```

A doc's identity in these commands is its `hashid` (from `list`), never
an integer id. Create and edit need `docs.write`; reads need `docs.read`.
If a call 403s, the seat lacks the capability — say so. If it 403s with
`agent_token_refused`, it is an app action; tell the person to do it in
the app.
