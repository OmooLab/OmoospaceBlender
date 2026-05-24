## 1. Add Preference Fields

- [x] 1.1 Add category folder name StringProperty fields to `OmoospacePreferences` in `preferences.py`
- [x] 1.2 Add `draw()` method to render the new preference fields in the UI

## 2. Update Path Collection Functions

- [x] 2.1 Create a helper function `get_category_folder(category_key)` to read from preferences with fallback defaults
- [x] 2.2 Update `collect_input_paths()` in `manage_paths.py` to use custom folder names
- [x] 2.3 Update `collect_output_paths()` in `manage_paths.py` to use custom folder names

## 3. Verify and Test

- [x] 3.1 Verify `correct_input_path()` and `correct_output_path()` work with custom folder names
- [x] 3.2 Test the UI by opening addon preferences and changing folder names
- [x] 3.3 Test path collection with custom folder names and confirm paths are constructed correctly