"""Offline additive SYNTHETIC authority candidate. Does not modify the original corpus."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parent / "synthetic-fullflow-20261031"
NAME = "14_technical_final_clarification_SYNTHETIC.docx"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build():
    path = CORPUS / "generate.py"
    module = importlib.util.spec_from_file_location(
        "synthetic_original_generator", path
    )
    original = importlib.util.module_from_spec(module)
    module.loader.exec_module(original)
    base_manifest = json.loads((CORPUS / "manifest.json").read_bytes())
    metadata = {Path(item["path"]).name: item for item in base_manifest["artifacts"]}
    protected = {}
    for number in (9, 10, 11, 12, 13):
        name = next(name for name in metadata if name.startswith(f"{number:02}_"))
        data = (CORPUS / metadata[name]["path"]).read_bytes()
        assert (
            sha(data) == metadata[name]["sha256"]
            and len(data) == metadata[name]["bytes"]
        )
        protected[name] = {"sha256": sha(data), "bytes": len(data)}
    tender = "10_technical_tender_SYNTHETIC.docx"
    body = "12_technical_text_normal_SYNTHETIC.docx"
    pages = [
        [
            ("heading", "SYNTHETIC 第14号最终技术澄清补遗 / 完全虚构"),
            (
                "text",
                "项目：SYNTHETIC 技术正文证据映射案例。本文件由本虚构案例唯一招标人角色“SYNTHETIC资料编制组”确认并签发；该角色不是现实单位或真人。本文件仅用于软件机制验收，不是真实招标文件、签章、官方评分或工程实施依据。",
            ),
            ("heading", "一、原件对应、现行依据与效力"),
            (
                "text",
                "本轮唯一招标原件是文件10_technical_tender_SYNTHETIC.docx，标题“SYNTHETIC 技术正文专用招标要求 / 虚构”，项目名称“SYNTHETIC 技术正文证据映射案例”，版本为原始第1版。其DOCX原件SHA256为"
                + metadata[tender]["sha256"]
                + "。原件摘要仅用于辨认原DOCX，不冒充其转换PDF的摘要。",
            ),
            (
                "text",
                "本轮现行权威依据仅为上述第10号原件与本第14号最终补遗；两者共同覆盖本轮全部技术要求。发生不同表述时，本第14号优先于第10号。本文件已经完成本虚构案例要求的招标人确认，自本轮资料提交前生效，无待签批或另行同意事项。",
            ),
            (
                "text",
                "旧第11号技术补遗已由本第14号整体吸收并替代，只是历史版本，不属于本轮现行输入，不要求另行提供。本文件已自行完整写明所有现行更正，不依赖任何未提供的补遗、附件、评分办法或外部文件。",
            ),
            ("heading", "二、T-01工期唯一现行值及T-02、T-03"),
            (
                "text",
                "T-01现行条文：总工期90天。第10号T-01原来的120天已经失效；凡本轮技术文件引用该旧120天工期，均统一替换为90天。120天仅可作为已废止历史说明，不是另一并行要求。该更正已经由本虚构招标人确认，不需另作批准。",
            ),
            (
                "text",
                "T-02现行条文：混凝土强度C30。T-03现行条文：技术措施应说明输入登记、检查、输出三个步骤。工期更正不改变T-02或T-03，也不增加商务、报价或资质要求。",
            ),
        ],
        [
            ("heading", "SYNTHETIC 适用边界与人工核实责任 / 完全虚构"),
            ("heading", "三、T-04本轮不适用及工法变更边界"),
            (
                "text",
                "T-04原条文仅在采用顶管施工时要求顶管专项技术说明。本轮唯一提交场景已确定采用明挖施工，不采用顶管；明挖与顶管在本轮场景互斥，本轮不存在施工工法变更。故T-04顶管专项技术说明明确不适用，本轮不要求提交该专项说明，不以缺少该专项说明认定缺项。",
            ),
            (
                "text",
                "若未来拟改为顶管，那是本轮输入之外的新情形，必须先由上述虚构招标人另行签发新版本变更文书，明确生效后才适用顶管要求；本轮T-04不会自动恢复适用，不得假设本轮已发生这种变更。",
            ),
            ("heading", "四、T-05责任流程明确，现场事实仍未核实"),
            (
                "text",
                "T-05现行条文：现场土层条件需人工核实后再确认支护措施。责任主体是本虚构案例的“SYNTHETIC施工技术负责人”岗位（虚构角色，不是现实个人）；核实时点为实际开挖前且支护措施批准前；核实依据应为现场土层勘察或现场记录，并由该岗位形成可追溯核实记录。",
            ),
            (
                "text",
                "当前输入确实没有现场土层勘察结果、现场记录或该岗位的核实确认记录，亦没有支护措施批准记录；现状为“未核实，待人工核实”。本补遗只明确责任主体、时点及程序，不提供任何地质事实，也不证明已经完成核实。",
            ),
            (
                "text",
                "未取得上述核实依据与确认记录时，不得确认或批准支护措施，不得据此进行依赖土层核实的实施。本轮文件核查中T-05的现场事实仍信息不足、待人工核实；不得推定已满足、已批准或已由真人签收。后续只有真实依据和明确人工确认齐备，才可另行变更该事实状态。责任流程明确与现场事实未知是不同事项。",
            ),
            ("heading", "五、仅技术符合性，不采用评分与额外废标机制"),
            (
                "text",
                "本虚构项目本轮只进行上述技术要求的符合性核查，不采用评分法；评分项、分值、评分表和成绩均不适用，不存在另行未提供的评分办法。本轮没有额外的废标条件或隐含废标条款，不要求从空白处补造条款。实际技术不一致或缺项须如实记录，但本文件不设置官方扣分、废标处罚或真实资格认定。",
            ),
            (
                "text",
                "所有文字均为SYNTHETIC软件机制测试材料，非模型质量标签、非真人业务签收。文书内的虚构效力设定不能替代应用的真实上传、转换、来源发布、证据核对和冻结流程；任何实际解析缺口或来源阻断仍须保留。",
            ),
        ],
    ]
    raw = original.make_doc("SYNTHETIC 第14号最终技术澄清补遗", pages)
    original.structural_checks({NAME: raw})
    with ZipFile(io.BytesIO(raw)) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        assert not document.findall(".//{" + original.W + "}tbl")
        assert not document.findall(".//{" + original.W + "}drawing")
        content = [
            node.text or "" for node in document.findall(".//{" + original.W + "}t")
        ]
    metadata[NAME] = {
        "path": "generated/" + NAME,
        "title": "SYNTHETIC 第14号最终技术澄清补遗",
        "source_kind": "authority",
        "purpose": "addendum",
        "sha256": sha(raw),
        "bytes": len(raw),
        "declared_logical_pages": 2,
        "actual_pdf_pages": None,
    }
    expectations = {
        "label_kind": "mechanism_expectations_only_not_observed_model_result",
        "synthetic": True,
        "case_id": "SYNTHETIC-TECHNICAL-CLARIFIED-NORMAL",
        "uploads": [tender, NAME, body],
        "roles": ["tender", "supplement", "body"],
        "replaces_for_new_case_only": "11_technical_addendum_SYNTHETIC.docx; original file remains untouched",
        "official_score": None,
        "scoring_applicability": "not_applicable; no points or invented score",
        "expected_checks": [
            {
                "clause": "T-01",
                "mechanism_expectation": "90 days current; all120-day references superseded; body90 may be satisfied",
            },
            {
                "clause": "T-02",
                "mechanism_expectation": "C30 unchanged; bodyC30 may be satisfied",
            },
            {
                "clause": "T-03",
                "mechanism_expectation": "input registration/check/output unchanged; body has those steps",
            },
            {
                "clause": "T-04",
                "mechanism_expectation": "not_applicable only with real14 source evidence and explicit normal scope declaration",
            },
            {
                "clause": "T-05",
                "mechanism_expectation": "unable_to_judge / unknown; real soil evidence and human confirmation remain absent; no positive fact admission",
            },
        ],
        "not_guaranteed": "A model may still emit ambiguities or omit requirements; retain real output, gaps, full denominator and normal gates. No correction to old model results.",
        "schema_templates_not_api_requests": [
            original.package(
                "clarified-normal-14", "authority", [tender, NAME], metadata
            ),
            original.package("clarified-normal-14", "bid", [body], metadata),
        ],
        "body_file_unchanged": protected[body],
        "conversion_executed": False,
        "parse_executed": False,
        "model_calls": 0,
    }
    manifest = {
        "fixture_id": "SYNTHETIC-TECHNICAL-CLARIFICATION-14-20261031",
        "synthetic": True,
        "artifact": metadata[NAME],
        "protected_originals": protected,
        "generator_source": {
            "path": "../synthetic-fullflow-20261031/generate.py",
            "sha256": sha(path.read_bytes()),
        },
        "base_manifest_sha256": sha((CORPUS / "manifest.json").read_bytes()),
        "expected_sha256": sha(original.stable_json(expectations)),
        "new_document_only": True,
        "official_scores": None,
        "network_calls": 0,
        "model_calls": 0,
    }
    return {
        "generated/" + NAME: raw,
        "manifest.json": original.stable_json(manifest),
        "expected.json": original.stable_json(expectations),
        "14-content.json": original.stable_json(
            {"paragraphs": content, "fictional_authority_only": True}
        ),
    }, expectations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--schema",
        type=Path,
        help="Explicit existing bid-package.schema.json; optional offline template validation",
    )
    args = parser.parse_args()
    allowed = {
        "generate.py",
        "README.md",
        "manifest.json",
        "expected.json",
        "14-content.json",
        "ambiguity-map.json",
        "generated",
        "verification.json",
    }
    if any(p.is_symlink() or p.name not in allowed for p in HERE.iterdir()):
        raise ValueError("UNKNOWN_OUTPUT_CONTENT_REFUSED")
    files, expected = build()
    if args.schema:
        import jsonschema

        schema = json.loads(args.schema.read_bytes())
        if schema.get("$id") != "https://tender.invalid/contracts/bid-package/1":
            raise ValueError("UNEXPECTED_APPLICATION_SCHEMA")
        for value in expected["schema_templates_not_api_requests"]:
            jsonschema.Draft202012Validator(schema).validate(value)
    generated = HERE / "generated"
    if generated.exists() and any(
        p.is_symlink() or not p.is_file() or p.name != NAME for p in generated.iterdir()
    ):
        raise ValueError("UNKNOWN_GENERATED_CONTENT_REFUSED")
    for name, raw in files.items():
        path = HERE / name
        if path.is_symlink() or (
            path.exists() and (not path.is_file() or path.read_bytes() != raw)
        ):
            raise ValueError("EXISTING_BYTES_DIFFER_REFUSED")
        if args.check and not path.is_file():
            raise ValueError("OUTPUT_MISSING")
    if not args.check:
        generated.mkdir(exist_ok=True)
        for name, raw in files.items():
            path = HERE / name
            if not path.exists():
                path.write_bytes(raw)
    print(
        json.dumps(
            {
                "status": "checked" if args.check else "generated",
                "new_docx": NAME,
                "conversion_executed": False,
                "model_calls": 0,
                "schema_templates_validated": 2 if args.schema else 0,
            }
        )
    )


if __name__ == "__main__":
    main()
