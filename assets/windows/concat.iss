; RB Videofire's Windows installer.
;
; Built by build-app.yml with Inno Setup from the staged folder the .msi
; is also made of, so the two ship the same files; this is the one a
; person double-clicks, and it puts RB Videofire in the Start menu and can take
; it out again. Everything it needs is handed in on the command line:
;
;   iscc /DVersion=0.2.8 /DArch=x64compatible /DSuffix=x86_64 ^
;        /DStage=C:\...\stage\RBVideofire-0.2.8-windows-x86_64 /DOut=C:\...\stage ^
;        assets\windows\concat.iss
;
; Arch is Inno's own word for the machine: x64compatible for the x86_64
; build (which also installs on ARM PCs, under emulation), arm64 for the
; native one. Suffix is the bundle's word for it, which names the file.

#ifndef Version
  #error Version is required
#endif
#ifndef Arch
  #error Arch is required: x64compatible or arm64
#endif
#ifndef Suffix
  #error Suffix is required: x86_64 or aarch64
#endif
#ifndef Stage
  #error Stage is required: the staged folder to install
#endif
#ifndef Out
  #define Out "."
#endif

[Setup]
; One id for the life of the product, so an install over an older one is
; an upgrade and not a second copy.
AppId={{CE69D4BC-298A-4BFC-9B47-CB4359033C2B}
AppName=RB Videofire
AppVersion={#Version}
AppVerName=RB Videofire {#Version}
AppPublisher=RB8 Soluções Digitais
AppPublisherURL=https://github.com/nandoribersbr/rbvideofire2026
AppSupportURL=https://github.com/nandoribersbr/rbvideofire2026/issues
AppUpdatesURL=https://github.com/nandoribersbr/rbvideofire2026/releases
DefaultDirName={autopf}\RB Videofire
DefaultGroupName=RB Videofire
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
OutputDir={#Out}
OutputBaseFilename=RBVideofire-{#Version}-windows-{#Suffix}-setup
SetupIconFile=..\icons\rb-videofire.ico
UninstallDisplayIcon={app}\rb-videofire.ico
UninstallDisplayName=RB Videofire
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed={#Arch}
ArchitecturesInstallIn64BitMode={#Arch}
; For the user alone unless they ask for the machine: no prompt for an
; administrator to install a video editor into one's own account.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; Follow Windows' display language when the setup speaks it, and ask only
; when it does not.
ShowLanguageDialog=auto

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#Stage}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\icons\rb-videofire.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\RB Videofire"; Filename: "{app}\RBVideofire.exe"; IconFilename: "{app}\rb-videofire.ico"
; The way in when a graphics driver draws the window as coloured squares:
; it turns off Settings > General > Draw on the GPU, which that window hides.
Name: "{autoprograms}\RB Videofire (modo gráfico seguro)"; Filename: "{app}\RBVideofire.exe"; Parameters: "--software"; IconFilename: "{app}\rb-videofire.ico"
Name: "{autodesktop}\RB Videofire"; Filename: "{app}\RBVideofire.exe"; IconFilename: "{app}\rb-videofire.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\RBVideofire.exe"; Description: "{cm:LaunchProgram,RB Videofire}"; Flags: nowait postinstall skipifsilent
