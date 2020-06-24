# Release

This file documents the release history of `fsetools`.

- B1 Means of Escape
    - 0101 ADB vol. 2 data sheet no. 1 - means of escape
    - 0102 BS 9999 data sheet no. 1 - means of escape
    - 0103 BS 9999 merging flow at final exit level
    - 0104 ADB merging flow at final exit level
    - 0111 PD 7974 heat detector device activation time calculator
    
- B4 External Fire Spread
    - 0401 BR 187 BR 187 parallel oriented rectangle emitter and receiver
    - 0402 BR 187 perpendicular oriented rectangle emitter and receiver
    - 0403 BR 187 parallel oriented rectangle emitter and eccentric receiver
    - 0404 BR 187 perpendicular oriented rectangle emitter and eccentric receiver
    - 0405 TRA 3D polygon emitter and a single point
    - 0406 TRA 2D parallel orientated contour plot
    - 0407 TRA cuboid enclosure model
    
- Miscellaneous
    - 0601 OFR file name generator
    - 0602 PD 7974 flame height calculator
    - 0611 EC 1991-1-2 parametric fire generator

## Version history

### XX/05/2020 VERSION: 0.0.4

New features.
- [x] 0103 BS 9999 merging flow at final exit level.
- [x] 0104 ADB merging flow at final exit level.
- [x] 0407 TRA cuboid enclosure model.
- [x] 0611 EC 1991-1-2 parametric fire generator.

Fixes.
- [x] Fixed an issue where the update download url label no responses when clicked.

Improvements.
- [x] 0401, 0402, 0403 & 0404: Added critical heat flux input parameter.
- [x] Installer: Interface optimisation.

### 14/02/2020 VERSION: 0.0.1.dev20200214

Initial version. The following features/modules are implemented.

- [x] 0101 ADB data sheet.
- [x] 0102 BS 9999 data sheet.
- [x] 0111 PD 7974 heat detector activation time.
- [x] 0401 BR 187 parallel simple.
- [x] 0402 BR 187 perpendicular simple.
- [x] 0403 BR 187 parallel complex.
- [x] 0404 BR 187 perpendicular complex.
- [x] 0405 general thermal radiation analysis.
    - [x] Calculation checked.
- [x] 0601 OFR naming.
- [x] 0602 PD 7974 flame height.
    - [x] Calculation checked.
- [x] 0111 implemented display numerical results in table.
- [x] 0111 implemented graphical output.
- [x] Converted all independent modules into QMainWindow objects, i.e. to have a status bar.
- [x] Installer for MS Windows.
- [x] All output files set to readonly.
- [x] Shortcut for all module GUI windows press ESC to close.
- [x] Implemented error handling.
- [x] Implemented check GUI tip texts.

## Checklist before release

- [ ] Update version number in `fsetoolsGUI`.
- [ ] Build `fsetoolsGUI` executable.
- [ ] Install and test the program.
- [ ] Get a public accessible url of the new executable and update version info in `.json` file.
- [ ] GitHub commit Changes and pull to master.
