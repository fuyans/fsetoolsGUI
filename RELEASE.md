# Release

This file documents the release history of `fseutil`.

- B1 Means of Escape
    - 0101 Approved Document B Vol. 2 (2019) Data Sheet 1
    - 0102 BS 9999:2017 Data Sheet 1
    - 0111 Heat Detecting Element Activation time
    
- B3 Internal Fire Spread (Lining)
    - 03## Heat Transfer 1D
    
- B4 External Fire Spread
    - 0401 BR 187 Parallel
    - 0402 BR 187 Perpendicular
    - 0403 BR 187 Parallel Complex
    - 0404 BR 187 Perpendicular Complex
    - 0405 Thermal Heat Transfer 3D
    
- Miscellaneous
    - 0601 OFR Naming Convention
    - 0602 Flame Height

## Version history

### XX/XX/2020 VERSION: 0.0.1.dev20200214

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
