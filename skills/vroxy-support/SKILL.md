---
name: vroxy-support
description: Triage a vroxy workspace's visitor support — support chats, widget visitors, and client errors — over `vroxy chats`, `vroxy visitors` and `vroxy errors`. Applies when asked about a visitor conversation, who opened the widget, or a client error.
---

# vroxy-support

The visitor-facing surface, readable from the terminal.

```bash
# Support chats
vroxy chats <workspace> list --filter all --q "refund"
vroxy chats <workspace> list --filter awaiting_human   # or open
vroxy chats <workspace> show <chat>                    # full transcript

# Widget visitors
vroxy visitors <workspace> list --active
vroxy visitors <workspace> list --identity identified
vroxy visitors <workspace> show <visitor>

# Client errors (reported by the widget / SDKs)
vroxy errors <workspace> list --source ruby
vroxy errors <workspace> show <fingerprint>
```

Chats and visitors need `chats.read` and `visitors.read`; errors need
`errors.read`. A plain `403` means the seat lacks the capability — say
so. `agent_token_refused` means an app action; tell the person to do it
in the app. Identifiers are hashids or fingerprints, not integer ids.
