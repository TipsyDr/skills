#!/usr/bin/env python3
# setup_hooks.py - 生成 Openclaw Code Hooks 脚本，实现 Obsidian 记忆自动化
# 用法: python3 setup_hooks.py <vault_path>
# 示例: python3 setup_hooks.py ~/obsidian/my-vault

import sys
import json
import textwrap
import os
from pathlib import Path


def main():
    vault_path_str = None

    if len(sys.argv) >= 2:
        vault_path_str = sys.argv[1]

    # 尝试从配置文件读取
    if not vault_path_str:
        config_file = Path(os.environ.get("OBSIDIAN_CONFIG", "~/.openclaw/obsidian/obsidian-config.json")).expanduser()
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text(encoding="utf-8"))
                vault_path_str = config.get("vault_path")
            except Exception:
                pass

    if not vault_path_str:
        print("❌ 错误：请提供 Vault 路径")
        print("用法: python3 setup_hooks.py <vault_path>")
        sys.exit(1)

    vault_path = Path(vault_path_str).expanduser().resolve()
    hooks_dir = Path(os.environ.get("OBSIDIAN_HOOKS_DIR", "~/.openclaw/obsidian/hooks")).expanduser()

    print("⚡ 生成 Openclaw Code Hooks 脚本...")
    print(f"📁 Vault 路径: {vault_path}")
    print(f"📁 Hooks 目录: {hooks_dir}")

    hooks_dir.mkdir(parents=True, exist_ok=True)

    # 在生成的脚本中使用正斜杠路径字符串，确保跨平台一致性
    vault_path_posix = vault_path.as_posix()

    # --- 1. session_start_load.py（SessionStart hook）---
    (hooks_dir / "session_start_load.py").write_text(
        textwrap.dedent(f"""\
            #!/usr/bin/env python3
            # SessionStart hook: 对话开始时加载 Obsidian 记忆
            from pathlib import Path

            vault_path = Path(r"{vault_path}")
            active_ctx = vault_path / "01-AI核心层" / "AI-当前活跃上下文.md"
            longterm_ctx = vault_path / "01-AI核心层" / "AI-长期上下文.md"
            sessions_dir = vault_path / "02-时间线层" / "sessions"

            print("=== 🧠 Obsidian AI 记忆已加载 ===")
            print()
            if active_ctx.exists():
                print("📌 当前活跃上下文已就绪")
            if longterm_ctx.exists():
                print("🌱 长期上下文已就绪")
            # 显示最新 session
            md_files = sorted(sessions_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
            if md_files:
                print(f"💬 最近会话: {{md_files[0].stem}}")
            print("==================================")
        """),
        encoding="utf-8",
    )

    # --- 2. obsidian_session_load.py（UserPromptSubmit hook）---
    (hooks_dir / "obsidian_session_load.py").write_text(
        textwrap.dedent(f"""\
            #!/usr/bin/env python3
            # UserPromptSubmit hook: 每条消息前注入 Obsidian AI 上下文
            import tempfile
            from pathlib import Path

            vault_path = Path(r"{vault_path}")
            lock_dir = Path(tempfile.gettempdir()) / ".openclaw_obsidian_locks"
            lock_file = lock_dir / "context_loaded"

            # 防止重复注入（同一会话只注入一次）
            lock_dir.mkdir(parents=True, exist_ok=True)
            if lock_file.exists():
                raise SystemExit(0)

            active_ctx = vault_path / "01-AI核心层" / "AI-当前活跃上下文.md"
            longterm_ctx = vault_path / "01-AI核心层" / "AI-长期上下文.md"
            sessions_dir = vault_path / "02-时间线层" / "sessions"

            if not active_ctx.exists() and not longterm_ctx.exists():
                raise SystemExit(0)

            print("---OBSIDIAN-CONTEXT-START---")
            print()
            if active_ctx.exists():
                print("## AI 当前活跃上下文")
                print(active_ctx.read_text(encoding="utf-8"))
                print()
            if longterm_ctx.exists():
                print("## AI 长期上下文")
                print(longterm_ctx.read_text(encoding="utf-8"))
                print()
            # 加载最新 1-2 个 session
            md_files = sorted(sessions_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
            for i, session_file in enumerate(md_files[:2]):
                if i == 0:
                    print("## 最近会话记录")
                print(f"### {{session_file.stem}}")
                print(session_file.read_text(encoding="utf-8"))
                print()
            print("---OBSIDIAN-CONTEXT-END---")

            # 标记已注入
            lock_file.touch()
        """),
        encoding="utf-8",
    )

    # --- 3. session_end_summary.py（SessionEnd hook）---
    (hooks_dir / "session_end_summary.py").write_text(
        textwrap.dedent("""\
            #!/usr/bin/env python3
            # SessionEnd hook: 对话结束时清理锁文件
            import shutil
            import tempfile
            from pathlib import Path

            lock_dir = Path(tempfile.gettempdir()) / ".openclaw_obsidian_locks"
            if lock_dir.exists():
                shutil.rmtree(lock_dir, ignore_errors=True)
            print("🔄 Obsidian 记忆上下文锁已清除")
        """),
        encoding="utf-8",
    )

    # --- 4. save_session.py（手动执行）---
    (hooks_dir / "save_session.py").write_text(
        textwrap.dedent(f"""\
            #!/usr/bin/env python3
            # 手动保存会话到 Obsidian
            # 用法: python3 save_session.py [会话主题]
            import sys
            from pathlib import Path
            from datetime import datetime

            vault_path = Path(r"{vault_path}")
            sessions_dir = vault_path / "02-时间线层" / "sessions"
            active_ctx = vault_path / "01-AI核心层" / "AI-当前活跃上下文.md"

            topic = sys.argv[1] if len(sys.argv) > 1 else "对话记录"
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d-%H%M%S")
            today = now.strftime("%Y-%m-%d")
            now_str = now.strftime("%Y-%m-%d %H:%M")
            filename = f"session-{{timestamp}}.md"
            filepath = sessions_dir / filename

            sessions_dir.mkdir(parents=True, exist_ok=True)

            content = f\"\"\"\\
            ---
            type: dialogue
            title: {{today}} {{topic}}
            date: {{today}}
            dialogue_type: 工作
            tags:
              - 💬对话
            ---

            # 💬 {{today}} {{topic}}

            ## 会话主题

            {{topic}}

            ## 关键产出

            - （请填写本次对话的关键产出）

            ## 重要结论

            | 结论 | 置信度 | 备注 |
            |------|--------|------|
            |      |        |      |

            ## 待办事项

            - [ ] （从对话中提取的待办事项）

            ## 需要沉淀的内容

            - 知识：→ 待整理
            - 错误：→ 待整理
            - 成功：→ 待整理

            ## 关联笔记

            - [[01-AI核心层/AI-当前活跃上下文]]

            ---
            *会话时间：{{now_str}}*
            \"\"\"

            # 去掉 textwrap.dedent 产生的缩进
            import textwrap
            filepath.write_text(textwrap.dedent(content), encoding="utf-8")
            print(f"✅ 会话已保存: {{filepath}}")

            if active_ctx.exists():
                print("📝 建议手动更新 AI-当前活跃上下文.md 中的最近关键结论")

            print()
            print("💡 后续操作建议：")
            print(f"1. 在 Obsidian 中打开 {{filepath}}")
            print("2. 填写关键产出和重要结论")
            print("3. 将有价值的内容沉淀到知识层/经验层")
        """),
        encoding="utf-8",
    )

    print()
    print("✅ 已生成 4 个 Hook 脚本：")
    print(f"   {hooks_dir / 'session_start_load.py'}   (SessionStart)")
    print(f"   {hooks_dir / 'obsidian_session_load.py'} (UserPromptSubmit)")
    print(f"   {hooks_dir / 'session_end_summary.py'}  (SessionEnd)")
    print(f"   {hooks_dir / 'save_session.py'}         (手动保存)")
    print()

    # --- 输出 hooks.json 配置 ---
    hooks_dir_posix = hooks_dir.as_posix()
    hooks_config = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {hooks_dir_posix}/session_start_load.py",
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {hooks_dir_posix}/obsidian_session_load.py",
                        }
                    ],
                }
            ],
            "SessionEnd": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {hooks_dir_posix}/session_end_summary.py",
                        }
                    ],
                }
            ],
        }
    }

    print("📋 请将以下内容合并到你的 agent runtime 配置 hooks 字段：")
    print()
    print(json.dumps(hooks_config, ensure_ascii=False, indent=2))
    print()
    print("🎉 Hooks 配置完成！重启会话后生效。")
    print(f"手动保存会话：python3 {hooks_dir_posix}/save_session.py [主题]")


if __name__ == "__main__":
    main()
