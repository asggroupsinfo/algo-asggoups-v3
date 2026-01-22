# TASK 005: ZERO-TYPING BUTTON FLOW SYSTEM

**Task ID:** JULES-TASK-005  
**Created:** 2026-01-22 18:50:00 IST  
**Priority:** 🔴 CRITICAL  
**Assigned To:** Jules AI  
**Status:** 🟡 PENDING  
**Estimated Time:** 5-7 hours  
**Complexity:** VERY HIGH (UX/State)

---

## 🎯 OBJECTIVE

Implement a complete **Zero-Typing Interaction System**. Users should NEVER have to type command arguments manually. All complex commands (`/buy`, `/setlot`, `/config`) must be converted into guided, multi-step button flows.

---

## 📋 SOURCE DOCUMENT

**Planning Document Location:**
```
ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/04_ZERO_TYPING_BUTTON_FLOW.md
```

**Document Size:** 981 lines | 36 KB  
**Version:** V5.0  
**Design Principle:** CLICK FIRST, TYPE NEVER

---

## 🏗️ IMPLEMENTATION REQUIREMENTS

### **1. Core System (`src/telegram/core/`)**

#### **A. Conversation State Manager (`conversation_state_manager.py`)**
- **Purpose:** Track where a user is in a multi-step flow.
- **Storage:** Per-user state dictionary.
- **Methods:**
  - `start_flow(chat_id, command)`
  - `update_step(chat_id, step, data)`
  - `get_data(chat_id)`
  - `clear_state(chat_id)`

#### **B. Navigation Engine (`navigation_manager.py`)**
- **Breadcrumbs:** Generate `🏠 > 📊 > 💰` path string.
- **Back Button Logic:** Handle dynamic "Back" routing based on flow history.

#### **C. Callback Data Registry (`callback_registry.py`)**
- Central file defining ALL callback strings.
- Format: `{category}_{action}_{target}_{value}`.
- Parser function to decode callbacks.

---

### **2. Flow Implementations (`src/telegram/flows/`)**

Create a new directory `flows/` to handle complex logic steps.

#### **A. Trading Flows (`trading_flow.py`)**
- **Buy/Sell:** Plugin -> Symbol -> Lot -> Confirm.
- **Close:** Plugin -> Symbol -> Application (Partial/Full) -> Confirm.

#### **B. Risk Flows (`risk_flow.py`)**
- **Set Lot:** Plugin -> Strategy/TF -> Lot Size -> Confirm.
- **Set SL/TP:** Plugin -> Strategy -> Pips -> Confirm.

#### **C. Analytics Flows (`analytics_flow.py`)**
- **Report:** Plugin -> Period (Daily/Weekly) -> View.

---

### **3. UI Components (`src/telegram/ui/`)**

#### **A. Dynamic Keyboards**
- **Symbol Selector:** Grid of buttons for available pairs.
- **Lot Selector:** Preset buttons (0.01, 0.05, 0.1) + "Custom" button.
- **Toggle Switches:** ON/OFF toggles that auto-update the message.

---

## ✅ ACCEPTANCE CRITERIA

### **Functional Requirements**
- [ ] `/buy` initiates a 4-step button flow.
- [ ] Breadcrumbs update at every step.
- [ ] "Back" button works correctly at every deep level.
- [ ] Selecting a value (e.g., "0.05") moves to the next step automatically.
- [ ] Final "Confirm" button executes the actual order.
- [ ] No manual typing required for any standard operation.

### **Code Quality**
- [ ] Modular "Flow" classes (don't stuff everything in one file).
- [ ] Centralized callback parsing.
- [ ] Robust error handling (e.g., if state expires).

---

## 📝 DELIVERABLES

1. **Code Files:**
   - `src/telegram/core/conversation_state_manager.py` (Enhanced)
   - `src/telegram/core/callback_registry.py`
   - `src/telegram/flows/base_flow.py`
   - `src/telegram/flows/trading_flow.py`
   - `src/telegram/flows/risk_flow.py`
   - `src/telegram/ui/dynamic_keyboards.py`

2. **Updates:**
   - `controller_bot.py` (Route callbacks to Flow Manager)
   - `callback_router.py` (Enhanced parsing)

3. **Documentation:**
   - `ZERO_TYPING_FLOW_NOTES.md`

3. **Git Push:**
   - Push to `main` branch.

---

## 🚨 CRITICAL INSTRUCTIONS

1. **State Persistence:** If the bot restarts, active flows can be reset, but inform the user.
2. **Timeout:** Auto-clear state after 5 minutes of inactivity.
3. **Escaping:** "Main Menu" button must ALWAYS clear state and return home.

---

**STATUS: 🟡 AWAITING START**
