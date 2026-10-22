# Rooznegar UI — task list

Source: the design canvas (14 boards). One row = one message to Claude: "do F1", "do S3", ...
Order matters only where "needs" is listed. After each task: typecheck, tests, build, and a look in the browser (or the emulator for A-tasks).

## F — Foundation (do these first)

| ID | Task | Needs |
|---|---|---|
| F1 | Design tokens and glass look: colours, blurred gradient background with blobs, glass card, primary/secondary/icon buttons, chips, switch, checkbox circle, inputs, progress bar. Vazirmatn 300–900 bundled locally (no Google Fonts link). | – |
| F2 | Icon set: the ~25 line icons used in the design as one `Icon` component (inline SVG, no network). | – |
| F3 | App shell: glass nav bar (امروز / تقویم / کارها / تولدها / بیشتر) with the blue "+" quick-add button, and routing between pages. Replaces the current 4 text tabs. | F1, F2 |
| F4 | Dark theme per the DarkToday board; follows system or the manual setting (light / dark / auto). | F1 |

## D — Data changes the design needs (small, do before the screens that use them)

| ID | Task | Needed by |
|---|---|---|
| D1 | Settings object in one place: user name, main calendar, auxiliary calendars, week start, theme, notification switches. Moves today's loose localStorage keys into it. | S1, S8, F4 |
| D2 | Task fields: description, time (HH:MM), reminder lead (minutes), active switch. Dexie migration v3; sync rows keep working. | S5, S1, S3 |
| D3 | Notes: several notes per day, each with title, tags, pinned. Migration from "one note = the date". | S3, S4, S7 |
| D4 | Done rows remember when they were ticked ("انجام شد ساعت ۰۷:۲۰"). | S3 |

## S — Screens

| ID | Screen (board) | What is in it | Needs |
|---|---|---|---|
| S1 | ۰۱ امروز | Greeting + offline badge + search button; date card (weekday, big Jalali day, Gregorian and Hijri chips); week strip with today selected; today's tasks with times/reminder hint and "۲ از ۴ انجام شد"; birthday-today card with next birthday; today's note card. | F1–F3, D1, D2 |
| S2 | ۰۲ تقویم | Title + "امروز" button; month card with prev/next, other calendars' month ranges under the title; grid cells (Jalali number, small Gregorian, note/task/birthday dots, Friday red, dimmed days outside the month); legend; selected-day card with counts and "مشاهده جزئیات روز". | F1–F3 |
| S3 | ۰۳ جزئیات روز | Header with back/more; date card with two chips and progress bar; tasks split into "باقی‌مانده / انجام شده" with times; birthday card with the congratulate button; day note with autosave status. | F1–F3, D2–D4 |
| S4a | ۰۴ یادداشت جدید — editor | Cancel/Save, autosave pill, date picker button (3 calendars), title + body, word count. | S3, D3 |
| S4b | ۰۴ — tags | Tag chips (select, add new). | S4a |
| S4c | ۰۴ — toolbar | Checklist, pin, reminder (notification), tag buttons. | S4a, S4b |
| S5 | ۰۵ کار تکراری جدید | Title, description, weekday segmented control, presets (هر روز / شنبه تا چهارشنبه / آخر هفته), reminder time, lead time picker, active switch, "اولین تکرار" line, create button. Also edit mode. | D2 |
| S6 | ۰۶ تولدها | List: "امروز" and "به‌زودی" with "N روز"; add form with Jalali/Gregorian/Hijri segmented control, day, month, optional year; search; edit and delete. | F1–F3 |
| S7 | ۰۷ جستجو | Search field, filter chips (همه / یادداشت‌ها / کارها / تولدها), recent searches, results grouped by type with the match highlighted. | D3 |
| S8 | ۰۸ تنظیمات | Calendar (main, auxiliary, week start); appearance; notifications (reminders, ongoing summary); data and sync row; backup/restore; app lock. | D1, F4 |
| S9 | ۰۹ همگام‌سازی | Pending-changes badge, offline notice, local data card (counts, size), pending list with what/when, backup status, "همگام‌سازی اکنون". | S8 |
| S10 | App lock | PIN or fingerprint lock (needs a Capacitor biometric plugin). | S8 |
| S11 | کارها (tab) | A list page to manage weekly tasks (edit, pause, delete). **Not in the design** — see questions. | S5 |
| S12 | بیشتر (tab) | Menu page linking Settings, Search, Sync, Backup. **Not in the design** — see questions. | S8, S9 |

## A — Android (the Android board)

| ID | Task | Needs |
|---|---|---|
| A1 | Small 2×2 widget: weekday, big day number, month and year, Gregorian date, "۲ کار" chip. | F1 |
| A2 | Large 4×2 widget redesign: two dates, progress "۲/۴", task rows with times, tick from the widget (exists, restyle). | A1 |
| A3 | Ongoing notification redesign with the two actions "انجام شد" and "یادآوری ۱۵ دقیقه بعد". | D2 |
| A4 | Task reminders at the task's own time (and lead time) instead of the fixed 08:00. | D2 |

## Questions (they change the tasks above)

1. **کارها** and **بیشتر** tabs have no board. OK to design S11/S12 myself in the same style?
2. Several notes per day (D3) or keep one note per day with a title?
3. The greeting "صبح بخیر، نیلوفر": a name field in Settings, hidden when empty?
4. The congratulate button on a birthday card: open the Android share sheet with a ready message?
5. "پشتیبان هر شب خودکار" on the Sync board: a nightly sync when the app is open, or only a label?

## Suggested order

F1 → F2 → F3 → D1 → S2 → S1 → D2 → D4 → D3 → S3 → S4a → S5 → S6 → F4 → S8 → S9 → S7 → S4b → S4c → A1 → A2 → A3 → A4 → S11 → S12 → S10
