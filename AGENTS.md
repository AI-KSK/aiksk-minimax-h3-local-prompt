# AGENTS.md — AIKSK MiniMax H3 Prompt v1.7

For Codex or other coding agents operating in this directory:

1. Read `SKILL.md` first.
2. For Base tasks read `references/official/base-en.txt`.
3. For r2v/v2v/rv2v read `references/official/ref-en.txt` and `references/director/AIMIXER_DIRECTOR_RULES.md`.
4. Preserve all official field names and section ordering exactly.
5. Treat `<Subject N>` as semantic identity and `<Picture N>/<Video N>/<Audio N>` as material/source labels.
6. Do not guess AIMixer material indexes when a Director `@` picker/exported mapping is available.
7. For multi-shot stories build causal bridges before writing prose.
8. Do not present AIKSK production heuristics as official MiniMax requirements.
9. Run `python tests/test_structure.py` after editing this package.
