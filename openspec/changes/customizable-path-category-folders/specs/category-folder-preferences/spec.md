## ADDED Requirements

### Requirement: Category folder names are user-configurable
The system SHALL allow users to configure custom folder names for each path category (images, videos, volumes, dynamics, libraries, misc, renders, audios, geo-nodes) via addon preferences.

#### Scenario: User sets custom folder name for images
- **WHEN** user opens addon preferences and sets "images" category folder name to "textures"
- **THEN** all new image paths collected by `collect_input_paths()` shall use "textures" as the category folder name

#### Scenario: User sets custom folder name for videos
- **WHEN** user opens addon preferences and sets "videos" category folder name to "footage"
- **THEN** all new video paths collected by `collect_input_paths()` shall use "footage" as the category folder name

#### Scenario: Preferences use sensible defaults
- **WHEN** user has not customized any category folder names
- **THEN** the system SHALL use the standard hardcoded folder names (images, videos, volumes, etc.) as defaults

#### Scenario: Empty folder name is rejected
- **WHEN** user attempts to save an empty category folder name
- **THEN** the system SHALL display a validation warning and not save the empty value

### Requirement: Category folder preferences affect path collection
The `collect_input_paths()` and `collect_output_paths()` functions SHALL read category folder names from user preferences instead of using hardcoded default values.

#### Scenario: Input path collection uses custom folder names
- **WHEN** `collect_input_paths()` is called
- **THEN** it SHALL look up the category folder name from preferences for each path type
- **AND** use the custom name (or default if not set) when building the path

#### Scenario: Output path collection uses custom folder names
- **WHEN** `collect_output_paths()` is called
- **THEN** it SHALL look up the category folder name from preferences for each path type
- **AND** use the custom name (or default if not set) when building the path