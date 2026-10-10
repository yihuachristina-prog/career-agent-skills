# 导出记录

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
