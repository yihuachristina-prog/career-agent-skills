# Career Agent Skills

**Evidence-based job search, JD matching, tailored resumes, and interview preparation for AI agents.**

[English](#english) · [中文](#中文)

## English

### Overview

Career Agent Skills provides four connected workflows for discovering jobs, evaluating a job description (JD), preparing application materials from real evidence, and preparing for interviews. It is intended for job seekers working with an AI agent and developers adapting that workflow to another user.

This edition focuses on **brand, content, and product marketing roles in China**. Its source workflows include Beijing, Shanghai, Hangzhou, and Guangzhou, Chinese recruitment sources, and Chinese Word-document conventions. Confirm these starting assumptions against each user's actual preferences.

The repository contains instructions, reference guides, helper scripts, and a blank user-profile template. Supply resumes, evidence, operational ledgers, and accounts separately in a private workspace. This is not a hosted recruitment service, a browser login package, or a background scheduler.

### Included Skills

| Skill | Use it when | Main result |
|---|---|---|
| [`run-job-search-pipeline`](.agents/skills/run-job-search-pipeline/SKILL.md) | Continuing a job search or choosing the next workflow. | Stage identification, routing, and handoff. |
| [`discover-brand-roles`](.agents/skills/discover-brand-roles/SKILL.md) | Searching for roles, verifying employers, or reviewing saved opportunities. | Source-backed opportunities, salary interpretation, coverage accounting, and ledger update proposals. |
| [`tailor-job-application`](.agents/skills/tailor-job-application/SKILL.md) | Evaluating a specific JD or organizing candidate evidence. | Company/role research, JD-to-evidence mapping, Apply/Pending/Skip decisions, tailored resume review drafts, and readiness notes. |
| [`prepare-job-interview`](.agents/skills/prepare-job-interview/SKILL.md) | Preparing for a target role with a confirmed resume, or explicitly practicing. | An eight-module preparation package, spoken answers, follow-up questions, knowledge-gap work, and mock interviews. |

The general **Skill Product Manager** has moved to [`productize-skills`](https://github.com/yihuachristina-prog/productize-skills). It is optional for developing workflows; ordinary career tasks do not require it.

### Installation and first use

1. Download the repository through **Code → Download ZIP**, or clone it:

   ```bash
   git clone https://github.com/yihuachristina-prog/career-agent-skills.git
   cd career-agent-skills
   ```

2. Open it as your agent's working project. Read [START_HERE.md](START_HERE.md) and [PORTABILITY.md](docs/PORTABILITY.md). Hosts supporting project Skill discovery can use `.agents/skills/`; otherwise, explicitly ask the agent to read the relevant `SKILL.md` and linked references.
3. Create a **private workspace outside the repository**. Copy and complete [the profile template](examples/user-profile.template.md) there, and provide the paths to your source materials. An existing private handoff package takes precedence for locating authoritative files.
4. Confirm target roles, cities, salary boundaries, evidence, and permitted actions. Missing information stays unknown; installation supplies neither candidate facts nor authorization.
5. Try one role or one search batch first. Inspect source coverage and actual outputs before expanding the task.

When installing elsewhere, preserve all **four Skill directories as siblings**, their support files, and `docs/PORTABILITY.md`. Tell the agent where the portability rules are stored. Compare and merge an existing installation instead of overwriting customizations.

### Inputs

| Input | Purpose |
|---|---|
| Target functions, industries, seniority, and cities | Prevents the original workflow defaults from silently becoming user preferences. |
| Current and expected salary boundaries | Supports explicit compensation comparisons; example numbers are not defaults. |
| Resume versions, verified experience, and work evidence | Supports truthful responsibilities, dates, ownership, and results. |
| JD, source URL, and company/role information | Defines the position and preserves traceability. |
| Existing job ledger, resume index, and capability library, if available | Continues from one authoritative state instead of creating competing copies. |
| Available browser, document, spreadsheet, and rendering tools | Determines which steps can actually be completed. |

Keep names, contacts, salaries, original work files, and credentials outside the public repository. Ignore rules reduce accidental commits but do not provide access control.

### Workflow and deliverables

1. **Orient:** identify the current stage, evidence, unfinished work, and relevant Skill.
2. **Discover:** search agreed sources, verify hiring entities, deduplicate roles, interpret salary, and record restrictions. For saved jobs, separately report total, scanned, deduplicated, and restricted counts; incomplete coverage remains partial.
3. **Evaluate:** research the company and role, map requirements to evidence, distinguish capability fit from screening probability, and explain Apply/Pending/Skip decisions and gaps.
4. **Prepare materials:** for eligible roles, create a Word review draft with company/JD context and a separate resume section, plus readiness notes. Use the full evidence library and preserve confirmed facts.
5. **Prepare interviews:** build spoken answers and follow-ups from the target role and confirmed resume. Label practice based on unconfirmed drafts explicitly.
6. **Verify and hand off:** check content, page rendering, authoritative versions, and authorized updates. Separate completed work from missing inputs and unavailable capabilities.

Deliverables depend on the supplied evidence and tools. A review draft is not an application submission. Automated document checks do not replace page-by-page visual review.

### Copyable examples

**Continue a job search**

```text
Use $run-job-search-pipeline. Read the repository entry points and my private
handoff package. Report the authoritative ledger, unfinished items, missing
sources, and next action. Continue only the stage I have requested.
```

**Evaluate a JD and prepare a review draft**

```text
Use $tailor-job-application with this JD and source URL. Verify the company
and role, use my full resume and evidence library, and explain fit and gaps.
If the role meets the workflow criteria, prepare a tailored resume review
draft and readiness notes. Do not invent experience or submit an application.
```

**Review saved opportunities**

```text
Use $discover-brand-roles to review saved jobs in the browser account I have
authorized. Report total, scanned, deduplicated, and restricted counts.
If a page is inaccessible, mark coverage as partial and preserve a checkpoint.
```

**Prepare an interview**

```text
Use $prepare-job-interview with this JD, verified company information, and
my confirmed final resume. Prepare spoken answers, two levels of follow-up
questions, evidence gaps, and a focused mock interview.
```

### Tools and dependencies

- An agent that can read files and follow Skill instructions.
- Search/browser tools for current job and company research. Signed-in pages require the receiving environment's authenticated browser; the Skills do not supply or transfer sessions.
- Python 3.10+ for helper scripts. When needed, install [requirements.txt](requirements.txt) in an appropriate environment:

  ```bash
  python -m pip install -r requirements.txt
  ```

- `python-docx` for Word inspection, `pypdf` for PDF reading, and `PyYAML` for Skill validation. Document rendering, spreadsheet editing, and required fonts must be available separately.
- [`vendor/skill-creator`](vendor/skill-creator/SKILL.md) is an optional packaging/validation tool snapshot, not a fifth career workflow.

See [PORTABILITY.md](docs/PORTABILITY.md) for salary parameters, resume markers, concurrent writes, and adaptation rules.

### Repository layout

```text
.agents/skills/
  run-job-search-pipeline/   Routing and handoff
  discover-brand-roles/     Discovery, coverage, salary, and ledger rules
  tailor-job-application/   Evidence matching and application materials
  prepare-job-interview/    Interview preparation and practice
docs/                      Portability rules and export history
examples/                  Blank user-profile template
vendor/skill-creator/      Third-party development/validation snapshot
START_HERE.md              Agent entry point
requirements.txt           Python helper dependencies
VALIDATION.json            Package-check scope and results
SHA256SUMS.json             File hashes, excluding this manifest itself
```

### Boundaries, verification, and licensing

Candidate facts must come from the current user's evidence. Plans are not proof of execution, and participation must not be inflated into ownership. Applications, recruiter messages, platform-state changes, and personal-file deletion require authorization for that action. Historical permissions do not transfer to a new user.

This is a portable export. Package checks cover structure, links, preserved files, and documented script regressions; they do not prove a successful live job-search run in every environment. Read [VALIDATION.json](VALIDATION.json) for the precise scope and [EXPORT_NOTES.md](docs/EXPORT_NOTES.md) for provenance. Browser access, rendering, and write-back need verification in the receiving environment.

No additional open-source license has been granted for the custom Skills. The vendored `skill-creator` retains its [Apache-2.0 license](vendor/skill-creator/license.txt), which does not automatically cover the rest of this repository.

Search terms: AI agent skills, job search workflow, JD matching, evidence-based resume, career assistant, brand marketing, content marketing, product marketing, interview preparation.

---

## 中文

### 项目简介

Career Agent Skills 提供四个相互衔接的求职工作流，覆盖**职位发现、JD 匹配、定向简历和面试准备**。适合与 AI Agent 协作求职的人，也适合为其他用户适配流程的开发者。

当前版本主要面向**中国市场的品牌、内容和产品营销岗位**。原流程包含北京、上海、杭州、广州四城、中文招聘来源和中文 Word 排版约定，使用前应核对这些初始设定是否符合当前用户需求。

仓库包含指令、参考规范、辅助脚本和空白用户配置模板。真实简历、经历证据、职位台账和账号由使用者在私密工作区单独提供。它不包含现成的招聘服务、浏览器登录状态或后台定时任务。

### 包含的 Skill

| Skill | 适用场景 | 主要结果 |
|---|---|---|
| [`run-job-search-pipeline`](.agents/skills/run-job-search-pipeline/SKILL.md) | 接续求职任务，或判断下一步调用哪个流程。 | 识别阶段、路由专业 Skill、整理交接状态。 |
| [`discover-brand-roles`](.agents/skills/discover-brand-roles/SKILL.md) | 搜索岗位、核验招聘主体，或检查收藏机会。 | 有来源的职位清单、薪资解释、覆盖情况和台账更新建议。 |
| [`tailor-job-application`](.agents/skills/tailor-job-application/SKILL.md) | 分析具体 JD，或整理候选人的完整能力证据。 | 公司与岗位情报、JD—证据映射、Apply/Pending/Skip 判断、定向简历审阅稿及补强说明。 |
| [`prepare-job-interview`](.agents/skills/prepare-job-interview/SKILL.md) | 根据目标岗位和已确认简历准备面试，或明确要求练习。 | 八模块准备包、口述答案、追问、知识补足和模拟面试。 |

通用的 **“Skill 产品经理”** 已迁移到独立的 [`productize-skills`](https://github.com/yihuachristina-prog/productize-skills) 仓库。开发或改造工作流时可按需使用，日常求职任务不依赖它。

### 安装与首次使用

1. 点击 **Code → Download ZIP** 下载仓库，或克隆：

   ```bash
   git clone https://github.com/yihuachristina-prog/career-agent-skills.git
   cd career-agent-skills
   ```

2. 把仓库作为 Agent 的工作项目打开，先读 [START_HERE.md](START_HERE.md) 和 [PORTABILITY.md](docs/PORTABILITY.md)。支持项目 Skill 发现的环境可读取 `.agents/skills/`；其他环境可明确要求 Agent 阅读对应的 `SKILL.md` 及其引用。
3. 在**仓库外建立私密工作区**，复制并填写[用户配置模板](examples/user-profile.template.md)，提供真实材料路径。已有交接包时，按其入口和路径映射定位唯一主库。
4. 确认岗位、城市、薪资边界、证据和允许执行的操作。缺失信息保留未知，安装不会提供个人事实或自动授予权限。
5. 先处理一个岗位或一小批结果，检查来源覆盖和实际输出后再扩大范围。

安装到其他位置时，保留**四个 Skill 文件夹的同级关系**、各自支持文件和 `docs/PORTABILITY.md`，告知 Agent 迁移规则的位置。已有安装时先比较再合并，避免覆盖本地修改。

### 需要准备的输入

| 输入 | 用途 |
|---|---|
| 目标职能、行业、职级和城市 | 避免把原流程预设自动当成当前用户偏好。 |
| 当前薪资与目标薪资边界 | 支持明确的薪资比较；示例数字不代表默认值。 |
| 简历版本、已核验经历和工作证据 | 支撑真实职责、日期、本人贡献和结果。 |
| JD、来源链接及公司与岗位信息 | 明确分析对象，保留追溯依据。 |
| 已有职位台账、简历资产索引和能力库 | 从唯一可信状态续接，避免多个相互冲突的主库。 |
| 浏览器、文档、表格和渲染工具 | 决定哪些步骤能够实际完成。 |

姓名、联系方式、薪资、原始工作资料和凭据应留在公开仓库之外。忽略规则可减少误提交，但不能替代访问控制。

### 工作流程与交付结果

1. **识别阶段：** 确认已有证据、未完成事项及对应 Skill。
2. **发现职位：** 在约定来源搜索，核验主体、去重、解释薪资并记录限制。收藏检查分别报告总数、已扫描、去重后和受限数量，覆盖不全就标记部分完成。
3. **判断岗位：** 调研公司与职位，将要求映射到真实证据，区分能力匹配与初筛可能性，说明 Apply/Pending/Skip 的理由及缺口。
4. **准备材料：** 对符合条件的岗位生成 Word 审阅稿，前置公司与 JD 信息，简历正文单独分节，并提供补强说明。使用完整证据库，保留已确认事实。
5. **准备面试：** 围绕岗位与已确认简历形成口述答案和追问；用未确认稿练习时标注演练性质。
6. **核验交接：** 检查内容、逐页渲染、主库版本及有授权的更新，区分实际完成、材料待补和工具受限事项。

实际产出取决于材料和工具。审阅稿不等于已经投递，自动格式检查也不能替代逐页视觉验收。

### 可直接使用的示例

**接续求职任务**

```text
使用 $run-job-search-pipeline，阅读仓库入口和我的私密交接包。
先报告唯一主库、未完成项、缺失来源和下一步，再继续我明确指定的阶段。
```

**分析 JD 并准备审阅稿**

```text
使用 $tailor-job-application 处理这份 JD 和来源链接。先核验公司与岗位，
再从我的完整简历库和经历证据中分析匹配与缺口。若符合流程条件，
制作定向简历审阅稿和补强说明，不虚构经历，也不自动投递。
```

**检查真实账号中的收藏机会**

```text
使用 $discover-brand-roles，在我授权的浏览器账号中检查收藏职位。
分别报告总数、已扫描、去重后和受限数量；页面打不开时标记部分完成，
保留检查点，不把未读取的收藏算作已核验。
```

**准备定向面试**

```text
使用 $prepare-job-interview，依据这份 JD、已核验公司信息和已确认最终简历，
准备口述答案、两层追问、证据缺口及一轮有重点的模拟面试。
```

### 工具与依赖

- 能读取文件并执行 Skill 指令的 Agent。
- 核验当前职位和公司的检索或浏览器工具。登录页面需要接手环境拥有对应的已登录浏览器，本仓库不提供或迁移登录状态。
- 辅助脚本需要 Python 3.10+；有需要时在合适环境安装 [requirements.txt](requirements.txt)：

  ```bash
  python -m pip install -r requirements.txt
  ```

- `python-docx` 用于 Word 检查，`pypdf` 用于 PDF 读取，`PyYAML` 用于 Skill 校验。文档渲染、表格编辑和所需字体需要另行具备。
- [`vendor/skill-creator`](vendor/skill-creator/SKILL.md) 是可选的打包与结构校验工具快照，不是第五个求职流程。

薪资参数、简历检查标记、并发写入和迁移细节见 [PORTABILITY.md](docs/PORTABILITY.md)。

### 目录结构

```text
.agents/skills/
  run-job-search-pipeline/   阶段识别与交接
  discover-brand-roles/     职位发现、覆盖、薪资与台账规则
  tailor-job-application/   证据匹配与申请材料
  prepare-job-interview/    面试准备与练习
docs/                      迁移规则与导出历史
examples/                  空白用户配置模板
vendor/skill-creator/      第三方开发与校验工具快照
START_HERE.md              Agent 接手入口
requirements.txt           Python 辅助脚本依赖
VALIDATION.json            打包检查范围与结果
SHA256SUMS.json             文件哈希，不包含清单自身
```

### 边界、验证情况与许可

候选人事实只能来自当前用户证据。方案不能写成已执行事实，参与不能夸大为主导。投递、联系招聘方、改变平台状态和删除个人文件均需要对应授权，历史权限不会自动转移。

本版是可迁移导出包。打包检查涵盖结构、引用、保留文件和已记录的脚本回归，不代表在所有环境完成过真实求职全流程。具体范围见 [VALIDATION.json](VALIDATION.json)，来源见 [EXPORT_NOTES.md](docs/EXPORT_NOTES.md)。接手环境仍需验证浏览器、渲染和写回能力。

原定制 Skills 未额外授予开源许可。第三方 `skill-creator` 保留原 [Apache-2.0 许可](vendor/skill-creator/license.txt)，不会自动扩展到整个仓库。

检索关键词：AI 求职助手、职业 Agent、职位搜索、JD 匹配、定向简历、经历证据库、品牌营销、内容营销、产品营销、面试准备、求职工作流。
