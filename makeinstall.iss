; Inno Setup Script
[Setup]
AppName=Youtube Downloader
AppVersion=2024.09.23
DefaultDirName={localappdata}\kaoniewji\mduyoutube
DefaultGroupName=Youtube Downloader
OutputDir=.\installer
OutputBaseFilename=YoutubeDownloaderInstaller
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes

[Files]
Source: "build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Youtube Downloader"; Filename: "{app}\ytmdu.exe"
Name: "{userdesktop}\Youtube Downloader"; Filename: "{app}\ytmdu.exe"

[Run]
Filename: "{app}\ytmdu.exe"; Description: "Launch Youtube Downloader"; Flags: nowait postinstall skipifsilent
