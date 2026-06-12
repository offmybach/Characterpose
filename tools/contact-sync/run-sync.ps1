# run-sync.ps1 — the daily/on-wake launcher the scheduled task calls.
#
# Default mode (safe): if a LinkedIn "Connections.csv" export is sitting in
# Downloads, append any new people from it to the workbook, then move the export
# aside so it isn't reprocessed. No browser, no LinkedIn automation, no risk.
#
# OpenClaw mode (optional): uncomment the block at the bottom to have OpenClaw
# gather new connections from the browser into _new_connections.json first.

$ErrorActionPreference = "Stop"
$here      = $PSScriptRoot
$python    = "python"
$workbook  = "$env:USERPROFILE\Downloads\finlit_contacts_categorized_bespoke_groups.xlsx"
$downloads = "$env:USERPROFILE\Downloads"
$log       = Join-Path $here "sync.log"

function Log($msg) { "$(Get-Date -Format s)  $msg" | Tee-Object -FilePath $log -Append }

Log "----- contact sync run -----"

# --- Safe mode: ingest a LinkedIn CSV export if present ---------------------
$csv = Join-Path $downloads "Connections.csv"
if (Test-Path $csv) {
    Log "Found Connections.csv — ingesting."
    & $python (Join-Path $here "sync_contacts.py") --file $workbook --from-csv $csv 2>&1 | Tee-Object -FilePath $log -Append
    $processed = Join-Path $downloads ("Connections.processed-{0}.csv" -f (Get-Date -Format yyyyMMdd-HHmmss))
    Move-Item -Path $csv -Destination $processed -Force
    Log "Moved export to $processed"
}
else {
    Log "No Connections.csv in Downloads — nothing to ingest in safe mode."
}

# --- OpenClaw mode (optional) ----------------------------------------------
# Requires OpenClaw installed and the linkedin-contact-sync skill registered.
# The user must be at the machine to approve the browser attach prompt.
#
# $json = Join-Path $downloads "_new_connections.json"
# Log "Asking OpenClaw to gather new connections..."
# openclaw run linkedin-contact-sync          # adjust to your OpenClaw invocation
# if (Test-Path $json) {
#     & $python (Join-Path $here "sync_contacts.py") --file $workbook --from-json $json 2>&1 | Tee-Object -FilePath $log -Append
#     Remove-Item $json -Force
# }

Log "Done."
