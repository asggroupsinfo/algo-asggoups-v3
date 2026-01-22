# TASK 007: THE GRAND ARCHITECTURAL MERGE & UPGRADE

**Task ID:** JULES-TASK-007  
**Created:** 2026-01-22 20:20:00 IST  
**Priority:** 🔴🔴 SUPER CRITICAL  
**Assigned To:** Jules AI  
**Status:** 🟡 PENDING  
**Scope:** COMPLETE MIGRATION (144 Commands + Plugin Architecture + Zero-Typing UI)

---

## 🎯 OBJECTIVE: SINGLE UNIFIED BOT

**Problem:** Currently, we have a "Legacy Bot" (Feature-rich but sync) and an "Async Bot" (Modern but empty).  
**Goal:** Migrate **ALL 144 LEGACY COMMANDS** into the **ASYNC BOT ARCHITECTURE**.  
**Result:** One high-performance, async bot with Plugin Selection, Zero-Typing UI, and Full Feature Set.

---

## 📋 SOURCE DOCUMENTS (STRICT ADHERENCE REQUIRED)

1.  **Execution Plan:** `ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/06_COMPLETE_MERGE_EXECUTION_PLAN.md`
2.  **Migration Analysis:** `ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/COMPLETE_COMMAND_MIGRATION_ANALYSIS.md`
3.  **Upgrade Strategy:** `ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/COMPLETE_MERGE_AND_UPGRADE_STRATEGY.md`

---

## 🏗️ ARCHITECTURE (Must Be Exact)

Implement this **folder structure** inside `src/telegram/`:

```text
src/telegram/
├── core/
│   ├── base_command_handler.py (Base Class)
│   ├── base_menu_builder.py (Base Class)
│   ├── handler_verifier.py
│   └── ... (Managers)
├── plugins/
│   ├── plugin_context_manager.py
│   ├── command_interceptor.py
│   └── plugin_selection_menu.py
├── commands/ (All 144 Handlers)
│   ├── system/ (start, help, status...)
│   ├── trading/ (positions, buy, sell...)
│   ├── risk/ (setlot, setsl...)
│   ├── v3_strategy/
│   ├── v6_timeframes/
│   ├── analytics/
│   ├── reentry/
│   ├── profit/
│   ├── plugin/
│   ├── session/
│   └── voice/
├── menus/ (All Menu Builders)
│   ├── main_menu.py
│   ├── system_menu.py
│   └── ... (for each category)
├── callbacks/ (Callback Routers)
│   └── ...
└── bots/
    └── controller_bot.py (THE MAIN BRAIN - Updated to use new structure)
```

---

## 📅 IMPLEMENTATION PHASES (Execute sequentially)

### **PHASE 1: FOUNDATION (The Core)**
1.  Create `BaseCommandHandler`: Abstract class with `execute(update, context, plugin_context)`.
2.  Create `BaseMenuBuilder`: Abstract class for consistent UI.
3.  Move/Update `PluginContextManager` & `CommandInterceptor` to `src/telegram/plugins/`.
4.  Implement `StickyHeaderBuilder` integration.

### **PHASE 2: CRITICAL MIGRATION (Trading & Risk)**
1.  Implement `commands/trading/` handlers:
    - `/positions`, `/pnl`, `/buy`, `/sell`, `/close`, `/closeall`
    - **MUST USE:** Zero-typing flows logic (from Task 005) inside these handlers.
2.  Implement `commands/risk/` handlers:
    - `/setlot`, `/setsl`, `/settp`, `/risktier`
    - **MUST USE:** Risk Wizards.

### **PHASE 3: CORE LOGIC (V3 & V6)**
1.  Implement `commands/v3_strategy/` handlers.
2.  Implement `commands/v6_timeframes/` handlers.
3.  Ensure **Auto-Context** works (typing `/tf15m` automatically implies V6 context).

### **PHASE 4: INTEGRATION**
1.  Update `ControllerBot`:
    - Clean initialization.
    - Register ALL handlers using `CommandHandler`.
    - Register `CallbackQueryHandler` routers.
2.  Run `HandlerVerifier` on startup to confirm 144 commands are active.

---

## ✅ ACCEPTANCE CRITERIA (0% ERROR TOLERANCE)

- [ ] Folder structure matches the plan EXACTLY.
- [ ] `ControllerBot` imports handlers from `src/telegram/commands/...`.
- [ ] `Legacy` code (sync) is fully converted to `Async/Await`.
- [ ] Plugin Selection Menu appears for ambiguous commands (e.g., `/positions`).
- [ ] "Back" buttons and "Main Menu" buttons work across all interactions.
- [ ] `HandlerVerifier` reports **144/144** commands found.

---

## 📝 DELIVERABLES

1.  **Code Structure:** Full `src/telegram/` folder refactored.
2.  **Handlers:** Individual files for command logic (modular).
3.  **Documentation:** `COMPLETED_MIGRATION_LOG.md`.
4.  **Verification:** Screenshot/Log showing startup success.

---

## 🚨 CRITICAL INSTRUCTIONS

- **DO NOT** delete the old `ControllerBot` reference logic until the new one is 100% verified.
- **DO** verify imports carefully. Circular dependencies are the enemy here.
- **DO** ensure the `StickyHeader` is present in **EVERY** menu response.

**START NOW.** This is the project's most important task.
