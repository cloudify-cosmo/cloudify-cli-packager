#define AppVersion GetEnv('CFYVERSION')

[Setup]
AppId={{C0E2542D-5940-4EFC-8ADA-82317E9C8C40}
AppName=Cloudify CLI
AppVersion={#AppVersion}
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
Source: "C:\Cygwin\home\Administrator\cloudify-cli-packager\pyinstaller\dist\cfy\cfy.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Cygwin\home\Administrator\cloudify-cli-packager\pyinstaller\dist\cfy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

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
