nsi_script = r"""
;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"


;--------------------------------
;General

  ;Properly display all languages
  Unicode true

    BrandingText "OFR Consultants Ltd"
    
  ;Define name of the product
  !define APPNAME FSETOOLS
  !define COMPANYNAME OFR
  !define VERSIONMAJOR {version_major}
  !define VERSIONMINOR {version_minor}
  !define VERSIONBUILD {version_build}

    
  ;Define optional URL that will be opened after the installation was successful
  !define AFTER_INSTALLATION_URL "https://github.com/AnonymerNiklasistanonym/NsiWindowsInstallerExamples"


  ;Define the main name of the installer
  Name "${{COMPANYNAME}}\${{APPNAME}}"

  ;Define the directory where the installer should be saved
  OutFile "{fn_installer}"


  ;Define the default installation folder (Windows ProgramFiles example)
  InstallDir "$PROGRAMFILES\${{COMPANYNAME}}\${{APPNAME}}"

  ;Define optional a directory for program files that change (Windows AppData example)
  !define INSTDIR_DATA "$APPDATA\${{COMPANYNAME}}\${{APPNAME}}"


  ;Request rights if you want to install the program to program files
  RequestExecutionLevel admin

  ;Properly display all languages
  Unicode true

  ;Show 'console' in installer and uninstaller
  ShowInstDetails "show"
  ShowUninstDetails "show"

  ;Get installation folder from registry if available
  InstallDirRegKey HKLM "Software\${{COMPANYNAME}}\${{APPNAME}}" ""


;--------------------------------
;Interface Settings

  ;Show warning if user wants to abort
  !define MUI_ABORTWARNING

  ;Show all languages, despite user's codepage
  !define MUI_LANGDLL_ALLLANGUAGES

  ;Use optional a custom icon:
  !define MUI_ICON "etc\ofr_logo_1_80_80.ico" # for the Installer
  !define MUI_UNICON "etc\ofr_logo_1_80_80.ico" # for the later created UnInstaller

  ;Use optional a custom picture for the 'Welcome' and 'Finish' page:
  ;!define MUI_HEADERIMAGE_RIGHT
  ;!define MUI_WELCOMEFINISHPAGE_BITMAP "etc\test.png"  # for the Installer
  ;!define MUI_UNWELCOMEFINISHPAGE_BITMAP "etc\test.png"  # for the later created UnInstaller

  ;Optional no descripton for all components
  !define MUI_COMPONENTSPAGE_NODESC


;--------------------------------
;Pages

  ;For the installer
  !insertmacro MUI_PAGE_WELCOME # simply remove this and other pages if you don't want it
  !insertmacro MUI_PAGE_LICENSE "..\LICENSE" # link to an ANSI encoded license file
  !insertmacro MUI_PAGE_COMPONENTS # remove if you don't want to list components
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  ;For the uninstaller
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH


;--------------------------------
;Languages

  ;At start will be searched if the current system language is in this list,
  ;if not the first language in this list will be chosen as language
  !insertmacro MUI_LANGUAGE "English"
  !insertmacro MUI_LANGUAGE "French"
  !insertmacro MUI_LANGUAGE "German"
  !insertmacro MUI_LANGUAGE "Spanish"
  !insertmacro MUI_LANGUAGE "SpanishInternational"
  !insertmacro MUI_LANGUAGE "SimpChinese"
  !insertmacro MUI_LANGUAGE "TradChinese"
  !insertmacro MUI_LANGUAGE "Japanese"
  !insertmacro MUI_LANGUAGE "Korean"
  !insertmacro MUI_LANGUAGE "Italian"
  !insertmacro MUI_LANGUAGE "Dutch"
  !insertmacro MUI_LANGUAGE "Danish"
  !insertmacro MUI_LANGUAGE "Swedish"
  !insertmacro MUI_LANGUAGE "Norwegian"
  !insertmacro MUI_LANGUAGE "NorwegianNynorsk"
  !insertmacro MUI_LANGUAGE "Finnish"
  !insertmacro MUI_LANGUAGE "Greek"
  !insertmacro MUI_LANGUAGE "Russian"
  !insertmacro MUI_LANGUAGE "Portuguese"
  !insertmacro MUI_LANGUAGE "PortugueseBR"
  !insertmacro MUI_LANGUAGE "Polish"
  !insertmacro MUI_LANGUAGE "Ukrainian"
  !insertmacro MUI_LANGUAGE "Czech"
  !insertmacro MUI_LANGUAGE "Slovak"
  !insertmacro MUI_LANGUAGE "Croatian"
  !insertmacro MUI_LANGUAGE "Bulgarian"
  !insertmacro MUI_LANGUAGE "Hungarian"
  !insertmacro MUI_LANGUAGE "Thai"
  !insertmacro MUI_LANGUAGE "Romanian"
  !insertmacro MUI_LANGUAGE "Latvian"
  !insertmacro MUI_LANGUAGE "Macedonian"
  !insertmacro MUI_LANGUAGE "Estonian"
  !insertmacro MUI_LANGUAGE "Turkish"
  !insertmacro MUI_LANGUAGE "Lithuanian"
  !insertmacro MUI_LANGUAGE "Slovenian"
  !insertmacro MUI_LANGUAGE "Serbian"
  !insertmacro MUI_LANGUAGE "SerbianLatin"
  !insertmacro MUI_LANGUAGE "Arabic"
  !insertmacro MUI_LANGUAGE "Farsi"
  !insertmacro MUI_LANGUAGE "Hebrew"
  !insertmacro MUI_LANGUAGE "Indonesian"
  !insertmacro MUI_LANGUAGE "Mongolian"
  !insertmacro MUI_LANGUAGE "Luxembourgish"
  !insertmacro MUI_LANGUAGE "Albanian"
  !insertmacro MUI_LANGUAGE "Breton"
  !insertmacro MUI_LANGUAGE "Belarusian"
  !insertmacro MUI_LANGUAGE "Icelandic"
  !insertmacro MUI_LANGUAGE "Malay"
  !insertmacro MUI_LANGUAGE "Bosnian"
  !insertmacro MUI_LANGUAGE "Kurdish"
  !insertmacro MUI_LANGUAGE "Irish"
  !insertmacro MUI_LANGUAGE "Uzbek"
  !insertmacro MUI_LANGUAGE "Galician"
  !insertmacro MUI_LANGUAGE "Afrikaans"
  !insertmacro MUI_LANGUAGE "Catalan"
  !insertmacro MUI_LANGUAGE "Esperanto"
  !insertmacro MUI_LANGUAGE "Asturian"
  !insertmacro MUI_LANGUAGE "Basque"
  !insertmacro MUI_LANGUAGE "Pashto"
  !insertmacro MUI_LANGUAGE "Georgian"
  !insertmacro MUI_LANGUAGE "Vietnamese"
  !insertmacro MUI_LANGUAGE "Welsh"
  !insertmacro MUI_LANGUAGE "Armenian"
  !insertmacro MUI_LANGUAGE "Corsican"


;--------------------------------
;Installer Section

Section "Main Component"
    SectionIn RO # Just means if in component mode this is locked
    
    ;Set output path to the installation directory.
        SetOutPath $INSTDIR
    
    ;Put the following file in the SetOutPath
        File /r 'dist\FSETOOLS\*'
    
    ;Create uninstaller
        WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ;Store installation folder in registry
        WriteRegStr HKLM "Software\${{COMPANYNAME}}\${{APPNAME}}" "" $INSTDIR

    ;Registry information for add/remove programs
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayName" "${{APPNAME}}"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "UninstallString" "$INSTDIR\uninstall.exe"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "QuietUninstallString" "$INSTDIR\uninstall.exe /S"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "InstallLocation" "$INSTDIR"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayIcon" "$INSTDIR\etc\ofr_logo_1_80_80.ico"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
        WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
        WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    
    ;Start menu
        createDirectory "$SMPROGRAMS\${{COMPANYNAME}}"
        createShortCut "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}.lnk" "$INSTDIR\${{APPNAME}}.exe" "" "$INSTDIR\etc\ofr_logo_1_80_80.ico"
    
    ;Create optional start menu shortcut for uninstaller and Main component
        ;CreateDirectory "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}"
        ;CreateShortCut "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}\Main Component.lnk" "$INSTDIR\example_file_component_01.txt" "" "$INSTDIR\example_file_component_01.txt" 0
        ;CreateShortCut "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}\Uninstall ${{COMPANYNAME}}\${{APPNAME}}.lnk" "$INSTDIR\${{COMPANYNAME}}\${{APPNAME}}_uninstaller.exe" "" "$INSTDIR\${{COMPANYNAME}}\${{APPNAME}}_uninstaller.exe" 0

  

SectionEnd

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;Remove all registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}}\${{APPNAME}}"
  DeleteRegKey HKLM "Software\${{COMPANYNAME}}\${{APPNAME}}"

  ;Delete the installation directory + all files in it
  ;Add 'RMDir /r "$INSTDIR\folder\*.*"' for every folder you have added additionaly
  RMDir /r "$INSTDIR\*.*"
  RMDir "$INSTDIR"

  ;Delete the appdata directory + files
  RMDir /r "${{INSTDIR_DATA}}\*.*"
  RMDir "${{INSTDIR_DATA}}"

  ;Delete Start Menu Shortcuts
  Delete "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}\*.*"
  RmDir  "$SMPROGRAMS\${{COMPANYNAME}}\${{APPNAME}}"

SectionEnd


;--------------------------------
;After Installation Function

Function .onInstSuccess

  ;Open 'Thank you for installing' site or something else
  ;ExecShell "open" "microsoft-edge:${{AFTER_INSTALLATION_URL}}"

FunctionEnd
"""