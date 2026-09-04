; Inno Setup script for the ActVib Windows installer.
; Compiled by installer/build_windows.ps1 (or manually with ISCC.exe), which
; defines AppVersion, SourceDir and OutputDir on the command line, e.g.:
;
;   ISCC.exe /DAppVersion=0.9.1 /DSourceDir=..\dist\ActVib /DOutputDir=..\dist ActVib.iss
;
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
#ifndef SourceDir
  #define SourceDir "..\dist\ActVib"
#endif
#ifndef OutputDir
  #define OutputDir "..\dist"
#endif

; Stable AppId: do not change between releases, or upgrades will install
; side-by-side instead of replacing the previous version.
#define AppId "{{6C1E9F0A-6E9C-4C3F-9F1B-1E7C6E3F5B10}"

[Setup]
AppId={#AppId}
AppName=ActVib
AppVersion={#AppVersion}
AppVerName=ActVib {#AppVersion}
AppPublisher=Eduardo Batista
AppPublisherURL=https://github.com/eduardobatista/ActVibSoftware
AppSupportURL=https://github.com/eduardobatista/ActVibSoftware/issues
AppUpdatesURL=https://github.com/eduardobatista/ActVibSoftware/releases
VersionInfoVersion={#AppVersion}
DefaultDirName={autopf}\ActVib
DefaultGroupName=ActVib
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#OutputDir}
OutputBaseFilename=ActVib-{#AppVersion}-windows-x64-setup
SetupIconFile={#SourceDir}\ActVib\assets\actvib.ico
UninstallDisplayIcon={app}\ActVib.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile={#SourceDir}\LICENSE
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ActVib"; Filename: "{app}\ActVib.exe"
Name: "{group}\{cm:UninstallProgram,ActVib}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ActVib"; Filename: "{app}\ActVib.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ActVib.exe"; Description: "{cm:LaunchProgram,ActVib}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove any stray onedir contents PyInstaller may have left behind on
; upgrade/uninstall, without touching per-user settings (stored via
; QSettings under HKCU / the user profile, not under {app}).
Type: filesandordirs; Name: "{app}"
