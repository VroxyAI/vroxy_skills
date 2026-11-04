# vroxy_skills

Agent skills for the `vroxy` CLI — a pack of `SKILL.md` files that teach
every coding harness on a box how to talk to a vroxy workspace, plus an
installer that drops them into whichever harnesses are present.

The CLI is the operator API the phone uses (`/api/mobile/v1`). It
authenticates as whatever user owns `VROXY_TOKEN` (or `vroxy login`),
and every call is gated on that user's seat and capabilities — so a
skill never widens reach, it just makes the reachable surface easy to
use without shelling into production.

## Install

```bash
git clone git@github.com:wartron/vroxy_skills.git
cd vroxy_skills
python3 install_skills.py --dry-run   # see what would change
python3 install_skills.py             # install
python3 install_skills.py --uninstall # remove from every harness
```

The installer detects harnesses on PATH and copies each skill into that
harness's skill root. The map is a table at the top of
`install_skills.py`:

| harness | skill root |
| --- | --- |
| `claude` | `~/.claude/skills` |
| `cursor-agent` | `~/.cursor/skills` |
| `codex` | `~/.codex/skills` |
| `copilot` | `~/.copilot/skills` |
| `opencode` | `~/.config/opencode/skills` |
| `gemini`, `amp` | `~/.agents/skills` |

A harness that isn't listed yet is one line to add once its convention
is confirmed.

## The skills

| skill | surface |
| --- | --- |
| `vroxy` | login, workspaces, rooms, read/post, search, dispatch status |
| `vroxy-docs` | knowledge-base docs the bot answers from |
| `vroxy-tools` | custom bot tools |
| `vroxy-support` | support chats, visitors, client errors |
| `vroxy-dispatch` | agent targets, plan usage, dispatch status |
| `vroxy-admin` | create/rename workspaces, create rooms, invite / role / remove members (mobile token) |

## The walls

The CLI mints an **agent-scoped** token by default, and the mobile API's
agent allow-list is deliberately narrow. A plain `403` means the seat
lacks the capability; `agent_token_refused` means the call is closed to
agents by design — inviting, promoting or removing members, creating
workspaces, accepting invitations, answering room questions, and
dispatch queue control. Those are app actions: the skill says to hand
the person back to the app rather than routing around it. An agent
reading a visitor transcript inviting itself as admin is exactly the
prompt-injection path that wall exists to block, so it is not something
the skills are meant to climb over.

Workspace setup and member management (`vroxy-admin`) ride a
**separately-minted `mobile` token** — `vroxy login --mobile`, which
prints a browser link the person signs into and approves. The agent
never mints it; it only consumes a token the person already stored.
Creating a dispatch agent has no mobile endpoint at all and stays an
app action.
