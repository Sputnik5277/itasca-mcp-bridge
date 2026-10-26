---
title: 煤岩与水作用研究的 Itasca 数值模拟资源图谱
subtitle: 从 Itasca 运行桥接到 AE 能量、空间破裂与可复用论文图源码
headline: 先建立可靠的模型与取数链路，再组织曲线、裂纹与 AE 图件
headline_detail: 将自己的维护仓、对应上游、建模技能和方法代码合并对照；保留旧工具与待核条目，后期按 SIM 编号逐项处理。
eyebrow: 数值模拟专项 · 2026-10-26
meta: 35 项仓库入口 · 自有维护仓 21/21 · SIM 稳定编号 · OMP 轻量长页
produced_by: codex (model ID unavailable)
produced_at: 2026-10-26 19:28 +08:00
last_edit_by: codex (model ID unavailable)
last_edit_at: 2026-10-26 21:05 +08:00
---

本专项服务于水作用煤岩力学研究，重点衔接论文1_2的 DIC 应变场与 AE 能量—空间双视角：寻找能够解释刚度退化、裂纹聚集及能量释放的 PFC 建模、试验模拟和后处理入口。以下“已核”指仓库文本与文件结构核对；研究适配与后期计划均为建议，不代表已经完成数值验证。

**项目归属与当前主线（2026-10-26 用户补充）：** 本报告现由 `Sputnik5277/itasca-mcp-bridge` 维护。后续以统一的 `itasca-mcp＋bridge` 为主线，PFC／FLAC3D／3DEC 分仓作为历史与迁移对照；UDEC 按用户说明继续独立维护，具体版本、仓库关系和台式机部署情况待后续回填。文档迁移不升级桥代码或修改运行配置。

上游核对中，旧 `yusong652/pfc-mcp` 的 API 请求已解析到 `yusong652/itasca-mcp`，支持入口合并这一判断；统一仓当前说明列有 PFC、FLAC、3DEC 等引擎。其他旧分仓和 UDEC 的 API 未取得可用记录，不能仅据此判定正式停止维护。以下日期与版本保留为迁移前核验快照，文档提交不视为引擎版本升级。

## 01 | 原四个核心仓库分别承担什么

原四仓内容继续保留；本次通过 `gh repo list` 和 `gh api` 补充自有仓、上游及方法仓。默认分支提交、根许可、仓库关系和入口以本次 [JSON 证据](itasca-supplement-evidence-20261026.json) 为快照；原 [逐仓维护证据](itasca-supplement-evidence-20261026.json) 保留来源身份。完整 SIM 编号清单见第 09、10 节。

| 仓库与 README | 层次及可交付物 | 已核提交日期／短 SHA | 根许可 |
| --- | --- | --- | --- |
| [itasca-mcp](https://github.com/yusong652/itasca-mcp/blob/main/README.md) | 文档检索、引擎桥接、任务执行与监控 | 10-24／f9a0e16 | MIT |
| [pfc-codex-skills](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/README.md) | 试样、标准试验、标定、场图与 AE 模板 | 08-09／743a111 | MIT，含独立许可子目录 |
| [asphalt-codex-skills-5](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/README.md) | PFC5 沥青专用流程、离线后处理示例 | 08-26（北京时间）／a47b379 | MIT |
| [itasca-parametric-skill](https://github.com/chendengji/itasca-parametric-skill/blob/master/README.md) | 工况生成、批算、结果汇总、网格标定与绘图 | 07-29／9474f46 | MIT |

PFC 技能包的双目标标定子目录另采用 AGPL-3.0-or-later，见 [NOTICE](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/dual-target-calibration/NOTICE.md)。根 MIT 记录不能代替具体复用文件的许可判断。

## 02 | 桥接运行层先解决执行与取数

已核 itasca-mcp 当前 README 将十个工具分为五个文档工具和五个执行工具；执行侧需要引擎内桥接。可从 [addon.py](https://github.com/yusong652/itasca-mcp/blob/main/addon.py) 和 [桥接客户端源码](https://github.com/yusong652/itasca-mcp/blob/main/src/itasca_mcp/bridge/client.py) 进入，README 中的[操作演示](https://raw.githubusercontent.com/yusong652/itasca-mcp/assets/itasca-mcp.gif)用于理解连接方式。

它提供调用模型、读取状态和导出数据的通道。煤岩接触本构、含水分组与加载路径仍需建模技能和研究者定义。此前笔记中的另一台电脑、四套 server 与旧桥接协议仅为历史快照，本轮没有核实当前电脑运行栈，也不据此替换现役配置。桥接本身不具备作为 colorplot 绘图卡的输入输出闭环。

## 03 | 建模与试验模拟从煤岩靶标开始

建议以 pfc-codex-skills 的标准试验和脆性岩石专题为主要候选，先建立干燥基准，再按实测浸水组标定弹性模量、峰值强度与破坏形态。含水作用如何映射到胶结刚度、强度或摩擦参数，需要实验与机制依据；仅降低一个参数不足以说明水致损伤机制。

批量工况可参考参数化仓的 [PFC3D 示例配置](https://github.com/chendengji/itasca-parametric-skill/blob/master/examples/pfc3d_ucs_fric/config.yaml)与[试样模板](https://github.com/chendengji/itasca-parametric-skill/blob/master/examples/pfc3d_ucs_fric/ucs_template.p3dat)。已读配置采用 PFC9，扫描摩擦与刚度，默认提取接触数、颗粒数和不平衡比；UCS 标定仍需自行实现提取函数，不能把示例命名当作完整强度标定结果。

asphalt 仓明确限定 PFC5 沥青材料。可借其数据契约与离线后处理组织方法；Burger、Marshall 和车辙参数不直接迁移到煤岩。

## 04 | 后处理把曲线、力链与裂纹连起来

PFC 技能包已提供 [plot_curves.py](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-postprocessing/scripts/plot_curves.py)、场图和玫瑰图脚本；三维入口是 [pfc_export.py](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-vedo-postprocess/scripts/pfc_export.py) 与 view_balls.py。已读[导出契约](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-vedo-postprocess/references/export-schema.md)列出颗粒位置、位移、接触法向力、裂纹中心和类型，并要求确认力的正负号及裂纹尺寸约定。

建议按峰前、峰值、峰后三个力学阶段对齐应力—应变、力链重排和张剪裂纹空间分布，再与 DIC 局部化带比较。表面 DIC 与内部颗粒场的观测范围不同，先统一坐标和阶段，再讨论空间对应。

可跳转查看 asphalt 仓的[已有示例帧](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/skills/pfc-postprocessing/examples/animation_case/raw_frames/jieguo_1.png)与[动画说明](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/skills/pfc-postprocessing/examples/animation_case/README.md)。这是仓库教学素材入口，本轮未逐像素审图，不作为本研究结果。

## 05 | AE 能量需要明确事件与量纲

旧笔记把 pfc-ae-energy 描述为纯参考资料；当前树中已见 [heavy-ae 模板](https://github.com/jiangnan030-del/pfc-codex-skills/tree/main/skills/pfc-ae-energy/templates/heavy-ae)，含裂纹回调、导出 FISH 和多种绘图脚本。已读 [plot_ae_energy.py](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-ae-energy/templates/heavy-ae/plot_ae_energy.py)开头包含 CSV 读取、积分与应变求导，并依赖案例 config；这仍是待适配模板。

建议分别记录断键、聚类事件、模型能量项和仪器 AE 能量，明确单位、时间窗、聚类规则及采样间隔，再比较累计变化与突增阶段。不能将一次断键等同一次实测 AE 事件，也不能直接把模型能量当仪器能量值；论文1_2可优先检验其与应变局部化是否同步。

## 06 | 论文图与可复用源码怎样交付

建议保留“输入数据—字段与单位—处理脚本—配置—图件”的完整链路。曲线和参数响应图可在数据契约稳定后评估接入 colorplot；力链、裂纹三维渲染应保留专用后端与相机配置。参数化仓的 [plot.py](https://github.com/chendengji/itasca-parametric-skill/blob/master/scripts/plot.py)已核为 results.csv 驱动的基础 PNG 绘图入口，仍需另做论文排版适配。

asphalt 的[最小案例](https://github.com/Echo-aloha/asphalt-codex-skills-5/tree/main/skills/pfc-postprocessing/examples/minimal_case)提供曲线、场与方向数据，可用于后续熟悉字段；教学数据与真实实验、模拟输出分开保存。本轮不生成图，也不新增工作台卡片。

## 07 | 后期待办与本轮纠正

后期按以下顺序推进：

- [ ] 锁定实际 PFC 版本与二维／三维要求，核实桥接和技能兼容性。
- [ ] 选择一个干燥基准试验，明确弹性模量、峰值强度和破坏形态等靶标。
- [ ] 适配并真实运行一个最小模型，核对导出字段、单位与 AE 能量定义。
- [ ] 扩展有实验依据的浸水工况，联动曲线、裂纹与 AE 阶段。
- [ ] 整理“预览图＋源码＋数据＋配色”成果包，再评估接入 Color Plot。

这些均为计划，本轮没有启动执行。

原四仓 README、定向文件树与上述源码／配置／案例说明继续作为研究路线依据，本次扩充的清单和读取范围另见第 08—13 节；这不是逐仓完整源码审计。PFC 技能包 README 自述 24 个技能，旧笔记题名为 27 个，故不以数量作为筛选依据。参数化 README 列 UDEC，但当前统一桥接 README 未列；采用桥接仓的当前范围，统一包的 UDEC 支持保留待核。自有 udec-mcp 单列，其 TCP FISH socket 架构不能由统一 HTTP 桥推定支持。

本机连接、脚本完整执行、图像质量及 PFC6/7 兼容性仍待后期验证；本轮没有安装或运行仿真。通用绘图卡的整理要求见 [Color Plot 专项](https://github.com/Sputnik5277/lu_color_plot/blob/main/docs/colorplot-card-research-20261026.md)。

## 08 | 35 项完整清单怎样使用

本页共 35 个仓库入口：自己的相关仓库 21 项，原四个外部仓库，另补统一桥接与 PFC5 分支 2 项、方法／上游候选 8 项。相对前稿新增 31 项。自己的维护副本和对应上游分别留档并注明关系，仓库数不等于独立能力数。

所有项目使用 SIM-001—SIM-035 稳定编号，后续直接指定编号处理。维护状态只按本次默认分支最近提交作快照，不将一次提交当作持续活跃。表内“源码入口”“图件文件”“数据／配置”表示文件或目录已定位，不保证彼此已构成可运行包；缺图、缺数据、许可未核和旧版本仍保留。

## 09 | 自己账号下的 21 项逐项清单

账号清单通过 gh repo list，limit 1000，以 itasca、pfc、flac、3dec、udec、acoustic、arma 等相关名称检出；这也保留了编辑工具、历史接口和方法副本，便于后期人工取舍。

| 编号与仓库 | 用途 | README／源码入口 | 图件与数据入口 | 最近提交／信号 | 根许可记录 | 后期动作 |
| --- | --- | --- | --- | --- | --- | --- |
| SIM-001 [Sputnik5277/itasca-mcp-bridge](https://github.com/Sputnik5277/itasca-mcp-bridge)；[关联上游](https://github.com/yusong652/itasca-mcp-bridge) | 引擎桥接／GUI 数据通道 | [README](https://github.com/Sputnik5277/itasca-mcp-bridge/blob/main/README.md) · [源码入口](https://github.com/Sputnik5277/itasca-mcp-bridge/blob/main/start_bridge.py) | 对应图件待核；独立数据待核 | [2026-10-05](https://github.com/Sputnik5277/itasca-mcp-bridge/commit/c9c333dc2fdc05ffe67aa4b9b49bf8b17cefd9e6)／近90天 | MIT | 先按具体客户端和引擎版本核对桥接协议；分别记录自己的维护副本和上游，暂不替换当前机器配置。 |
| SIM-002 [Sputnik5277/3dec-mcp](https://github.com/Sputnik5277/3dec-mcp) | 3DEC 专用 MCP | [README](https://github.com/Sputnik5277/3dec-mcp/blob/master/README.md) · [源码／示例目录](https://github.com/Sputnik5277/3dec-mcp/tree/master/src) | 对应图件待核；独立数据待核 | [2026-06-23](https://github.com/Sputnik5277/3dec-mcp/commit/3d7d81a0830f0e8b8b0252d9898e2aa7d6480b0c)／近一年 | 许可待核（未识别根 SPDX） | 历史／迁移对照：块体／节理问题沿统一入口核版本，保留旧仓示例和工具差异。 |
| SIM-003 [Sputnik5277/udec-mcp](https://github.com/Sputnik5277/udec-mcp) | UDEC 专用 MCP／TCP FISH | [README](https://github.com/Sputnik5277/udec-mcp/blob/master/README.md) · [源码／示例目录](https://github.com/Sputnik5277/udec-mcp/tree/master/src) | 对应图件待核；独立数据待核 | [2026-06-23](https://github.com/Sputnik5277/udec-mcp/commit/207372481e5e979765f55775cb2b991f5acd4168)／近一年 | 许可待核（未识别根 SPDX） | 按 TCP FISH socket 单独核对，不能直接接到统一 HTTP 桥；版本与本机运行待核。 |
| SIM-004 [Sputnik5277/flac3d-mcp](https://github.com/Sputnik5277/flac3d-mcp) | FLAC3D 专用 MCP | [README](https://github.com/Sputnik5277/flac3d-mcp/blob/main/README.md) · [源码／示例目录](https://github.com/Sputnik5277/flac3d-mcp/tree/main/src) | 对应图件待核；独立数据待核 | [2026-06-23](https://github.com/Sputnik5277/flac3d-mcp/commit/8424a90237e1652b9033a7ba9f773149aaa2551e)／近一年 | MIT | 历史／迁移对照：连续介质能力沿统一入口核版本，旧分仓的工具与资料另行映射。 |
| SIM-005 [Sputnik5277/pfc-mcp](https://github.com/Sputnik5277/pfc-mcp) | PFC 专用 MCP | [README](https://github.com/Sputnik5277/pfc-mcp/blob/main/README.md) · [源码／示例目录](https://github.com/Sputnik5277/pfc-mcp/tree/main/src) | 对应图件待核；独立数据待核 | [2026-06-23](https://github.com/Sputnik5277/pfc-mcp/commit/405f0caf091c6bed53d20302f14573fb5d1424e6)／近一年 | MIT | 历史／迁移对照：核案例、经验库与 code-history 如何衔接统一入口，不作为新的独立接入主线。 |
| SIM-006 [Sputnik5277/itasca-mcp-common](https://github.com/Sputnik5277/itasca-mcp-common) | per-product MCP 公共层 | [README](https://github.com/Sputnik5277/itasca-mcp-common/blob/master/README.md) · [源码／示例目录](https://github.com/Sputnik5277/itasca-mcp-common/tree/master/src) | 对应图件待核；独立数据待核 | [2026-06-10](https://github.com/Sputnik5277/itasca-mcp-common/commit/d13cf8e3417fbcadf848f6725fe788f12854a648)／近一年 | 许可待核（未识别根 SPDX） | README 仍描述 WebSocket；按所依赖的具体 server／桥版本核对，不与新统一桥混用。 |
| SIM-007 [Sputnik5277/flac-mcp](https://github.com/Sputnik5277/flac-mcp)；[关联上游](https://github.com/yusong652/flac-mcp) | FLAC MCP 维护副本 | [README](https://github.com/Sputnik5277/flac-mcp/blob/main/README.md) · [源码／示例目录](https://github.com/Sputnik5277/flac-mcp/tree/main/scripts) | 对应图件待核；独立数据待核 | [2026-06-03](https://github.com/Sputnik5277/flac-mcp/commit/9d70e9ae91e46c40109238c97ffaafa9a9f49ef4)／近一年 | MIT | 后置保留，与 FLAC3D 仓区分；按实际软件版本决定是否需要。 |
| SIM-008 [Sputnik5277/3dec-mcp-1](https://github.com/Sputnik5277/3dec-mcp-1)；[关联上游](https://github.com/charlie-945/3dec-mcp) | 另一份 3DEC fork | [README](https://github.com/Sputnik5277/3dec-mcp-1/blob/main/README.md) · [源码入口](https://github.com/Sputnik5277/3dec-mcp-1/blob/main/addon.py) | 对应图件待核；[数据／配置](https://github.com/Sputnik5277/3dec-mcp-1/blob/main/src/threedec_mcp/knowledge/resources/command_docs/commands/fracture/copy.json) | [2026-05-27](https://github.com/Sputnik5277/3dec-mcp-1/commit/1189f50bd9515395aa8509013c0331f6d28685c0)／近一年 | MIT | 先与主维护仓对照，确认差异后决定取舍，不作为另一套新能力重复接入。 |
| SIM-009 [Sputnik5277/Itasca-Bond-Damage-dll](https://github.com/Sputnik5277/Itasca-Bond-Damage-dll)；[关联上游](https://github.com/mociantia/Itasca-Bond-Damage-dll) | 胶结损伤／C++ 本构插件 | [仓库](https://github.com/Sputnik5277/Itasca-Bond-Damage-dll) · [源码入口](https://github.com/Sputnik5277/Itasca-Bond-Damage-dll/blob/main/Bond%20Damage%20usage%20examples/TX.dat) | [图件文件](https://github.com/Sputnik5277/Itasca-Bond-Damage-dll/blob/main/Model%20user%20guide.pdf)；独立数据待核 | [2025-02-10](https://github.com/Sputnik5277/Itasca-Bond-Damage-dll/commit/8a2f85bb7a548a45b13389a43ca20acc00986e2e)／超一年 | CC0-1.0 | 保留本构方法候选；先核引擎版本、编译工具链和模型参数，不直接将现成 DLL 用作已标定煤岩模型。 |
| SIM-010 [Sputnik5277/itasca-stub](https://github.com/Sputnik5277/itasca-stub)；[关联上游](https://github.com/panhaoyu/itasca-stub) | Python API 类型桩／开发辅助 | [README](https://github.com/Sputnik5277/itasca-stub/blob/master/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2023-05-14](https://github.com/Sputnik5277/itasca-stub/commit/ba90daf43c5fd991ed5e9b40ed64da2e3dd7d456)／超一年 | MIT | 用于补全和静态检查；不计作可运行试验模型或图模板。 |
| SIM-011 [Sputnik5277/PFC_pressure_pulse](https://github.com/Sputnik5277/PFC_pressure_pulse)；[关联上游](https://github.com/itascaconsulting/PFC_pressure_pulse) | 压力脉冲／渗透相关算例 | [README](https://github.com/Sputnik5277/PFC_pressure_pulse/blob/main/README.md) · [源码入口](https://github.com/Sputnik5277/PFC_pressure_pulse/blob/main/pfc_pressure_example/deliver/load.py) | [图件文件](https://github.com/Sputnik5277/PFC_pressure_pulse/blob/main/pfc_example.pdf)；[数据／配置](https://github.com/Sputnik5277/PFC_pressure_pulse/blob/main/pfc_pressure_example/deliver/README.txt) | [2023-06-13](https://github.com/Sputnik5277/PFC_pressure_pulse/commit/3581207b865d878bee02151437a2625c8c4b14b8)／超一年 | 许可待核（未识别根 SPDX） | 水作用方向候选：先核边界、流体变量、软件版本与输出定义，不直接视作局部浸水损伤模型。 |
| SIM-012 [Sputnik5277/matlab-flac](https://github.com/Sputnik5277/matlab-flac)；[关联上游](https://github.com/dkaramitros/matlab-flac) | MATLAB–FLAC 工具 | [README](https://github.com/Sputnik5277/matlab-flac/blob/main/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2023-05-24](https://github.com/Sputnik5277/matlab-flac/commit/baaf66d5c400cac876055ec7c5add3a0c8abc368)／超一年 | MIT | 保留接口与数据交换参考；MATLAB 依赖、版本和结果格式待核。 |
| SIM-013 [Sputnik5277/DEM_PFC2D_models](https://github.com/Sputnik5277/DEM_PFC2D_models)；[关联上游](https://github.com/kchiama/DEM_PFC2D_models) | PFC2D 断层变形模型 | [README](https://github.com/Sputnik5277/DEM_PFC2D_models/blob/main/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2023-05-05](https://github.com/Sputnik5277/DEM_PFC2D_models/commit/ae0cbc598354152df0340577b9bed450479f3304)／超一年 | 许可待核（未识别根 SPDX） | 可参考参数组织与变形场导出；地表断层算例需按煤岩试验另行建模。 |
| SIM-014 [Sputnik5277/Itasca-PFC3D-FISH_script-for-Notepad-plus-plus](https://github.com/Sputnik5277/Itasca-PFC3D-FISH_script-for-Notepad-plus-plus)；[关联上游](https://github.com/Wilson-TW/Itasca-PFC3D-FISH_script-for-Notepad-plus-plus) | PFC6 FISH 编辑辅助 | [README](https://github.com/Sputnik5277/Itasca-PFC3D-FISH_script-for-Notepad-plus-plus/blob/main/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2022-06-13](https://github.com/Sputnik5277/Itasca-PFC3D-FISH_script-for-Notepad-plus-plus/commit/a0c9f626e9e160ab3298a8d488bd7ffe67a87cf2)／超一年 | MIT | 后置工具项，核版本和编辑器配置；不作为仿真能力或科研图卡。 |
| SIM-015 [Sputnik5277/PFC3D_OpenFOAM](https://github.com/Sputnik5277/PFC3D_OpenFOAM)；[关联上游](https://github.com/itascaconsulting/PFC3D_OpenFOAM) | 流体—颗粒耦合 | [README](https://github.com/Sputnik5277/PFC3D_OpenFOAM/blob/master/README.md) · [源码入口](https://github.com/Sputnik5277/PFC3D_OpenFOAM/blob/master/pyDemFoam/setup.py) | [图件文件](https://github.com/Sputnik5277/PFC3D_OpenFOAM/blob/master/diagram.png)；[数据／配置](https://github.com/Sputnik5277/PFC3D_OpenFOAM/blob/master/porous/vel.txt) | [2022-01-29](https://github.com/Sputnik5277/PFC3D_OpenFOAM/commit/39e6330a8c7efd383d99af9750ce7cc810ff7b0c)／超一年 | 许可待核（未识别根 SPDX） | 保留水力耦合方向；先核 PFC／OpenFOAM 版本、双向耦合和验证算例，作为后期独立任务。 |
| SIM-016 [Sputnik5277/Itasca-3dec2Tecplot](https://github.com/Sputnik5277/Itasca-3dec2Tecplot)；[关联上游](https://github.com/absterguy/Itasca-3dec2Tecplot) | 3DEC5.2→Tecplot 后处理 | [README](https://github.com/Sputnik5277/Itasca-3dec2Tecplot/blob/main/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2021-06-23](https://github.com/Sputnik5277/Itasca-3dec2Tecplot/commit/21fb341d41917badbba629aeb7855a49e2e08a69)／超一年 | MIT | 旧版本转换参考；先核字段、坐标、单位与目标 Tecplot 格式。 |
| SIM-017 [Sputnik5277/Itasca_UDEC6.0_2_Tecplot360](https://github.com/Sputnik5277/Itasca_UDEC6.0_2_Tecplot360)；[关联上游](https://github.com/absterguy/Itasca_UDEC6.0_2_Tecplot360) | UDEC6→Tecplot 后处理 | [README](https://github.com/Sputnik5277/Itasca_UDEC6.0_2_Tecplot360/blob/main/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2021-06-20](https://github.com/Sputnik5277/Itasca_UDEC6.0_2_Tecplot360/commit/59d743ab0b2161880bfad06f1025aa0c6795e0c4)／超一年 | MIT | 旧版本转换参考；与现用 UDEC 输出对照后再决定适配。 |
| SIM-018 [Sputnik5277/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method](https://github.com/Sputnik5277/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method)；[关联上游](https://github.com/glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method) | PFC5 AE 事件／矩张量 | [README](https://github.com/Sputnik5277/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/blob/master/README.md) · [源码入口](https://github.com/Sputnik5277/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/blob/master/2D%20simulation/look_AE_2D.dat) | 对应图件待核；独立数据待核 | [2021-06-07](https://github.com/Sputnik5277/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/commit/5d45c425522d0cfed3a931b0a786d0b5b1bd8810)／超一年 | Apache-2.0 | 优先方法参考：核事件定义、聚类、矩张量和能量量纲，后续与实测 AE、DIC 阶段对齐。 |
| SIM-019 [Sputnik5277/2021_ARMA_frac](https://github.com/Sputnik5277/2021_ARMA_frac)；[关联上游](https://github.com/itascaconsulting/2021_ARMA_frac) | PFC／FLAC3D 岩石爆破耦合 | [README](https://github.com/Sputnik5277/2021_ARMA_frac/blob/main/README.txt) · [源码入口](https://github.com/Sputnik5277/2021_ARMA_frac/blob/main/load.py) | [图件文件](https://github.com/Sputnik5277/2021_ARMA_frac/blob/main/matrix.png)；[数据／配置](https://github.com/Sputnik5277/2021_ARMA_frac/blob/main/fistSrc/dirContents.txt) | [2021-02-07](https://github.com/Sputnik5277/2021_ARMA_frac/commit/48168fa7fc84d2399f500f76986b4a3ef8679375)／超一年 | 许可待核（未识别根 SPDX） | 保留动力破裂与耦合算例；不能把爆破参数直接用于准静态浸水煤岩。 |
| SIM-020 [Sputnik5277/itasca-python](https://github.com/Sputnik5277/itasca-python)；[关联上游](https://github.com/itascaconsulting/itasca-python) | 旧 Python 连接接口 | [README](https://github.com/Sputnik5277/itasca-python/blob/master/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2020-07-24](https://github.com/Sputnik5277/itasca-python/commit/91c766abc64e4940605b454ef96ad694926b61d7)／超一年 | 根正文为 BSD 三条款结构；子目录另核 | 低优先接口历史参考；README／各目录许可、当前原生 SDK 替代关系与版本另核。 |
| SIM-021 [Sputnik5277/itasca-emacs](https://github.com/Sputnik5277/itasca-emacs)；[关联上游](https://github.com/jkfurtney/itasca-emacs) | FISH／数据文件编辑辅助 | [README](https://github.com/Sputnik5277/itasca-emacs/blob/master/README.md) · 独立源码入口待核 | 对应图件待核；独立数据待核 | [2017-06-02](https://github.com/Sputnik5277/itasca-emacs/commit/3d15dd1b70d6db69b0f4758a3e28b8b506cc84ca)／超一年 | 许可待核（未识别根 SPDX） | 旧编辑工具保留，不进入模型或图卡配额。 |

## 10 | 外部研究主线、上游与补充候选 14 项

同一家族的上游保留为追溯与比较入口；空仓和许可未明确的旧仓只留待核记录。前四仓的研究路线仍见第01—07节。

| 编号与仓库 | 用途 | README／源码入口 | 图件与数据入口 | 最近提交／信号 | 根许可记录 | 后期动作 |
| --- | --- | --- | --- | --- | --- | --- |
| SIM-022 [yusong652/itasca-mcp](https://github.com/yusong652/itasca-mcp) | 新统一 MCP／文档与执行 | [README](https://github.com/yusong652/itasca-mcp/blob/main/README.md) · [源码／示例目录](https://github.com/yusong652/itasca-mcp/tree/main/scripts) | 对应图件待核；独立数据待核 | [2026-10-24](https://github.com/yusong652/itasca-mcp/commit/f9a0e16fb1fbccf913a118a63d10ee0b5091e49f)／近90天 | MIT | 与旧 per-product 工具面、案例／经验库及桥接逐项比较，保持当前配置至兼容性核实。 |
| SIM-023 [jiangnan030-del/pfc-codex-skills](https://github.com/jiangnan030-del/pfc-codex-skills) | 建模、标定、AE、力链裂纹 | [README](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/README.md) · [源码入口](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/dual-target-calibration/adapters/check.py) | [图件文件](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-postprocessing/examples/animation_case/raw_frames/jieguo_1.png)；[数据／配置](https://github.com/jiangnan030-del/pfc-codex-skills/blob/main/skills/pfc-fast-calibration/agents/openai.yaml) | [2026-08-09](https://github.com/jiangnan030-del/pfc-codex-skills/commit/743a1119be791eee52b69d8e292167e02d6a29df)／近90天 | MIT；标定子目录另有 AGPL | 研究主线：先选干燥基准和标准试验，再用可追溯字段串起力学、裂纹与能量图；注意子目录独立许可。 |
| SIM-024 [Echo-aloha/asphalt-codex-skills-5](https://github.com/Echo-aloha/asphalt-codex-skills-5) | PFC5 沥青技能／离线后处理 | [README](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/README.md) · [源码入口](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/skills/pfc5-ae-energy/scripts/ae_energy_metrics.py) | [图件文件](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/skills/pfc-postprocessing/examples/animation_case/raw_frames/jieguo_1.png)；[数据／配置](https://github.com/Echo-aloha/asphalt-codex-skills-5/blob/main/skills/pfc5-servo-calibration/dependencies.json) | [2026-08-26](https://github.com/Echo-aloha/asphalt-codex-skills-5/commit/a47b37940efec2434929b70ff7c1c255a3975881)／近90天 | MIT | 借鉴数据契约、示例组织和后处理源码；沥青材料参数与煤岩分开。 |
| SIM-025 [chendengji/itasca-parametric-skill](https://github.com/chendengji/itasca-parametric-skill) | 参数扫描／批算／结果汇总 | [README](https://github.com/chendengji/itasca-parametric-skill/blob/master/README.md) · [源码入口](https://github.com/chendengji/itasca-parametric-skill/blob/master/scripts/calibrate.py) | 对应图件待核；[数据／配置](https://github.com/chendengji/itasca-parametric-skill/blob/master/examples/pfc3d_ucs_fric/config.yaml) | [2026-07-29](https://github.com/chendengji/itasca-parametric-skill/commit/9474f46cdb7b2f41b9405b5fadca05a89ed0c811)／近90天 | MIT | 核 master 分支示例、桥接依赖和提取函数；UCS 目标提取及 PFC 版本仍需适配。 |
| SIM-026 [yusong652/itasca-mcp-bridge](https://github.com/yusong652/itasca-mcp-bridge)；对应 SIM-001 | 引擎桥接／GUI 数据通道 | [README](https://github.com/yusong652/itasca-mcp-bridge/blob/main/README.md) · [源码入口](https://github.com/yusong652/itasca-mcp-bridge/blob/main/start_bridge.py) | 对应图件待核；独立数据待核 | [2026-10-20](https://github.com/yusong652/itasca-mcp-bridge/commit/bb18b430e654d615add4e31fa2ba71dbb4bc2aea)／近90天 | MIT | 先按具体客户端和引擎版本核对桥接协议；分别记录自己的维护副本和上游，暂不替换当前机器配置。 |
| SIM-027 [molt213/itasca-mcp-pfc5.00](https://github.com/molt213/itasca-mcp-pfc5.00) | 统一 MCP 的 PFC5 兼容分支 | [README](https://github.com/molt213/itasca-mcp-pfc5.00/blob/main/README.md) · [源码入口](https://github.com/molt213/itasca-mcp-pfc5.00/blob/main/addon.py) | 对应图件待核；[数据／配置](https://github.com/molt213/itasca-mcp-pfc5.00/blob/main/bridge/itasca_mcp_bridge/_compat_marker.txt) | [2026-07-16](https://github.com/molt213/itasca-mcp-pfc5.00/commit/df98738625859e6531a7564889749cdbcf8dbf2c)／近一年 | MIT | 与旧 PFC5 MCP、上游统一包比较；先核实际接口／桥与特定版本，不据仓库名认定本机可运行。 |
| SIM-028 [mociantia/Itasca-Bond-Damage-dll](https://github.com/mociantia/Itasca-Bond-Damage-dll)；对应 SIM-009 | 胶结损伤／C++ 本构插件 | [仓库](https://github.com/mociantia/Itasca-Bond-Damage-dll) · [源码入口](https://github.com/mociantia/Itasca-Bond-Damage-dll/blob/main/Bond%20Damage%20usage%20examples/TX.dat) | [图件文件](https://github.com/mociantia/Itasca-Bond-Damage-dll/blob/main/Model%20user%20guide.pdf)；独立数据待核 | [2025-02-10](https://github.com/mociantia/Itasca-Bond-Damage-dll/commit/8a2f85bb7a548a45b13389a43ca20acc00986e2e)／超一年 | CC0-1.0 | 保留本构方法候选；先核引擎版本、编译工具链和模型参数，不直接将现成 DLL 用作已标定煤岩模型。 |
| SIM-029 [glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method](https://github.com/glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method)；对应 SIM-018 | PFC5 AE 事件／矩张量 | [README](https://github.com/glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/blob/master/README.md) · [源码入口](https://github.com/glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/blob/master/2D%20simulation/look_AE_2D.dat) | 对应图件待核；独立数据待核 | [2021-06-07](https://github.com/glx5027/Acoustic-emission-and-moment-tensor-simulation-with-discrete-element-method/commit/5d45c425522d0cfed3a931b0a786d0b5b1bd8810)／超一年 | Apache-2.0 | 优先方法参考：核事件定义、聚类、矩张量和能量量纲，后续与实测 AE、DIC 阶段对齐。 |
| SIM-030 [itascaconsulting/PFC3D_OpenFOAM](https://github.com/itascaconsulting/PFC3D_OpenFOAM)；对应 SIM-015 | 流体—颗粒耦合 | [README](https://github.com/itascaconsulting/PFC3D_OpenFOAM/blob/master/README.md) · [源码入口](https://github.com/itascaconsulting/PFC3D_OpenFOAM/blob/master/pyDemFoam/setup.py) | [图件文件](https://github.com/itascaconsulting/PFC3D_OpenFOAM/blob/master/diagram.png)；[数据／配置](https://github.com/itascaconsulting/PFC3D_OpenFOAM/blob/master/porous/vel.txt) | [2022-01-29](https://github.com/itascaconsulting/PFC3D_OpenFOAM/commit/39e6330a8c7efd383d99af9750ce7cc810ff7b0c)／超一年 | 许可待核（未识别根 SPDX） | 保留水力耦合方向；先核 PFC／OpenFOAM 版本、双向耦合和验证算例，作为后期独立任务。 |
| SIM-031 [itascaconsulting/PFC_pressure_pulse](https://github.com/itascaconsulting/PFC_pressure_pulse)；对应 SIM-011 | 压力脉冲／渗透相关算例 | [README](https://github.com/itascaconsulting/PFC_pressure_pulse/blob/main/README.md) · [源码入口](https://github.com/itascaconsulting/PFC_pressure_pulse/blob/main/pfc_pressure_example/deliver/load.py) | [图件文件](https://github.com/itascaconsulting/PFC_pressure_pulse/blob/main/pfc_example.pdf)；[数据／配置](https://github.com/itascaconsulting/PFC_pressure_pulse/blob/main/pfc_pressure_example/deliver/README.txt) | [2023-06-13](https://github.com/itascaconsulting/PFC_pressure_pulse/commit/3581207b865d878bee02151437a2625c8c4b14b8)／超一年 | 许可待核（未识别根 SPDX） | 水作用方向候选：先核边界、流体变量、软件版本与输出定义，不直接视作局部浸水损伤模型。 |
| SIM-032 [itascaconsulting/2021_ARMA_frac](https://github.com/itascaconsulting/2021_ARMA_frac)；对应 SIM-019 | PFC／FLAC3D 岩石爆破耦合 | [README](https://github.com/itascaconsulting/2021_ARMA_frac/blob/main/README.txt) · [源码入口](https://github.com/itascaconsulting/2021_ARMA_frac/blob/main/load.py) | [图件文件](https://github.com/itascaconsulting/2021_ARMA_frac/blob/main/matrix.png)；[数据／配置](https://github.com/itascaconsulting/2021_ARMA_frac/blob/main/fistSrc/dirContents.txt) | [2021-02-07](https://github.com/itascaconsulting/2021_ARMA_frac/commit/48168fa7fc84d2399f500f76986b4a3ef8679375)／超一年 | 许可待核（未识别根 SPDX） | 保留动力破裂与耦合算例；不能把爆破参数直接用于准静态浸水煤岩。 |
| SIM-033 [825811880/PFC3D-Calibration](https://github.com/825811880/PFC3D-Calibration) | PFC3D 微参数标定 | [README](https://github.com/825811880/PFC3D-Calibration/blob/master/README.md) · 独立源码入口待核 | 对应图件待核；[数据／配置](https://github.com/825811880/PFC3D-Calibration/blob/master/test.txt) | [2019-03-13](https://github.com/825811880/PFC3D-Calibration/commit/86605bbc647075bff3ee739ee68b2041751ef6ee)／超一年 | 许可待核（未识别根 SPDX） | 历史标定方法候选；先核宏观靶标、参数空间、算法与许可，再讨论适配。 |
| SIM-034 [ChenXu16/Micro_parameters-calibration-of-PFC3D](https://github.com/ChenXu16/Micro_parameters-calibration-of-PFC3D) | 微参数标定占位／空仓 | [仓库](https://github.com/ChenXu16/Micro_parameters-calibration-of-PFC3D) · 独立源码入口待核 | 对应图件待核；独立数据待核 | 无可读提交／空仓／待核 | 许可待核（未识别根 SPDX） | 本次 API 返回空仓 409／404；仅保留待核入口，不进入当前实施队列。 |
| SIM-035 [klfy0405/agent-pfc3d5-triaxial-calibration](https://github.com/klfy0405/agent-pfc3d5-triaxial-calibration) | PFC3D5 三轴标定 agent | [README](https://github.com/klfy0405/agent-pfc3d5-triaxial-calibration/blob/main/README.md) · [源码入口](https://github.com/klfy0405/agent-pfc3d5-triaxial-calibration/blob/main/triaxial_agent/cli.py) | 对应图件待核；[数据／配置](https://github.com/klfy0405/agent-pfc3d5-triaxial-calibration/blob/main/client_mcp.example.json) | [2026-10-21](https://github.com/klfy0405/agent-pfc3d5-triaxial-calibration/commit/6626075028c8a601ad373da7d4ce643752f76033)／近90天 | MIT | 新增较近的标定候选；先核围压、宏观靶标、优化过程、输入输出与真实求解回执。 |

## 11 | 按研究需要逐项处理的队列

先确定当前机器和实际 PFC 版本，再沿统一 itasca-mcp＋bridge 与技能包各选一个最小试验；旧分仓仅用于工具面和数据迁移对照。以下队列共用完整表编号，所有实施项均待办。

| 优先方向 | 对应编号 | 后期可单独执行的任务 | 交付形式 |
| --- | --- | --- | --- |
| 运行与桥接 | SIM-005, SIM-001, SIM-022, SIM-026 | 以统一 itasca-mcp＋bridge 为主线核当前配置，per-product 仅作迁移对照，再完成受控最小任务 | 版本／协议对照、真实运行与取数回执 |
| 煤岩干燥基准 | SIM-023, SIM-025 | 明确 E、峰值强度与破坏形态靶标，补实际提取函数再做参数扫描 | 模型源码、参数、输入与结果表 |
| AE／能量／裂纹 | SIM-023, SIM-029 | 区分断键、聚类事件、模型能量与仪器 AE；核矩张量、时间窗、量纲 | 分阶段曲线、裂纹场、处理源码与字段约定 |
| PFC5 分支与标定 | SIM-027, SIM-035, SIM-024 | 按实际版本决定是否需要，先核接口和三轴靶标，不直接套沥青参数 | 兼容性记录、最小模型及处理图 |
| 水作用／耦合后期专题 | SIM-031, SIM-030 | 先研究渗透／耦合边界与验证算例，再讨论含水／局部浸水参数映射 | 有实验依据的工况设计及后处理 |
| 可复用图卡 | SIM-025, SIM-024 | 先稳定曲线／统计数据字段，再按 Color Plot 卡包要求整理 | 预览图＋源码＋示例数据＋配色；力链三维另保留相机配置 |


## 12 | 台式机、桥接协议与许可的具体纠正

历史笔记的 C:\Users\11408\Desktop\itasca-mcp\ 指向原机器快照。2026-10-02 的观察包含 pfc-mcp 405f0ca 和 bridge 本地改动；后续条目提出 git pull 建议，没有找到台式机更新完成的回报。当前电脑或台式机的安装、服务及引擎可用性仍待核，不能由仓库存在或 pushed_at 推断。

自己的 bridge 默认分支为 c9c333dc／0.6.3（2026-10-05），仓库另有 10-20 推送活动。其 README 实际是 HTTP＋SSE，GitHub 简介的 WebSocket 措辞已落后；本次与上游 main 比较落后 3 提交。common 的 README 仍描述 WebSocket，udec-mcp 使用 TCP FISH socket，各自依赖必须按版本核对，不能只看包名统一替换。

参数化仓默认分支为 master，本页修正原 main 链接。PFC 技能包根 MIT 不覆盖全部子目录；itasca-python 虽被 API 标为 NOASSERTION，根许可正文有 BSD 三条款结构且说明子目录可另有许可，不应仅凭元数据认定无许可或限制严格。其他未识别根许可的条目继续待核。

## 13 | 本轮检索记录、待筛入口与范围

本轮以自己的 21 仓及 fork／来源关系追溯为主要增量，另做六组主题、每组原查询与收窄／改写查询，共 12 次 GitHub 搜索。组合词零命中不代表没有相关项目，具体查询与结果见下表和 [补充证据](itasca-supplement-evidence-20261026.json)。35 项清单完成身份／默认分支提交／根目录与许可入口盘点；19 处定向树和 README／源码片段仅覆盖所记录对象，不代替逐仓运行。

| 主题组 | 原查询／返回总数 | 改写查询／返回总数 |
| --- | --- | --- |
| 1 | Itasca PFC coal water fracture／0 | Itasca PFC water in:readme／2 |
| 2 | PFC acoustic emission moment tensor／0 | PFC acoustic emission／0 |
| 3 | PFC FLAC3D rock fracture／0 | PFC FLAC3D fracture／0 |
| 4 | 3DEC UDEC fracture FISH／0 | 3DEC fracture／0 |
| 5 | Itasca parameter calibration PFC／0 | UDEC FISH／0 |
| 6 | PFC hydromechanical water coupling／0 | PFC calibration／9 |

另有 7 个搜索命中未纳入上述 35 项，保留待筛入口；它们可能是聚合清单或其他领域技能，尚未按源码／图件／许可核对。

:::accordion
### 展开未核搜索命中

| 待筛编号 | 仓库 | 命中组 | 状态 |
| --- | --- | --- | --- |
| SIM-P001 | [JinZhangLab/PFCE](https://github.com/JinZhangLab/PFCE) | 6 | 待筛／尚未核对功能 |
| SIM-P002 | [MoonSoon69/awesome-mcp-servers-punkpeye](https://github.com/MoonSoon69/awesome-mcp-servers-punkpeye) | 1 | 待筛／尚未核对功能 |
| SIM-P003 | [Zehebi29/engineering-skill-hub](https://github.com/Zehebi29/engineering-skill-hub) | 1 | 待筛／尚未核对功能 |
| SIM-P004 | [konush/PFClusterCalib](https://github.com/konush/PFClusterCalib) | 6 | 待筛／尚未核对功能 |
| SIM-P005 | [kw3rk/actinf-pfc](https://github.com/kw3rk/actinf-pfc) | 6 | 待筛／尚未核对功能 |
| SIM-P006 | [mmylly/PFCalibration](https://github.com/mmylly/PFCalibration) | 6 | 待筛／尚未核对功能 |
| SIM-P007 | [spandeyehep/PFCalibration](https://github.com/spandeyehep/PFCalibration) | 6 | 待筛／尚未核对功能 |

:::

本次完成清单扩充、来源入口与后期待办整理；安装、仿真、桥接迁移、真实图件复现与台式机部署均未启动。后续按编号逐项修改，通用图卡要求仍见 [Color Plot 专项](https://github.com/Sputnik5277/lu_color_plot/blob/main/docs/colorplot-card-research-20261026.md)。
