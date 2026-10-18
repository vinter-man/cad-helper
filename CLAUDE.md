@AGENTS.md

## Claude Code

- Design requests (new garden, redesign, "add a pond", "move the bench") go through the
  `landscape-design` skill. It has the interview, plan template, review checklist and
  the full API reference.
- After every build, open `projects/<name>/preview.png` with the Read tool before you
  report back. The checks catch geometry errors; only the image shows whether the plan
  reads well.
- Reply in the user's language (they often write Russian or Bulgarian). Files in the
  repo stay English.
