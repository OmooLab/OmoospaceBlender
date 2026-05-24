## Why

Currently, the `manage path` feature uses hardcoded folder names for categories (e.g., `images`, `videos`, `renders`). Users cannot customize these folder names. For example, a user may want to store image textures in a folder named `textures` instead of `images`, or use `footage` instead of `videos`. This limits flexibility and forces conventions that may not match users' existing project structures.

## What Changes

1. Add new preference fields in `OmoospacePreferences` to allow users to customize category folder names for each path type.
2. Modify `collect_input_paths()` and `collect_output_paths()` to read category folder names from preferences instead of using hardcoded defaults.
3. Provide sensible defaults that match the current behavior, so existing users are unaffected.
4. Add validation to ensure no empty folder names are allowed.

## Capabilities

### New Capabilities

- `category-folder-preferences`: Allow users to set custom folder names for each path category (images, videos, volumes, etc.) via addon preferences. Includes validation to prevent empty or duplicate folder names.

### Modified Capabilities

- `input-path-collection`: The `collect_input_paths()` function will now use user-configured folder names instead of hardcoded category names when constructing paths.
- `output-path-collection`: The `collect_output_paths()` function will now use user-configured folder names instead of hardcoded category names when constructing paths.

## Impact

- **Files modified**: `src/omoospaceblender/preferences.py` (add new preference fields), `src/omoospaceblender/manage_paths.py` (use preferences for folder names)
- **No breaking changes**: Defaults match current behavior, so existing workflows are unaffected
- **User-facing**: New preference section in addon preferences for category folder customization