## ADDED Requirements

### Requirement: Profile auto-load on file open
The system SHALL automatically load the omoospace profile when a user opens a `.blend` file that is part of an omoospace project.

#### Scenario: Profile loads when opening omoospace file
- **WHEN** user opens a `.blend` file that is part of an omoospace project
- **THEN** the system SHALL retrieve the profile file path via `omoospace.profile_file`
- **AND** SHALL load the profile as a Blender script
- **AND** SHALL execute the profile to apply configuration

#### Scenario: No profile load for non-omoospace files
- **WHEN** user opens a `.blend` file that is not part of any omoospace project
- **THEN** `get_omoospace()` SHALL return `None`
- **AND** the system SHALL silently skip profile loading

### Requirement: Previously loaded profiles are removed before loading new profile
Before loading a new profile, the system SHALL remove all previously loaded profile scripts from Blender's text editor registry.

#### Scenario: Old profile scripts are removed
- **WHEN** a new profile is about to be loaded
- **THEN** the system SHALL iterate through `bpy.data.texts`
- **AND** SHALL remove any text block whose name matches case-insensitive pattern `omoospace.*`
- **AND** SHALL then load the new profile

#### Scenario: Different case variations are removed
- **WHEN** a profile is about to be loaded
- **THEN** the system SHALL remove text blocks named `omoospace.profile`, `Omoospace.profile`, `OMOOSPACE.profile`, etc.
- **AND** SHALL keep only the newly loaded profile

### Requirement: Profile is executed after loading
The system SHALL execute the loaded profile script to apply the configuration.

#### Scenario: Loaded profile is executed
- **WHEN** the profile file has been loaded into `bpy.data.texts`
- **THEN** the system SHALL execute the script text
- **AND** SHALL apply the profile configuration to the omoospace instance

### Requirement: Profile loading errors are handled gracefully
The system SHALL handle profile loading errors without preventing file usage.

#### Scenario: Missing profile file is handled gracefully
- **WHEN** `omoospace.profile_file` points to a non-existent file
- **THEN** the system SHALL catch the error
- **AND** SHALL log the error
- **AND** SHALL allow the file to be opened normally

#### Scenario: Corrupt profile file causes error
- **WHEN** the profile file contains invalid Python syntax
- **THEN** the system SHALL catch the syntax error
- **AND** SHALL log the error with details
- **AND** SHALL allow the file to be used

### Requirement: Profile is updated on save when location changes
After a save operation, the system SHALL check if the file's omoospace association has changed and update the loaded profile accordingly.

#### Scenario: File saved to new omoospace loads new profile
- **WHEN** user saves the file to a different omoospace
- **THEN** the system SHALL remove the old profile scripts
- **AND** SHALL load the new omoospace's profile
- **AND** SHALL execute it to apply the new configuration

#### Scenario: File saved outside omoospace removes profile
- **WHEN** user saves the file to a location that is not part of any omoospace
- **THEN** `get_omoospace()` SHALL return `None`
- **AND** the system SHALL remove all loaded profile scripts