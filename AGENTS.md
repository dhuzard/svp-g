# SVP-G Agent Guardrails (OpenCode + MCP)

Agents in this repository must interact with SVP through MCP tools.

## Canonical Loop

1. Call `load_state_tool(project_root)` before taking action.
2. Call `explain_next_action_tool(project_root)`.
3. Execute the recommended action.
4. Prefer `apply_next_action_tool(project_root, response, expected_action_type)` instead of manual dispatch.
5. After success (`ok=true`), call `save_state_tool(project_root, state)`.
6. Repeat.

## Required Rules

- Always call `load_state_tool` first.
- Then call `explain_next_action_tool`.
- Execute only the recommended action for the current state.
- Prefer `apply_next_action_tool` over direct dispatch tools.
- Always save after a successful apply result.
- Never invent phases.
- Never invent status lines.
- Never bypass gates defined by `svp_core`.

## Safety Notes

- If `apply_next_action_tool` returns `ok=false`, call `explain_next_action_tool` again and follow returned guidance.
- Use direct dispatch tools only when explicitly debugging dispatch behavior.
