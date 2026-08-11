# Dialogue & Audio Recipes

## Single speaker

`the calm young woman (S1) says: <d>[Chinese] 我们现在开始。</d>`

Keep S1 stable across cuts.

## Two speakers

- first actual vocal source = S1;
- second actual vocal source = S2;
- preserve IDs even if one goes off-screen.

## Voice reference

`<Audio 1>` describes timbre/delivery source; `(S1)` describes the target speaker.
Do not copy source words unless reuse/reperformance is requested.

## Dialogue crossing a cut

Use the official continuity convention from the bundled base/ref guide. Do not invent a custom marker.

## Narration

Narrator is a real vocal source and receives an S ID if it produces independent speech.

## Singing

Lyrics remain inside `<d>` in original language.
Music bed belongs to `non_diegetic_music` unless physically produced/heard inside scene.
