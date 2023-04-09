# checks if the script is running in elevated environment, else create elevated environment to run this script
If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # Relaunch as an elevated process:
    Start-Process powershell.exe "-File", ('"{0}"' -f $MyInvocation.MyCommand.Path) -Verb RunAs 
    exit
}

# checks if the folder is already present, else create a new folder named HungerBox
$scheduleObject = New-Object -ComObject schedule.service
$scheduleObject.connect()
try {
    $scheduleObject.GetFolder("\HungerBox")
}
catch {
    $scheduleObject.CreateFolder("\HungerBox")
}

# checks and deletes the task if already present
if (get-scheduledtask | Where-Object { $_.TaskPath -eq "\HungerBox\" -and $_.TaskName -eq "Bot" }) {
    Unregister-ScheduledTask -TaskName "Bot" -TaskPath "\HungerBox\" -Confirm:$false
}

# sets the action
$STAction = New-ScheduledTaskAction -Execute .\src\bot.bat -WorkingDirectory $PSScriptRoot

# sets the trigger
[string[]]$Day = 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'
$STTrigger = New-ScheduledTaskTrigger -Weekly -WeeksInterval 1 -At 06:05PM -DaysOfWeek $Day

# sets the setting
$STSettings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -RestartInterval (New-TimeSpan -Minutes 10) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -RestartCount 3 -StartWhenAvailable `
    -Compatibility Win8 -DontStopOnIdleEnd

# sets the principal
$STPrincipal = New-ScheduledTaskPrincipal -RunLevel Highest -UserId ($env:UserDomain + '\' + $env:UserName)

# registers the tasks
Register-ScheduledTask -TaskName "Bot" -TaskPath "\HungerBox" -Action $STAction -Trigger $STTrigger `
    -Settings $STSettings -Principal $STPrincipal

# self-destructs this file
# Remove-Item -Path $MyInvocation.MyCommand.Source