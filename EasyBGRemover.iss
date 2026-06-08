[Setup]
AppName=Easy Background Remover
AppVersion=1.0
AppPublisher=Easy Background Remover
DefaultDirName={localappdata}\EasyBGRemover
DisableDirPage=yes
DisableProgramGroupPage=yes
DefaultGroupName=Easy Background Remover
OutputDir=.
OutputBaseFilename=EasyBGRemover_Setup
SetupIconFile=app.ico
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\EasyBGRemover\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{userdesktop}\Easy Background Remover"; Filename: "{app}\EasyBGRemover.exe"
Name: "{group}\Easy Background Remover"; Filename: "{app}\EasyBGRemover.exe"
Name: "{group}\Uninstall Easy Background Remover"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\EasyBGRemover.exe"; Description: "Launch Easy Background Remover"; Flags: nowait postinstall skipifsilent

[Code]
var
  SetupDone: Boolean;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone then
    SetupDone := True;
end;

procedure DeinitializeSetup();
var
  ResultCode: Integer;
begin
  // After a completed install, self-delete the installer so the user isn't
  // left with a confusing extra file - only the app shortcut remains.
  if SetupDone then
    Exec(ExpandConstant('{cmd}'),
      '/C ping 127.0.0.1 -n 4 > nul & del /f /q "' + ExpandConstant('{srcexe}') + '"',
      '', SW_HIDE, ewNoWait, ResultCode);
end;
