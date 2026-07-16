$container = "flask-monitor"

$status = docker inspect -f "{{.State.Running}}" $container 2>$null

if ($status -ne "true") {
    Write-Host "Container stopped. Restarting..."
    docker restart $container
} else {
    Write-Host "Container is running."
}