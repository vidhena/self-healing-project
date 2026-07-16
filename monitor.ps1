$ContainerName = "flask-monitor"

$LogFolder = ".\logs"
$LogFile = "$LogFolder\incidents.log"

if (!(Test-Path $LogFolder)) {
    New-Item -ItemType Directory -Path $LogFolder | Out-Null
}

$status = docker inspect -f "{{.State.Running}}" $ContainerName

if ($status -eq "true") {

    $message = "$(Get-Date) - Container is RUNNING"
    Write-Host $message
    Add-Content -Path $LogFile -Value $message

}
else {

    $message = "$(Get-Date) - Container stopped. Restarting..."
    Write-Host $message
    Add-Content -Path $LogFile -Value $message

    docker restart $ContainerName

    $message = "$(Get-Date) - Container restarted successfully."
    Write-Host $message
    Add-Content -Path $LogFile -Value $message

}