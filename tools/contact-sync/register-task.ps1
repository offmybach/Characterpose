# register-task.ps1 — install the daily/on-logon scheduled task.
# Run once, in a normal (non-admin) PowerShell window:
#     powershell -ExecutionPolicy Bypass -File .\register-task.ps1
#
# This registers two triggers: at logon, and daily at 9:00 AM. To also run the
# moment you unlock after waking the PC, add an "On workstation unlock" trigger
# by hand in Task Scheduler (see README) — that trigger has no clean PowerShell
# equivalent, so the GUI is the reliable way to add it.

$here   = $PSScriptRoot
$script = Join-Path $here "run-sync.ps1"
$name   = "CGB Contact Sync"

$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$script`""

$triggers = @(
    (New-ScheduledTaskTrigger -AtLogOn),
    (New-ScheduledTaskTrigger -Daily -At 9:00AM)
)

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask -TaskName $name -Action $action -Trigger $triggers `
    -Settings $settings -Description "Append new LinkedIn connections to the CGB contacts workbook." -Force

Write-Host "Registered '$name'. Run it now to test with:  Start-ScheduledTask -TaskName '$name'"
