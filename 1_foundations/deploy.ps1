# Deploy to Hugging Face Spaces without interactive token prompt
# Add your token to .env as HF_TOKEN, or set it here (don't commit!)
$token = $env:HF_TOKEN
if (-not $token) {
    # Load from .env if present
    $envPath = Join-Path $PSScriptRoot "..\.env"
    if (Test-Path $envPath) {
        Get-Content $envPath | ForEach-Object {
            if ($_ -match '^\s*HF_TOKEN=(.+)$') { $token = $matches[1].Trim() }
        }
    }
}
if ($token) {
    $env:HF_TOKEN = $token
}
uv run gradio deploy
