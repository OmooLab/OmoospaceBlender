## ADDED Requirements

### Requirement: Versioned default config selection
The system SHALL select Omoospace default config files from the versioned directories under `src/omoospaceblender/configs`.

#### Scenario: Exact Blender version config exists
- **WHEN** the current Blender version is 4.5
- **AND** `configs/b45` exists
- **THEN** the system SHALL select `configs/b45`

#### Scenario: Exact Blender version config does not exist
- **WHEN** the current Blender version is 4.3
- **AND** `configs/b43` does not exist
- **AND** `configs/b42` exists
- **THEN** the system SHALL select `configs/b42`

#### Scenario: Multiple lower config versions exist
- **WHEN** the current Blender version is 5.1
- **AND** `configs/b42`, `configs/b45`, `configs/b50`, and `configs/b51` exist
- **THEN** the system SHALL select `configs/b51`

#### Scenario: No compatible config exists
- **WHEN** all available config directories are newer than the current Blender version
- **THEN** the system SHALL skip config installation
- **AND** SHALL provide a diagnostic error message

### Requirement: Keymap preset is installed after addon registration
After the addon is registered, the system SHALL install the selected `Omoospace.py` keymap preset into the Blender user keyconfig preset directory.

#### Scenario: Keymap preset is copied to user config
- **WHEN** the addon is registered
- **AND** a compatible `Omoospace.py` file exists
- **THEN** the system SHALL get the user keyconfig preset directory through Blender API
- **AND** SHALL copy `Omoospace.py` into that directory

#### Scenario: User keyconfig directory is cross-platform
- **WHEN** the system needs the keyconfig preset directory
- **THEN** it SHALL use `bpy.utils.user_resource("SCRIPTS", path="presets/keyconfig", create=True)`
- **AND** SHALL NOT hard-code operating system specific Blender config paths

#### Scenario: Existing keymap preset can be updated
- **WHEN** `Omoospace.py` already exists in the user keyconfig preset directory
- **AND** the bundled keymap file content differs
- **THEN** the system SHALL replace the existing file with the bundled file

#### Scenario: Keymap install failure does not block addon registration
- **WHEN** copying the keymap preset fails
- **THEN** the system SHALL catch the error
- **AND** SHALL log a diagnostic message
- **AND** SHALL allow addon registration to continue

### Requirement: Omoospace startup can be installed from File Defaults menu
The system SHALL add a `Use Omoospace Startup` item at the top of Blender `File > Defaults` menu that installs the selected Omoospace startup file as the Blender user startup file.

#### Scenario: Menu item is added on addon register
- **WHEN** the addon is registered
- **THEN** the system SHALL prepend `Use Omoospace Startup` to `File > Defaults`
- **AND** SHALL add a separator below that menu item

#### Scenario: Menu item is removed on addon unregister
- **WHEN** the addon is unregistered
- **THEN** the system SHALL remove the `Use Omoospace Startup` menu item

#### Scenario: Startup file is installed from selected version directory
- **WHEN** the user clicks `Use Omoospace Startup`
- **AND** a compatible `startup.blend` exists in the selected version directory
- **THEN** the system SHALL copy that file to the Blender user config directory as `startup.blend`
- **AND** SHALL NOT open that file as the current Blender scene

#### Scenario: Existing startup file is backed up before replacement
- **WHEN** the user clicks `Use Omoospace Startup`
- **AND** the Blender user config directory already contains `startup.blend`
- **THEN** the system SHALL back it up as `startup.bak.blend`
- **AND** SHALL replace `startup.blend` with the selected Omoospace startup file

#### Scenario: Missing startup source file is reported
- **WHEN** the user clicks `Use Omoospace Startup`
- **AND** no compatible source `startup.blend` exists
- **THEN** the system SHALL report an error
- **AND** SHALL keep Blender usable

### Requirement: Installed default configs are restored on addon unregister
When the addon is unregistered, the system SHALL remove or restore the user configuration files installed by this addon.

#### Scenario: Keymap preset is removed on unregister
- **WHEN** the addon is unregistered
- **AND** the user keyconfig preset directory contains `Omoospace.py`
- **THEN** the system SHALL delete that keymap preset file

#### Scenario: Startup backup is restored on unregister
- **WHEN** the addon is unregistered
- **AND** the Blender user config directory contains `startup.bak.blend`
- **THEN** the system SHALL restore `startup.bak.blend` to `startup.blend`

#### Scenario: Restore failure does not block unregister
- **WHEN** removing keymap or restoring startup fails
- **THEN** the system SHALL catch the error
- **AND** SHALL log a diagnostic message
- **AND** SHALL allow addon unregister to continue
