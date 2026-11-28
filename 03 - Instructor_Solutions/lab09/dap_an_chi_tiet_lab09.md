# TÀI LIỆU GIẢNG DẠY VÀ ĐÁP ÁN CHI TIẾT: BÀI 9 (LAB 09)
# BỘ CỘNG NHANH 4-BIT CARRY LOOKAHEAD ADDER (CLA)
*(Tài liệu chuyên môn dành riêng cho Giảng viên & Trợ giảng — Đồng bộ với Teacher's Book Lab 09)*

> **Script kiểm chứng số liệu:** [verify_lab09_new.py](../../scripts/verify_lab09_new.py)  
> **Teacher's Book đầy đủ:** [Lab09_Teacher_Book.md](../../Teacher_Book/Lab09_Teacher_Book.md)  
> **Tiến trình công nghệ:** MOSIS SCMOS C5N 0,5 µm ($V_{DD} = 5,0\,\text{V}, \lambda = 0,30\,\mu\text{m}, L_{min} = 0,60\,\mu\text{m}$).

---

## 1. Tóm tắt Đính chính Kỹ thuật (Audit Lab 09)
1. **Kiểm kê Transistor `clg_4b` & CLA 4-bit:** `clg_4b` đầy đủ CMOS gồm `AOI21` ($6\text{T}$) + `AOI321` ($12\text{T}$) + `AOI4321` ($20\text{T}$) + `AOI54321` ($30\text{T}$) + 4 INV ($8\text{T}$) = **$76\text{T}$** (bản cũ ghi $62\text{T}$). Toàn bộ CLA 4-bit là **$132\text{T}$** (`4T` XOR), **$148\text{T}$** (`6T` XOR), hoặc **$164\text{T}$** (`8T` XOR như `cla_4bit_tran.sp`), không ra `134T (+19,6%)`.
2. **Phân biệt Số transistor vs Diện tích ($\Sigma W$):** `clg_4b` cố định $8\lambda/24\lambda$ có $\Sigma W = 1\,152\lambda$; nếu định cỡ cùng sức kéo ($8,12,16,20\lambda$ N và $24,36,48,60\lambda$ P) thì $\Sigma W = \mathbf{2\,288\lambda}$ (so với RCA $4 \times 528\lambda = 2\,112\lambda$).
3. **Bỏ khẳng định "nhanh hơn trên 60%":** Ước lượng thô $C_0 \to C_4$ cho $\approx 117\,\text{ps}$ so với RCA $\approx 240\,\text{ps}$ (giảm $\sim 51$%, chưa chắc vượt 60%).
4. **Đo đầy đủ đường $A, B \to C_4, S_3$:** Không chỉ đo $C_0$ (khi $P,G$ tĩnh); phải đo khi $G_0, P_0$ chuyển để thấy ảnh hưởng của tầng `PG` chịu tải nặng ($P_1, P_2$ xuất hiện $6$ lần $\implies W_{gate} = 192\lambda \approx 86\,\text{fF}$).

---

## 2. Đáp án Chi tiết Pre-lab & Bảng Đối Chuẩn

### 2.1 Khai triển $C_3$ & Đếm Transistor (`XOR = 8T`)
- $C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$.
- Với `XOR = 8T`: `pg_cell` $= 14\text{T}$ ($56\text{T}$), `clg_4b` $= 76\text{T}$, `sum_cell` $= 8\text{T}$ ($32\text{T}$) $\implies$ Tổng = **$164\text{T}$** (+46,4% so với RCA $112\text{T}$).
- $\Sigma W$ (`clg_4b` cố định $8\lambda/24\lambda$) = $1\,152\lambda$.

### 2.2 Tải Fan-in & Đường xấu nhất
- $P_1, P_2$: $6$ nhánh $\implies 192\lambda \approx 86,4\,\text{fF}$ ($12\times$ `inv_x1`).
- $G_0 \to C_4$ chậm hơn $C_0 \to C_4$ vì phải đi qua thêm tầng `PG` (`NAND2 + INV`) và nút $G_0$ gánh tải $4$ nhánh CLG ($128\lambda$).

---

## 3. Đáp án 3 Câu hỏi Thảo luận Post-lab
1. **Vai trò đo đường $A, B \to C_4, S_3$:** Ca $C_0 \to C_4$ bỏ qua độ trễ tầng `PG` và tải Fan-in nặng trên $P_1, P_2$.
2. **Cố định $8\lambda/24\lambda$ vs Cùng sức kéo:** Cỡ cố định làm chuỗi 5 transistor của `AOI54321` giảm sức kéo còn $\approx 40$% `inv_x1`; tăng cỡ theo độ sâu đưa $\Sigma W$ của `clg_4b` lên $2\,288\lambda$.
3. **Mở rộng 8/16-bit:** Phải dùng CLA phân cấp nhiều tầng (nhóm 4-bit dùng $P_G, G_G$) để tránh chuỗi AOI quá dài ($9-17$ transistor nối tiếp).
