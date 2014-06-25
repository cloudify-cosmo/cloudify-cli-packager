#define AppVersion GetEnv('CFYVERSION')

[Setup]
AppId={{C0E2542D-5940-4EFC-8ADA-82317E9C8C40}
AppName=Cloudify CLI
AppVersion={#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher=GigaSpaces
AppPublisherURL=http://www.gigaspaces.com
AppSupportURL=https://github.com/cloudify-cosmo/cloudify-cli
DefaultDirName={pf}\cfy
DisableProgramGroupPage=yes
OutputBaseFilename=CloudifyCLI-{#AppVersion}
Compression=lzma
SolidCompression=yes
ChangesEnvironment=true
SetupIconFile=icons/CloudifyIcon256.ico

[Tasks]
Name: modifypath; Description: Add application directory to your environmental path; Flags:

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{%CFYDISTPATH}\cfy\cfy.exe"; DestDir: "{app}"; Flags: ignoreversion external
Source: "{%CFYDISTPATH}\cfy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs external

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
