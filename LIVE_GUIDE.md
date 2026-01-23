# Zepix Trading Bot - Live Deployment Guide

## Prerequisites
1. **Windows Server/PC**: Required for MetaTrader 5 (MT5).
2. **MetaTrader 5 Terminal**: Installed and logged in to your broker account.
3. **Python 3.10+**: Installed on the machine.

## Step 1: Environment Setup
1. Clone the repository to your Windows machine.
2. Open PowerShell or Command Prompt in the `Trading_Bot` folder.
3. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Step 2: Configuration
1. Rename `.env.example` to `.env` (or create a new one).
2. Edit `.env` with your actual credentials:
   ```ini
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   MT5_LOGIN=your_mt5_account_number
   MT5_PASSWORD=your_mt5_password
   MT5_SERVER=YourBroker-Server
   ```
3. Verify `config/config.json` for risk settings (optional).

## Step 3: Launch
1. Ensure MT5 terminal is running and "Algo Trading" is enabled in the toolbar.
2. Run the bot:
   ```powershell
   python src/main.py
   ```
3. You should see `✅ MT5 Connection Successful` and `✅ BOT STARTUP COMPLETE` in the console.

## Step 4: Verification
1. Send `/status` to the bot on Telegram.
2. It should reply with system status.
3. Use `/v6_status` to check V6 engine status.

## Troubleshooting
- **MT5 Connection Failed**: Check if `MT5_SERVER` matches EXACTLY what is shown in MT5 login window. Ensure "Algo Trading" is on.
- **Audio Error**: If `pyttsx3` fails, install `pywin32`: `pip install pywin32`.
