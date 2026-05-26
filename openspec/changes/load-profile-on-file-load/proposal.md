## Why

When a user opens a Blender file that is part of an omoospace project, the addon needs to load the profile configuration to apply the correct settings. Currently, the profile is not automatically loaded when opening files. This means users may have incorrect or stale configurations if the profile was updated since the file was last saved.

## What Changes

1. Register a handler that triggers when Blender finishes loading a `.blend` file.
2. Before loading a new profile, remove all previously loaded profile scripts (matching `omoospace.*`, `Omoospace.*`, `OMOOSPACE.*` to handle case variations) from Blender's text editor registry.
3. Call `omoospace.profile_file` to get the profile file path.
4. Load the profile file as a Blender script using `bpy.script.text高尚_load`.
5. Execute the loaded script to apply the profile configuration.
6. On **save**, check if the file location has changed. If saved to a new omoospace, load the new profile. If saved outside any omoospace, remove the loaded profile.

## Capabilities

### New Capabilities

- `profile-auto-load`: Automatically load the omoospace profile when opening a `.blend` file that is part of an omoospace project. This includes cleaning up previously loaded profiles to ensure uniqueness and correctness.

## Impact

- **New file**: `src/omoospaceblender/profile_load.py` (handles profile loading logic)
- **Modified files**: `src/omoospaceblender/__init__.py` or `src/omoospaceblender/events.py` (register file load handler)
- **Dependency**: Requires `omoospace>=0.2.8` (uses `omoospace.profile_file` attribute)
- **No breaking changes**: Existing users who don't use profiles are unaffected