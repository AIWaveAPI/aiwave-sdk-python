# AGENTS.md — AIWave Python SDK（云端代理操作手册）

本文件约束所有自动化代理（Codex 云端、CI、脚本）在本仓库的行为。违反任一红线 = 立即停止并报告，不要自行修复。

## 你在操作什么

AIWave（https://aiwave.live/）的官方 Python SDK：OpenAI 兼容客户端封装，发布到 PyPI。读者通过 pip 安装后调用付费 API——**README 与 docstring 里的每个数字都会被当成定价事实**。

## 权威数据源（唯一事实）

- **实时价格**：`https://aiwave.live/api/pricing` —— 运行时 `data` 数组长度即模型数，**不要在本文件里写死数字**
  （2026-11-25 实测 91 行；历史写的 97 已过期，删掉即为此故）
- `/api/v1/pricing` 是 **2026-10-24 冻结的 51 行快照**（自带 `checked` 字段自证），禁止用于"现价"表述
  - 与实时端点不是同一份数据的两个视图：实测仅 44 个 ID 相交，另有 7 个 ID 已不在实时价卡上
  - 两者对同时存在的 42 个 token 计费模型价格一致，故可作**交叉校验**，不可作**数据源**
- 文档里不写静态模型总数。要写计数就写"以 `/api/pricing` 当前返回为准"，并给出核验方式
- 任何写进 README/docstring/示例的价格或模型 ID，必须能逐字回溯到实时端点；回溯不了就不写数字
- 模型 ID 必须真实在售（以服务器 abilities 路由为准，端点在场 ≠ 在售）
- 计费单位不可一概而论：`quota_type` 为 1 是按次、为 0 是按 token，同一类目（如视频）内部也会混用

## 营销红线（主理人已否决，禁止出现）

- ❌ 未上线功能预告（免费层未上线，不得写 "free tier included" 类表述）
- ❌ 一键切换话术（"just change one string" / "swap base_url and go"）
- ❌ 无证据竞品断言
- ❌ 未实测的性能/延迟数字

## 写操作规则

- 分支 → commit → PR（草稿）。不直接 push main；不自行 merge
- 版本号遵循 SemVer；破坏性 API 变更必须 major
- 发布流程（仅主理人授权后）：版本 bump → changelog → tag → 发布。**代理不得自行发布 PyPI**
- 提交前：`python -m compileall -q .` + 现有测试全过；涉及文档数字时对照实时端点
- 凭据（PyPI token、测试 API key）永不入库；`.env` 只在本地

## 事实冲突裁决

现场锚点与文档/记忆冲突时以现场为准，双源复核后再下结论。单一来源 grep 0 = 假阴性候选。
