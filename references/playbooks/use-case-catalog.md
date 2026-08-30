# AIKSK H3 Use-Case Catalog

This catalog is an AIKSK production layer. It does not replace official H3 prompt grammar. Compile every selected recipe back into the official base-mode or Ref2VA output structure.

## 1. Cinematic short film

Priority: continuity → performance → camera → sound.

Prompt ingredients:
- establish genre, lighting and composition in Shot 1;
- give each character one stable appearance anchor;
- define physical action beats rather than plot summary;
- use one dominant camera move per shot;
- put diegetic sounds on the same timeline as actions;
- use music as audience-only score unless physically present in scene.

## 2. Chinese micro-drama / dialogue scene

Priority: exact dialogue → speaker stability → reaction timing → simple camera.

- keep Chinese wording exact inside `<d>[Chinese] ...</d>`;
- assign stable S IDs;
- align gestures and eye-lines with speaker turns;
- avoid excessive cuts during long lines;
- separate room tone/SFX from music.

## 3. Suspense / horror

Priority: withholding information and sound staging.

- use controlled negative space;
- slow camera reveal before the main event;
- use specific off-screen sounds;
- avoid generic “scary atmosphere” language without visible/audible cues.

## 4. Comedy reaction

Priority: setup → pause → reaction → payoff.

- preserve reaction timing;
- use static or simple camera framing where timing matters;
- use SFX sparingly so the gag stays readable.

## 5. Romance / emotional close-up

Priority: facial micro-action and eye-line.

- small movement amplitude;
- subtle breathing, blinking, hand motion;
- avoid overloading scene changes.

## 6. Documentary / observational

Priority: believable behavior and environmental continuity.

- natural handheld or restrained static camera;
- realistic ambience;
- no excessive cinematic VFX unless requested.

## 7. POV / first-person

Priority: camera-body relationship.

- specify first-person camera height/orientation;
- describe visible hands/body only when needed;
- keep head/body movement physically plausible;
- avoid switching to third-person unless intentionally cut.

## 8. Action / fight choreography

Priority: clear contact geometry and readable action chain.

- define left/right hand or weapon when relevant;
- define attack direction, block, impact and recovery;
- avoid multiple simultaneous impossible attacks;
- keep camera simpler than the body choreography.

## 9. Transformation / creature / fantasy VFX

Priority: transformation sequence and identity boundaries.

- define initial anatomy;
- specify ordered morphological changes;
- state which identity traits remain;
- describe material/light interaction of VFX;
- land on a stable final form.

## 10. Dance / performance / sports

Priority: body rhythm and full-body readability.

- keep limbs visible for important movement;
- specify tempo and direction;
- distinguish camera orbit from dancer rotation;
- use music/beat references only when actually available.

## 11. Minimalist product ad

Priority: product geometry → material → hero lighting → restrained motion.

- lock product silhouette and label placement;
- one key selling point per beat;
- use macro/details only if they reveal real product features;
- do not invent claims.

## 12. Brand promo / launch film

Priority: brand facts → use case → payoff → CTA.

- preserve authorized logo/text only;
- separate product facts from visual metaphors;
- use fast cuts only when content remains readable.

## 13. Beauty / fashion showcase

Priority: face/garment consistency.

- lock fabric cut, color, accessories and hairstyle;
- specify allowed garment motion;
- use flattering but physically coherent lighting;
- avoid face identity drift during extreme camera moves.

## 14. Food / cooking commercial

Priority: texture and physical cooking states.

- describe steam, oil, condensation, crust, sauce viscosity;
- connect action to sound: slicing, sizzling, pouring;
- keep food geometry stable between cuts.

## 15. Tech / device / UI showcase

Priority: device geometry and readable interaction.

- lock ports/buttons/screen orientation;
- avoid morphing device edges;
- if on-screen text must be exact, preserve source text rather than inventing it.

## 16. E-commerce product demo

Priority: clarity over cinema.

- medium/close views;
- show one function at a time;
- preserve hands/product contact;
- avoid camera moves that obscure the feature.

## 17. Architecture / travel / hotel promo

Priority: spatial continuity.

- establish exterior/interior location;
- use smooth movement that respects room geometry;
- avoid impossible teleporting through walls unless stylized transition is requested.

## 18. 3D animation short

Priority: stylized character consistency and readable staging.

- define character proportions/material style;
- use clear silhouette poses;
- keep environment art direction stable;
- pair foley with stylized movement.

## 19. Hand-drawn + live-action fusion

Priority: boundary between real and drawn elements.

- state which layer is live action;
- state which elements are sketch/ink/paint;
- describe how drawn elements interact with physical surfaces.

## 20. Papercraft stop-motion explainer

Priority: tactile material logic.

- layered paper edges, cut marks, tabs, folds;
- stop-motion stepping rather than fluid organic motion;
- paper/cloth foley; restrained music unless requested.

## 21. Paper collage explainer

Priority: editorial composition and symbolic visual metaphor.

- halftone/photo-cutout/paper-texture consistency;
- animate placement, tearing, sliding and layering;
- keep text legible and sparse.

## 22. Clay / miniature / toy-world

Priority: scale cues and material response.

- fingerprints, matte clay, miniature depth cues;
- limited joint motion consistent with miniature style;
- tactile foley.

## 23. Anime / 2D stylized shot

Priority: line/style stability.

- lock character design cues;
- use anime-appropriate camera and timing only if requested;
- avoid accidental live-action texture contamination.

## 24. Game intro / character menu / UI animation

Priority: fixed UI geometry + character presentation.

- treat menu/card locations as composition locks;
- animate selection/highlight states sequentially;
- keep UI text exact when source text exists.

## 25. MV / lyric visual

Priority: beat, lyric timing and visual motif.

- preserve lyric text exactly;
- use text only where the user asks for visible lyrics;
- map visual transitions to audible beat changes;
- distinguish diegetic performance from audience-only soundtrack.

## 26. Singing performance

Priority: singer identity, mouth/performance timing, music role.

- stable S ID;
- lyrics in `<d>`;
- describe stage/performance gestures without cluttering mouth performance.

## 27. Voice-reference digital human

Priority: identity + voice timbre + restrained movement.

- `<Audio N>` is a timbre/delivery reference unless reuse is requested;
- target person keeps stable `(Sx)`;
- do not copy source words automatically.

## 28. Two-person dialogue

Priority: speaker alternation and eye-line.

- stable S1/S2;
- distinguish who is visible/off-screen;
- reactions occur after or during the correct line;
- avoid speaker-ID swap after cuts.

## 29. Narration-led explainer

Priority: narration pace + supportive visuals.

- narrator may remain off-screen;
- visuals illustrate the current claim rather than unrelated decoration;
- do not repeat narration text as visible text unless asked.

## 30. Sound-design-led atmospheric clip

Priority: audible environment.

- start from room tone/environment baseline;
- layer physical events with precise timing;
- music optional; silence can be intentional.

## 31. Character identity reference generation

Ref2VA.

- define person as `<Subject N>`;
- preserve face/hair/age/body cues;
- use clothing/environment references separately if they come from other assets.

## 32. Multi-image identity + costume composition

Ref2VA.

- one asset may define identity, another outfit, another environment;
- use `attribute_transfer` only for the attribute actually transferred;
- do not merge reference labels ambiguously.

## 33. Environment transfer

- define environment as its own `<Subject N>` when it must be preserved across shots;
- keep target character identity independent.

## 34. Motion/camera reference transfer

- use `<Video N>` for temporal/camera structure;
- keep source identity weak/unused unless requested;
- state whether body motion, camera motion or edit rhythm is referenced.

## 35. Source-video edit

- define `<Video 1>` as source video for editing;
- preserve unchanged structure explicitly;
- isolate requested edits;
- use audio reuse/reference markers accurately.

## 36. Source-video continuation

- begin from source video's ending state;
- preserve continuation direction and motion phase;
- newly generated audio should continue characteristics unless source audio is directly copied.

## 37. Audio replacement / voice-reference edit

- preserve source visual video if requested;
- replace only target vocal layer;
- separate voice reference from source soundtrack reuse.

## 38. BGM reuse / rhythm reference

- `fully_copy` or `partially_copy` only when signal is reused;
- `reference` when only rhythm/style/timbre informs new music.

## 39. First-frame continuation

I2VA.

- start exactly from Picture 1 state;
- first action should be a plausible immediate continuation.

## 40. First-to-last-frame controlled transition

FL2VA.

- describe observable intermediate changes;
- do not merely describe Picture 1 then Picture 2;
- favor single-shot continuity.

## 41. Last-frame landing

L2VA.

- infer a plausible earlier state;
- progressively converge to the final frame.

## 42. Loop-like ending

- plan ending composition/state to resemble or reconnect to opening;
- do not claim perfect seamless looping unless actual generated frames verify it.

## 43. Prompt compression

- keep field names;
- keep reference labels;
- keep action/state/camera/audio/timing;
- remove repeated adjectives and redundant visual facts.

## 44. Prompt expansion

- add observable details, not plot prose;
- expand actions, camera and sound where under-specified;
- do not invent new references.

## 45. Failed-generation repair

- diagnose failure class first;
- edit only the prompt dimensions likely responsible;
- do not rewrite everything after one isolated failure.

## 46. Reference-map repair

- rebuild asset roles and labels before rewriting prose.

## 47. Dialogue timing repair

- simplify camera/action during dense speech;
- align cuts with pauses;
- preserve wording when locked.

## 48. Camera simplification

- reduce to one dominant move per shot;
- remove decorative motion that does not reveal new information.

## 49. Identity-drift repair

- strengthen reference anchor and repeated label use;
- reduce large style/anatomy changes.

## 50. Product-geometry repair

- lock silhouette/material/label placement;
- reduce extreme perspective and transformations touching the product.
