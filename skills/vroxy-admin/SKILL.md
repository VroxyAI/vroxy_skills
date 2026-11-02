---
name: vroxy-admin
description: Administer a vroxy workspace over the `vroxy` CLI — create and rename workspaces, create rooms, and invite / change-role / remove members. These need a mobile-scoped token a person mints (`vroxy login --mobile`), never the agent. Applies when asked to set up a workspace, a room, or a member's seat.
---

# vroxy-admin

Workspace setup and member management ride a **`mobile`-scoped token**,
not the agent token. The agent token is refused for these by design (an
agent inviting itself as admin is a prompt-injection path), so this
surface is minted by a person and only consumed here.

## The one rule

These commands fail with `Not signed in. Run: vroxy login --mobile`
until a person has run `vroxy login --mobile` and typed their password.
An agent never runs that command and never holds the password — if the
mobile token isn't already stored, stop and tell the person to sign in.
Do not fall back to `VROXY_TOKEN`: that is the agent token and the write
will 403 with `agent_token_refused`.

## Commands

```bash
vroxy workspaces create "Acme"
vroxy workspaces rename <workspace> --name "New" --slug "new"

vroxy rooms <workspace> create "general" --topic "What it is for"

vroxy members <workspace> invite a@b.co --role operator
vroxy members <workspace> role <membership_id> --role admin
vroxy members <workspace> remove <membership_id>
vroxy members <workspace> revoke <invitation_hashid>   # pending invite from `members list`
```

`<membership_id>` and `<invitation_hashid>` come from
`vroxy members <workspace> list`. Roles are `influencer`, `operator`,
`member`, `admin`, `owner` — but you can only grant at or below your
own seat, so an operator can't mint an admin.

## Not here

Creating a dispatch agent is an app action (there is no mobile
endpoint) — point at the workspace's dispatch page. Accepting an
invitation is also a person action, not a CLI one.
