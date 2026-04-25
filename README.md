# HackAZ-2026

## Getting Started
1. If you are using Windows, install wsl by opening PowerShell as administrator and typing this command: "wsl --install" and then restart your computer
2. Download and install Docker Desktop: https://www.docker.com/products/docker-desktop/ **Make sure to run the Docker Desktop installer as administrator
3. Clone this repo (Do this inside WSL if on Windows)
4. Within the repo, make a directory named "data"
5. In VSCode, install the following extensions: "Dev Containers", "Container Tools", "FastAPI Extension". If you are on Windows, also install the "WSL" extension.
6. Run the Docker Desktop application and keep it open
7. To run the dev server, navigate to the project directory (do this in WSL if on Windows) and run the command "docker compose up". Now open your browser and go to "http://127.0.0.1:8000". You can also add "/docs" to the end of that URL to find extra resources. When you want to stop the dev server, do ctrl+c and then "docker compose down". 

### After initial setup, just refer to steps #6 and #7. If on Windows, when opening VSCode, on the bottom left corner, click "Connect to WSL". Then you can do File → Open Folder and navigate to where you cloned the repo inside WSL. 
