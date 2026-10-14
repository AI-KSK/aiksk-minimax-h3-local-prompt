# AGENTS.md — AIKSK MiniMax H3 Prompt v1.8.1

For Codex or other coding agents operating in this directory:

1. Read `SKILL.md` first.
2. For Base tasks read `references/official/base-en.txt`.
3. For r2v/v2v/rv2v read `references/official/ref-en.txt` and `references/director/AIMIXER_DIRECTOR_RULES.md`.
4. Preserve all official field names and section ordering exactly.
5. Treat `<Subject N>` as semantic identity and `<Picture N>/<Video N>/<Audio N>` as material/source labels.
6. Do not guess AIMixer material indexes when a Director `@` picker/exported mapping is available.
7. For multi-shot stories build causal bridges before writing prose.
8. Do not present AIKSK production heuristics as official MiniMax requirements.
9. For fighting / martial arts / JOKER141 tasks, read `references/playbooks/fight-choreography.md` and optional `references/playbooks/fight-lora-presets.json` before writing; preserve two-fighter and weapon continuity.
10. LoRA weights, Veda, and one-/two-stage generation are **runtime config**, never new official H3 prompt sections.
11. Run `python tests/test_structure.py` after editing this package.

Martial workflow: read `references/playbooks/fight-trigger-policy.md` and `references/playbooks/fight-prompt-mapping.md`; do not equate GUI preset change with live prompt recompilation.
