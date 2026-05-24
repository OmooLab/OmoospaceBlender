## Context

The `manage path` feature in OmoospaceBlender assigns paths to category folders (e.g., `images`, `videos`, `renders`). These folder names are currently hardcoded in `manage_paths.py`. Users have no way to customize these folder names to match their own project conventions.

Current category folder mapping:
- images → `images`
- volumes → `volumes`
- dynamics → `dynamics`
- libraries → `libraries`
- misc → `misc`
- renders → `renders`
- videos → `videos`
- audios → `audios`
- geonodes → `geonodes`

## Goals / Non-Goals

**Goals:**
- Allow users to customize category folder names in addon preferences
- Maintain backward compatibility with sensible defaults
- Validate user input to prevent empty or duplicate folder names

**Non-Goals:**
- Validation of folder names (empty defaults to hardcoded value, duplicates allowed)

## Decisions

**Decision 1: Store custom folder names in OmoospacePreferences**

Using the existing `OmoospacePreferences` class to store folder name preferences.

*Rationale*: This follows the existing pattern for addon preferences (`omoospace_home`), is persistent across sessions, and uses Blender's native preferences system.

*Alternative*: Store in subspace JSON data. Rejected because preferences should be global addon settings, not subspace-specific.

**Decision 2: Use StringProperty with validation**

Each category gets its own StringProperty in preferences.

*Rationale*: StringProperty allows any folder name while being simple to implement.

*Alternative*: EnumProperty. Rejected because users may want arbitrary custom names not in a predefined enum.

**Decision 3: Provide hardcoded defaults matching current behavior**

Default values are the current hardcoded category names.

*Rationale*: Ensures existing users are unaffected - their paths will continue to work the same way.

## Risks / Trade-offs

[Risk] User changes folder name preference after paths already constructed → **Mitigation**: The preference only affects new path collection operations. Existing paths retain their original category folder names.

[Risk] User leaves folder name empty → **Mitigation**: Use default hardcoded category name as fallback.

[Risk] Duplicate folder names across categories → **Mitigation**: Allow duplicates (some users may want shared folders).

## Open Questions

- Should we add a "reset to defaults" button in preferences? (Nice-to-have, can be added later)