---
title: Itasca 数值模拟工具与煤岩研究——第二批学习汇报
subtitle: 四组源码核读＋补充批（Bond-Damage／技能包深挖／待筛裁决）
produced_by: zcode (GLM)
produced_at: "2026-10-27 +08:00"
last_edit_by: zcode (GLM)
last_edit_at: "2026-10-27 +08:00"
---

# 总重点

1. 执行链以本机 per-product pfc-mcp 为主链：统一版（yusong652/itasca-mcp，SIM-022）仅 10 工具，本机版 20 工具为功能超集；统一版价值仅在单会话切多产品。
2. 试验骨架以 SIM-023 的 2D UCS 六存态闭环为最短路径（PFC6，linearpbond），但全仓无煤参数、无平节理脚本、无 history export 桥接。
3. AE 与 DIC 阶段对照走 heavy-ae 链（六阶段×源类型交叉表）；glx5027（SIM-018/029）R 值分类仅作第二口径。
4. 补充批关键发现：SIM-009/028 Itasca-Bond-Damage-dll 证实为**可追溯损伤变量框架**（D 演化律＋(1-D) 刚度强度连续折减，附带 PFC7 dll），是水致损伤机制解释的最直接候选——但模型无水项，需实验映射。
5. 最危险静默错误：SIM-025 case 目录纯序号无参数哈希，改网格必须换 project.dir。
6. 7 项待筛全部裁决为**排除**：均为名称撞车（粒子物理 Particle Flow、近红外光谱、前额叶皮层），与 Itasca PFC 无关。

# 一、四组源码核读（要点）

## 第一组：统一执行与取数（SIM-022／SIM-001,026）

- 端到端：`itasca_execute_task`（tools/execute_task.py:20，6 位 task_id）→httpx POST localhost:9001（bridge/client.py:191，不重试、trust_env=False）→`ScriptRunner.run`（execution/script.py:40）→`MainThreadExecutor`（main_thread.py:158）cycle-gap 泵出→stdout 落盘 `.itasca-mcp-bridge/logs/`＋脚本 `result` 变量回传。CSV 由用户脚本自写。
- bridge 自升级默认开启（upgrade.py maybe_upgrade L309）；固定实验版本设 `ITASCA_MCP_BRIDGE_AUTO_UPGRADE=0`。GUI/console 模式选择在 runtime.py:276。自有版落后上游 3 提交（c6620b4/45e244e/bb18b43）均为稳定性修复，利好长 solve。
- 本机 pfc-mcp 多 FISH 文档、案例库、经验库、错误库、code_history；`program call` 在 PFC 6/7 锁桥、9.7+ 全响应（本机实测 9.7）。

## 第二组：煤岩建模与标定（SIM-023 首轮）

- UCS 六存态：`1chengyang`(成样)→`2yuya`(伺服预压 0.1MPa，Get_zonggang/addVel)→`3liewen`(30°裂隙)→`3jiaojiaojie`(restore 装 linearpbond+bond)→`4xiezai`(卸载)→`5jiazai`(删侧墙、strainrate 0.1/s、挂 fracture.p2fis)。教学参数 emod 1e9/pb_ten 10e6；FISH 全局 width/wly 靠存态传递。
- 宏观提取在 pfc-fast-calibration/scripts/canonical/extract_macro_metrics.py（UCS L39、E 0.0005–0.0015 割线 L28、σcd L50-53）。缺口：UCS 链无 history export；平节理零脚本；grep coal 零命中。
- dual-target 契约＝adapters/check.py 的 trials.csv（result.csv 单行 A/B＋params.json），与 SIM-025 result.json 不直接兼容。

## 第三组：参数化研究（SIM-025）

- 链：config.yaml→generate_cases.py（case_%04d 纯序号）→run_study.py（L260 串行、续跑只认 status=ok）→bridge→case_run.py.tpl（L148 逐条 it.command、L96 `__iparam_<idx>` 一次性 FISH 求值）→result.json{params,metrics,extract_errors,status}（partial=取值失败）→collect_results.py 平铺 CSV→calibrate.py（match=|v−t|/|t| 单目标）→calibration_report.txt。
- UCS 示例补全：重写 ~150 行 p3dat（linearpbond＋压板伺服＋峰值/E 提取）＋config 30 行；host 脚本零改动（方案A 标量提取）。与 bridge 0.6.3/0.6.4 四端点兼容已核。

## 第四组：AE、能量与裂纹

- heavy-ae：track_init（fracture-heavy-mt.p2fis:193）cache_bond_state@39.9＋add_crack@bond_break→add_ae_event（L114，逐断键 hit，伪 MT=断前胶结力×力臂，mt_xy 对称化）→ae_events.csv（13 字段）＋stress_strain.csv（同源 weyy/wsyy）→cluster_hits_to_events（plot_ae_energy.py:102，时间窗 max(10×median Δt,2.5e-4s)）→cluster_stage（L767）六分段（O-A…Post-Peak）×源类型交叉表——DIC 阈值填 `stage_[a-d]_strain` 即自动出图。
- glx5027（PFC5）：look_AE 在线聚合（时间 AE_long=30 步＋空间 6×ball.radius）、barycenter_find 体积加权质心、moment_tensor 不平衡力×力臂 9 分量、R=tr×100/(|tr|+Σm) 三分类（3D ±30／2D −45/46）。移植 6/7 必改：`ball.force.unbal(bp,1)` 分量语法、`ration_R` 拼写（3D dat:64）。
- 能量三口径（glx5027 ΔE／heavy-ae pbstrain_energy／曲线梯形积分）未统一；2D mt_zz=0 与 3D Mw 量纲不可比；断键≠仪器 AE 事件。

# 二、补充批A：SIM-009/028 Itasca-Bond-Damage-dll（源码核读）

两仓为纯镜像（fork，3 提交一致 8a2f85bb，2025-02-10）。来源论文：Zheng J & Ciantia MO (2025) RMRE, doi 10.1007/s00603-025-04411-0。

- **本构**：模型 `dbondrotation`（PB 模板扩展，ContactModelDBondrotation.h:23）。损伤变量 D_（h:464，属性 `D_var`）逐接触 0→1，演化律 `D = 1 − exp(−(|u_n^p|/ucn + |u_s^p|/ucs + |θ^p|/ucb))`（cpp:2666–2674，拉域 ucn／压域 ucn1，源自 Nguyen et al. 2017 IJP）。三维屈服面 F=|M/M̄|^1.001+(N/N̄)²+(V/V̄)⁴/(1−(N/N̄)²)−1（cpp:1933），最近点投影回映＋一致切线含损伤耦合（cpp:2499–2552）。**卸载 D 不增长、路径依赖、拉压双向累积**。
- **退化**：pb_kn1/pb_ks1/pb_ten1/pb_com1/pb_coh1=(1−D)·原值（cpp:2678–2685），D>0.99 断键（cpp:2938，触发 bond_break＋键应变能）。
- **无水项**：grep water/moist/humidity/saturat/wett 零命中——水致损伤只能靠"不同饱和度→各组参数"实验映射。
- **接入**：仓库附带编译好 dll（187KB，PFC7）＋示例链（pb_change.dat→preload→TX 三轴）。`program load contactmodelmechanical '...dll'`→cmat model DBondrotation→property pb_ten/pb_com/pb_coh/ucn/ucn1/ucs/ucb。注意 pb_change.dat:3 dll 路径缺闭合引号。
- **参数**：与 linearpbond 同名同义 pb_kn/pb_ks/pb_ten/pb_coh/pb_mcf 等；新增 pb_com（压强度）、ucn/ucn1/ucs/ucb（软化位移阈值）、诊断量 Npd/Spd/Bpr/Fy；移除 pb_fa。迁移成本中低。
- **导出**：`D_var`/`Fy`/`Npd`/`Spd`/`Bpr` 均逐接触可读（`contact.prop(cp,'D_var')`），损伤带可视化需自写 FISH（仓库无现成脚本）。
- **验证**：作者声明尺寸无关性/颗粒放大律/桩贯入（论文正文），源码证实损伤-塑性框架实现；对白垩灰岩（孔隙率 0.5、E 1 GPa 量级）的标定质量不在仓库——**煤需全套重标，ucn/ucs/ucb 靠 UCS 峰后曲线反演**。

# 三、补充批B：SIM-023 第二次深挖

- **"贝叶斯标定"实为 GP-EI 代理优化**（无 MCMC/似然/先验采样）：`_campaign_common.py:505 propose_bayes_candidate`，GP(RBF+WhiteKernel)/RF(300 树)/二阶 RSM 5 折交叉验证选型，5000 候选池 EI（xi=0.01），每轮 1 次真跑；可选 optuna_tpe。目标=加权平方残差 Σw·((metric−value)/tol)²。
- **路线选择**：≤2 杠杆 2 目标→dual-target；≥3 参数多目标→BO 默认（预算 50-70% 初探/20-30% 局部/10-20% 确认）；粗糙目标→DE 兜底；LPBM 全参初定→13 因子正交。d=4 时 BO ≥36 次真跑＋1 次独立确认（代理预测不算标定结果）。
- **vedo NPZ**：pfc_export.py:34-41 导出 cr_pos(K,3)/cr_nrm(K,3)/cr_size/cr_type(0拉1剪)——位置+法向+尺寸+类型齐全，可做 Ripley K/方位玫瑰/DIC 叠加；但 cr_size 口径未固化、仅瞬时快照无 per-stage 回调、力链 c_fn 符号需核。
- **P1-P7 与 G0-G9**：G0-G9 全为内容条件（版本/可溯性/seed/平衡/CMAT/重平衡/加载/测量/V&V/交付），无自动检查，"文件存在≠通过"。CI validate_skills.py 只保仓库卫生（结构/UTF-8/五章节/断链/密钥/绝对路径），不跑 pytest 不验示例。
- **27 skill 盘点**：煤岩直接相关 12（standard-tests/ae-energy/stress-wave-aelocation/gbm-brittle-rock/mineral-heterogeneity/brittle-rock-bpm/flat-joint/equivalent-crystal/fast-calibration/dual-target/vedo/servo-calibration）；通用支撑 8；其他用途 6（dynamics/fluid/flac-coupling/sand-small-strain/freeze-thaw/xxd-data-viz）；治理 1。skill-index.md 缺 3 条目。
- **契约缺口**：pfc-workflow（runs.csv metric__*）与 dual-target trials.csv、parametric result.json 零衔接，共用需自写 adapter；runner.command_template 需自写 PFC wrapper（读 params.yaml→跑→写 metrics.json）。

# 四、7 项待筛裁决（全部排除）

| SIM-P | 仓库 | 事实 | 裁决 |
| --- | --- | --- | --- |
| P001 | JinZhangLab/PFCE | MATLAB，近红外光谱参数无关标定（2023 停更） | 排除：NIRS 领域，名称撞车 |
| P002 | MoonSoon69/awesome-mcp-servers-punkpeye | MCP server 清单 fork | 排除：清单类，无 Itasca 内容 |
| P003 | Zehebi29/engineering-skill-hub | Python，泛工程 AI skill 集（2026-08 活跃） | 排除：无 Itasca/PFC 专属内容 |
| P004 | konush/PFClusterCalib | Python，CMS/LHC ECAL 粒子流簇标定（2015） | 排除：粒子物理 PF≠Itasca PFC |
| P005 | kw3rk/actinf-pfc | Python，本地 LLM 主动推理编排 | 排除：PFC=前额叶皮层 |
| P006 | mmylly/PFCalibration | Python 472GB，CMS Run2 强子标定 | 排除：粒子物理 |
| P007 | spandeyehep/PFCalibration | C，Particle Flow 强子标定（2018） | 排除：粒子物理 |

待筛队列清零；35 项 SIM 主清单不变。

# 五、研究任务—工具—缺口—产物对照表（更新版）

| 研究任务 | 主用工具 | 现成可借 | 需补缺口 | 产物 |
| --- | --- | --- | --- | --- |
| 干燥基准（应力-应变/E/峰值/形态） | SIM-023 六存态链＋本机 pfc-mcp | 六 .dat、fracture.p2fis、extract_macro_metrics.py | history export 桥接；煤参数 | 曲线＋UCS/E＋DFN 裂纹图 |
| 参数标定 | SIM-025 框架＋SIM-023 靶标（≤2 杠杆）或 GP-EI BO（≥3 参） | 四 host 脚本；lhs/run_campaign/fit/optimize | UCS 模板重写；E/UCS/peak_strain 靶标；标定三系统间 adapter | results.csv／runs.csv＋报告 |
| 浸水分区/参数映射 | SIM-025 扫描框架 | 断点续跑、partial 语义 | 浸水分区建模、饱和度→参数组实验映射（全空白） | 分区参数表＋组间曲线 |
| 损伤机制解释（新增） | SIM-009/028 DBondrotation | D_var 演化律＋(1-D) 折减＋PFC7 dll＋D 逐接触导出 | 煤参数全套重标（ucn/ucs/ucb 靠峰后反演）；损伤带导出 FISH；无水项须实验映射 | 损伤场云图＋D-应变演化 |
| 能量演化 | heavy-ae＋plot_ae_energy.py | 曲线弹性/耗散积分、pbstrain_energy | 三口径统一 | 能量-应变曲线 |
| AE 事件 | heavy-ae（主）＋glx5027 R 值（副） | ae_events.csv、聚类、R 分类 | CSV 契约；口径声明 | 事件表＋聚类表 |
| 裂纹空间场 | vedo pfc_export NPZ | cr_pos/cr_nrm/cr_size/cr_type | cr_size 口径固化、per-stage 回调 | 裂纹盘/方位玫瑰/局部化带 |
| DIC 阶段对照 | plot_ae_energy.py 六分段 | cluster_stage 交叉表 | 论文1_2 DIC 阈值回填 | 阶段×源类型占比图 |

# 六、三个最小实施候选（先后依赖 1→2→3，均未执行）

1. **干燥基准 UCS 闭环冒烟**：本机 PFC6/7 跑通六存态链＋heavy-ae，验两 CSV 同源性。需用户补：本机/台式机 PFC 版本与 2D/3D、模型尺寸与颗粒数上限。预期：首条可复核曲线＋AE 事件表。
2. **标定扫描接通**：新 project 目录重写 UCS 模板（~150 行 p3dat），2-3 工况冒烟再扩网格；若采用 DBondrotation 路线，参数集切至 pb_ten/pb_com/pb_coh/ucn 系列（先在干态跑通示例链与 linearpbond 基线对比）。需用户补：干燥煤样 E/峰值/peak_strain 靶标与参数范围。
3. **AE-DIC 阶段对照**：回填 stage_[a-d]_strain，输出六阶段×源类型交叉表；vedo per-stage NPZ 同步对齐。需用户补：论文1_2 DIC 阶段阈值。

# 七、边界与未完成项

- 本轮全部源码核读＋建议验收判据，无模拟结果；未启动引擎、未调用 bridge、未安装升级。
- 未完成：三份 docs 的逐节精读（批 2-B，只完成摘要级）；bridge 剩余模块（signals/utils/tests）速览。均不阻塞上述候选。
- 仍缺失（另机库外）：itasca-first-batch-review-20261026.md/.html；D:/codex备份/20261026-itasca-album/evidence/ 六套证据 JSON。
- 本机待补（用户）：PFC 版本与 2D/3D、干燥煤样标定靶标、论文1_2 DIC 阈值。

完整证据与流程图在 Obsidian vault：Itasca知识库/跨产品/ 下《第二批源码核读-20261027》《代码流程图-20261027》。
