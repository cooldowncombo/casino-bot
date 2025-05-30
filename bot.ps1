# bot.ps1
# PowerShell script to activate Python virtual environment and install requirements
# and run a Discord bot script
# Ensure the script is run with administrative privileges
$venvPath = "C:\Users\Admin\Documents\GitHub\casino-games-bot\.venv"
$activateScript = "$venvPath\Scripts\Activate.ps1"
$pythonExe = "$venvPath\Scripts\python.exe"

# Activate the virtual environment
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Error "Virtual environment not found. Please ensure the path is correct."
    exit 1
}

# upgrade pip to the latest version
& $pythonExe -mpip install --upgrade pip

# Install requirements
& $pythonExe -m pip install -r requirements.txt

# run the bot script
& $pythonExe bot.py