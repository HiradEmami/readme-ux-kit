# Terminal Colors

| Token | Hex | Use |
| --- | --- | --- |
| Console ink | `#0f172a` | Dark shell panels, headings, and labels |
| Terminal green | `#22c55e` | Successful commands, prompts, and ready states |
| Command blue | `#38bdf8` | Flags, paths, and command names |
| Warning amber | `#f59e0b` | Recoverable warnings and missing optional inputs |
| Failure red | `#ef4444` | Blocking errors and dangerous commands |
| Muted gray | `#64748b` | Log metadata and secondary diagnostics |
| Grid line | `#1e293b` | Terminal dividers and table separators |

## Guidance

- Use terminal green for success only, not for every decorative line.
- Keep code blocks short and split longer flows by command phase.
- Pair logs with status tables so users can scan behavior quickly.

