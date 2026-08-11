# Ref2VA Reference Recipes

## A. Identity from image, motion from video, voice from audio

- `<Subject 1>` = target identity from image.
- `<Video 1>` = motion/camera reference only.
- `<Audio 1>` = voice timbre reference.
- Target speaker = `<Subject 1> (S1)`.
- Keep source video's identity/environment outside the preservation set unless requested.

## B. Source-video edit with original audio retained

- `<Video 1>` = source edit video.
- `<Audio 1>` = synchronized source audio if exposed separately.
- Summary begins as an edited version of `<Video 1>`.
- Visual source structure usually `fully_preserved` or `partially_preserved` depending on edit scope.
- Audio `fully_copy` only if the complete signal is reused 1:1.

## C. Source-video edit with new voice

- `<Video 1>` = source visuals/timing.
- `<Audio 1>` = new voice reference.
- Original source dialogue is not automatically reused.
- Target speaker keeps stable S ID.

## D. Multi-person identity composition

- Give each person its own `<Subject N>`.
- Never let one `<Subject N>` represent two people.
- If an outfit from one picture is transferred to another person, use `attribute_transfer` for that clothing attribute only.

## E. Environment + character + product

- separate environment, person and product subjects;
- product geometry is a hard lock;
- do not merge product with environment reference.
