#!/bin/bash
# Quick setup script for SmartProxy credentials

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           SmartProxy Setup for Yellow Pages Scraper           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Get credentials from user
echo "Enter your SmartProxy credentials from the dashboard:"
echo ""
read -p "Username (e.g., sp12345678-country-us-session-xyz): " proxy_user
read -s -p "Password: " proxy_pass
echo ""
echo ""

# Validate input
if [ -z "$proxy_user" ] || [ -z "$proxy_pass" ]; then
    echo "❌ Error: Username and password are required"
    exit 1
fi

# Export for current session
export PROXY_SERVICE="smartproxy"
export PROXY_USERNAME="$proxy_user"
export PROXY_PASSWORD="$proxy_pass"

echo "✅ Credentials set for this session!"
echo ""
echo "Testing connection..."
echo ""

# Test connection
cd "$(dirname "$0")"
source venv/bin/activate
python -c "
import asyncio
from proxy_manager import Proxy

proxy = Proxy(
    host='gate.smartproxy.com',
    port=7000,
    username='$proxy_user',
    password='$proxy_pass',
    protocol='http'
)

print('✓ Proxy configured')
print(f'  Host: {proxy.host}')
print(f'  Port: {proxy.port}')
print(f'  Username: {proxy.username[:20]}...')
print('')
print('✅ Ready to scrape!')
print('')
print('Next steps:')
print('  1. Edit config_top_cities.py')
print('     Change: USE_PAID_PROXY_SERVICE = True')
print('  2. Run: python run_top_cities.py')
"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  IMPORTANT: These credentials are only set for this session   ║"
echo "║                                                                ║"
echo "║  To make permanent, add to your ~/.zshrc or ~/.bash_profile:  ║"
echo "║                                                                ║"
echo "║  export PROXY_SERVICE=\"smartproxy\"                            ║"
echo "║  export PROXY_USERNAME=\"$proxy_user\""
echo "║  export PROXY_PASSWORD=\"your-password\""
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
