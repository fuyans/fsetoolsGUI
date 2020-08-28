
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
    !define AFTER_INSTALLATION_URL "https://github.com/fsepy/fsetools"
    
    
    ;Define the main name of the installer
    Name "${{APPNAME}}"
    
    
    ;Define the directory where the installer should be saved
    OutFile "{fn_installer}"
    
    
    ;Define the default installation folder (Windows ProgramFiles example)
    InstallDir "$PROGRAMFILES\${{COMPANYNAME}}\${{APPNAME}}"
    
    
    ;Define optional a directory for program files that change (Windows AppData example)
    ;!define INSTDIR_DATA "$APPDATA\${{COMPANYNAME}}\${{APPNAME}}"
    
    
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
    ;!insertmacro MUI_PAGE_COMPONENTS # remove if you don't want to list components
    !insertmacro MUI_PAGE_INSTFILES
    !define MUI_FINISHPAGE_RUN "$INSTDIR\${{APPNAME}}.exe"
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
    !insertmacro MUI_LANGUAGE "SimpChinese"
    !insertmacro MUI_LANGUAGE "English"

;--------------------------------
!macro UninstallExisting exitcode uninstcommand
    Push `${{uninstcommand}}`
        Call UninstallExisting
    Pop ${{exitcode}}
!macroend

Function UninstallExisting
    Exch $1                             ; uninstcommand
    ;Push $2                             ; Uninstaller
    ;Push $3                             ; Len
    ExecWait "$1 /S _?$INSTDIR"
FunctionEnd


Function .onInit
    ;ReadRegStr $0 HKCU "Software\Software\Microsoft\Windows\CurrentVersion\Uninstall\${{APPNAME}}" "UninstallString"
    ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "UninstallString"
    ${{If}} $0 != ""
    ${{AndIf}} ${{Cmd}} `MessageBox MB_YESNO|MB_ICONQUESTION "$INSTDIR\${{APPNAME}}.exe Uninstall previous version? (Recommended)$\nThis installation will overwrite some of the previous files." /SD IDYES IDYES`
        !insertmacro UninstallExisting $0 $0
        ${{If}} $0 <> 0
            MessageBox MB_YESNO|MB_ICONSTOP "Failed to uninstall, continue anyway?" /SD IDYES IDYES +2
                Abort
        ${{EndIf}}
    ${{EndIf}}
FunctionEnd


;--------------------------------
;Installer Section

Section "Main Component"
    SectionIn RO # Just means if in component mode this is locked
    
    ;Set output path to the installation directory.
        SetOutPath $INSTDIR
    
    ;Put the following file in the SetOutPath
        File /r 'dist\FSETOOLS\*'
    
    ;Create uninstaller
        WriteUninstaller "$INSTDIR\${{APPNAME}}_uninstaller.exe"
    
    ;Store installation folder in registry
        WriteRegStr HKLM "Software\${{COMPANYNAME}}\${{APPNAME}}" "" $INSTDIR

    ;Registry information for add/remove programs
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayName" "${{APPNAME}}"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "UninstallString" "$INSTDIR\${{APPNAME}}_uninstaller.exe"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "QuietUninstallString" "$INSTDIR\${{APPNAME}}_uninstaller.exe /S"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "InstallLocation" "$INSTDIR"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayIcon" "$INSTDIR\etc\ofr_logo_1_80_80.ico"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
        WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
        WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    
    ;Create optional start menu shortcut for uninstaller and Main component
        CreateDirectory "$SMPROGRAMS\${{APPNAME}}"
        CreateShortCut "$SMPROGRAMS\${{APPNAME}}\${{APPNAME}}.lnk" "$INSTDIR\${{APPNAME}}.exe" "" "$INSTDIR\etc\ofr_logo_1_80_80.ico" 0
        CreateShortCut "$SMPROGRAMS\${{APPNAME}}\Uninstall ${{APPNAME}}.lnk" "$INSTDIR\${{APPNAME}}_uninstaller.exe" "" "$INSTDIR\etc\ofr_logo_1_80_80.ico" 1

SectionEnd

;--------------------------------
;Uninstaller Section

Section "Uninstall"
  
    ;Remove Start Menu launcher
    Delete "$SMPROGRAMS\${{APPNAME}}\${{APPNAME}}.lnk"
    Delete "$SMPROGRAMS\${{APPNAME}}\*.*"
    RmDir  "$SMPROGRAMS\${{APPNAME}}"
    
    ;Try to remove the Start Menu folder - this will only happen if it is empty
    rmDir "$SMPROGRAMS\${{APPNAME}}"
    
    ;Remove the files (using externally generated file list)
    ;!include ${{UNINST_LIST}}
    
    ;Delete the installation directory + all files in it
    ;Add 'RMDir /r "$INSTDIR\folder\*.*"' for every folder you have added additionaly
    RMDir /r "$INSTDIR\*.*"
    RMDir "$INSTDIR"
    
    ;Delete the appdata directory + files
    ;RMDir /r "${{INSTDIR_DATA}}\*.*"
    ;RMDir "${{INSTDIR_DATA}}"
    
    ;Always delete uninstaller as the last action
    Delete $INSTDIR\uninstall.exe
    
    ;Try to remove the install directory - this will only happen if it is empty
    rmDir /r $INSTDIR
 
    ;Remove uninstaller information from the registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${{COMPANYNAME}} ${{APPNAME}}"
    DeleteRegKey HKLM "Software\${{COMPANYNAME}}\${{APPNAME}}"

SectionEnd


;--------------------------------
;After Installation Function

Function .onInstSuccess

    ;Open 'Thank you for installing' site or something else
    ;ExecShell "open" "microsoft-edge:${{AFTER_INSTALLATION_URL}}"
    ;ExecShell "" "$SMPROGRAMS\${{APPNAME}}\${{APPNAME}}.lnk"

FunctionEnd
"""
