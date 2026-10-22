# تقویم من

Offline-first calendar (Jalali / Gregorian / Hijri), notes, birthdays and weekly tasks.
All data lives on the device; sync through Cloudflare is optional.

## Commands (Node 22: prefix with `fnm exec --using=22`)

| What | Command |
|---|---|
| Web dev server | `pnpm dev` |
| Tests | `pnpm test` |
| Debug APK | `pnpm android:apk` |
| Signed release APK -> `release/taghvim.apk` | `pnpm android:release` |
| Local sync server (port 8799) | `pnpm exec wrangler dev --port 8799` |
| Server smoke test | `node scripts/smoke-sync.mjs <url>` |

Back up `android/release.keystore` and `android/keystore.properties` somewhere safe: without them an installed app can never be updated.

## Deploying the sync server (once)

```bash
pnpm exec wrangler login
pnpm exec wrangler d1 create taghvim          # copy the printed database_id into wrangler.jsonc
pnpm exec wrangler d1 migrations apply taghvim --remote
pnpm build && pnpm exec wrangler deploy        # prints https://taghvim.<you>.workers.dev
```

Then put that URL in `.env.production` as `VITE_SYNC_URL=https://taghvim.<you>.workers.dev` and rebuild the APK.
Without `VITE_SYNC_URL` the app has no sync section and never touches the network.

No invite codes: anyone with the app can create an account with email + password, and the server stores only a hash of the derived key. The sync entry stays hidden in Settings until the title is tapped five times.
