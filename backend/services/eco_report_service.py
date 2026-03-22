from datetime import datetime
from typing import Any, Dict, List, Sequence, Tuple


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 42
RIGHT_MARGIN = 42
TOP_MARGIN = 36
BOTTOM_MARGIN = 34
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

HEADER_HEIGHT = 72
FOOTER_HEIGHT = 22
SECTION_GAP = 14
CARD_GAP = 12

FONT_REGULAR = "F1"
FONT_BOLD = "F2"

COLOR_TEXT = (0.10, 0.13, 0.18)
COLOR_MUTED = (0.42, 0.47, 0.55)
COLOR_BORDER = (0.82, 0.85, 0.89)
COLOR_PANEL = (0.97, 0.98, 0.99)
COLOR_HEADER = (0.13, 0.22, 0.38)
COLOR_HEADER_ACCENT = (0.23, 0.48, 0.98)
COLOR_SUCCESS = (0.15, 0.62, 0.36)
COLOR_WARNING = (0.84, 0.54, 0.11)
COLOR_DANGER = (0.78, 0.24, 0.20)
COLOR_TABLE_HEADER = (0.90, 0.94, 0.99)


def _escape_pdf_text(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _normalize_value(value: Any) -> str:
    if value in (None, "", [], {}):
        return "-"
    if isinstance(value, dict):
        return ", ".join(f"{k}: {v}" for k, v in value.items()) if value else "-"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "-"
    return str(value)


def _format_timestamp(value: Any) -> str:
    if not value:
        return "-"
    try:
        dt = datetime.fromisoformat(str(value))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(value)


def _wrap_text(text: str, width: float, font_size: int) -> List[str]:
    value = _normalize_value(text)
    if value == "-":
        return ["-"]

    max_chars = max(12, int(width / max(font_size * 0.52, 1)))
    lines: List[str] = []
    for paragraph in value.splitlines():
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                while len(word) > max_chars:
                    lines.append(word[:max_chars])
                    word = word[max_chars:]
                current = word
        if current:
            lines.append(current)
    return lines or ["-"]


class PdfReportBuilder:
    def __init__(self, report_data: Dict[str, Any]):
        self.report_data = report_data
        self.pages: List[List[str]] = []
        self.page_number = 0
        self.cursor_y = 0.0
        self._new_page()

    def _new_page(self) -> None:
        self.pages.append([])
        self.page_number += 1
        self.cursor_y = TOP_MARGIN + HEADER_HEIGHT + 18
        self._draw_page_header()

    @property
    def commands(self) -> List[str]:
        return self.pages[-1]

    def _emit(self, command: str) -> None:
        self.commands.append(command)

    def _ensure_space(self, height: float) -> None:
        usable_bottom = PAGE_HEIGHT - BOTTOM_MARGIN - FOOTER_HEIGHT
        if self.cursor_y + height > usable_bottom:
            self._new_page()

    def _set_fill(self, color: Tuple[float, float, float]) -> str:
        return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg"

    def _set_stroke(self, color: Tuple[float, float, float]) -> str:
        return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} RG"

    def _draw_rect(
        self,
        x: float,
        top_y: float,
        width: float,
        height: float,
        fill: Tuple[float, float, float] = None,
        stroke: Tuple[float, float, float] = None,
        line_width: float = 1.0,
    ) -> None:
        bottom_y = PAGE_HEIGHT - top_y - height
        cmds: List[str] = [f"{line_width:.2f} w"]
        if fill:
            cmds.append(self._set_fill(fill))
        if stroke:
            cmds.append(self._set_stroke(stroke))
        paint = "B" if fill and stroke else "f" if fill else "S"
        cmds.append(f"{x:.2f} {bottom_y:.2f} {width:.2f} {height:.2f} re {paint}")
        self._emit("\n".join(cmds))

    def _draw_line(self, x1: float, top_y1: float, x2: float, top_y2: float, color=COLOR_BORDER, width=1.0) -> None:
        y1 = PAGE_HEIGHT - top_y1
        y2 = PAGE_HEIGHT - top_y2
        self._emit(
            "\n".join([
                f"{width:.2f} w",
                self._set_stroke(color),
                f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S",
            ])
        )

    def _draw_text(
        self,
        x: float,
        top_y: float,
        text: str,
        font: str = FONT_REGULAR,
        size: int = 10,
        color: Tuple[float, float, float] = COLOR_TEXT,
    ) -> None:
        baseline = PAGE_HEIGHT - top_y - size
        self._emit(
            "\n".join([
                f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg",
                "BT",
                f"/{font} {size} Tf",
                f"1 0 0 1 {x:.2f} {baseline:.2f} Tm",
                f"({_escape_pdf_text(text)}) Tj",
                "ET",
            ])
        )

    def _draw_wrapped_text(
        self,
        x: float,
        top_y: float,
        width: float,
        text: str,
        font: str = FONT_REGULAR,
        size: int = 10,
        color: Tuple[float, float, float] = COLOR_TEXT,
        leading: int = None,
    ) -> float:
        leading = leading or (size + 4)
        lines = _wrap_text(text, width, size)
        for idx, line in enumerate(lines):
            self._draw_text(x, top_y + idx * leading, line, font=font, size=size, color=color)
        return len(lines) * leading

    def _draw_page_header(self) -> None:
        self._draw_rect(0, 0, PAGE_WIDTH, HEADER_HEIGHT, fill=COLOR_HEADER)
        self._draw_rect(0, HEADER_HEIGHT - 6, PAGE_WIDTH, 6, fill=COLOR_HEADER_ACCENT)
        self._draw_text(LEFT_MARGIN, TOP_MARGIN + 2, "KINETIC PLM", font=FONT_BOLD, size=19, color=(1, 1, 1))
        self._draw_text(
            LEFT_MARGIN,
            TOP_MARGIN + 22,
            f"ECO REPORT | {self.report_data.get('eco_name', 'Unnamed ECO')}",
            font=FONT_BOLD,
            size=10,
            color=(0.93, 0.96, 1.00),
        )
        self._draw_text(
            PAGE_WIDTH - 155,
            TOP_MARGIN + 6,
            f"Generated: {_format_timestamp(self.report_data.get('generated_at'))}",
            size=9,
            color=(0.90, 0.94, 1.00),
        )

    def _draw_page_footer(self) -> None:
        footer_y = PAGE_HEIGHT - BOTTOM_MARGIN - 8
        self._draw_line(LEFT_MARGIN, footer_y, PAGE_WIDTH - RIGHT_MARGIN, footer_y, color=COLOR_BORDER, width=0.8)
        self._draw_text(
            LEFT_MARGIN,
            footer_y + 6,
            f"{self.report_data.get('eco_name', 'ECO')} | {self.report_data.get('eco_type', '-')}",
            size=8,
            color=COLOR_MUTED,
        )
        self._draw_text(
            PAGE_WIDTH - RIGHT_MARGIN - 48,
            footer_y + 6,
            f"Page {self.page_number}",
            size=8,
            color=COLOR_MUTED,
        )

    def _footer_commands_for_page(self, page_number: int) -> List[str]:
        original_index = len(self.pages) - 1
        original_page_number = self.page_number
        self.pages.append([])
        self.page_number = page_number
        self._draw_page_footer()
        footer_commands = self.pages.pop()
        self.page_number = original_page_number
        return footer_commands

    def section_title(self, title: str, subtitle: str = None) -> None:
        needed = 34 if subtitle else 22
        self._ensure_space(needed)
        self._draw_text(LEFT_MARGIN, self.cursor_y, title.upper(), font=FONT_BOLD, size=12, color=COLOR_HEADER)
        if subtitle:
            self._draw_text(LEFT_MARGIN, self.cursor_y + 16, subtitle, size=9, color=COLOR_MUTED)
        self.cursor_y += needed

    def estimate_paragraph_height(self, text: str) -> float:
        wrapped = _wrap_text(text or "-", CONTENT_WIDTH - 28, 10)
        return max(68, len(wrapped) * 13 + 20)

    def card(self, title: str, rows: Sequence[Tuple[str, Any]], x: float, width: float) -> float:
        label_width = 118
        body_height = 18
        for label, value in rows:
            value_lines = _wrap_text(value, width - label_width - 34, 10)
            block_height = 18 + len(value_lines) * 12
            body_height += block_height
        height = max(92, body_height + 14)
        self._draw_rect(x, self.cursor_y, width, height, fill=COLOR_PANEL, stroke=COLOR_BORDER)
        self._draw_rect(x, self.cursor_y, width, 28, fill=COLOR_TABLE_HEADER, stroke=COLOR_BORDER, line_width=0.6)
        self._draw_text(x + 14, self.cursor_y + 9, title, font=FONT_BOLD, size=11, color=COLOR_HEADER)
        row_y = self.cursor_y + 36
        for idx, (label, value) in enumerate(rows):
            if idx:
                self._draw_line(x + 14, row_y - 5, x + width - 14, row_y - 5, color=COLOR_BORDER, width=0.5)
            self._draw_text(x + 14, row_y + 2, label, font=FONT_BOLD, size=9, color=COLOR_MUTED)
            text_height = self._draw_wrapped_text(
                x + label_width,
                row_y,
                width - label_width - 18,
                _normalize_value(value),
                size=10,
            )
            row_y += max(20, text_height + 6)
        return height

    def metric_cards(self, metrics: Sequence[Tuple[str, Any, Tuple[float, float, float]]]) -> None:
        self._ensure_space(84)
        card_width = (CONTENT_WIDTH - CARD_GAP * 3) / 4
        x = LEFT_MARGIN
        for label, value, accent in metrics:
            self._draw_rect(x, self.cursor_y, card_width, 62, fill=COLOR_PANEL, stroke=COLOR_BORDER)
            self._draw_rect(x, self.cursor_y, 6, 62, fill=accent)
            self._draw_text(x + 18, self.cursor_y + 12, label.upper(), font=FONT_BOLD, size=8, color=COLOR_MUTED)
            self._draw_text(x + 18, self.cursor_y + 30, str(value), font=FONT_BOLD, size=20, color=COLOR_TEXT)
            x += card_width + CARD_GAP
        self.cursor_y += 76

    def bullet_list(self, items: Sequence[str], empty_text: str) -> None:
        lines = list(items) if items else [empty_text]
        for item in lines:
            wrapped = _wrap_text(item, CONTENT_WIDTH - 24, 10)
            height = max(20, len(wrapped) * 12 + 6)
            self._ensure_space(height)
            self._draw_rect(LEFT_MARGIN, self.cursor_y, CONTENT_WIDTH, height, fill=(1, 1, 1), stroke=COLOR_BORDER, line_width=0.7)
            self._draw_rect(LEFT_MARGIN, self.cursor_y, 5, height, fill=COLOR_HEADER_ACCENT)
            self._draw_wrapped_text(LEFT_MARGIN + 16, self.cursor_y + 6, CONTENT_WIDTH - 28, item, size=10)
            self.cursor_y += height + 6

    def paragraph_box(self, text: str, empty_text: str) -> None:
        content = text or empty_text
        wrapped = _wrap_text(content, CONTENT_WIDTH - 28, 10)
        height = max(68, len(wrapped) * 13 + 20)
        self._ensure_space(height)
        self._draw_rect(LEFT_MARGIN, self.cursor_y, CONTENT_WIDTH, height, fill=COLOR_PANEL, stroke=COLOR_BORDER)
        self._draw_wrapped_text(LEFT_MARGIN + 14, self.cursor_y + 12, CONTENT_WIDTH - 28, content, size=10)
        self.cursor_y += height + 8

    def table(self, title: str, columns: Sequence[Tuple[str, str, float]], rows: Sequence[Dict[str, Any]], empty_text: str) -> None:
        self.section_title(title)
        if not rows:
            self.paragraph_box(empty_text, empty_text)
            return

        col_widths = [CONTENT_WIDTH * frac for _, _, frac in columns]
        header_height = 24

        def draw_table_header(top_y: float) -> None:
            self._draw_rect(LEFT_MARGIN, top_y, CONTENT_WIDTH, header_height, fill=COLOR_TABLE_HEADER, stroke=COLOR_BORDER)
            x = LEFT_MARGIN
            for (_, label, _), width in zip(columns, col_widths):
                self._draw_text(x + 6, top_y + 7, label.upper(), font=FONT_BOLD, size=8, color=COLOR_HEADER)
                x += width

        self._ensure_space(header_height + 20)
        draw_table_header(self.cursor_y)
        self.cursor_y += header_height

        for row_index, row in enumerate(rows):
            cell_lines = []
            max_lines = 1
            for (key, _, _), width in zip(columns, col_widths):
                lines = _wrap_text(row.get(key, "-"), width - 10, 9)
                cell_lines.append(lines)
                max_lines = max(max_lines, len(lines))
            row_height = max(26, max_lines * 12 + 10)
            self._ensure_space(row_height + 2)
            if self.cursor_y == TOP_MARGIN + HEADER_HEIGHT + 18:
                draw_table_header(self.cursor_y)
                self.cursor_y += header_height

            fill = COLOR_PANEL if row_index % 2 == 0 else (1.0, 1.0, 1.0)
            self._draw_rect(LEFT_MARGIN, self.cursor_y, CONTENT_WIDTH, row_height, fill=fill, stroke=COLOR_BORDER, line_width=0.6)
            x = LEFT_MARGIN
            for idx, lines in enumerate(cell_lines):
                width = col_widths[idx]
                if idx:
                    self._draw_line(x, self.cursor_y, x, self.cursor_y + row_height, color=COLOR_BORDER, width=0.5)
                for line_idx, line in enumerate(lines):
                    self._draw_text(x + 6, self.cursor_y + 7 + line_idx * 12, line, size=9, color=COLOR_TEXT)
                x += width
            self.cursor_y += row_height
        self.cursor_y += 8

    def finalize(self) -> bytes:
        for index, page in enumerate(self.pages, start=1):
            page.extend(self._footer_commands_for_page(index))
        return _assemble_pdf(self.pages)


def _assemble_pdf(page_commands: Sequence[Sequence[str]]) -> bytes:
    objects: List[bytes] = []

    def add_object(content: bytes) -> int:
        objects.append(content)
        return len(objects)

    font_regular_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold_id = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    page_ids: List[int] = []
    for commands in page_commands:
        content_stream = "\n".join(commands).encode("latin-1", errors="replace")
        content_id = add_object(
            f"<< /Length {len(content_stream)} >>\nstream\n".encode("latin-1")
            + content_stream
            + b"\nendstream"
        )
        page_id = add_object(
            (
                "<< /Type /Page /Parent PAGES_ID 0 R "
                f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Contents {content_id} 0 R "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> >>"
            ).encode("latin-1")
        )
        page_ids.append(page_id)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    pages_id = add_object(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1"))
    for page_id in page_ids:
        objects[page_id - 1] = objects[page_id - 1].replace(b"PAGES_ID", str(pages_id).encode("ascii"))

    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1"))

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode("latin-1"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode("latin-1")
    )
    return bytes(pdf)


def _change_rows(changes: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in changes:
        rows.append({
            "change_type": (item.get("change_type") or "updated").capitalize(),
            "label": item.get("label") or item.get("field") or "Item",
            "old_value": _normalize_value(item.get("old_value")),
            "new_value": _normalize_value(item.get("new_value")),
        })
    return rows


def build_eco_report_pdf(report_data: Dict[str, Any]) -> bytes:
    builder = PdfReportBuilder(report_data)

    overview_left = [
        ("ECO Name", report_data.get("eco_name")),
        ("Type", report_data.get("eco_type")),
        ("Product / BoM", report_data.get("target_name")),
        ("Current Stage", report_data.get("current_stage")),
        ("Update Version", "Yes" if report_data.get("update_version") else "No"),
    ]
    overview_right = [
        ("Initiated By", report_data.get("initiated_by")),
        ("Generated At", _format_timestamp(report_data.get("generated_at"))),
        ("Old Version", report_data.get("old_version")),
        ("New Version", report_data.get("new_version")),
        ("Description", report_data.get("description")),
    ]

    builder.section_title("Overview", "Final-stage ECO report with comparison, approval, and AI analysis")
    card_width = (CONTENT_WIDTH - CARD_GAP) / 2
    builder._ensure_space(180)
    left_height = builder.card("Document Overview", overview_left, LEFT_MARGIN, card_width)
    right_height = builder.card("Version Snapshot", overview_right, LEFT_MARGIN + card_width + CARD_GAP, card_width)
    builder.cursor_y += max(left_height, right_height) + SECTION_GAP

    component_changes = report_data.get("component_changes", [])
    workorder_changes = report_data.get("workorder_changes", [])
    approvals = report_data.get("approvals", [])

    if report_data.get("eco_type") == "Product":
        product = report_data.get("product_details") or {}
        builder.section_title("Product Details")
        builder._ensure_space(150)
        detail_rows = [
            ("Product Name", product.get("product_name")),
            ("Internal Reference", product.get("internal_reference")),
            ("Sale Price", product.get("sale_price")),
            ("Cost Price", product.get("cost_price")),
            ("Change Notes", product.get("change_notes")),
            ("Attachments", ", ".join(product.get("attachments") or []) or "-"),
        ]
        height = builder.card("Product Change Details", detail_rows, LEFT_MARGIN, CONTENT_WIDTH)
        builder.cursor_y += height + SECTION_GAP
    else:
        bom = report_data.get("bom_details") or {}
        builder.section_title("BoM Details")
        detail_rows = [
            ("BoM Name", bom.get("bom_name")),
            ("Notes", bom.get("notes")),
            ("Proposed Components", len(bom.get("proposed_components") or [])),
            ("Proposed Work Orders", len(bom.get("proposed_workorders") or [])),
        ]
        builder._ensure_space(120)
        height = builder.card("BoM Change Details", detail_rows, LEFT_MARGIN, CONTENT_WIDTH)
        builder.cursor_y += height + SECTION_GAP
        builder.table(
            "Proposed Components",
            [("component", "Component", 0.36), ("quantity", "Quantity", 0.12), ("notes", "Notes", 0.52)],
            list(bom.get("proposed_components") or []),
            "No proposed components.",
        )
        builder.table(
            "Proposed Work Orders",
            [("operation", "Operation", 0.36), ("work_center", "Work Center", 0.34), ("duration_minutes", "Duration (Min)", 0.30)],
            list(bom.get("proposed_workorders") or []),
            "No proposed work orders.",
        )

    ai_summary_text = report_data.get("ai_summary") or "AI summary not available."
    builder._ensure_space(22 + builder.estimate_paragraph_height(ai_summary_text))
    builder.section_title("AI Summary")
    builder.paragraph_box(ai_summary_text, "AI summary not available.")

    old_label = f"Old Value ({report_data.get('old_version', '-')})"
    new_label = f"New Value ({report_data.get('new_version', '-')})"
    builder.table(
        "Field Changes",
        [("label", "Field", 0.24), ("old_value", old_label, 0.38), ("new_value", new_label, 0.38)],
        _change_rows(report_data.get("field_changes") or []),
        "No field changes.",
    )

    component_rows = _change_rows(report_data.get("component_changes") or [])
    if component_rows:
        builder.table(
            "Component Changes",
            [("change_type", "Type", 0.14), ("label", "Component", 0.22), ("old_value", old_label, 0.32), ("new_value", new_label, 0.32)],
            component_rows,
            "No component changes.",
        )

    workorder_rows = _change_rows(report_data.get("workorder_changes") or [])
    if workorder_rows:
        builder.table(
            "Work Order Changes",
            [("change_type", "Type", 0.14), ("label", "Work Order", 0.22), ("old_value", old_label, 0.32), ("new_value", new_label, 0.32)],
            workorder_rows,
            "No work order changes.",
        )

    approval_rows = [
        {
            "stage": item.get("stage"),
            "user": item.get("user"),
            "required": "Yes" if item.get("approval_required") else "No",
            "status": "Approved" if item.get("approved") else "Pending",
            "time": _format_timestamp(item.get("approval_time")),
        }
        for item in approvals
    ]
    builder.table(
        "Approval Details",
        [("stage", "Stage", 0.20), ("user", "Approver", 0.28), ("required", "Required", 0.12), ("status", "Status", 0.14), ("time", "Approval Time", 0.26)],
        approval_rows,
        "No approval details available.",
    )

    return builder.finalize()
