# Khởi tạo Môi trường Antigravity IDE (Kế thừa Setup Lõi)

Hãy sao chép toàn bộ khối Prompt dưới đây, tạo một dự án mới (New Chat) trong Antigravity IDE của bạn và dán vào để AI tự động xây dựng hệ thống:

---
**[Copy phần dưới đây và dán vào Antigravity]**

Bạn là một Chuyên gia Kiến trúc Hệ thống AI. Nhiệm vụ của bạn là khởi tạo một Second Brain hoàn chỉnh cho Giảng viên. Hãy sử dụng công cụ của bạn (`write_to_file`, `run_command`) để tuần tự thực hiện các bước sau:

### BƯỚC 1: TẠO CẤU TRÚC THƯ MỤC CƠ BẢN
Tạo các thư mục sau (nếu chưa có):
- `00 - Inbox/`
- `01 - Projects/`
- `02 - Knowledge/sources/`
- `02 - Knowledge/concepts/`
- `03 - Resources/`
- `04 - Classes/`
- `05 - Operations/`
- `06 - Archive/`
- `.agents/skills/picos-extractor/`
- `.agents/skills/sia-feedback-auditor/`
- `.agents/skills/academic-autoresearch-autopilot/`
- `.agents/skills/pdf-ninja-fetcher/`
- `.agents/skills/edu-assignment-auto-grader/`
- `.agents/skills/socratic-learning-coach/`

### BƯỚC 2: TẠO FILE HƯỚNG DẪN LÕI (`CLAUDE.md`)
Tạo file `CLAUDE.md` tại thư mục gốc với nội dung nguyên văn dưới đây. Đây là file cực kỳ quan trọng định nghĩa toàn bộ nguyên tắc hoạt động (Lớp Luật):

```markdown
# CLAUDE.md - Giảng Viên Second Brain Operating Manual

You are going to help me build and maintain a Second Brain. This is a persistent, compounding knowledge system. Instead of retrieving from raw documents at query time, you will incrementally build and maintain a structured knowledge base.

## 1. Cấu trúc 3 Lớp (Three Layers)
**Layer 1: 00 - Inbox** — Khu vực chứa dữ liệu thô. Immutable (không bao giờ sửa file gốc ở đây).
**Layer 2: 02 - Knowledge** — Lớp Tri thức do AI sở hữu và quản lý (tạo page, update link).
**Layer 3: CLAUDE.md** — Lớp Luật. Bạn phải đọc file này đầu tiên trong mỗi phiên làm việc.

## 2. Four Core Workflows (4 Quy trình Cốt lõi)

### 2.1 Ingest (Tiêu hóa dữ liệu)
Chạy quy trình này khi tôi ném một file vào `00 - Inbox/` và yêu cầu xử lý.
1. Đọc toàn bộ source file.
2. Thảo luận với tôi: Đâu là 2-3 điểm quan trọng nhất?
3. Viết `02 - Knowledge/sources/<Title>.md`.
4. Tạo/Cập nhật các concept liên quan trong `02 - Knowledge/concepts/`.
5. Cập nhật `02 - Knowledge/index.md`.
6. Ghi vết vào `02 - Knowledge/log.md`. **Bước 2 là bắt buộc. Không được bỏ qua.**

### 2.2 Query (Truy vấn)
Khi tôi hỏi, hãy đọc `index.md`, tìm page liên quan, trả lời có trích dẫn `[[Page]]`.

### 2.3 Lint (Dọn dẹp hệ thống)
Tìm các mâu thuẫn, file mồ côi (orphan pages), broken links và báo cáo để sửa chữa.

### 2.4 Review (Đánh giá)
Đánh giá định kỳ các project đang active, các file chưa xử lý trong Inbox.

## 3. Page Conventions & Syntax

**Frontmatter Bắt buộc:** (Trừ index.md và log.md)
---
type: source | concept | synthesis
title: "Tên hiển thị tiếng Việt có dấu"
sources: 1
tags: [tag1, tag2]
updated: YYYY-MM-DD
---

**Quy tắc Đặt tên File (Naming):**
- Source: Kebab-case (VD: `phuong-phap-nghien-cuu.md`)
- Concept: lowercase-hyphens (VD: `tu-duy-he-thong.md`)
- Luôn sử dụng Wiki-links: `[[PageName]]`.

## 4. Log Format (Cú pháp Ghi Log)
Nối thêm (append) vào `02 - Knowledge/log.md` theo ĐÚNG định dạng:
`## [YYYY-MM-DD] <type> | <title>`
(Types: setup, ingest, query, lint, review, edit)

## 5. Working Principles (Nguyên tắc làm việc)
- **Propose before acting:** Đề xuất trước khi hành động.
- **Verification Gate:** Tự kiểm chứng tính chính xác của dữ liệu (không ảo giác) trước khi xuất kết quả.
- Tiến hóa: Gặp lỗi phải đúc kết vào `05 - Operations/patterns.md`.
```

### BƯỚC 3: TẠO CÁC FILE BỘ NHỚ
- Tạo `02 - Knowledge/index.md` (Mục lục tri thức).
- Tạo `02 - Knowledge/log.md` (Lịch sử hệ thống).
- Tạo `05 - Operations/patterns.md` (Bài học kinh nghiệm).

### BƯỚC 4: TẠO FILE SKILL TỰ ĐỘNG HÓA
Viết file `SKILL.md` vào thư mục `.agents/skills/picos-extractor/`:
```yaml
---
name: picos-extractor
description: Kỹ năng bóc tách phương pháp luận (PICOS) từ bài báo khoa học.
---
# PICOS Extractor
Bạn phải đọc file và trích xuất đúng 5 yếu tố P-I-C-O-S dưới dạng Bảng Markdown. Áp dụng Lớp Kiểm Chứng: Kiểm tra xem có bịa số liệu không trước khi in kết quả.
```

Viết file `SKILL.md` vào thư mục `.agents/skills/sia-feedback-auditor/`:
```yaml
---
name: sia-feedback-auditor
description: Tự động rút ra bài học khi gặp lỗi.
---
# SIA Feedback Auditor
Đúc kết nguyên lý cốt lõi khi có lỗi và ghi bài học vào `05 - Operations/patterns.md`.
```

Viết file `SKILL.md` vào thư mục `.agents/skills/academic-autoresearch-autopilot/`:
```yaml
---
name: academic-autoresearch-autopilot
description: Kỹ năng điều phối tự động hóa tìm kiếm, bóc tách PICOS, tổng hợp báo cáo và tự động tạo Slide trình chiếu khoa học (Sơ đồ Mermaid).
---
# Academic AutoResearch Autopilot
Tự động gọi các công cụ tìm kiếm bài báo, gọi `picos-extractor`, và sinh ra báo cáo markdown. Tự động chuyển đổi báo cáo thành định dạng Slide Markdown.
```

Viết file `SKILL.md` vào thư mục `.agents/skills/pdf-ninja-fetcher/`:
```yaml
---
name: pdf-ninja-fetcher
description: Tự động tìm và tải file PDF toàn văn của bài báo khoa học dựa trên mã DOI, tự động vượt rào Paywall.
---
# PDF Ninja Fetcher
Chỉ cần nhập DOI, tự động tra cứu các nguồn Open Access, Sci-Hub, Anna's Archive để tải file PDF về thư mục Inbox.
```

Viết file `SKILL.md` vào thư mục `.agents/skills/edu-assignment-auto-grader/`:
```yaml
---
name: edu-assignment-auto-grader
description: Trợ giảng chấm thi tự động. Đọc file PDF bài làm, chấm điểm dựa trên file Rubric.
---
# Auto-Grader
Đọc kỹ file Rubric. Đánh giá từng tiêu chí, xuất ra bảng điểm CSV chi tiết kèm nhận xét từng lỗi sai của sinh viên.
```

Viết file `SKILL.md` vào thư mục `.agents/skills/socratic-learning-coach/`:
```yaml
---
name: socratic-learning-coach
description: Gia sư Socratic. Ép học sinh tự giải thích vấn đề (Feynman technique) để hiểu sâu.
---
# Socratic Learning Coach
Tuyệt đối không đưa ra câu trả lời trực tiếp. Liên tục đặt câu hỏi gợi mở, ép học sinh tư duy để tìm ra đáp án.
```

### BƯỚC 5: NGHIỆM THU
Tự đọc lại `CLAUDE.md` vừa tạo (bằng công cụ view_file) để xác nhận. Sau đó báo cáo: "Quá trình Khởi tạo đã hoàn tất thành công!"
