# TipsyDr Skills

Personal Codex skill library.

This repository stores reusable skills that have been useful enough to keep outside a single chat or machine. The goal is simple: make the skills portable, reviewable, and easy to reinstall on a fresh Codex setup.

## What's Inside

| Skill | Purpose |
| --- | --- |
| `agent-loop` | Durable loop for long-running implementation, research, debugging, lesson, and documentation work. |
| `obsidian-memory` | Obsidian second-brain workflow for loading active context and saving useful conclusions back into a vault. |
| `webnovel-topic` | Chinese webnovel topic and market-aware concept planning. |
| `webnovel-outline` | Worldbuilding, character, plot, volume, and chapter-outline design. |
| `webnovel-write` | Drafting, continuing, expanding, and rewriting webnovel chapters. |
| `webnovel-review` | Timeline, plot-hole, OOC, foreshadowing, and word-count review. |
| `webnovel-polish` | Prose, pacing, payoff, and dialogue polishing. |
| `webnovel-finalize` | Final typo, punctuation, compliance, and export-format checks. |
| `webnovel-worldbuilder` | Full workflow orchestration from idea to final manuscript. |
| `webnovel-hot-memes` | Chinese hot memes, platform voice, and male-channel craft notes for fiction. |
| `webnovel-female-radar` | Female-channel emotion, relationship, gufeng, and platform voice notes. |

## Install

Clone the repository and copy the wanted skill folders into `~/.codex/skills/`:

```bash
git clone https://github.com/TipsyDr/skills.git
mkdir -p ~/.codex/skills
cp -R skills/agent-loop ~/.codex/skills/
cp -R skills/obsidian-memory ~/.codex/skills/
```

To install everything:

```bash
git clone https://github.com/TipsyDr/skills.git
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Restart Codex after copying new skills so they are discovered.

## Notes

- `obsidian-memory` is a public/template-safe version of a personal Obsidian workflow. Configure your own vault path and hooks directory before using automation scripts.
- The webnovel skills are a local curated snapshot intended as reusable writing workflow guidance. Trend and ranking references can go stale; verify fresh sources when recency matters.
- This repository intentionally stores skill source files only, not private vault content, chat logs, generated manuscripts, API keys, or machine cache directories.

See [docs/INSTALL.md](docs/INSTALL.md) and [docs/SKILLS.md](docs/SKILLS.md) for details.
