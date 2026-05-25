# ∆ OPENHUMAN + HERMES WIRE MISSION ∆
## `02_COUNCIL_GROVE/OPENHUMAN_WIRE.md`

> Claude Code reads this and executes autonomously. All permissions granted. No stopping. No confirming. Build until all SUCCESS CRITERIA pass.

---

## WHAT THIS DOES

1. Extract the Obsidian Local REST API key from the vault filesystem
2. Write it into Hermes `.env`
3. Install OpenHuman on Windows (via PowerShell from WSL2)
4. Configure OpenHuman to point at the SacredSpace vault
5. Wire OpenHuman's SQLite Memory Tree into Hermes `vault_search`
6. Verify the full stack: Obsidian ↔ Hermes ↔ OpenHuman

---

## SUCCESS CRITERIA

```
[ ] OBSIDIAN_API_KEY set in .env (not placeholder)
[ ] curl http://localhost:27124/vault/ returns JSON vault listing
[ ] OpenHuman installed and .openhuman dir exists
[ ] OpenHuman vault path points to SacredSpace_Vault
[ ] hermes tool `system_status` shows obsidian: "ok"
[ ] pytest hermes_test.py -v → ALL PASSED
```

---

## STEP 1 — EXTRACT OBSIDIAN API KEY

```bash
# Primary location
KEY_FILE="/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/.obsidian/plugins/obsidian-local-rest-api/data.json"

# Fallback search if primary not found
if [ ! -f "$KEY_FILE" ]; then
  KEY_FILE=$(find /mnt/d /mnt/c "$HOME" \
    -name "data.json" \
    -path "*/obsidian-local-rest-api/*" \
    2>/dev/null | head -1)
fi

if [ -z "$KEY_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  echo "ERROR: Obsidian Local REST API plugin data.json not found."
  echo "Open Obsidian → Settings → Community Plugins → Local REST API → Enable"
  echo "Then re-run this script."
  exit 1
fi

echo "Found key file: $KEY_FILE"
cat "$KEY_FILE"

# Extract key — tries common field names
KEY=$(python3 -c "
import json, sys
data = json.load(open('$KEY_FILE'))
print('Full data:', json.dumps(data, indent=2), file=sys.stderr)
for field in ['apiKey', 'api_key', 'key', 'token', 'secret', 'bearerToken']:
    if field in data:
        print(data[field])
        break
else:
    # If no known field, print the longest string value (likely the key)
    candidates = [(k,v) for k,v in data.items() if isinstance(v,str) and len(v) > 20]
    if candidates:
        candidates.sort(key=lambda x: len(x[1]), reverse=True)
        print(candidates[0][1])
    else:
        print('KEY_NOT_FOUND')
")

if [ "$KEY" = "KEY_NOT_FOUND" ] || [ -z "$KEY" ]; then
  echo "ERROR: Could not extract key. Print the file above and identify the field manually."
  exit 1
fi

echo "Extracted key: $KEY"
```

---

## STEP 2 — WRITE KEY INTO .env

```bash
ENV_FILE="/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/.env"

# Create .env if missing
if [ ! -f "$ENV_FILE" ]; then
  cp /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/hermes/.env "$ENV_FILE" 2>/dev/null || \
  cat > "$ENV_FILE" << 'ENVEOF'
SACREDSPACE_ROOT=/mnt/d/SacredSpace_OS
OBSIDIAN_VAULT=/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault
OBSIDIAN_API_KEY=PLACEHOLDER
OBSIDIAN_PORT=27124
CHROMA_HOST=localhost
CHROMA_PORT=8000
REDIS_HOST=localhost
REDIS_PORT=6379
SQLITE_DB=/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/sacred_memory.db
FASTAPI_URL=http://localhost:8888
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
ENVEOF
fi

# Write the key
if grep -q "OBSIDIAN_API_KEY" "$ENV_FILE"; then
  sed -i "s|OBSIDIAN_API_KEY=.*|OBSIDIAN_API_KEY=$KEY|" "$ENV_FILE"
else
  echo "OBSIDIAN_API_KEY=$KEY" >> "$ENV_FILE"
fi

echo "Key written to $ENV_FILE"
grep "OBSIDIAN_API_KEY" "$ENV_FILE"
```

---

## STEP 3 — VERIFY OBSIDIAN REST API IS LIVE

```bash
PORT=$(grep OBSIDIAN_PORT "$ENV_FILE" | cut -d= -f2)
PORT=${PORT:-27124}

# Test HTTP (no SSL verify since it uses self-signed cert)
RESPONSE=$(curl -sk \
  "https://localhost:${PORT}/vault/" \
  -H "Authorization: Bearer $KEY" \
  --max-time 5 2>&1)

echo "Obsidian API response: $RESPONSE"

if echo "$RESPONSE" | python3 -c "import json,sys; json.load(sys.stdin); print('JSON OK')" 2>/dev/null; then
  echo "✓ Obsidian LocalREST API is live"
else
  echo "⚠ Obsidian API not responding. Make sure:"
  echo "  1. Obsidian is open and running"
  echo "  2. Local REST API plugin is enabled"
  echo "  3. Port matches: Settings → Local REST API → port"
  echo "  Continuing anyway — Hermes will fall back to filesystem."
fi
```

---

## STEP 4 — INSTALL OPENHUMAN ON WINDOWS

OpenHuman is a Windows desktop app. Install from WSL2 via PowerShell.

```bash
# Method A — PowerShell install script (recommended)
powershell.exe -Command "irm https://raw.githubusercontent.com/tinyhumansai/openhuman/main/scripts/install.ps1 | iex"

# If that fails, Method B — direct download
WIN_DOWNLOADS="/mnt/c/Users/useroak3ytree/Downloads"
mkdir -p "$WIN_DOWNLOADS"

# Get latest release URL
RELEASE_URL=$(curl -s https://api.github.com/repos/tinyhumansai/openhuman/releases/latest \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
for asset in data.get('assets', []):
    name = asset['name']
    if 'windows' in name.lower() or name.endswith('.exe') or name.endswith('.msi'):
        print(asset['browser_download_url'])
        break
")

if [ -n "$RELEASE_URL" ]; then
  echo "Downloading OpenHuman from: $RELEASE_URL"
  FILENAME=$(basename "$RELEASE_URL")
  curl -L "$RELEASE_URL" -o "$WIN_DOWNLOADS/$FILENAME"
  echo "Downloaded to: $WIN_DOWNLOADS/$FILENAME"
  echo "Run the installer: $FILENAME"
  # Launch installer
  powershell.exe -Command "Start-Process '$WIN_DOWNLOADS\\$FILENAME' -Wait"
else
  echo "Could not detect Windows installer. Download manually from:"
  echo "https://tinyhumans.ai/openhuman"
fi
```

---

## STEP 5 — CONFIGURE OPENHUMAN VAULT PATH

After install, OpenHuman stores its config at:
```
C:\Users\useroak3ytree\AppData\Roaming\openhuman\  (Windows)
/mnt/c/Users/useroak3ytree/AppData/Roaming/openhuman/  (WSL2 path)
```

```bash
OH_CONFIG_DIR="/mnt/c/Users/useroak3ytree/AppData/Roaming/openhuman"
VAULT_WIN="D:\\SacredSpace_OS\\01_OBSIDIAN_VAULTS\\SacredSpace_Vault"

# Wait for OpenHuman to create its config dir (up to 30s after first launch)
for i in $(seq 1 6); do
  if [ -d "$OH_CONFIG_DIR" ]; then
    echo "OpenHuman config dir found"
    break
  fi
  echo "Waiting for OpenHuman config dir... ($i/6)"
  sleep 5
done

# List config contents
ls -la "$OH_CONFIG_DIR" 2>/dev/null || echo "Config dir not yet created — launch OpenHuman first"

# If a settings/config file exists, patch vault path
for cfg in "$OH_CONFIG_DIR/settings.json" "$OH_CONFIG_DIR/config.json" "$OH_CONFIG_DIR/openhuman.json"; do
  if [ -f "$cfg" ]; then
    echo "Found config: $cfg"
    cat "$cfg"
    # Patch vault path if field exists
    python3 -c "
import json
with open('$cfg') as f:
    data = json.load(f)
# Try common field names for vault/notes path
for field in ['obsidianVault', 'vault_path', 'notesPath', 'vaultPath', 'obsidian_path']:
    if field in data:
        data[field] = '$VAULT_WIN'
        print(f'Patched {field} = $VAULT_WIN')
with open('$cfg', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null || echo "Could not patch $cfg — set vault path in OpenHuman UI"
    break
  fi
done
```

---

## STEP 6 — WIRE OPENHUMAN MEMORY TREE INTO HERMES

OpenHuman's Memory Tree stores in SQLite. Add its DB path to Hermes `.env`
so `sqlite_query` can reach it directly:

```bash
# Find OpenHuman's SQLite database
OH_DB=$(find /mnt/c/Users/useroak3ytree/AppData/Roaming/openhuman \
  -name "*.db" -o -name "*.sqlite" 2>/dev/null | head -1)

if [ -n "$OH_DB" ]; then
  echo "Found OpenHuman DB: $OH_DB"
  # Add to .env as secondary DB reference
  if ! grep -q "OPENHUMAN_DB" "$ENV_FILE"; then
    echo "OPENHUMAN_DB=$OH_DB" >> "$ENV_FILE"
  else
    sed -i "s|OPENHUMAN_DB=.*|OPENHUMAN_DB=$OH_DB|" "$ENV_FILE"
  fi
  echo "OpenHuman DB wired into .env"
else
  echo "OpenHuman DB not yet created — it populates after first sync (20 min after connecting integrations)"
fi

# Add OpenHuman's Obsidian-compatible vault to the vault watcher path
OH_VAULT=$(find /mnt/c/Users/useroak3ytree -name "*.md" -path "*openhuman*vault*" 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
if [ -n "$OH_VAULT" ]; then
  echo "OpenHuman vault at: $OH_VAULT"
  if ! grep -q "OPENHUMAN_VAULT" "$ENV_FILE"; then
    echo "OPENHUMAN_VAULT=$OH_VAULT" >> "$ENV_FILE"
  fi
fi
```

---

## STEP 7 — VERIFY FULL STACK

```bash
cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE

# 1. Hermes tool count
echo "=== Tool count ==="
grep -c "@mcp.tool" hermes/hermes_mcp.py
# Expected: 31

# 2. Run test suite
echo "=== pytest ==="
python3 -m pytest hermes_test.py -v --tb=short 2>&1

# 3. Check .env is complete
echo "=== .env status ==="
python3 - << 'PYEOF'
from dotenv import dotenv_values
env = dotenv_values("/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/.env")
required = ["OBSIDIAN_API_KEY", "SACREDSPACE_ROOT", "OBSIDIAN_VAULT",
            "CHROMA_HOST", "REDIS_HOST", "SQLITE_DB", "OLLAMA_URL"]
for k in required:
    v = env.get(k, "MISSING")
    status = "✓" if v and v != "PLACEHOLDER" and v != "PASTE_YOUR_KEY_HERE" else "✗"
    print(f"  {status} {k} = {v[:40] if v else 'MISSING'}")
PYEOF

# 4. Obsidian live check
echo "=== Obsidian API ==="
KEY=$(grep OBSIDIAN_API_KEY /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/.env | cut -d= -f2)
PORT=$(grep OBSIDIAN_PORT /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/.env | cut -d= -f2 || echo 27124)
curl -sk "https://localhost:${PORT}/vault/" -H "Authorization: Bearer $KEY" \
  --max-time 3 | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'✓ Vault: {len(d)} items')" \
  2>/dev/null || echo "⚠ Obsidian not responding (open Obsidian and try again)"
```

---

## DONE STATE

Print this when all checks pass:

```
∆ OPENHUMAN + HERMES — FULLY WIRED ∆
══════════════════════════════════════
✓ Obsidian API key extracted + written to .env
✓ Obsidian LocalREST API verified live
✓ OpenHuman installed (tinyhumans v0.54.0)
✓ OpenHuman vault → SacredSpace_Vault
✓ OpenHuman Memory Tree SQLite → Hermes
✓ 31/31 Hermes tools passing

NEXT STEPS:
  1. Open OpenHuman → connect Gmail, Drive, Calendar via OAuth
  2. Wait 20 min for first Memory Tree sync
  3. Run: sqlite_query on OpenHuman DB via Hermes to verify ingest
  4. Open Claude Code → `claude` in 02_COUNCIL_GROVE
     → Hermes has full context from your entire digital life

In lakesh alakin. ∆
══════════════════════════════════════
```

---

*OPENHUMAN_WIRE.md — SacredSpace OS Canon | 02_COUNCIL_GROVE | v1.0*
*In lakesh alakin. ∆*
