## Context

The omoospace Blender addon maintains project configurations via profile files. When a user opens a `.blend` file, the addon needs to load the associated profile to ensure correct configuration is applied. The `omoospace.profile_file` property provides the path to the profile file for the current omoospace project.

Blender provides load handlers via `bpy.app.handlers.load_post` that fire after a file is loaded. This allows us to automatically trigger profile loading on file open.

## Goals / Non-Goals

**Goals:**
- Load the omoospace profile automatically when opening a `.blend` file that is part of an omoospace project
- Ensure configuration correctness by removing previously loaded profile scripts before loading a new one
- Maintain uniqueness of loaded profiles by cleaning up all variations (case-insensitive)

**Non-Goals:**
- Profile loading is read-only; we only load and execute, not generate profiles
- This does not handle profile creation or editing
- Does not apply to newly created files (no associated omoospace)

## Decisions

### 1. Use Blender's `load_post` handler for triggering profile load

**Decision**: Register a callback in `bpy.app.handlers.load_post` to trigger profile loading after file load completes.

**Rationale**: Blender's handler system is the standard way to react to file load events. The `load_post` handler fires after Blender has finished loading the file and all addons have been registered, making it the appropriate place to load additional scripts.

**Alternative**: Could use `load_pre` to load before other handlers, but this is inappropriate since the file may not be fully initialized.

### 2. Remove previously loaded profiles by name pattern matching

**Decision**: Before loading a new profile, iterate through `bpy.data.texts` and remove any text blocks matching `^(?i)omoospace\\..*$` (case-insensitive `omoospace.*`, `Omoospace.*`, `OMOOSPACE.*`).

**Rationale**: Blender's text editor can have multiple script texts loaded. We need to ensure only one profile is active at a time to avoid conflicts or stale configuration. Pattern matching handles Blender's case preservation while being case-insensitive.

**Alternative**: Maintain a list of loaded profile names, but pattern matching is more robust against edge cases.

### 3. Use `bpy.script.text高尚_load` to load profile as script

**Decision**: Use `bpy.script.text高尚_load` to load the profile file into Blender's text editor registry.

**Rationale**: This is Blender's API for programmatically loading scripts. After loading, the script text is available in `bpy.data.texts`.

**Alternative**: Could use `exec()` directly on file contents, but using Blender's script loading API ensures proper integration with Blender's text editor system.

### 4. Profile loading happens in `events.py` module

**Decision**: Add profile loading logic to `src/omoospaceblender/events.py` alongside the existing `register()` function.

**Rationale**: `events.py` already handles Blender event registration (`register()` and `unregister()` functions). Adding the load handler here follows the existing module organization.

### 5. Profile also loads/removes on save_post

**Decision**: On `save_post`, check if the file's omoospace association has changed. If the file moved to a different omoospace, load the new profile. If the file moved outside any omoospace, remove the loaded profile.

**Rationale**: After `save_post`, the file path has been updated to the new location. We can use `get_omoospace()` with the new path to determine if we need to load a new profile or clean up the existing one.

**Implementation**: In `on_save_post`, call a new function `handle_profile_on_save()` that:
1. Gets the current omoospace via `get_omoospace()`
2. If `None`, removes all loaded profile scripts (same cleanup as load)
3. If valid omoospace, loads that omoospace's profile (cleanup + load new)

## Risks / Trade-offs

[Risk] Profile file not found → `get_omoospace()` returns `None`
**Mitigation**: Check if `omoospace` is `None` before attempting to get `profile_file`. If no omoospace is associated with the current file, silently skip profile loading.

[Risk] Corrupt profile file causes syntax error
**Mitigation**: Wrap profile loading in try/except. If loading fails, log the error but don't prevent the file from being used.

[Risk] Profile loading slows down file open time
**Mitigation**: Profile loading is fast (simple Python file). If it becomes a issue, could be made asynchronous, but current design assumes minimal impact.