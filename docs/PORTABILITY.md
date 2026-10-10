# 迁移与多用户配置

本说明是导出包的参数适配层。四个职业 skills 的入口均要求先读本说明；它覆盖旧文中“本项目”“用户已确认”“常设授权”等指向原使用者的限定。保留现有专业判断和事实核验要求，原环境权限不转移。

## 每个用户的独立资料

在仓库外使用 `<workspace>/<user-id>/`；里面放 `候选人画像与薪资边界.md` 和 `data/`。`data/` 包含唯一 `品牌职位台账.xlsx`、`简历资产索引.xlsx`、`经历证据库.xlsx`、`个人能力库.md`、运行状态及 `application_packages/`。同名文件不能按修改时间猜测主库。已有私密交接包必须以它的入口和 PATH_MAP 为准，不覆盖原主库。

每个用户的姓名、实际经历、日期、工资、城市、原稿、确认记录和账号均单独读取。四城（北京/上海/杭州/广州）和七来源是本版品牌营销预设；不符合时先明确新范围，不悄悄沿用。历史日期仅说明流程来源。

## 授权

所有“已授权清理”“自动删除”措辞只表示执行已有授权时的流程，不构成当前用户授权。没有当前用户已确认的范围、精确清单和核验，停在 plan。任何清理脚本的 apply 均须单独满足当前权限，禁止仅凭安装本包执行。投递、联系招聘方和平台状态改变继续要求当前用户明确指令。

## 参数与脚本

Python 3.10+。Word 检查依赖 `python-docx`，PDF 读取需要 `pypdf`；安装依赖应遵循接手环境的授权和管理方式。薪资、覆盖和清理脚本主要使用标准库。

薪资脚本已移除原候选人的默认数值，五项参数必须显式来自当前用户：

```text
python .agents/skills/discover-brand-roles/scripts/normalize_salary.py "20-30K·13薪" --current-annual 180000 --current-monthly-base 15000 --offer-floor 200000 --listing-max-floor 240000 --listing-min-preference 180000
```

以上数字仅用于语法示例，不是任何用户的默认边界。Python 调用 `normalize(text, profile)` 必须传五项完整 profile；缺参数会报错，不按零处理。

简历检查姓名由 `--name-marker` 提供，可重复；具体项目词由 `--case-marker` 提供，可重复。审阅区定位或格式检查缺姓名会停止。未提供项目词时不会自动检查特定项目名称，仍须人工核查个人简介。

```text
python .agents/skills/tailor-job-application/scripts/audit_resume_delivery.py resume.docx --name-marker "候选人姓名" --after-page-break --check-format
```

文档旧命令示例如未列新参数，按本说明补齐。字体、排版和自动检查通过不等于逐页视觉通过，更不等于用户认可或已投递。

## 并发与恢复

同一用户同一主库采用单写者；写前核对新鲜哈希，先暂存后窄范围合并、回读和验收。跨 agent 交接只迁移必要数据和明确状态。换用户时不要继承账号、授权、个人阈值或本地路径。

本包不实现后台调度、账号管理或服务端租户隔离。需要开发这些功能时，可按需使用独立的 [productize-skills 仓库](https://github.com/yihuachristina-prog/productize-skills)；该流程已从本仓库迁出，不是普通求职任务的安装依赖。不要把目录约定宣传为已完成多用户系统。
