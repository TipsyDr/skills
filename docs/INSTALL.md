# Install Guide

## Install One Skill

```bash
git clone https://github.com/TipsyDr/skills.git
mkdir -p ~/.codex/skills
cp -R skills/agent-loop ~/.codex/skills/
```

Replace `agent-loop` with any folder name under `skills/`.

## Install All Skills

```bash
git clone https://github.com/TipsyDr/skills.git
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Restart Codex after installation.

## Update Existing Local Skills

```bash
cd skills
git pull
cp -R skills/* ~/.codex/skills/
```

If you keep local edits inside `~/.codex/skills`, back them up before copying over them.

## Obsidian Memory Setup

`obsidian-memory` expects an Obsidian vault with the directory structure described in `skills/obsidian-memory/SKILL.md`.

To create a new vault scaffold:

```bash
python3 skills/obsidian-memory/scripts/setup_vault.py /path/to/your/vault
```

To generate hook scripts:

```bash
export OBSIDIAN_HOOKS_DIR="$HOME/.openclaw/obsidian/hooks"
python3 skills/obsidian-memory/scripts/setup_hooks.py /path/to/your/vault
```

The script prints a hooks JSON snippet. Merge it into your agent runtime config if your runtime supports command hooks.
