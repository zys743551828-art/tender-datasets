"""Offline, deterministic SYNTHETIC DOCX fixtures; never call an application API."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from importlib.metadata import version
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
WARNING = "SYNTHETIC / 虚构测试资料：非真实招标、企业资质、投标或官方成绩。"
SCHEMA_ID = "https://tender.invalid/contracts/bid-package/1"
for prefix, uri in (("w", W), ("r", R), ("wp", WP), ("a", A), ("pic", PIC)):
    ET.register_namespace(prefix, uri)


def element(parent, name, text=None, **attributes):
    node = ET.SubElement(
        parent, f"{{{W}}}{name}", {f"{{{W}}}{k}": str(v) for k, v in attributes.items()}
    )
    node.text = text
    return node


def paragraph(parent, text, heading=False):
    p = element(parent, "p")
    props = element(p, "pPr")
    element(props, "spacing", after=120, line=300, lineRule="auto")
    if heading:
        element(props, "pStyle", val="Heading1")
    run = element(p, "r")
    element(run, "t", text)
    return p


def table(parent, headers, rows):
    tbl = element(parent, "tbl")
    props = element(tbl, "tblPr")
    element(props, "tblW", w=9000, type="dxa")
    element(props, "tblLayout", type="fixed")
    borders = element(props, "tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element(borders, side, val="single", sz=4, color="64748B")
    grid = element(tbl, "tblGrid")
    for _ in headers:
        element(grid, "gridCol", w=9000 // len(headers))
    for index, values in enumerate([headers, *rows]):
        row = element(tbl, "tr")
        if index == 0:
            element(element(row, "trPr"), "tblHeader")
        for value in values:
            cell = element(row, "tc")
            cell_props = element(cell, "tcPr")
            element(cell_props, "tcW", w=9000 // len(headers), type="dxa")
            if index == 0:
                element(cell_props, "shd", fill="E2E8F0")
            paragraph(cell, str(value))


def diagram():
    image = Image.new("RGB", (720, 180), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text(
        (18, 10), "SYNTHETIC - NOT A REAL ENGINEERING DRAWING", fill="black", font=font
    )
    for x, title in [(20, "INPUT"), (270, "CHECK"), (520, "OUTPUT")]:
        draw.rectangle(
            (x, 55, x + 175, 140), fill="#e2e8f0", outline="#334155", width=3
        )
        draw.text((x + 48, 90), title, fill="black", font=font)
    for x in (195, 445):
        draw.line((x, 96, x + 65, 96), fill="#0f766e", width=4)
        draw.polygon([(x + 65, 96), (x + 53, 89), (x + 53, 103)], fill="#0f766e")
    stream = io.BytesIO()
    image.save(stream, format="PNG", optimize=False, compress_level=9)
    return stream.getvalue()


def picture(parent):
    p = element(parent, "p")
    drawing = element(element(p, "r"), "drawing")
    inline = ET.SubElement(drawing, f"{{{WP}}}inline")
    ET.SubElement(inline, f"{{{WP}}}extent", {"cx": "5400000", "cy": "1350000"})
    ET.SubElement(inline, f"{{{WP}}}docPr", {"id": "1", "name": "SYNTHETIC流程示意图"})
    graphic = ET.SubElement(inline, f"{{{A}}}graphic")
    data = ET.SubElement(graphic, f"{{{A}}}graphicData", {"uri": PIC})
    pic = ET.SubElement(data, f"{{{PIC}}}pic")
    nv = ET.SubElement(pic, f"{{{PIC}}}nvPicPr")
    ET.SubElement(nv, f"{{{PIC}}}cNvPr", {"id": "0", "name": "synthetic.png"})
    ET.SubElement(nv, f"{{{PIC}}}cNvPicPr")
    fill = ET.SubElement(pic, f"{{{PIC}}}blipFill")
    ET.SubElement(fill, f"{{{A}}}blip", {f"{{{R}}}embed": "fixture_image"})
    ET.SubElement(ET.SubElement(fill, f"{{{A}}}stretch"), f"{{{A}}}fillRect")
    shape = ET.SubElement(pic, f"{{{PIC}}}spPr")
    transform = ET.SubElement(shape, f"{{{A}}}xfrm")
    ET.SubElement(transform, f"{{{A}}}off", {"x": "0", "y": "0"})
    ET.SubElement(transform, f"{{{A}}}ext", {"cx": "5400000", "cy": "1350000"})
    geometry = ET.SubElement(shape, f"{{{A}}}prstGeom", {"prst": "rect"})
    ET.SubElement(geometry, f"{{{A}}}avLst")


def xml(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def make_doc(title, pages, *, dynamic_page=False):
    document = ET.Element(f"{{{W}}}document")
    body = element(document, "body")
    has_image = False
    for number, blocks in enumerate(pages):
        if number:
            element(element(element(body, "p"), "r"), "br", type="page")
        paragraph(body, WARNING)
        paragraph(body, f"第{number + 1}页（静态设计页码，转换后核对）")
        for block in blocks:
            if block[0] == "text":
                paragraph(body, block[1])
            elif block[0] == "heading":
                paragraph(body, block[1], heading=True)
            elif block[0] == "table":
                table(body, block[1], block[2])
            elif block[0] == "image":
                picture(body)
                has_image = True
    section = element(body, "sectPr")
    for kind in ("header", "footer"):
        node = element(section, kind + "Reference", type="default")
        node.set(f"{{{R}}}id", "fixture_" + kind)
    element(section, "pgSz", w=11906, h=16838)
    element(
        section,
        "pgMar",
        top=1134,
        right=1134,
        bottom=1134,
        left=1134,
        header=500,
        footer=500,
        gutter=0,
    )
    element(section, "pgNumType", fmt="decimal", start=1)
    footer = ET.Element(f"{{{W}}}ftr")
    p = paragraph(footer, "SYNTHETIC · 虚构资料")
    # Reuses generated_docx.py's canonical sole dynamic field, with fixed ZIP metadata.
    if dynamic_page:
        field = element(p, "fldSimple", instr=" PAGE ")
        element(element(field, "r"), "t", "1")
    header = ET.Element(f"{{{W}}}hdr")
    paragraph(header, "SYNTHETIC · 合成试验工程 · 禁用于真实投标")
    styles = ET.Element(f"{{{W}}}styles")
    normal = element(styles, "style", type="paragraph", default=1, styleId="Normal")
    element(normal, "name", val="Normal")
    rp = element(normal, "rPr")
    element(
        rp,
        "rFonts",
        ascii="Noto Sans CJK SC",
        hAnsi="Noto Sans CJK SC",
        eastAsia="Noto Sans CJK SC",
    )
    element(rp, "sz", val=22)
    element(rp, "lang", val="zh-CN", eastAsia="zh-CN")
    heading = element(styles, "style", type="paragraph", styleId="Heading1")
    element(heading, "name", val="heading 1")
    element(heading, "basedOn", val="Normal")
    element(element(heading, "rPr"), "b")
    element(element(heading, "pPr"), "keepNext")
    settings = ET.Element(f"{{{W}}}settings")
    element(settings, "updateFields", val="true")
    rels = ET.Element("Relationships", xmlns=REL)
    for kind, target in (
        ("styles", "styles.xml"),
        ("settings", "settings.xml"),
        ("header", "header.xml"),
        ("footer", "footer.xml"),
    ):
        ET.SubElement(
            rels,
            "Relationship",
            {"Id": "fixture_" + kind, "Type": R + "/" + kind, "Target": target},
        )
    if has_image:
        ET.SubElement(
            rels,
            "Relationship",
            {
                "Id": "fixture_image",
                "Type": R + "/image",
                "Target": "media/synthetic.png",
            },
        )
    types = ET.Element("Types", xmlns=CT)
    for extension, content_type in (
        ("rels", "application/vnd.openxmlformats-package.relationships+xml"),
        ("xml", "application/xml"),
        ("png", "image/png"),
    ):
        ET.SubElement(
            types, "Default", {"Extension": extension, "ContentType": content_type}
        )
    for part, content_type in (
        ("document", "document.main"),
        ("styles", "styles"),
        ("settings", "settings"),
        ("header", "header"),
        ("footer", "footer"),
    ):
        ET.SubElement(
            types,
            "Override",
            {
                "PartName": "/word/" + part + ".xml",
                "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml."
                + content_type
                + "+xml",
            },
        )
    root_rels = ET.Element("Relationships", xmlns=REL)
    ET.SubElement(
        root_rels,
        "Relationship",
        {
            "Id": "document",
            "Type": R + "/officeDocument",
            "Target": "word/document.xml",
        },
    )
    parts = {
        "[Content_Types].xml": xml(types),
        "_rels/.rels": xml(root_rels),
        "word/document.xml": xml(document),
        "word/_rels/document.xml.rels": xml(rels),
        "word/styles.xml": xml(styles),
        "word/settings.xml": xml(settings),
        "word/header.xml": xml(header),
        "word/footer.xml": xml(footer),
    }
    if has_image:
        parts["word/media/synthetic.png"] = diagram()
    stream = io.BytesIO()
    with ZipFile(stream, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(parts.items()):
            info = ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, data)
    return stream.getvalue()


def heading(text):
    return ("heading", text)


def text(value):
    return ("text", value)


def cover(title, toc):
    return [
        heading(title + " / SYNTHETIC"),
        text("项目：合成试验市虚构管线工程；企业：SYNTHETIC示例施工单位（不存在）。"),
        text("编号SYN-2030-001；所有日期、金额和资格字段均为机制测试构造。"),
        heading("静态目录（人工核对，不是自动TOC域）"),
        *[text(item) for item in toc],
    ]


def documents():
    def technical(conflict):
        return [
            cover(
                "技术响应" + (" · 场景B" if conflict else " · 场景A"),
                ["一、总体方案 …… 2", "二、图文说明 …… 3", "三、进度与检查 …… 4"],
            ),
            [
                heading("一、总体方案"),
                text("施工范围：虚构管线100米、检查井10座，均非真实项目工程量。"),
                (
                    "table",
                    ["参数", "本文件承诺", "说明"],
                    [
                        ["工期", "150天" if conflict else "90天", "从虚构开工日起计"],
                        [
                            "混凝土强度",
                            "C25" if conflict else "C30",
                            "同本项目设计范围",
                        ],
                        ["企业身份", "SYNTHETIC示例施工单位", "不证明真实资质"],
                    ],
                ),
            ],
            [
                heading("二、图文说明"),
                text(
                    "先登记输入，再检查，最后形成输出；图仅验证图像、图注和正文顺序。"
                ),
                ("image",),
                text("图1：SYNTHETIC 施工资料检查流程示意（非工程图）。"),
                text("图中INPUT、CHECK、OUTPUT分别对应输入、检查、输出。"),
            ],
            [
                heading("三、进度与检查"),
                (
                    "table",
                    ["阶段", "时段", "交付"],
                    [
                        ["准备", "第1—10天", "合成场地核对"],
                        ["管线", "第11—60天", "合成管线记录"],
                        ["检查井", "第61—80天", "合成检查记录"],
                        ["收尾", "第81—90天", "合成成果清单"],
                    ],
                ),
                text("质量、安全和人员仅为机制描述；未提供真实证书、签章或业绩。"),
            ],
        ]

    result = {
        "01_tender_SYNTHETIC.docx": (
            "authority",
            "tender_body",
            "招标正文",
            [
                cover("招标正文", ["一、范围与要求 …… 2", "二、提交要求 …… 3"]),
                [
                    heading("一、范围与要求"),
                    (
                        "table",
                        ["条款", "原始要求", "性质"],
                        [
                            ["R-01", "总工期120天", "补遗可明确替换"],
                            ["R-02", "混凝土强度C30", "虚构技术要求"],
                            ["R-03", "报价不超过1000000.00元", "虚构限价"],
                            ["R-04", "截止2030-01-20 09:00", "虚构日期"],
                        ],
                    ),
                    text("本资料没有官方评分办法、评委成绩或真实资质认定。"),
                ],
                [
                    heading("二、提交要求"),
                    (
                        "table",
                        ["条款", "须交文件"],
                        [
                            ["R-05", "技术、商务、报价、提交清单四类附件"],
                            ["R-06", "投标有效期不少于60天"],
                            ["R-07", "缺项不得伪造为已提交或自动满足"],
                        ],
                    ),
                    text("同一条款有明确补遗时按补遗检查；不得忽略来源和版本。"),
                ],
            ],
        ),
        "02_addendum_SYNTHETIC.docx": (
            "authority",
            "addendum",
            "补遗",
            [
                cover("补遗一", ["变更条款 …… 2"]),
                [
                    heading("变更条款"),
                    (
                        "table",
                        ["条款", "原要求", "替换要求"],
                        [
                            ["R-01", "120天", "90天"],
                            ["R-04", "2030-01-20 09:00", "2030-01-22 10:00"],
                        ],
                    ),
                    text(
                        "本补遗明确替换以上两条，其余招标要求保持；虚构编制日期2030-01-10。"
                    ),
                ],
            ],
        ),
        "03_technical_normal_SYNTHETIC.docx": (
            "own",
            "technical",
            "技术正常样本",
            technical(False),
        ),
        "04_business_SYNTHETIC.docx": (
            "own",
            "business",
            "商务附件",
            [
                cover("商务附件", ["声明与资料 …… 2"]),
                [
                    heading("声明与资料"),
                    (
                        "table",
                        ["字段", "内容"],
                        [
                            ["企业", "SYNTHETIC示例施工单位（不存在）"],
                            ["投标有效期", "90天"],
                            ["证书占位", "SYNTHETIC-NOT-A-LICENSE"],
                            ["声明", "证书占位不代表已取得资质，不可用于真实投标"],
                        ],
                    ),
                    text(
                        "无真实统一信用代码、证书、身份证、签章或联系方式；本文件不主张企业资质合格。"
                    ),
                ],
            ],
        ),
        "05_quote_SYNTHETIC.docx": (
            "own",
            "pricing",
            "报价附件",
            [
                cover("报价附件", ["合成明细 …… 2"]),
                [
                    heading("合成明细"),
                    (
                        "table",
                        ["名称", "数量", "单价（元）", "合价（元）"],
                        [
                            ["管线（米）", "100", "300.00", "30000.00"],
                            ["检查井（座）", "10", "2000.00", "20000.00"],
                            ["安全文明（项）", "1", "5000.00", "5000.00"],
                            ["合计", "—", "—", "55000.00"],
                        ],
                    ),
                    text(
                        "全部金额虚构，含税总价口径仅供算术机制核对，不表示市场价、正式报价或评分。"
                    ),
                ],
            ],
        ),
        "06_submission_list_SYNTHETIC.docx": (
            "own",
            "submission_checklist",
            "提交清单",
            [
                cover("提交清单", ["附件对照 …… 2"]),
                [
                    heading("附件对照"),
                    (
                        "table",
                        ["序号", "声明附件", "检查方式"],
                        [
                            ["1", "技术响应", "核实对应实际上传文件"],
                            ["2", "商务附件", "核实对应实际上传文件"],
                            ["3", "报价附件", "核实对应实际上传文件"],
                        ],
                    ),
                    text(
                        "清单声明不等于文件确已上传；场景缺失时应显示缺口，不伪造提交回执。"
                    ),
                ],
            ],
        ),
        "07_technical_conflict_SYNTHETIC.docx": (
            "own",
            "technical",
            "技术矛盾样本",
            technical(True),
        ),
    }
    # Keep the main external-upload set small: ordinary attachments use one page,
    # technical responses use two. All page numbers and TOCs are plain text.
    for name, (source, purpose, title, pages) in list(result.items()):
        if purpose == "technical":
            pages = [
                cover(
                    "技术响应 · " + ("场景B" if "conflict" in name else "场景A"),
                    ["总体方案、图文与进度 …… 2"],
                ),
                [block for page in pages[1:] for block in page],
            ]
        else:
            pages = [
                [
                    heading(title + " / SYNTHETIC"),
                    *[block for page in pages[1:] for block in page],
                ]
            ]
            if purpose == "tender_body":
                pages[0].insert(
                    1,
                    text(
                        "项目：合成试验市虚构管线工程，编号SYN-2030-001。静态目录：范围与要求1；提交要求1。"
                    ),
                )
        result[name] = (source, purpose, title, pages)
    result["08_field_policy_rejected_SYNTHETIC.docx"] = (
        "own",
        "field_policy_rejected",
        "动态域拒绝反例",
        [
            [
                heading("SYNTHETIC 动态域拒绝反例（不得加入正常材料包）"),
                text(
                    "本文件故意在页脚含PAGE动态域。外来Word端口应按现有域策略拒绝；不是服务器可信生成PAGE/RICH链。"
                ),
            ]
        ],
    )
    return result


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stable_json(value):
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def uid(value):
    return str(
        uuid5(NAMESPACE_URL, "https://synthetic.invalid/fullflow-20261031/" + value)
    )


def package(case, kind, names, metadata):
    scope = {
        "engineering_project_id": uid("project"),
        "lot_id": uid("lot"),
        "round_id": uid("round"),
        "bid_id": uid(case + "/bid"),
        "bidder_id": uid("bidder"),
        "bidder_status": "pending",
    }
    parse = {
        "status": "not_frozen",
        "parse_run_id": None,
        "parser_digest": None,
        "config_digest": None,
        "evidence_digest": None,
        "reason": "SYNTHETIC template: upload, conversion and real parsing have not run",
    }
    return {
        "identity_version": "bid-package/1",
        "package_id": uid(case + "/" + kind),
        "revision_id": uid(case + "/" + kind + "/r1"),
        "revision": 1,
        "kind": kind,
        "scope": scope,
        "predecessor_digest": None,
        "members": [
            {
                "member_id": uid(case + "/" + name),
                "document_version_id": uid("placeholder-document/" + name),
                "file_digest": metadata[name]["sha256"],
                "source_kind": "authority" if kind == "authority" else "own",
                "source_ref": "SYNTHETIC/" + name,
                "scope": scope,
                "purposes": [metadata[name]["purpose"]],
                "page_count": None,
                "parse": parse,
                "parts": [],
            }
            for name in names
        ],
    }


def build_outputs():
    if version("Pillow") != "12.3.0":
        raise ValueError("Pillow 12.3.0 is the existing locked generator dependency")
    files, metadata = {}, {}
    for name, (source, purpose, title, pages) in documents().items():
        raw = make_doc(title, pages, dynamic_page=purpose == "field_policy_rejected")
        files["generated/" + name] = raw
        metadata[name] = {
            "path": "generated/" + name,
            "title": title,
            "source_kind": source,
            "purpose": purpose,
            "sha256": sha(raw),
            "bytes": len(raw),
            "declared_logical_pages": len(pages),
            "actual_pdf_pages": None,
        }
    authority = list(metadata)[:2]
    own = list(metadata)[2:6]
    cases = []
    for name, members, checks in [
        (
            "normal",
            own,
            [
                "R-01由补遗覆盖为90天，技术承诺90天；不是120与90同时适用",
                "R-02技术C30与要求一致",
                "报价100×300+10×2000+1×5000=55000.00",
                "R-05声明附件与实际上传集合核对；R-06有效期90天不少于60天",
            ],
        ),
        (
            "contradiction",
            [list(metadata)[6], *own[1:]],
            [
                "技术工期150天与补遗90天形成待核对冲突",
                "技术C25与招标C30形成待核对冲突",
                "保留来源定位；不得当作真实违规处罚或官方扣分",
            ],
        ),
        (
            "missing",
            [own[0], own[3]],
            [
                "实际不上传商务和报价文件，但清单仍声明附件存在",
                "显示商务/报价材料缺口，不能从清单推断已提交",
                "缺少报价时金额未知，不自动填零或沿用正常场景55000",
            ],
        ),
    ]:
        cases.append(
            {
                "id": "SYNTHETIC-" + name.upper(),
                "uploads": authority + members,
                "mechanism_expectations": checks,
                "schema_templates_not_api_requests": [
                    package(name, "authority", authority, metadata),
                    package(name, "bid", members, metadata),
                ],
            }
        )
    expected = {
        "synthetic": True,
        "label_kind": "mechanism_expectations_only",
        "official_score": None,
        "real_company_qualification": "not_assessed",
        "real_business_acceptance": "not_assessed",
        "format_qualification": "pending_real_conversion",
        "schema_id": SCHEMA_ID,
        "placeholder_warning": "UUIDs are synthetic placeholders. Bind real uploaded identities through the existing application before any API use. No parse receipt, physical page or database state is fabricated.",
        "common_checks": [
            "原件字节和SHA保持一致；逐文件显著SYNTHETIC",
            "真实转换后核对中文、表格、内嵌图、图注、静态目录和静态页码",
            "正常外来DOCX无动态域，PAGE仅限单独拒绝反例；不混入主包",
            "静态目录页码仅按显式分页设计，实际溢页须核对，不伪造complete",
            "接口/队列/Worker/权限/幂等/刷新恢复由独立真实运行器验收",
        ],
        "field_policy_rejection": {
            "upload_only": "08_field_policy_rejected_SYNTHETIC.docx",
            "mechanism_expectation": "Existing external Word policy must reject its PAGE dynamic field; do not use it in the main scenarios",
            "observed_result": None,
        },
        "scenarios": cases,
    }
    files["expected.json"] = stable_json(expected)
    files["manifest.json"] = stable_json(
        {
            "fixture_id": "SYNTHETIC-FULLFLOW-20261031",
            "synthetic": True,
            "generator": "generate.py/1",
            "dependencies": {
                "Pillow": "12.3.0",
                "DOCX": "stdlib OOXML; canonical PAGE/ZIP pattern from packages/authoring/generated_docx.py",
            },
            "schema_id": SCHEMA_ID,
            "artifacts": list(metadata.values()),
            "expected_sha256": sha(files["expected.json"]),
            "conversion_executed": False,
            "network_calls": 0,
            "official_scores": None,
        }
    )
    return files, expected


def structural_checks(files):
    for name, raw in files.items():
        if not name.endswith(".docx"):
            continue
        with ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None
            for member in archive.infolist():
                assert member.date_time == (2020, 1, 1, 0, 0, 0)
                if member.filename.endswith((".xml", ".rels")):
                    ET.fromstring(archive.read(member))
            doc = ET.fromstring(archive.read("word/document.xml"))
            assert "SYNTHETIC" in "".join(doc.itertext())
            fields = ET.fromstring(archive.read("word/footer.xml")).findall(
                ".//{" + W + "}fldSimple"
            )
            wanted = [" PAGE "] if "08_field_policy_rejected" in name else []
            assert [item.get("{" + W + "}instr") for item in fields] == wanted
            assert not doc.findall(".//{" + W + "}fldSimple")
            assert not doc.findall(".//{" + W + "}fldChar")
            assert (
                doc.find(".//{" + W + "}pgNumType").get("{" + W + "}fmt") == "decimal"
            )
            assert b'TargetMode="External"' not in archive.read(
                "word/_rels/document.xml.rels"
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Read-only deterministic-byte comparison; requires existing outputs",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="Explicit existing bid-package.schema.json; validate templates offline with installed jsonschema",
    )
    args = parser.parse_args()
    allowed = {
        "generate.py",
        "README.md",
        "manifest.json",
        "expected.json",
        "generated",
    }
    if any(path.is_symlink() or path.name not in allowed for path in ROOT.iterdir()):
        raise ValueError("Unknown fixture-root content; refusing writes")
    files, expected = build_outputs()
    structural_checks(files)
    if args.schema:
        import jsonschema

        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        if schema.get("$id") != SCHEMA_ID:
            raise ValueError("Unexpected application schema")
        validator = jsonschema.Draft202012Validator(schema)
        for case in expected["scenarios"]:
            for payload in case["schema_templates_not_api_requests"]:
                validator.validate(payload)
    generated = ROOT / "generated"
    if ROOT.is_symlink() or generated.is_symlink():
        raise ValueError("Symlink output forbidden")
    if generated.exists():
        known = {Path(name).name for name in files if name.startswith("generated/")}
        for path in generated.iterdir():
            if path.is_symlink() or not path.is_file() or path.name not in known:
                raise ValueError("Unknown output content; refusing writes")
    for name, raw in files.items():
        path = ROOT / name
        if path.is_symlink() or (
            path.exists() and (not path.is_file() or path.read_bytes() != raw)
        ):
            raise ValueError("Existing output differs; refusing overwrite: " + name)
        if args.check and not path.is_file():
            raise ValueError("Missing output: " + name)
    if not args.check:
        generated.mkdir(exist_ok=True)
        for name, raw in files.items():
            path = ROOT / name
            if not path.exists():
                with path.open("xb") as stream:
                    stream.write(raw)
    print(
        json.dumps(
            {
                "synthetic": True,
                "docx_files": 8,
                "main_scenarios": 3,
                "field_policy_negative": 1,
                "schema_validated": bool(args.schema),
                "byte_check": args.check,
                "conversion_executed": False,
                "network_calls": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
