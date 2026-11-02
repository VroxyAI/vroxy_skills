---
name: vroxy
description: Query and post to a vroxy workspace over the `vroxy` CLI — sign in, list workspaces and rooms, read and post room messages, search, and check dispatch status. Use this instead of shelling into production. Applies when someone asks about a workspace, room, or message, or wants to read, post or search a room.
---

# vroxy

The `vroxy` CLI is the operator API the phone uses, reachable from a
terminal. It authenticates as whatever user owns `VROXY_TOKEN` (or
`vroxy login`), and every call is gated on that user's seat and
capabilities. It is a client, not a new permission surface.

## Auth

```bash
vroxy login            # saves a token to ~/.config/vroxy (or $VROXY_HOST's)
vroxy whoami           # which user the saved token belongs to, plus workspaces
```

`VROXY_TOKEN` in the environment wins over the saved token. `--host`
overrides `$VROXY_HOST` / the saved host. `--json` prints raw JSON.

## Getting around

```bash
vroxy workspaces                       # workspaces you hold a seat in
vroxy rooms <workspace>                # rooms in a workspace
vroxy read <workspace> <room> --limit 20
vroxy post <workspace> <room> "hi"     # body of "-" reads stdin
vroxy search <workspace> "phrase"      # messages across rooms you've joined
vroxy dispatch <workspace>             # is the workspace's agent up
```

## The two refusals

- A plain `403` means the token's seat lacks that capability — say so,
  do not try to bypass it.
- A `403` with `agent_token_refused` means the call needs something the
  agent token is never allowed: inviting, promoting or removing members,
  creating workspaces, accepting invitations, answering room questions,
  or dispatch queue control. These are app actions — tell the person to
  do it in the web app, never attempt to route around it.

Not signed in? Say so instead of guessing. A call that 403s for one
person may work for another; the seat, not the command, is the gate.

## Related skills

KB docs → `vroxy-docs`. Custom bot tools → `vroxy-tools`. Chats,
visitors and client errors → `vroxy-support`. Agent targets, plan usage
and dispatch status → `vroxy-dispatch`.
