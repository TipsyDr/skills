#!/usr/bin/env python3
# setup_vault.py - 初始化 Obsidian AI 记忆系统 Vault 目录结构
# 用法: python3 setup_vault.py <vault_path>
# 示例: python3 setup_vault.py ~/obsidian/my-vault

import sys
import json
from pathlib import Path
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print("❌ 错误：请提供 Vault 路径")
        print("用法: python3 setup_vault.py <vault_path>")
        print("示例: python3 setup_vault.py ~/obsidian/my-vault")
        sys.exit(1)

    vault_path = Path(sys.argv[1]).expanduser().resolve()
    today = datetime.now().strftime("%Y-%m-%d")

    print("🚀 开始初始化 Obsidian AI 记忆系统...")
    print(f"📁 Vault 路径: {vault_path}")

    # --- 创建目录结构 ---
    print("\n📂 创建 11 层目录结构...")

    dirs = [
        "00-系统层",
        "01-AI核心层",
        "02-时间线层/每日日志",
        "02-时间线层/每周回顾",
        "02-时间线层/每月回顾",
        "03-对话层",
        "04-项目层",
        "05-知识层/概念",
        "05-知识层/原理",
        "05-知识层/操作手册",
        "05-知识层/研究笔记",
        "05-知识层/资源资料",
        "05-知识层/永久笔记",
        "05-知识层/术语表",
        "06-经验层/错误记录",
        "06-经验层/成功案例",
        "06-经验层/检查清单",
        "06-经验层/决策模式",
        "07-任务层",
        "08-灵感层",
        "09-用户画像层",
        "10-归档层/旧项目",
        "10-归档层/废弃知识",
        "10-归档层/已关闭事项",
        ".templates",
    ]

    for d in dirs:
        (vault_path / d).mkdir(parents=True, exist_ok=True)

    print("✅ 目录结构创建完成")

    # --- 创建 AI 当前活跃上下文 ---
    active_context = vault_path / "01-AI核心层" / "AI-当前活跃上下文.md"
    if not active_context.exists():
        active_context.write_text(
            f"""\
---
type: ai-context
subtype: active
title: AI-当前活跃上下文
created: {today}
modified: {today}
---

# 🧠 AI 当前活跃上下文

## 📦 当前重点项目

<!-- 在此添加正在进行的项目 -->

## 🔄 当前正在推进

- [ ] 完成系统初始化

## ❓ 当前待解决问题

| 问题 | 项目 | 优先级 | 状态 |
|------|------|--------|------|
|      |      |        |      |

## 🔧 工具配置

| 类型 | 已安装 | 状态 |
|------|--------|------|
|      |        |      |

## 📊 最近关键结论

| 日期 | 结论 | 来源 |
|------|------|------|
| {today} | Obsidian AI 记忆系统初始化完成 | 系统设置 |

---
*最后更新：{today}*
""",
            encoding="utf-8",
        )
        print("✅ 创建 AI-当前活跃上下文.md")

    # --- 创建 AI 长期上下文 ---
    longterm_context = vault_path / "01-AI核心层" / "AI-长期上下文.md"
    if not longterm_context.exists():
        longterm_context.write_text(
            f"""\
---
type: ai-context
subtype: longterm
title: AI-长期上下文
created: {today}
modified: {today}
---

# 🌱 AI 长期上下文

## 🎯 用户长期目标

1. （请填写你的长期目标）

## ⚙️ 用户偏好

### 语言规则
- 对话输出使用中文
- 结构清晰，直接给出可执行内容

### 输出偏好
- 中文输出、结构清晰、直接给出可执行内容

## 🔧 常用工具

| 工具 | 用途 | 熟练度 |
|------|------|--------|
|      |      |        |

## ✅ 已验证成功模式

1. 系统先跑起来
2. 结构化沉淀
3. 定期回顾

## ❌ 已学到的教训

| 时间 | 教训 | 预防措施 |
|------|------|---------|
|      |      |         |

---
*最后更新：{today}*
""",
            encoding="utf-8",
        )
        print("✅ 创建 AI-长期上下文.md")

    # --- 创建系统入口文件 ---
    index_file = vault_path / "00-系统层" / "系统入口.md"
    if not index_file.exists():
        index_file.write_text(
            f"""\
---
type: rules
title: 系统入口
created: {today}
---

# 🚀 Obsidian AI 记忆系统入口

初始化于 {today}

## 核心文件

- [[01-AI核心层/AI-当前活跃上下文]] - 每次对话开始时读取
- [[01-AI核心层/AI-长期上下文]] - 长期记忆存储

## 目录说明

| 目录 | 用途 |
|------|------|
| 00-系统层 | 系统入口、规则文档 |
| 01-AI核心层 | AI 记忆（上下文、技能、工具） |
| 02-时间线层 | 按时间组织内容（日志、sessions） |
| 03-对话层 | 原始对话记录 |
| 04-项目层 | 项目所有相关内容 |
| 05-知识层 | 沉淀后的知识 |
| 06-经验层 | 错误记录、成功案例 |
| 07-任务层 | 任务管理 |
| 08-灵感层 | 随手灵感 |
| 09-用户画像层 | 用户基本信息 |
| 10-归档层 | 已结束项目归档 |

## 每日工作流

1. 早晨：读取 AI 上下文，打开今日日志，确认今日重点
2. 傍晚：更新日志，整理收件箱，保存会话
3. 每周：写周回顾，更新项目进展，提炼知识
""",
            encoding="utf-8",
        )
        print("✅ 创建系统入口文件")

    # --- 保存 vault 路径配置 ---
    config_dir = Path.home() / ".openclaw"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "obsidian-config.json"
    config_data = {
        "vault_path": str(vault_path),
        "initialized_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }
    config_file.write_text(json.dumps(config_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Vault 路径已保存到 {config_file}")

    # --- 完成提示 ---
    print(f"""
🎉 Obsidian AI 记忆系统初始化完成！

📋 接下来的步骤：
1. 在 Obsidian 中打开 {vault_path} 作为 vault
2. 安装推荐插件：Templater、Dataview、Calendar、QuickAdd
3. 在 Templater 设置中将 .templates 设为模板目录
4. 运行 setup_hooks.py 配置自动化 hooks（可选但推荐）：
   python3 setup_hooks.py {vault_path}

💡 每次对话开始时，告诉 AI：
   "请加载我的 Obsidian 上下文，vault 路径是 {vault_path}"
""")


if __name__ == "__main__":
    main()
