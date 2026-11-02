---
name: vroxy-dispatch
description: Inspect a vroxy workspace's dispatch setup — which repo, base ref and ship policy each agent works on, plan usage, and whether the agent is up — over `vroxy targets`, `vroxy usage` and `vroxy dispatch`. Applies when asked which repo or policy an agent works on, plan usage, or dispatch status.
---

# vroxy-dispatch

Read-only inspection of the workspace's dispatch agents.

```bash
vroxy targets <workspace>       # each agent: repo, base ref, ship policy, online state
vroxy usage <workspace>         # plan, usage this month, what the plan includes
vroxy dispatch <workspace>      # is the workspace's agent running right now
```

`targets` needs `dispatch.read`; `usage` needs `settings.read`. A plain
`403` means the seat lacks the capability — say so. There is no command
here to create or reconfigure an agent: those are app actions, so if
someone asks, point them at the workspace's dispatch page rather than
trying to drive it from the CLI. `agent_token_refused` means exactly
that wall; tell the person to do it in the app.
