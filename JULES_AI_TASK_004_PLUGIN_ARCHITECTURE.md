# TASK 004: PLUGIN LAYER ARCHITECTURE IMPLEMENTATION

**Task ID:** JULES-TASK-004  
**Created:** 2026-01-22 18:30:00 IST  
**Priority:** 🔴 CRITICAL  
**Assigned To:** Jules AI  
**Status:** 🟡 PENDING  
**Estimated Time:** 4-6 hours  
**Complexity:** HIGH (Architecture)

---

## 🎯 OBJECTIVE

Implement the **Plugin Layer Architecture** that acts as a middleware between user commands and bot logic. This layer ensures that every command knows *which plugin* (V3, V6, or Both) it applies to.

---

## 📋 SOURCE DOCUMENT

**Planning Document Location:**
```
ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/03_PLUGIN_LAYER_ARCHITECTURE.md
```

**Document Size:** 527 lines | 19.3 KB  
**Version:** V5.0  
**Design Principle:** CONTEXT AWARE COMMANDS

---

## 🏗️ IMPLEMENTATION REQUIREMENTS

### **1. Core Components (Must Implement)**

#### **A. Plugin Context Manager (`plugin_context_manager.py`)**
- **Purpose:** Store user's plugin selection temporarily.
- **Expiry:** 5 minutes (300 seconds).
- **Storage:** Dictionary `{chat_id: {'plugin': 'v3', 'timestamp': ...}}`.
- **Methods:** `set_context`, `get_context`, `clear_context`.

#### **B. Command Interceptor (`command_interceptor.py`)**
- **Purpose:** Check every command before execution.
- **Logic:**
  - If command is in `V3_AUTO_CONTEXT` → Set context to 'v3', proceed.
  - If command is in `V6_AUTO_CONTEXT` → Set context to 'v6', proceed.
  - If command is in `PLUGIN_AWARE_COMMANDS`:
    - Check if context exists.
    - If YES → Proceed.
    - If NO → **STOP and show Selection Menu**.

#### **C. Plugin Selection Menu (`plugin_selection_menu.py`)**
- **UI:** 
  ```
  [🔵 V3 Only] [🟢 V6 Only]
  [🔷 Both Plugins]
  [❌ Cancel]
  ```
- **Callbacks:** `plugin_select_v3`, `plugin_select_v6`, `plugin_select_both`.

#### **D. Callback Router Integration (`callback_router.py`)**
- **Logic:**
  - Intercept `plugin_select_*` callbacks.
  - Set context in manager.
  - **Re-execute** the original command that triggered the selection.

---

### **2. Integration Plan**

**Step A:** Modify `ControllerBot.py`
- Initialize `PluginContextManager`.
- Initialize `CommandInterceptor`.
- Update `handle_command` loops to use interceptor.

**Step B:** Update Command Handlers
- Ensure all 83 plugin-aware commands (Trading, Risk, Analytics) accept `plugin_context` argument.
- Pass context to backend logic (e.g., `trading_engine.get_positions(plugin='v3')`).

---

## ✅ ACCEPTANCE CRITERIA

### **Functional Requirements**
- [ ] `/positions` triggers selection menu if no context.
- [ ] Selecting "V3" for `/positions` shows only V3 postions.
- [ ] `/v3_config` automatically skips selection (Auto-Context).
- [ ] Context expires after 5 minutes.
- [ ] "Both" option works for aggregation commands.

### **Code Quality**
- [ ] No hardcoded lists spread across files (centralize in Interceptor).
- [ ] Clean separation between UI (Menu) and State (Context).

---

## 📝 DELIVERABLES

1. **Code Files:**
   - `src/telegram/interceptors/plugin_context_manager.py`
   - `src/telegram/interceptors/command_interceptor.py`
   - `src/telegram/menus/plugin_selection_menu.py`
   - Updated `callback_router.py`
   - Updated `controller_bot.py`

2. **Documentation:**
   - `PLUGIN_ARCH_NOTES.md`

3. **Git Push:**
   - Push to `main` branch.

---

## 🚨 CRITICAL INSTRUCTIONS

1. **Do NOT break existing flows.** If interception fails, fallback to default behavior.
2. **Persistence:** Context is per-user (chat_id), NOT global.
3. **Re-routing:** When user selects a plugin, the bot MUST automatically execute the original command. Don't make them click twice.

---

**STATUS: 🟡 AWAITING START**
