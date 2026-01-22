# 01_PROJECT_UNDERSTANDING.md

## 1. Project Structure Analysis

### **1.1 Directory Structure**
The project is organized into two main directories under `ZepixTradingBot-old-v2-main`:
- **`Trading_Bot`**: The core application logic, written in Python. This is the main focus of the audit.
- **`Web_Application`**: A prototype/planning directory for a web dashboard. It contains a prototype HTML file and planning documents.
- **Documentation**: Extensive documentation is found in `Important_Doc_Trading_Bot`, `Important_Doc_Webapp`, and within `Trading_Bot/docs`.

### **1.2 Programming Languages**
- **Python**: The primary language for the `Trading_Bot` (versions 3.8+ supported, 3.12+ recommended).
- **HTML/CSS/JS**: Used in `Web_Application` for the prototype dashboard.
- **Batch/PowerShell**: Used for deployment and startup scripts (`deploy_vm.ps1`, `START_BOT.bat`).

### **1.3 Technology Stack**
- **Frameworks**:
    - **FastAPI**: Used for the API server (`src/app.py`).
    - **Uvicorn**: ASGI server for running the FastAPI app.
- **Libraries**:
    - **python-telegram-bot**: For Telegram integration.
    - **MetaTrader5**: For connecting to the MT5 trading terminal.
    - **Pandas/Numpy**: For data manipulation and calculations.
    - **SQLAlchemy/SQLite**: implied for database interactions (built-in `sqlite3` mentioned in requirements).
    - **Pydantic**: For data validation.
    - **pyttsx3**: For voice alerts.
- **External Integrations**:
    - **MetaTrader 5 (MT5)**: The trading platform.
    - **Telegram**: For user interaction, notifications, and commands.
    - **TradingView**: Via webhook integration.

### **1.4 Entry Points**
- **Standalone Script**: `Trading_Bot/src/main.py` - Runs the bot as a standalone process.
- **API Server**: `Trading_Bot/src/app.py` - Runs the bot as a FastAPI application with endpoints.
- **Startup Script**: `Trading_Bot/run_bot.py` (referenced in README, not yet verified in file list, likely calls one of the above).

## 2. Architecture Understanding

### **2.1 Overall Architecture**
The system follows a modular architecture with a clear separation of concerns:
- **Core Engine**: `TradingEngine` coordinates all activities.
- **Managers**: Handle specific business logic (Risk, Session, Dual Order, Profit Booking).
- **Clients**: Abstract external communications (MT5, Telegram).
- **Services**: Background tasks (Price Monitor, Analytics).
- **Processors**: Handle data processing (Alerts).
- **Database**: SQLite database for persistence.

### **2.2 Data Flow**
1.  **Market Data**: Fetched from MT5 via `MT5Client` or received via Webhooks from TradingView.
2.  **Signal Processing**: `TradingEngine` or Plugins process the data/signals.
3.  **Risk Check**: `RiskManager` validates trades against rules.
4.  **Execution**: Valid trades are sent to `MT5Client` for execution.
5.  **Notification**: `AlertProcessor` and `MultiBotManager` send updates to Telegram.
6.  **Persistence**: Trade data and state are saved to `TradeDatabase`.

### **2.3 API Endpoints**
Defined in `src/app.py`:
- `GET /`: API Info.
- `GET /health`: Health check for MT5, Trading Engine, and Telegram.
- `GET /status`: Detailed status of account, plugins, and bots.
- `POST /webhook`: Endpoint for TradingView alerts.
- `GET /config`: Safe configuration view.

## 3. Documentation Review
- **README.md**: Comprehensive guide covering features, deployment, structure, and configuration.
- **Features**:
    - Dual Order System (Order A: TP Trail, Order B: Profit Trail).
    - Profit Booking Chains (Pyramid system).
    - Re-entry Systems (SL Hunt, TP Continuation, Exit Continuation).
    - Risk Management (Daily/Lifetime caps, Tier-based lot sizing).
    - Telegram Integration (60 commands).
    - Forex Session System.
    - Voice Alerts.

## 4. Conclusion
The `Zepix Trading Bot` is a mature, feature-rich automated trading system. It is designed for production use with extensive error handling, logging, and recovery mechanisms. The architecture is sound, leveraging modern Python practices (asyncio, FastAPI). The `Web_Application` is currently in the planning stage.
