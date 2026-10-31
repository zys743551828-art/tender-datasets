# SYNTHETIC 第14号最终技术澄清补遗

本目录是添加式、可复现的公开合成 fixture，只准备一个新 positive-normal 组合：同级 `synthetic-fullflow-20261031` 的 **10号招标（tender）+ 本目录14号补遗（supplement）+ 12号正文（body）**。不修改旧09–13、旧manifest或历史失败结果。所有主体、文书效力和岗位均完全虚构，不是现实单位、签章、官方评分、真实地质资料或真人签收。

`generated/14_technical_final_clarification_SYNTHETIC.docx` 复用同级原生成器的 `make_doc` 确定性OOXML/ZIP，不复制其实现。只有纯文本、静态页码，无动态域或外部关系。`14-content.json` 是从实际DOCX提取的完整段落，便于审阅；`manifest.json` 记录新增原件字节摘要及受保护旧文件摘要；`expected.json` 只有机制期望和未冻结schema模板，不是API请求。

14号明确10号原件的文件名、标题、第1版及DOCX摘要，当前依据仅10+14，14优先；旧11号已由14整体吸收，不是本新案例的输入，也不要求另补。T01全部120天工期引用失效、唯一现行值为90天；C30和输入登记/检查/输出步骤不变。T04在本轮确定明挖、不采用顶管的条件下不适用；未来工法变更须另有新文书，不自动恢复。T05明确虚构责任岗位、开挖及支护批准前核实的时点与未核实后果，**但当前仍无现场土层资料、核实或批准记录，必须保留unknown/待人工核实**。仅做技术符合性，评分项、分值和额外废标机制不适用，不填零分或伪造官方分。

`ambiguity-map.json` 仅保留先前三次合成提取中的14条歧义、来源文件摘要/定位及对应候选澄清；不是原始模型全文。其 `evidence-local-...` 路径是原验收工作区的历史定位，相关完整运行日志不随fixture复制。不能据该文件声称新材料已消歧。

**未验证模型质量或新业务通过。** 本目录没有执行转换、解析、来源发布、模型提取、评审或冻结；实际PDF页数仍null，schema模板仍not_frozen/主体pending。模型可能继续报告歧义、漏项或gaps，必须保留真实结果、全部规则分母及正常准入，不得强改complete。只根据后续真实结果决定是否扩展conflict/missing；本目录不发调用。

从datasets仓根目录，用显式选择的现有Python3.12解释器运行：

```powershell
& $Python312 ./fixtures/technical-authority-clarification-20261031/generate.py
& $Python312 ./fixtures/technical-authority-clarification-20261031/generate.py --check
```

生成器相对定位 `../synthetic-fullflow-20261031`，没有个人绝对路径或task目录依赖。其导入复用原生成器已安装的Pillow，不安装新依赖、不联网、不读业务配置。若要验证schema模板，使用现有已安装jsonschema并显式给出应用schema：

```powershell
& $Python312 ./fixtures/technical-authority-clarification-20261031/generate.py --check --schema ../tender-app-dev/workbench/packages/contracts/schemas/bid-package.schema.json
```

应用仓目录名按实际检出位置调整；schema是可选的只读输入。生成器拒绝未知目录内容、符号链接或不同已有字节，不覆盖旧corpus。跨平台重建同一DOCX应保持固定ZIP时间/排序；实际转换与字体呈现需后续独立核验。
