# SYNTHETIC 全流程机制材料

所有内容均为虚构合成材料，不是真实招标、投标、企业资质、工程量、价格或官方成绩。只用于用户已授权的独立测试，不进入真实案例库、模型训练或正式成绩配对集。

## 生成和复核

在 `tender-datasets` 根目录运行，先把 `$Py` 显式设为已有应用虚拟环境的 Python 路径；不复制其他机器的 venv，不安装新依赖、不联网。

```powershell
& $Py -B fixtures/synthetic-fullflow-20261031/generate.py
& $Py -B fixtures/synthetic-fullflow-20261031/generate.py --check --schema ../tender-app-dev/workbench/packages/contracts/schemas/bid-package.schema.json
```

第二条 schema 路径是本工作区相邻目录示例；其他检出布局须显式选择实际 `tender-app/workbench/packages/contracts/schemas/bid-package.schema.json`。不设置或读取业务 `.env`、凭据、数据库、对象存储或模型配置。

仅依赖标准库和项目已锁 `Pillow==12.3.0`；可选 schema 校验复用已有 `jsonschema`。本轮确认新应用环境没有 python-docx，故使用项目 `packages/authoring/generated_docx.py` 已采用的标准库 OOXML、唯一规范 ` PAGE `字段和固定 ZIP 时间／排序方式，不安装 python-docx。

输出仅限此目录内 `generated/` 的八份 DOCX，以及 `manifest.json`、`expected.json`。七份主材料无动态域，第八份专用于域策略拒绝验证。已有输出字节相同则保留；任何不同文件、未知输出名、子目录或符号链接导致拒绝写入，不删除／覆盖旧数据。`--check`不写文件。PDF与转换回执应另存独立验收目录，不放入 `generated/`。

ZIP成员时间固定为2020-01-01，内容、图片、关系及JSON均无时钟、随机数、绝对路径或机器标识；在同一锁定Pillow版本下重复运行应逐字节一致。生成器不调用应用模块或API，不给自己签发 producer/qualification 回执。

## 八份原件及三场景

| 文件 | 内容 |
|---|---|
| `01_tender_SYNTHETIC.docx` | 招标正文、范围、要求及提交规则 |
| `02_addendum_SYNTHETIC.docx` | 工期120→90天，截止时间明确替换 |
| `03_technical_normal_SYNTHETIC.docx` | 90天／C30技术响应，中文表格、内嵌示意图及图注 |
| `04_business_SYNTHETIC.docx` | 虚构企业、有效期、明确无真实效力的证书占位 |
| `05_quote_SYNTHETIC.docx` | 三项虚构明细，合计55000.00元 |
| `06_submission_list_SYNTHETIC.docx` | 应交附件清单；声明不等于文件存在 |
| `07_technical_conflict_SYNTHETIC.docx` | 用150天／C25替换正常技术响应，构造两处冲突 |
| `08_field_policy_rejected_SYNTHETIC.docx` | 独立PAGE动态域拒绝反例，不加入主包 |

- **正常**：上传01—06。只预期机制可核对来源／补遗覆盖、明细算术和附件集合；不预设真实业务合格。
- **矛盾**：上传01、02、04、05、06、07，不上传03。预期能保留90／150天、C30／C25的待核对冲突与来源，不产生官方扣分。
- **缺失**：仅上传01、02、03、06，故意缺商务及报价。不能因清单声明而假设已提交，不能把未知报价填0或复用其他场景金额。

`expected.json` 仅含 mechanism expectations，官方得分为 null；三个场景独立建立项目／范围，不能混传正常与矛盾技术文件。所有文档逐页有 SYNTHETIC 声明，页眉页脚重复提醒，正文静态标记设计页码。普通附件一设计页、技术响应两设计页，静态目录仅为纯文本。主材料没有PAGE、TOC或其他动态域，以符合外来Word端口策略。

第08份故意包含项目已有生成器形式的规范 ` PAGE `字段，**预期外来Word端口仍拒绝**；规范PAGE仅允许服务器可信生成PAGE/RICH链，不能因字段写法规范而把外来文档放行。该文件只作单独策略反例，不参与正常、矛盾或缺失包，也不声称已经观察到拒绝结果。

## 与既有 schema 的关系

`expected.json` 各场景内的 authority／bid 模板复用当前 `bid-package/1` 结构，source_kind分开、scope一致，文件SHA来自实际DOCX。UUID都是确定性的合成占位；`bidder_status=pending`，`page_count=null`、`parts=[]`、`parse.status=not_frozen`，所有解析身份为null。它们不是可直接发送到API的真实请求，也不声称数据库已有该文档／版本。实际运行器必须先走现有上传、转换、解析流程，再绑定真实返回身份。

数据仓默认忽略DOCX原件，本轮不修改全局ignore或强制加入Git。提交生成器、README、manifest和expected即可；原件可离线再生成。不同于既有真实案例，此目录没有对象存储key，也不运行store push。

## 已检查与未覆盖

生成器检查ZIP、全部OOXML可解析、主材料无动态域、反例独含规范PAGE、页码格式、无外部关系、输出真实SHA及可选应用JSON schema。它不安装字体、不渲染、不制作PDF、不调用Gotenberg或模型。`declared_logical_pages`只表示设计页数，实际PDF页数仍为null。

后续由独立真实运行验证中文字体、表格／图像／图注、目录页码对应、真实分页、Word采用与解析、原件字节、队列／Worker／权限／幂等及刷新恢复。没有签章、复杂浮动对象、公式、扫描/OCR、宏、超长跨页表格、真实证书、真实投标或生产恢复覆盖；合成资料通过不等于真实复杂标书、规则效果、模型质量或真人验收通过。
