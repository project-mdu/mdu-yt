; NSIS Script for Youtube Downloader (Force Install)

; Define constants
!define APPNAME "Youtube Downloader"
!define APPVERSION "2024.09.25b5"
!define INSTALLDIR "$LOCALAPPDATA\kaoniewji\mduyoutube"

; Include necessary NSIS headers
!include "MUI2.nsh"

; General settings
Name "${APPNAME}"
OutFile "..\..\build\installer\mduinstall-20240925b5.exe"
InstallDir "${INSTALLDIR}"
RequestExecutionLevel user

; Interface settings
!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_INSTFILES

; Language
!insertmacro MUI_LANGUAGE "English"

; Installation section
Section "Install"
    SetOutPath "$INSTDIR"

    ; Display "Installing, please wait" message
    DetailPrint "Installing, please wait..."

    ; Copy all files from the build directory
    File /r "..\..\build\exe.win-amd64-3.12\*"

    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\mdu.exe"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\mdu.exe"

    ; Run the application after installation
    Exec "$INSTDIR\mdu.exe"

    ; Set auto-close
    SetAutoClose true
SectionEnd

; Uninstaller section (optional, remove if not needed)
Section "Uninstall"
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir /r "$INSTDIR"
    RMDir "$SMPROGRAMS\${APPNAME}"
SectionEnd
