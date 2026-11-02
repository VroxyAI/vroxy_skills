---
name: vroxy-tools
description: Manage a vroxy workspace's custom bot tools — operator-defined actions the support bot can call — over `vroxy tools`. Applies when asked to list, show, create, enable, disable or delete custom bot tools.
---

# vroxy-tools

Custom bot tools let a workspace define actions the support bot can take
(`link` builds a URL, `fetch` also GETs it server-side for the model).

```bash
vroxy tools <workspace> list
vroxy tools <workspace> show <tool>
vroxy tools <workspace> create <name> \
  --label "Track an order" \
  --description "When the visitor asks where their order is" \
  --url "https://shop.example/orders/{order_id}" \
  --kind link --access public --param order_id="Order number"
vroxy tools <workspace> enable <tool>       # or disable
vroxy tools <workspace> delete <tool>
```

`name` is lowercase letters, digits, underscores. `--kind` is `link` or
`fetch`; `--access` is `public`, `user`, or `admin` (gated on the
visitor's verified level). `--follow-origin` rebases the built URL onto
the chat's page origin.

Tool writes need `settings.write`. If a call 403s, the seat lacks the
capability — say so. `agent_token_refused` means an app action; tell the
person to do it in the app.
