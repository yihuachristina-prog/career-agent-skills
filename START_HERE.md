# 给接手 Agent 的入口

先读 `docs/PORTABILITY.md`，识别本次是“接手某一用户的求职”，还是“继续开发通用 skills”。

- 接手求职：读取该用户独立的交接包 `START_HERE.md`、主库、能力库和缺失清单，然后调用 `run-job-search-pipeline`。保留岗位/资产/证据 ID 和当前状态。
- 开发 skills：先读取 `.agents/skills/productize-skills/SKILL.md`；开发规范来自 `vendor/skill-creator/SKILL.md`。原用户历史授权不适用于新用户。
- 只分析一个 JD：调用 `tailor-job-application`，按限定范围完成，不自动扩展为完整求职流程。
- 没有个人交接包：从 `examples/user-profile.template.md` 收集必要输入。不要从本仓库推断候选人事实。

推荐首次指令：

> 阅读本仓库入口和我提供的私密交接包。先报告读到的主库版本、未完成项、缺失来源和下一步；依据已有规则继续处理我明确指定的求职阶段。不得自动投递或联系招聘方。

工具差异由当前 agent 适配。文档中的历史工具名不是对当前可用权限的证明；使用当前实际可用工具，缺能力时明确记录对应未完成项。
