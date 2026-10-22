// Turns monasebat.json (Jalali years 1404-1406, event lists per day) into the compact src/events.json the app bundles.
//   node scripts/build-events.mjs
import { readFileSync, writeFileSync } from 'node:fs';

const src = JSON.parse(readFileSync(new URL('../monasebat.json', import.meta.url), 'utf8'));

const years = {}; // "1405-7-29": { h: 1 if a day off, e: [[title, 1 if a day off], ...] }
const perYear = {}; // year -> Map("m-d|title" -> holiday flag), to find events that repeat on the same Jalali date every year
for (const month of src) {
  for (const day of month.days) {
    const key = `${month.year}-${month.month}-${day.day}`;
    const e = day.events.map((x) => [x.title.replace(/\s+/g, ' ').trim(), x.holiday ? 1 : 0]);
    if (!e.length) continue;
    years[key] = { h: day.holiday ? 1 : 0, e };
    const seen = (perYear[month.year] ??= new Map());
    for (const [t, h] of e) seen.set(`${month.month}-${day.day}|${t}`, h);
  }
}

// Outside the supplied years only the events that sit on the same Jalali date in every year are safe to show: lunar ones move.
const yearList = Object.keys(perYear);
const fixed = {};
for (const [k, h] of perYear[yearList[0]]) {
  if (!yearList.every((y) => perYear[y].get(k) === h)) continue;
  const [md, title] = k.split('|');
  (fixed[md] ??= { h: 0, e: [] }).e.push([title, h]);
  if (h) fixed[md].h = 1;
}

writeFileSync(new URL('../src/events.json', import.meta.url), JSON.stringify({ range: [Math.min(...yearList), Math.max(...yearList)], years, fixed }));
console.log(`years ${yearList.join(', ')}: ${Object.keys(years).length} days with events, ${Object.keys(fixed).length} fixed Jalali dates`);
