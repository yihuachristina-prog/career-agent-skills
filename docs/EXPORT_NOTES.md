# 导出记录

## 当前仓库范围：职业流程与通用开发拆分

2026-10-10，在原导出版本基础上拆分通用开发流程：

- 当前 `.agents/skills/` 仅保留四个职业 Skill：流程调度、职位发现、定向申请和面试准备。
- `productize-skills` 的三个文件已迁移到独立的 [productize-skills 仓库](https://github.com/yihuachristina-prog/productize-skills)，不再通过本仓库安装。其核心内容保持原样。
- 保留 `vendor/skill-creator` 作为可选的打包与结构校验工具及第三方许可快照，不计入职业 Skill 数量。
- README 重写为详细英文在前、中文在后；入口、迁移说明、仓库指引、验证记录和哈希清单同步更新。
- 四个职业 Skill 及其脚本、参考、配置和素材保持原文件内容。原安装目录和私密资料归档未修改。
- 下方是原导出历史记录，其中“五个 Skill”描述的是拆分前版本，不代表当前安装清单。

## 原导出历史

导出日期：2026-10-10。原安装文件未修改。

- 完整保留 5 个自定义 skill 目录及支持文件，去掉 Python 缓存。
- 原个人姓名、固定职业经历、历史真实简历例句、具体任务 ID 与个人薪资默认值从仓库版移除。
- 原项目资产根路径换为 `data/`；个人完整版使用独立映射，不改原始工作簿。
- 薪资 CLI 改为要求显式阈值，姓名检查参数化，具体项目检查支持显式词表。算法主体保持原版。
- 原用户清理授权不转移；迁移说明和 skill 入口明确此边界。
- 系统 skill-creator 单列 vendor，并保留原许可；不冒充用户原创。
- 所有原版文件及个人资料仅在单独的私密归档中。

通过本次结构和参数测试，不代表在新 agent、新用户上已完成真实任务试运行。新环境启用前应验证实际浏览器、文档渲染、字体和写回能力。

导出适配的文件：

- `.agents/skills/discover-brand-roles/references/shared-data-contract.md`
- `.agents/skills/discover-brand-roles/scripts/normalize_salary.py`
- `.agents/skills/discover-brand-roles/SKILL.md`
- `.agents/skills/prepare-job-interview/SKILL.md`
- `.agents/skills/run-job-search-pipeline/SKILL.md`
- `.agents/skills/tailor-job-application/references/candidate-baseline.md`
- `.agents/skills/tailor-job-application/references/candidate-writing-style.md`
- `.agents/skills/tailor-job-application/references/current-version-retention.md`
- `.agents/skills/tailor-job-application/references/package-maintenance.md`
- `.agents/skills/tailor-job-application/references/radar-review-package.md`
- `.agents/skills/tailor-job-application/references/recruiter-outreach.md`
- `.agents/skills/tailor-job-application/references/resume-content-quality-gate.md`
- `.agents/skills/tailor-job-application/references/shared-data-contract.md`
- `.agents/skills/tailor-job-application/references/targeted-resume-format.md`
- `.agents/skills/tailor-job-application/scripts/audit_resume_delivery.py`
- `.agents/skills/tailor-job-application/SKILL.md`
