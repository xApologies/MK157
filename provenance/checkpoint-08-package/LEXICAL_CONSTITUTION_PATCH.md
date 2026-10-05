# MK157 — LEXICAL CONSTITUTION PATCH

Purpose: prevent voice-to-text drift from mutating canon.

| Canonical | Normalize contextual variants |
|---|---|
| Valnak | Valnek, Valnac, Valmac, Valmek |
| Elara | Alara, Ilara |
| illi | Ellie, Illy, Ily |
| `vaen` | vein, vain, vane |
| `maege` | mage |
| `maegi` | mages, magi, magei |
| `velis` | phonetic variants |
| `ru’ne` | rune, ru'ne |
| `aera` | phonetic variants |
| `domai` | phonetic variants |
| ELDRIS | Eldris/Elders when unambiguous |
| Legacy / Legacies | old Pass/Passes and Path/Paths when referring to Valnak curated development |

Rules:
1. Normalize obvious transcription variants silently before adding them to the live model.
2. A transcription artifact never creates a new character/mechanic/place.
3. If mapping is ambiguous, mark unresolved rather than inventing canon.
4. `Aelis` is explicitly NOT retained; Trio third participant remains OPEN.
5. BLACKOUT and Direct/Directed Coherence do not need standing voice-normalization entries.
