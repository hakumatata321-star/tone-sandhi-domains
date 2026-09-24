# Invented Mandarin-Style Utterances with Third-Tone Sandhi

## Overview

This dataset contains 6,000 synthetic utterances built to study Mandarin-style third-tone sandhi over hidden prosodic domains. Each utterance is a string of invented syllables with a class tag and a lexical tone for every syllable, a recorded duration, and the surface tones a speaker would produce once the sandhi rule has applied inside each prosodic domain.

Nothing here is Mandarin. The syllables are spelled like pinyin, but they are invented, and their tones, classes and grouping come from a generator whose draws are HMAC-SHA256 keyed to a withheld 256-bit secret. No part of the release can be regenerated or matched against any lexicon, corpus or speech archive.

## Release At A Glance

- 6,000 utterances, 90,146 syllables, drawn from a lexicon of 140 invented syllables.
- 10 to 20 syllables per utterance.
- 8 syllable classes and 5 lexical tones (1 to 4, and 0 for a neutral tone).
- 30,123 contested sites, where a third tone is followed by another third tone; the sandhi applied at 56.3 percent of them.
- Recorded durations from 1,635 to 7,000 milliseconds.
- An utterance is the independent unit.

## How The Data Was Generated

A lexicon of invented syllables is drawn once, and each syllable is given a fixed class and a fixed lexical tone. Third tones are deliberately common, so runs of them occur often. Each utterance draws its syllables from the lexicon, and a hidden speech rate.

The syllables are grouped into prosodic domains by a fixed grammar that reads the class tags: neighbouring units join in order of how strongly their classes bind, and a join too weak for the utterance's speech rate becomes a boundary instead. Faster speech tolerates weaker joins. Within each domain the third-tone sandhi rule applies cyclically, innermost grouping first: a third tone followed by a third tone becomes a second tone. It never applies across a boundary, and no other tone changes.

The recorded duration is the number of syllables times a per-syllable time set by the speech rate, with multiplicative noise, so it reflects the rate without revealing it.

## Files

- `utterances.csv`: one row per utterance, with its id, the number of syllables, the syllables, their class tags and their lexical tones (each as a space-separated sequence), and the duration in milliseconds.
- `surface.csv`: one row per utterance, with the surface tones after sandhi as a space-separated sequence aligned with the syllables.
- `LICENSE`: CC BY 4.0.
- `DATASET_DESCRIPTION.md`: this description, shipped inside the archive so the card and the data cannot drift apart.
- `PACKAGE_MANIFEST.sha256`: a SHA-256 for every other file, so the archive can be verified after download.

## Intended Use And Limitations

The dataset is intended for work on recovering a latent grouping from sparse, indirect supervision, and on calibrated prediction where a hidden per-item variable couples the outputs. It is fully synthetic. The grouping grammar is a deliberate simplification of Mandarin prosodic structure, the syllables and their tones are not Mandarin, and results on it say nothing about real Mandarin speech.

## Licence

CC BY 4.0. The dataset is synthetic and contains no personal data and no third-party material.
