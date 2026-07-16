$ContainerName = "flask-monitor"

$ProjectPath = "C:\Users\User\self-healing-project"

$LogFolder = "$ProjectPath\logs"
$LogFile = "$LogFolder\incidents.log"

if (!(Test-Path $LogFolder)) {
    New-Item -ItemType Directory -Path $LogFolder | Out-Null
}

if (!(Test-Path $LogFile)) {
    New-Item -ItemType File -Path $LogFile | Out-Null
}

$status = docker inspect -f "{{.State.Status}}" $ContainerName

if ($status -eq "running") {

    $msg = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Container is running."
    Write-Host $msg
    Add-Content $LogFile $msg

}
else {

    $msg = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Container stopped. Restarting..."
    Write-Host $msg
    Add-Content $LogFile $msg

    docker restart $ContainerName

    $msg = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Container restarted successfully."
    Write-Host $msg
    Add-Content $LogFile $msg

}