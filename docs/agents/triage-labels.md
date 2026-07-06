# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `type:AFK`           | Agent can implement + merge unattended   |
| `ready-for-human`          | `type:HITL`          | Needs a human decision / implementation  |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

`ready-for-agent`/`ready-for-human` reuse this repo's existing `type:AFK`/`type:HITL` scheme rather than introducing parallel labels. `area:*` and `priority:*` are orthogonal (topic + urgency) and are not triage states.

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.
