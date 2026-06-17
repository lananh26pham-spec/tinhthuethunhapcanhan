import streamlit as st

# Cấu hình trang web của ứng dụng
st.set_page_config(page_title="App Tính Thuế TNCN Việt Nam_ĐỀ TÀI 7_ PHẠM THỊ LAN ANH", page_icon="💰", layout="centered")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write("Cập nhật theo quy định pháp luật thuế hiện hành tại Việt Nam")
st.markdown("---")

# --- PHẦN NHẬP DỮ LIỆU ĐẦU VÀO (TIẾNG VIỆT) ---
st.subheader("📋 Nhập thông tin thu nhập của bạn")

# 1. Nhập mức lương tổng
gross_salary = st.number_input(
    "Mức lương Tổng (Gross) của bạn trong tháng (VND):", 
    min_value=0, 
    value=20000000, 
    step=500000,
    format="%d"
)

# 2. Nhập số người phụ thuộc
dependents = st.number_input(
    "Số người phụ thuộc bạn đang nuôi dưỡng (người):", 
    min_value=0, 
    value=0, 
    step=1
)

# 3. Nhập tiền tăng ca
overtime_pay = st.number_input(
    "Tiền lương làm thêm giờ / tăng ca (VND):", 
    min_value=0, 
    value=0, 
    step=500000,
    format="%d",
    help="Theo luật VN, phần thu nhập cao hơn do làm đêm, làm thêm giờ được miễn thuế TNCN."
)

st.markdown("---")

# --- PHẦN LOGIC TÍNH TOÁN ---
if st.button("🧮 Tính Thuế & Nhận Kết Quả", type="primary"):
    
    # 1. Tính các khoản bảo hiểm bắt buộc (Tổng cộng 10.5% vào lương người lao động)
    # (Lưu ý: Thực tế có mức trần đóng BH theo lương cơ sở/lương tối thiểu vùng, dưới đây là công thức cơ bản)
    bhxh = gross_salary * 0.08
    bhyt = gross_salary * 0.015
    bhtn = gross_salary * 0.01
    total_insurance = bhxh + bhyt + bhtn
    
    # 2. Giảm trừ gia cảnh
    self_reduction = 11000000  # Giảm trừ bản thân: 11 triệu
    dependent_reduction = dependents * 4400000  # Giảm trừ người phụ thuộc: 4.4 triệu/người
    total_reduction = self_reduction + dependent_reduction
    
    # 3. Tính thu nhập chịu thuế và thu nhập tính thuế
    # Thu nhập chịu thuế = Gross - Lương tăng ca được miễn thuế
    taxable_income = max(0, gross_salary - overtime_pay)
    
    # Thu nhập tính thuế = Thu nhập chịu thuế - Bảo hiểm - Giảm trừ gia cảnh
    assessable_income = max(0, taxable_income - total_insurance - total_reduction)
    
    # 4. Tính toán thuế lũy tiến từng phần theo 7 bậc quy định tại VN
    tax = 0
    brackets = [
        {"limit": 5000000, "rate": 0.05, "desc": "Bậc 1: Đến 5 triệu đồng (5%)"},
        {"limit": 10000000, "rate": 0.10, "desc": "Bậc 2: Trên 5 đến 10 triệu đồng (10%)"},
        {"limit": 18000000, "rate": 0.15, "desc": "Bậc 3: Trên 10 đến 18 triệu đồng (15%)"},
        {"limit": 32000000, "rate": 0.20, "desc": "Bậc 4: Trên 18 đến 32 triệu đồng (20%)"},
        {"limit": 52000000, "rate": 0.25, "desc": "Bậc 5: Trên 32 đến 52 triệu đồng (25%)"},
        {"limit": 80000000, "rate": 0.30, "desc": "Bậc 6: Trên 52 đến 80 triệu đồng (30%)"},
        {"limit": float('inf'), "rate": 0.35, "desc": "Bậc 7: Trên 80 triệu đồng (35%)"}
    ]
    
    temp_income = assessable_income
    previous_limit = 0
    tax_breakdown = []
    
    for b in brackets:
        range_size = b["limit"] - previous_limit
        if temp_income > 0:
            taxable_in_bracket = min(temp_income, range_size)
            tax_in_bracket = taxable_in_bracket * b["rate"]
            tax += tax_in_bracket
            
            tax_breakdown.append({
                "Bậc thuế": b["desc"],
                "Thu nhập tính thuế ở bậc này": f"{taxable_in_bracket:,.0f} VND",
                "Tiền thuế phải nộp": f"{tax_in_bracket:,.0f} VND"
            })
            
            temp_income -= taxable_in_bracket
            previous_limit = b["limit"]
        else:
            break

    # 5. Lương NET thực nhận
    net_salary = gross_salary - total_insurance - tax

    # --- PHẦN HIỂN THỊ KẾT QUẢ ---
    st.subheader("🎯 Kết Quả Tính Toán Tóm Tắt")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tổng các khoản bảo hiểm trừ vào lương (10.5%)", value=f"{total_insurance:,.0f} VND")
        st.metric(label="Thuế TNCN bạn phải nộp", value=f"{tax:,.0f} VND")
    with col2:
        st.metric(label="LƯƠNG NET THỰC NHẬN", value=f"{net_salary:,.0f} VND", delta_color="inverse")

    st.markdown("---")
    st.subheader("📜 Giải Trình Chi Tiết Theo Luật Việt Nam")
    
    st.markdown(f"""
    * *Phí Bảo hiểm bắt buộc (trừ từ lương người lao động):*
        * Bảo hiểm xã hội (8%): {bhxh:,.0f} VND
        * Bảo hiểm y tế (1.5%): {bhyt:,.0f} VND
        * Bảo hiểm thất nghiệp (1%): {bhtn:,.0f} VND
    * *Các khoản giảm trừ gia cảnh:*
        * Giảm trừ cá nhân bản thân: 11,000,000 VND
        * Giảm trừ người phụ thuộc: {dependent_reduction:,.0f} VND (cho {dependents} người bạn nuôi dưỡng)
    * *Phần tăng ca miễn thuế:* {overtime_pay:,.0f} VND (Không tính vào thu nhập chịu thuế)
    * *Thu nhập tính thuế cuối cùng:* {assessable_income:,.0f} VND (Đây là số tiền đem đi áp vào bảng bậc thuế lũy tiến)
    """)
    
    if tax > 0:
        st.write("📊 *Chi tiết phân tách số tiền nộp theo từng bậc thuế:*")
        st.table(tax_breakdown)
    else:
        st.success("Thật tuyệt! Thu nhập tính thuế của bạn bằng 0 nên bạn chưa phải nộp thuế TNCN.")
