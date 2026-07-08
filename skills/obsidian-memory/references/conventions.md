# Obsidian AI 记忆系统 — 约定规范

包含 frontmatter 字段规范、type 类型标签、标签体系、链接规范。

## 目录

1. [Frontmatter 必填字段](#frontmatter-必填字段)
2. [type 类型标签](#type-类型标签)
3. [标签体系](#标签体系)
4. [链接规范](#链接规范)
5. [各层职责速查](#各层职责速查)

---

## Frontmatter 必填字段

各类型笔记的 frontmatter 必填字段：

| 笔记类型 | 必填字段 |
|---------|---------|
| 对话记录 | type, title, 日期, 对话类型 |
| 项目总览 | type, title, project_status, created |
| 错误记录 | type, title, 日期, 错误类型, 严重程度, status, 根因, 解决 |
| 成功案例 | type, title, 日期, 成功类型, 关键动作, 成功条件 |
| 知识卡片 | type, title, 定义, 核心要点 |
| 永久笔记 | type, title, created |
| 每日日志 | type, title, date |
| AI上下文 | type, subtype, title, created, modified |

---

## type 类型标签

```yaml
type: ai-context    # AI 上下文文件（01-AI核心层专用）
type: log           # 日志（每日/每周/每月）
type: dialogue      # 对话记录（sessions）
type: project       # 项目总览
type: knowledge     # 知识（卡片/永久笔记）
type: experience    # 经验（错误/成功）
type: task          # 任务
type: inspiration   # 灵感
type: rules         # 规则文档
```

subtype 细分（配合 type 使用）：

```yaml
# type: ai-context
subtype: active     # 当前活跃上下文
subtype: longterm   # 长期上下文

# type: knowledge
subtype: permanent  # 永久笔记

# type: experience
subtype: error      # 错误记录
subtype: success    # 成功案例
```

---

## 标签体系

| 标签 | 用途 | 示例 |
|------|------|------|
| `#对话` | 工作对话记录 | `#对话` |
| `#项目-XXX` | 属于某个项目 | `#项目-BTC` |
| `#知识` | 沉淀的知识 | `#知识` |
| `#错误` | 错误记录 | `#错误` |
| `#成功` | 成功案例 | `#成功` |
| `#灵感` | 随手想法 | `#灵感` |
| `#任务` | 任务相关 | `#任务` |

Emoji 标签前缀约定：

```
🧠知识   ⚡经验   📅日志   💬对话   📁项目   🔴错误   🟢成功
```

---

## 链接规范

### 核心原则

> 笔记不是孤岛，每篇笔记都应该连接到相关笔记。

### 链接数量要求（最少值）

| 笔记类型 | 所在层（目录） | 最少链接数 |
|---------|-------------|-----------|
| AI 核心层笔记 | 01, 09 | ≥5 条 |
| 知识卡片 | 05 | ≥3 条 |
| 项目总览 | 04 | ≥5 条 |
| 对话记录 | 03 | ≥2 条 |
| 每日日志 | 02 | ≥3 条 |

### 链接方向规范

```
上层笔记 → 下层具体内容（索引指向）
下层笔记 → 上层笔记（归属关系）
同层笔记 → 同层相关笔记（关联关系）
```

### 创建笔记时必检清单

- [ ] 是否连接到 `[[01-AI核心层/AI-当前活跃上下文]]`？
- [ ] 是否关联相关知识卡片？
- [ ] 是否连接到相关项目（如果有）？
- [ ] 是否满足最少链接数要求？

---

## 各层职责速查

| 层级 | 负责内容 | 不负责 |
|------|---------|--------|
| 00-系统层 | 系统入口、规则文档、临时存放 | 具体内容 |
| 01-AI核心层 | AI 记忆（上下文、技能、工具） | 用户内容 |
| 02-时间线层 | 按时间组织内容（日志、sessions） | 项目具体内容 |
| 03-对话层 | 原始对话记录 | 提炼后的知识 |
| 04-项目层 | 项目所有相关内容 | 非项目内容 |
| 05-知识层 | 沉淀后的知识（概念/原理/永久笔记） | 原始对话 |
| 06-经验层 | 错误记录、成功案例 | 一般知识 |
| 07-任务层 | 任务面板、收件箱任务 | 已完成任务详情 |
| 08-灵感层 | 随手灵感、闪念 | 成熟结论 |
| 09-用户画像层 | 用户基本信息、偏好 | AI 记忆 |
| 10-归档层 | 已结束项目归档 | 活跃内容 |

---

## 每日/每周工作流检查清单

### 每日（早晨）
- [ ] 打开今日日志（`02-时间线层/每日日志/YYYY-MM-DD.md`）
- [ ] 查看任务面板（`07-任务层/`）
- [ ] 确定今日重点
- [ ] 读取 `01-AI核心层/AI-当前活跃上下文.md`（告知 AI）

### 每日（傍晚）
- [ ] 更新今日日志
- [ ] 整理收件箱
- [ ] 更新 AI 上下文（如有大进展）
- [ ] 执行 `python3 ~/.openclaw/obsidian/hooks/save_session.py`

### 每周（周末）
- [ ] 写每周回顾（`02-时间线层/每周回顾/YYYY-WW.md`）
- [ ] 回顾项目进展，更新项目总览
- [ ] 整理收件箱，更新任务状态
- [ ] 提炼重要知识到知识层
- [ ] 更新 AI 长期上下文

---

## Hooks 配置参考

### hooks.json 示例

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.openclaw/obsidian/hooks/session_start_load.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.openclaw/obsidian/hooks/obsidian_session_load.py"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.openclaw/obsidian/hooks/session_end_summary.py"
          }
        ]
      }
    ]
  }
}
```

### 配置步骤

1. `mkdir -p ~/.openclaw/obsidian/hooks`
2. 运行 `python3 scripts/setup_hooks.py <vault_path>` 生成 4 个脚本到 `~/.openclaw/obsidian/hooks/`
3. 将 hooks.json 内容合并到你的 agent runtime 配置的 `hooks` 字段
4. 重启会话验证

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| Hook 不触发 | 检查 Python3 是否在 PATH 中可用 |
| Hook 执行无效果 | 检查 vault 路径配置是否正确 |
| 锁文件导致不注入 | 删除临时目录下的 `.openclaw_obsidian_locks/`（macOS/Linux: `/tmp/`，Windows: `%TEMP%`） |
| 脚本路径错误 | 确保使用绝对路径 |
