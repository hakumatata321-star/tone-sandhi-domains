# Invented Mandarin-Style Utterances with Third-Tone Sandhi

## Overview

This dataset contains 12,000 synthetic utterances from 1,000 speakers, built to study Mandarin-style third-tone sandhi over hidden prosodic domains. Each utterance is a string of invented syllables with a class tag and a lexical tone for every syllable, a speaker, a recorded duration, and the surface tones produced once the sandhi rule has applied inside each prosodic domain.

Nothing here is Mandarin. The syllables are spelled like pinyin, but they are invented, and their tones, classes, grouping strengths and speaker differences come from the generator `gen.py`, included in this package, whose draws are HMAC-SHA256 keyed to a withheld 256-bit secret. Without the secret, no part of the release can be regenerated or matched against any lexicon, corpus or speech archive.

## Release At A Glance

- 12,000 utterances from 1,000 speakers, twelve per speaker, 179,691 syllables, drawn from a lexicon of 140 invented syllables.
- 10 to 20 syllables per utterance.
- 8 syllable classes and 5 lexical tones (1 to 4, and 0 for a neutral tone).
- 55,753 contested sites, where a third tone is followed by another third tone; the sandhi applied at 57.7 percent of them.
- Recorded durations from 1,512 to 6,595 milliseconds.
- A speaker is the independent unit.

## How The Data Was Generated

A lexicon of invented syllables is drawn once, and each syllable is given a fixed class and a fixed lexical tone. Third tones are deliberately common, so runs of them occur often. A shared table of binding strengths between classes is drawn once, and each speaker receives their own copy with small deviations and their own shift of the boundary threshold. Each utterance draws its syllables from the lexicon, and a hidden speech rate.

The syllables are grouped into prosodic domains by the speaker's grammar: neighbouring units join in order of how strongly their classes bind, a joined unit presents its left member's class to its neighbours, and a join too weak for the utterance's speech rate becomes a boundary instead. Faster speech tolerates weaker joins. Within each domain the third-tone sandhi rule applies cyclically, innermost grouping first: a third tone followed by a third tone becomes a second tone. It never applies across a boundary, and no other tone changes.

The recorded duration is the number of syllables times a per-syllable time set by the speech rate, with multiplicative noise, so it reflects the rate without revealing it.

## Raw File Structure

The uploaded ZIP is flat and contains exactly these six files at its root:

- `utterances.csv`: one row per utterance: `case_id`, `speaker_id`, `n_syllables`, `syllables`, `classes`, `lexical_tones` (each sequence space-separated), `duration_ms`.
- `surface.csv`: one creator-side row per utterance: `case_id`, `surface_tones`, the tones after sandhi, aligned with the syllables; used by `prepare.py`, which publishes them only for training utterances and for five support utterances of each test speaker.
- `gen.py`: the generator that produced every file here, without its secret.
- `LICENSE`: CC BY 4.0 notice and licence URL.
- `DATASET_DESCRIPTION.md`: this description, shipped inside the archive so the card and the data cannot drift apart.
- `PACKAGE_MANIFEST.sha256`: SHA-256 checksum of every other file in the package.

## Intended Use And Limitations

The dataset is intended for work on recovering a latent grouping from sparse, indirect supervision, on adapting to a new speaker from a few labelled examples, and on calibrated prediction where a hidden per-item variable couples the outputs. It is fully synthetic. The grouping grammar is a deliberate simplification of Mandarin prosodic structure, the syllables and their tones are not Mandarin, and results on it say nothing about real Mandarin speech.

## Licence

CC BY 4.0. The dataset is synthetic and contains no personal data and no third-party material.

## Data access

The data files are distributed with the challenge that uses them. The generator `gen.py` is published here and in the package; the secret that keys it is withheld, so the release cannot be regenerated or matched against any external source.
