# workbuddy.md — 开发对话记录（WorkBuddy 联动活动奖励核验材料）

> 本作品全程在 WorkBuddy 中开发。本文为开发对话上下文的整理导出，记录需求输入、
> 设计决策与产出物，用于核验 WorkBuddy 联动活动奖励条件。

## 会话背景

- 开发时间：2026 年 10 月 25 日
- 开发环境：WorkBuddy（官方合作伙伴推荐开发平台）
- 目标赛道：WaytoAGI 1024 切磋大会「用餐」赛道 × 麦当劳程序员创意开发大赛
- 工作目录：`E:/allthings/mcd`

## 开发对话纪要

### 第 1 轮：需求输入

用户提出：阅读麦当劳点餐赛道开发文档（https://1024.waytoagi.com/tracks/dine 与
官方仓库 https://github.com/M-China/mcd-developer-innovation-challenge），并结合
其已有的"慧眼系统核心侧写引擎"（行为与心理侧写类 Skill，16 法则大一统框架），
设计并实现一个适用于麦当劳点餐赛道的 Skill 产品，按官方要求整理参赛仓库。

WorkBuddy 动作：
1. WebFetch 读取用餐赛道文档 → 提取关键要求：用麦当劳 MCP、形式不限、Skill 可同步
   参加麦当劳大赛、评审看"真的调用了 MCP + 实用或好玩至少占一样"、仓库必须包含
   README.md / CONTEST_DECLARATION.md（不可改动）/ MCP_INTEGRATION.md / 源代码 / workbuddy.md。
2. WebFetch 读取官方参赛仓库 → 提取参赛文件清单、报名 Issue 格式、Star 排名规则。
3. WebFetch 读取 CONTEST_DECLARATION.md 原文 → 原样复制，零改动。
4. WebFetch 读取麦当劳 MCP Server 指南 → 提取全部 Tool 列表、鉴权与限流规则。
5. 读取用户提供的 profile.txt（慧眼侧写引擎完整提示词）。

### 第 2 轮：产品概念设计

WorkBuddy 提出融合方案：**「麦门侧写师 McProfiling」——点单即人格**。

- 侧写引擎 16 法则特化为「点单十二律」（酱料控制律、冰块情绪律、优惠反射弧律、
  加购冲动律等），把麦当劳点单微操变成心理解码素材。
- 输出保留原引擎的 6 模块结构与黑客终端排版，模块六改为"麦门金句"，便于截图传播。
- 关键闭环：侧写不是终点——"人格套餐"通过 MCP 落地为真实订单（查菜单 → 领券 →
  算价 → 下单），同时满足"好玩"（侧写社交货币）与"实用"（真实点餐省钱）两个评审点。

用户确认方案，进入实现。

### 第 3 轮：Skill 实现

WorkBuddy 产出：

1. `skill/SKILL.md`：Skill 主文件，定义 4 阶段工作流（输入采集 → 侧写运算 → 报告输出
   → MCP 执行）、触发词、安全红线（知情同意、下单双确认、Token 占位符、限流纪律）。
2. `skill/references/profiling-engine.md`：点单侧写引擎（I/O 模态解码矩阵 + 点单十二律
   + 6 模块运算指令 + 排版规范）。
3. `skill/references/mcp-playbook.md`：MCP 调用手册（13 个 Tool 的调用时机表、标准
   调用链、失败降级策略、WorkBuddy 连接器配置 JSON）。
4. `skill/examples/report-samples.md`：完整示例报告样张（周五深夜加班场景）+
   侧写 → 下单对话示例。
5. `demo/index.html`：离线交互式演示页（黑客终端风格，输入点单碎片生成报告，
   含模拟 MCP 执行序列展示，无需 Token 即可体验核心玩法）。

### 第 4 轮：参赛材料与仓库整理

WorkBuddy 产出参赛材料并初始化 Git 仓库：

- `README.md`：项目介绍、安装方法（Token 申请 → 连接器配置 → Skill 安装）、使用示例、目标用户。
- `CONTEST_DECLARATION.md`：官方原文，未做任何改动。
- `MCP_INTEGRATION.md`：Server 信息、13 个实际使用 Tool 的业务角色表、六步调用流程图、业务价值与安全声明。
- `workbuddy.md`：本文件。
- `git init` + 首次提交；提交后按官方 Issue 格式完成报名（见下方"提交清单"）。

## 提交清单（对照官方要求）

| 官方要求 | 状态 | 文件 |
|---|---|---|
| README.md | ✅ | README.md |
| CONTEST_DECLARATION.md（内容不可改动） | ✅ | CONTEST_DECLARATION.md（官方原文） |
| MCP_INTEGRATION.md | ✅ | MCP_INTEGRATION.md |
| 源代码 | ✅ | skill/ 全部文件 + demo/index.html |
| workbuddy.md | ✅ | 本文件 |
| 公开 GitHub 仓库 | 待用户推送 | 推送后在官方仓库发报名 Issue |

## 报名 Issue 模板（推送后使用）

```
【参赛申请】
项目名称：麦门侧写师 McProfiling
项目地址：<你的仓库 URL，纯文本，不要 Markdown 链接格式>
项目简介：基于麦当劳 MCP 的点单行为侧写 Skill：输入点单碎片（时段/辣度/冰量/用券习惯），输出黑客终端风格心理侧写报告，并按"人格裁定"自动完成查菜单、领券、计价与真实下单，实现"先读懂你，再喂饱你"的点餐闭环。
```
