[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{C0E2542D-5940-4EFC-8ADA-82317E9C8C40}
AppName=Cloudify CLI
AppVersion={%CFYVERSION|0.1}
AppPublisher=GigaSpaces
AppPublisherURL={%GSURL}
AppSupportURL={%CFYURL}
DefaultDirName={pf}\cfy
DisableProgramGroupPage=yes
OutputBaseFilename=CloudifyCLI-{%CFYVERSION|0.1}
Compression=lzma
SolidCompression=yes
ChangesEnvironment=true
SourceDir={%CFYDISTDIR}

[Tasks]
Name: modifypath; Description: Add application directory to your environmental path; Flags:

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "cfy.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Code]
const
    ModPathName = 'modifypath';
    ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
    setArrayLength(Result, 1)
    Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"
