# TASK 003: V5 STICKY HEADER IMPLEMENTATION

**Task ID:** JULES-TASK-003  
**Created:** 2026-01-22 17:50:00 IST  
**Priority:** 🔴 CRITICAL  
**Assigned To:** Jules AI  
**Status:** 🟡 PENDING  
**Estimated Time:** 3-4 hours  
**Complexity:** HIGH (Async/Concurrency)

---

## 🎯 OBJECTIVE

Implement the **Sticky Header System** for Zepix V5 Telegram Bot. This header MUST persist on every message and update in real-time (every 30s) to show live bot status, time, sessions, and market prices.

---

## 📋 SOURCE DOCUMENT

**Planning Document Location:**
```
ZepixTradingBot-old-v2-main/Updates/V5 COMMAND TELEGRAM/02_STICKY_HEADER_DESIGN.md
```

**Document Size:** 955 lines | 26 KB  
**Version:** V5.0  
**Design Principle:** REAL-TIME STATUS AWARENESS

---

## 🏗️ IMPLEMENTATION REQUIREMENTS

### **1. Core Components (Must Implement)**

#### **A. Clock Component (`header_clock.py`)**
- Display current time in **GMT** (UTC).
- Format: `🕐 Time: 14:35:22 GMT`.
- Must be accurate to the second.

#### **B. Session Manager (`header_session.py`)**
- Track 4 major sessions:
  - 🇦🇺 Sydney (00:00 - 09:00 GMT)
  - 🇯🇵 Tokyo (01:00 - 10:00 GMT)
  - 🇬🇧 London (08:00 - 17:00 GMT)
  - 🇺🇸 New York (13:00 - 22:00 GMT)
- Detect **overlaps** (e.g., "LONDON + NEW YORK 🔥").
- Calculate time remaining (`2h 25m left`).

#### **C. Live Symbols (`header_symbols.py`)**
- Fetch live Bid/Ask from MT5.
- Default Symbols: `EURUSD`, `GBPUSD`, `USDJPY`, `AUDUSD`.
- Format: `💱 EUR:1.0825 GBP:1.2645`.
- **Caching:** Cache prices for 5 seconds to reduce MT5 load.

#### **D. Bot Status (`header_status.py`)**
- Check:
  - MT5 Connection (Connected/Disconnected).
  - Trading Engine (Paused/Active).
  - Plugin Status (V3/V6 active).
- States: `Active ✅`, `Paused ⏸️`, `Partial ⚠️`, `Error ❌`.

---

### **2. Header Builder (`sticky_header_builder.py`)**

Implement `StickyHeaderBuilder` class with 3 layouts:

**1. Full Header (Default for Menus)**
```
╔══════════════════════════════════════╗
║   🤖 ZEPIX TRADING BOT V5.0          ║
╠══════════════════════════════════════╣
║  📊 Status: ACTIVE ✅                ║
║  🕐 Time: 14:35:22 GMT               ║
║  📈 Session: LONDON (Active)         ║
║  💱 EURUSD: 1.0825 | GBPUSD: 1.2645  ║
╚══════════════════════════════════════╝
```

**2. Compact Header (For Alerts)**
```
🤖 ACTIVE ✅ | 🕐 14:35 GMT | 📈 LONDON
💱 EUR:1.0825 GBP:1.2645 USD:151.20
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**3. Minimal Header (For Quick Replies)**
```
🤖 ACTIVE ✅ | 🕐 14:35 GMT
```

---

### **3. Auto-Refresh System (`header_refresh_manager.py`)**

**Critical Logic:**
- Create an `asyncio` task for active loop.
- **Interval:** 30 seconds.
- **Mechanism:** `edit_message_text`.
- **Smart Management:**
  - Cancel old refresh task when user navigates.
  - Only one active refresh per user/chat.
  - Handle `MessageNotModified` errors gracefully.

---

## 🛠️ INTEGRATION PLAN

### **Step 1: Create Core Files**
- `src/telegram/headers/header_cache.py`
- `src/telegram/headers/header_clock.py`
- `src/telegram/headers/header_session.py`
- `src/telegram/headers/header_symbols.py`
- `src/telegram/headers/header_status.py`
- `src/telegram/headers/sticky_header_builder.py`
- `src/telegram/headers/header_refresh_manager.py`

### **Step 2: Updates Existing Bots**
- **Modify `ControllerBot.py`:**
  - Initialize `StickyHeaderBuilder`.
  - Initialize `HeaderRefreshManager`.
  - In `handle_callback` (navigation), call `refresh_manager.start_refresh()`.

### **Step 3: Integrate with V5 Menus**
- Update `BaseMenuBuilder` to use `StickyHeaderBuilder`.
- Ensure all menus (System, Trading, Risk, etc.) automatically get the header.

---

## ✅ ACCEPTANCE CRITERIA

### **Functional Requirements**
- [ ] Header appears on `/start`.
- [ ] Header persists on ALL menu clicks.
- [ ] Time updates every 30 seconds (approx).
- [ ] Session changes automatically (e.g., at 13:00 GMT for NY Open).
- [ ] Prices update from MT5 (simulated if offline, real if connected).
- [ ] Status reflects real bot state (Pause/Resume updates header).

### **Performance Requirements**
- [ ] No UI freezing during refresh.
- [ ] `MessageNotModified` errors suppressed.
- [ ] Old refresh loops cancelled immediately on navigation.

---

## 📝 DELIVERABLES

1. **Code Files:**
   - All files in `src/telegram/headers/`
   - Updated `controller_bot.py`
   - Updated `base_menu_builder.py`

2. **Documentation:**
   - `HEADER_IMPLEMENTATION_NOTES.md`
   - `REFRESH_LOGIC_DIAGRAM.md`

3. **Git Push:**
   - Push to `main` branch upon completion.

---

## 🚨 CRITICAL INSTRUCTIONS

1. **Do NOT break existing menus.** The header wraps the menu, it doesn't replace it.
2. **Handle Recursion:** Ensure refresh loop doesn't trigger another refresh loop.
3. **Error Handling:** If MT5 is disconnected, show "disconnected" in price field, don't crash.

---

**STATUS: 🟡 AWAITING START**
