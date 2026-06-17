; SACREDSPACE HYPERGLYPH — WINDOWS COMMAND BINDINGS
; Version: 1.0 | Owner: AURORA | Pillar: 04_CODEX
; Run as administrator for full command glyph access
; Right-click → Run as Administrator, or add to Windows Startup

#NoEnv
SendMode Input
#SingleInstance Force

; === TEXT GLYPHS (instant auto-replace) ===

:*:;ss::S∆CR3DSP@CE
:*:;seal::In lakesh alakin. ∆
:*:;oak::∆∆∆O∆K3YTREE∆∆∆
:*:;aina::∆LL !N ∆LL • ∆Y3 N ∆Y3

; Base 12-glyph grid
:*:;ai::∆
:*:;kn::◇
:*:;rt::✶
:*:;en::⚙
:*:;wb::☉
:*:;my::☽
:*:;qu::⚔
:*:;gw::⟡
:*:;ct::∞
:*:;cmd::⌘
:*:;net::⟠
:*:;pl::☍

; === STRUCTURAL GLYPHS ===

:*:;node::◇ N0DΞ ∆CT!VΞ ◇{Enter}
:*:;quest::⚔ Q∪ΞST BΞG!NS ⚔{Enter}
:*:;log::◈ MΞM0RY M0TΞ ◈{Enter}

; === COMMAND GLYPHS — OS LAUNCHERS ===
; These open applications or WSL environments:

X*:;sacred::
  Run, wsl -e bash -c "cd /mnt/d/SacredSpace_OS && claude"
return

X*:;spine::
  Run, wsl -e bash -c "cd /mnt/d/SacredSpace_OS/systems/fastapi && uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload"
return

X*:;obsidian::
  Run, D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\Obsidian.exe
return

X*:;sigil::
  Run, wsl -e bash -c "cd /mnt/d/SacredSpace_OS/06_AGENTS/sacred-sigil-terminal && npm run dev"
return
