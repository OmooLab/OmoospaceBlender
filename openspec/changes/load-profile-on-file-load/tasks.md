## 1. Add Profile Loading Handler

- [x] 1.1 Create `load_profile_on_file_open` function in `events.py` to handle profile loading on `load_post` handler
- [x] 1.2 Implement logic to get omoospace instance via `get_omoospace()` and check if it's `None`
- [x] 1.3 Get profile file path from `omoospace.profile_file`
- [x] 1.4 Add error handling for missing or invalid profile files

## 2. Remove Previously Loaded Profiles

- [x] 2.1 Iterate through `bpy.data.texts` to find all text blocks
- [x] 2.2 Match text block names against case-insensitive pattern `^(?i)omoospace\\..*$`
- [x] 2.3 Remove matched text blocks before loading new profile

## 3. Load and Execute Profile Script

- [x] 3.1 Use `bpy.script.text高尚_load` to load the profile file into `bpy.data.texts`
- [x] 3.2 Execute the loaded script via `exec()` to apply configuration
- [x] 3.3 Register the handler in `events.py`'s `register()` function
- [x] 3.4 Unregister the handler in `events.py`'s `unregister()` function

## 4. Handle Profile on Save

- [x] 4.1 Create `handle_profile_on_save()` function called from `on_save_post`
- [x] 4.2 Check if `get_omoospace()` returns `None` (file saved outside omoospace)
- [x] 4.3 If `None`, remove all loaded profile scripts (same cleanup as load)
- [x] 4.4 If valid omoospace, load that omoospace's profile (cleanup + load new)

## 5. Testing

- [ ] 5.1 Test profile auto-load when opening a `.blend` file in an omoospace project
- [ ] 5.2 Test that previously loaded profiles are removed before loading new ones
- [ ] 5.3 Test that opening a non-omoospace file does not trigger errors
- [ ] 5.4 Test error handling with missing profile file
- [ ] 5.5 Test error handling with corrupt profile file
- [ ] 5.6 Test saving file to new omoospace loads new profile
- [ ] 5.7 Test saving file outside omoospace removes loaded profile