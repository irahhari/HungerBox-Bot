# checks if the script is running in elevated environment, else create elevated environment to run this script
If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # Relaunch as an elevated process:
    Start-Process powershell.exe "-File", ('"{0}"' -f $MyInvocation.MyCommand.Path) -Verb RunAs 
    exit
}

# disables the bot
Disable-ScheduledTask -TaskName "Bot" -TaskPath "\HungerBox\"