import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Bảng màu tham chiếu lấy từ code gốc của người dùng.
COLOR_REFERENCE_MATRIX = [
    {"level":1,"fi":100,"rsl":48.0,"status":"AN TOÀN","badge_bg":(46,125,50),"zone_a":{"hex":"#ECE359","rgb":(236,227,89)},"zone_b":{"hex":"#8B4513","rgb":(139,69,19)}},
    {"level":2,"fi":90,"rsl":43.2,"status":"AN TOÀN","badge_bg":(46,125,50),"zone_a":{"hex":"#EEDD50","rgb":(238,221,80)},"zone_b":{"hex":"#E33132","rgb":(227,49,50)}},
    {"level":3,"fi":80,"rsl":38.4,"status":"AN TOÀN","badge_bg":(46,125,50),"zone_a":{"hex":"#F0CE48","rgb":(240,206,72)},"zone_b":{"hex":"#B22222","rgb":(178,34,34)}},
    {"level":4,"fi":70,"rsl":33.6,"status":"CHUYỂN GIAI ĐOẠN","badge_bg":(21,101,192),"zone_a":{"hex":"#E8A23C","rgb":(232,162,60)},"zone_b":{"hex":"#78321E","rgb":(120,50,30)}},
    {"level":5,"fi":60,"rsl":28.8,"status":"CẢNH BÁO","badge_bg":(230,81,0),"zone_a":{"hex":"#DF6E52","rgb":(223,110,82)},"zone_b":{"hex":"#552837","rgb":(85,40,55)}},
    {"level":6,"fi":50,"rsl":24.0,"status":"CẢNH BÁO","badge_bg":(230,81,0),"zone_a":{"hex":"#D84873","rgb":(216,72,115)},"zone_b":{"hex":"#32463C","rgb":(50,70,60)}},
    {"level":7,"fi":40,"rsl":19.2,"status":"CẢNH BÁO NẶNG","badge_bg":(230,81,0),"zone_a":{"hex":"#BC3D8D","rgb":(188,61,141)},"zone_b":{"hex":"#2E8B57","rgb":(46,139,87)}},
    {"level":8,"fi":30,"rsl":14.4,"status":"NGUY HIỂM","badge_bg":(198,40,40),"zone_a":{"hex":"#9B33A0","rgb":(155,51,160)},"zone_b":{"hex":"#1E643C","rgb":(30,100,60)}},
    {"level":9,"fi":20,"rsl":9.6,"status":"NGUY HIỂM","badge_bg":(198,40,40),"zone_a":{"hex":"#7B28AA","rgb":(123,40,170)},"zone_b":{"hex":"#0F4B28","rgb":(15,75,40)}},
    {"level":10,"fi":0,"rsl":0.0,"status":"NGUY HIỂM","badge_bg":(198,40,40),"zone_a":{"hex":"#5E1D9E","rgb":(94,29,158)},"zone_b":{"hex":"#052314","rgb":(5,35,20)}},
]

st.set_page_config(page_title="FreshScan | Quét độ tươi", page_icon="🧪", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Be Vietnam Pro',sans-serif;}
.stApp {background:linear-gradient(180deg,#f3faf7 0%,#f8fafc 50%,#eef5f2 100%);}
.hero {padding:1.8rem 2rem;border-radius:24px;background:linear-gradient(120deg,#103f36,#176b57);color:white;margin-bottom:1rem;}
.hero h1 {font-size:2.35rem;line-height:1.15;margin:0 0 .5rem 0;}
.hero p {font-size:1rem;opacity:.9;margin:0;}
.pill {display:inline-block;padding:.35rem .75rem;border-radius:99px;background:#d7f4e5;color:#155e46;font-weight:700;font-size:.8rem;margin-bottom:.8rem;}
.metric {background:white;border:1px solid #e1eee8;border-radius:18px;padding:1.1rem;}
.small-note {color:#64748b;font-size:.88rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="pill">SMART FOOD SENSOR · PROTOTYPE</div><h1>FreshScan 🧪</h1><p>Quét màu cảm biến kép để ước tính độ tươi thực phẩm từ ảnh tem hai vùng màu.</p></div>', unsafe_allow_html=True)
with st.sidebar:
    st.header("📷 Cách quét")
    st.markdown("1. Chụp **tem cảm biến hai ô** ở ánh sáng trắng, đều.\n2. Đặt ô A bên trái, ô B bên phải.\n3. Tránh bóng đổ, đèn màu và phản chiếu.\n4. Tải ảnh lên rồi nhấn **Phân tích màu**.")
    st.warning("Ảnh cần tập trung vào tem cảm biến, không phải ảnh toàn bộ món ăn.")
    st.caption("Định dạng: PNG, JPG, JPEG, BMP")

uploaded = st.file_uploader("Tải ảnh tem cảm biến lên", type=["png","jpg","jpeg","bmp"], help="Ô A nằm bên trái, ô B nằm bên phải.")
if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Ảnh đã tải lên", use_container_width=True)
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("#### Vùng màu trong ảnh")
        st.caption("Code gốc chia ảnh thành hai nửa: trái là Zone A, phải là Zone B; lấy trung bình màu ở vùng giữa mỗi nửa.")
    with col2:
        st.markdown("#### Kiểm tra trước khi quét")
        st.info("Hãy đảm bảo hai ô màu nằm đúng vị trí trái/phải và chiếm phần lớn ảnh. Nếu ảnh bị xoay hoặc có nhiều nền, kết quả có thể sai.")
    if st.button("🔬 Phân tích màu", type="primary", use_container_width=True):
        arr = np.array(image)
        h, w, _ = arr.shape
        crop_a = arr[:, :int(w*0.48)]
        crop_b = arr[:, int(w*0.52):]
        if crop_a.size == 0 or crop_b.size == 0:
            st.error("Không thể tách hai vùng màu từ ảnh này.")
            st.stop()
        ha, wa, _ = crop_a.shape
        hb, wb, _ = crop_b.shape
        roi_a = crop_a[int(ha*.2):int(ha*.8), int(wa*.2):int(wa*.8)]
        roi_b = crop_b[int(hb*.2):int(hb*.8), int(wb*.2):int(wb*.8)]
        rgb_a = tuple(np.mean(roi_a, axis=(0,1)).astype(int).tolist())
        rgb_b = tuple(np.mean(roi_b, axis=(0,1)).astype(int).tolist())
        best = None
        min_dist = float("inf")
        for ref in COLOR_REFERENCE_MATRIX:
            da = np.linalg.norm(np.array(rgb_a)-np.array(ref["zone_a"]["rgb"]))
            db = np.linalg.norm(np.array(rgb_b)-np.array(ref["zone_b"]["rgb"]))
            dist = (da+db)*.5
            if dist < min_dist:
                min_dist, best = dist, ref
        st.markdown("---")
        st.subheader("Kết quả phân tích")
        if best["fi"] >= 80:
            st.success(f"🟢 {best['status']}")
        elif best["fi"] >= 60:
            st.info(f"🔵 {best['status']}")
        elif best["fi"] >= 40:
            st.warning(f"🟠 {best['status']}")
        else:
            st.error(f"🔴 {best['status']}")
        m1,m2,m3 = st.columns(3)
        m1.metric("Chỉ số FI dự đoán", f"{best['fi']}%")
        m2.metric("Mức màu khớp", f"{best['level']}/10")
        m3.metric("RSL theo bảng gốc", f"{best['rsl']:.1f} giờ")
        st.progress(best["fi"]/100)
        a,b = st.columns(2)
        with a:
            st.markdown("**Zone A · PVA/Alizarin**")
            st.markdown(f'<div style="height:58px;border-radius:12px;background:rgb{rgb_a};border:1px solid #ddd"></div>', unsafe_allow_html=True)
            st.write(f"Màu đo được: RGB {rgb_a}")
            st.caption(f"Màu tham chiếu: {best['zone_a']['hex']} · RGB {best['zone_a']['rgb']}")
        with b:
            st.markdown("**Zone B · Agarose/Myoglobin**")
            st.markdown(f'<div style="height:58px;border-radius:12px;background:rgb{rgb_b};border:1px solid #ddd"></div>', unsafe_allow_html=True)
            st.write(f"Màu đo được: RGB {rgb_b}")
            st.caption(f"Màu tham chiếu: {best['zone_b']['hex']} · RGB {best['zone_b']['rgb']}")
        st.caption(f"Khoảng cách màu tới mẫu tham chiếu gần nhất: {min_dist:.1f} (RGB Euclidean, càng thấp càng giống).")
        result = image.copy()
        st.download_button("⬇️ Tải ảnh gốc", data=uploaded.getvalue(), file_name=uploaded.name, mime=uploaded.type)
else:
    st.markdown("""
    <div style="background:white;border:1px dashed #9bbdb0;border-radius:20px;padding:2rem;text-align:center">
    <div style="font-size:2.4rem">🖼️</div>
    <h3>Chưa có ảnh để quét</h3>
    <p style="color:#64748b">Tải lên ảnh tem cảm biến hai vùng màu để bắt đầu phân tích.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🎨 Bảng màu tham chiếu")
st.caption("Các màu dưới đây được lấy từ ma trận 10 mức trong code bạn cung cấp.")
cols = st.columns(5)
for i, ref in enumerate(COLOR_REFERENCE_MATRIX):
    with cols[i%5]:
        st.markdown(f'<div style="background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px;margin-bottom:10px"><b>Mức {ref["level"]} · FI {ref["fi"]}%</b><div style="display:flex;gap:6px;margin:8px 0"><div title="Zone A" style="height:28px;flex:1;border-radius:6px;background:{ref["zone_a"]["hex"]}"></div><div title="Zone B" style="height:28px;flex:1;border-radius:6px;background:{ref["zone_b"]["hex"]}"></div></div><small>{ref["status"]}</small></div>', unsafe_allow_html=True)

st.markdown("""
<div class="small-note">
<b>Lưu ý khoa học:</b> Đây là công cụ nguyên mẫu đối chiếu màu ảnh với ma trận tham chiếu trong code, không phải phép đo an toàn thực phẩm đã được kiểm định. FI (%) và RSL (giờ) là giá trị do bảng tham chiếu quy định, không phải kết quả kiểm nghiệm thực tế. Ánh sáng, camera, cân bằng trắng, vị trí tem và loại thực phẩm có thể làm thay đổi kết quả. Không dùng kết quả này để quyết định ăn hay bỏ thực phẩm; hãy tuân thủ bảo quản và hướng dẫn an toàn thực phẩm.
</div>
""", unsafe_allow_html=True)
