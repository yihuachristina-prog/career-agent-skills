# Career Agent Skills

品牌、内容与产品营销求职工作流的可迁移归档。包含 4 个职业 skills、1 个基础产品化开发 skill，以及系统开发工具 `skill-creator` 的带许可快照。

| Skill | 用途 |
|---|---|
| run-job-search-pipeline | 识别求职阶段并协调下列专业流程 |
| discover-brand-roles | 职位发现、主体核验、收藏覆盖与机会维护 |
| tailor-job-application | JD 匹配、证据选择、定向简历与补强说明 |
| prepare-job-interview | 基于确认简历准备面试与追问 |
| productize-skills | 需求研究、产品定义、开发路线和试运行 |
| vendor/skill-creator | Skill 目录规范、初始化与结构校验 |

## 接手方式

1. 阅读 [START_HERE.md](START_HERE.md) 和 [迁移规则](docs/PORTABILITY.md)。
2. 支持项目 skills 的 agent 可在本仓库工作并发现 `.agents/skills/`；其他 agent 直接读取对应 `SKILL.md` 和按需引用。
3. 安装到其他目录时，保留 5 个 skill 文件夹的同级关系，一并携带 `docs/PORTABILITY.md`。不要覆盖已有 skills；先比较并合并。Codex 已有系统 `skill-creator` 时优先使用现有版本；其他环境可读取 `vendor/skill-creator/SKILL.md`。
4. 在仓库外为当前用户建立私密工作区，按 [配置模板](examples/user-profile.template.md) 配置。没有个人数据时只做输入检查，不虚构简历、薪资或搜索状态。

本仓库不含个人简历、台账、证据库、联系方式、登录凭据或用户授权。它保留品牌营销、四城七源与中文 Word 版式的领域预设；不是已经部署的多用户服务。新增用户分别隔离资料、授权和运行状态；换行业、城市或流程时按基础开发 skill 再迭代。

这是已有流程的归档及参数脱敏版本。本次核验包括目录、引用、语法、参数回归与压缩包完整性，未替每个新 agent 执行真实搜索/生成/投递全流程。招聘搜索须接入接手环境的浏览器或检索工具；Word/PDF 渲染、字体和表格工具需单独具备。未配置这些能力不得声称已完成相关验收。

个人完整版须单独由资料所有者提供。仓库中的 `data/`、`private/` 等路径被忽略；不要通过强制添加把个人资料提交进仓库。详细改动见 [导出说明](docs/EXPORT_NOTES.md)。

原定制 skills 未额外授予开源许可。第三方 `skill-creator` 保留原 [Apache-2.0 许可](vendor/skill-creator/license.txt)；未将其他内容自动改为该许可。
