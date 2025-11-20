import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(
    page_title="Trợ lý Giáo viên Mầm Non", 
    page_icon="🌈", 
    layout="wide"
)

# CSS hiện đại với gradient đẹp
st.markdown("""
<style>
    /* Background gradient mềm mại */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card container cho chat */
    [data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Avatar containers */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
    }
    
    /* Toàn bộ chat message container */
    [data-testid="stChatMessage"] {
        background: transparent !important;
    }
    
    /* Markdown trong chat */
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] h1,
    [data-testid="stChatMessageContent"] h2,
    [data-testid="stChatMessageContent"] h3,
    [data-testid="stChatMessageContent"] li {
        color: #333 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Nút bấm glassmorphism */
    .stButton>button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(10px);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.3));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.6);
    }
    
    /* Input box */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Header styling */
    h1, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header với glassmorphism
st.markdown("""
<div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1));
            backdrop-filter: blur(20px);
            padding: 40px;
            border-radius: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 30px;'>
    <h1 style='color: white; font-size: 3em; margin: 0; text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);'>
        🌈 Trợ lý Giáo viên Mầm Non 🎨
    </h1>
    <p style='color: white; font-size: 1.3em; margin: 15px 0 0 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        ✨ Chào cô! Mình sẵn sàng hỗ trợ cô quản lý lớp học! ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Cấu hình API Key từ secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Khởi tạo model - sử dụng gemini-2.5-flash (mới nhất và nhanh)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"❌ Có lỗi xảy ra: {str(e)}")
    st.stop()

# System prompt cho chatbot quản lý giáo dục mầm non
SYSTEM_PROMPT = """Bạn là trợ lý thân thiện dành cho giáo viên mầm non, sử dụng giọng điệu ấm áp, gần gũi.

NHIỆM VỤ CỦA BẠN:
- Hỗ trợ giáo viên mầm non giải quyết các vấn đề quản lý lớp học
- Đưa ra giải pháp cụ thể, dễ áp dụng, phù hợp với độ tuổi mầm non (3-6 tuổi)
- Tạo kế hoạch hoạt động, trò chơi, bài học cho trẻ
- Tư vấn cách xử lý tình huống với trẻ và phụ huynh

PHONG CÁCH GIAO TIẾP:
- Thân thiện, ấm áp, dùng emoji phù hợp 🌈 🎨 ⭐ 💕
- Xưng hô "cô" với giáo viên, "các bé" với trẻ
- Ngôn ngữ đơn giản, dễ hiểu, gần gũi
- Luôn động viên và khích lệ giáo viên

KHI BẮT ĐẦU CUỘC TRÒ CHUYỆN:
Chào thân thiện và giới thiệu 3 vấn đề phổ biến mà giáo viên mầm non thường gặp.

KHI PHÂN TÍCH VẤN ĐỀ:
- Đồng cảm với giáo viên
- Đưa ra giải pháp thực tế, dễ làm
- Cung cấp ví dụ cụ thể về hoạt động, trò chơi
- Luôn nhấn mạnh sự phát triển tích cực của trẻ

HÃY BẮT ĐẦU BẰNG LỜI CHÀO ẤM ÁP."""

# Khởi tạo session state để lưu lịch sử chat và chế độ
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "👶 Giáo viên Mầm Non"

# Kiểm tra nếu chế độ thay đổi thì reset chat và gửi tin nhắn chào mới
if "mode" in locals() and mode != st.session_state.current_mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode

# Tin nhắn chào mừng theo chế độ
if len(st.session_state.messages) == 0:
    if st.session_state.current_mode == "👶 Giáo viên Mầm Non":
        welcome_message = """Chào cô! 🌸

Mình là trợ lý dành riêng cho các cô giáo mầm non. Mình sẵn sàng giúp cô giải quyết các vấn đề trong công việc!

**Các cô thường gặp 3 vấn đề này. Cô đang gặp vấn đề nào?**

**1. Trẻ không chú ý, hay nghịch phá trong giờ học**
Các bé chạy nhảy, không nghe lời, giờ học mất trật tự

**2. Khó khăn trong giao tiếp với phụ huynh**
Phụ huynh quá lo lắng, đòi hỏi nhiều, hoặc ít quan tâm đến con

**3. Thiết kế hoạt động học chơi hấp dẫn cho trẻ**
Cần ý tưởng trò chơi, bài học mới lạ, phù hợp lứa tuổi

---

Cô hãy chọn số 1, 2, 3 hoặc chia sẻ vấn đề khác nhé! Mình sẽ cùng cô tìm giải pháp!"""
    else:  # Chế độ Ban Giám hiệu
        welcome_message = """Xin chào Ban Giám hiệu! 🎓

Tôi là trợ lý quản lý giáo dục. Nhà trường đang gặp 3 vấn đề nổi bật gần đây. Bạn muốn phân tích vấn đề nào trước?

**1. Chất lượng giảng dạy của một số tổ chuyên môn giảm sút**

**2. Bất đồng quan điểm giữa các nhóm giáo viên thế hệ khác nhau**

**3. Mức độ tham gia hoạt động chung không đồng đều**

---

Hãy chọn số 1, 2, 3 hoặc mô tả vấn đề khác bạn đang gặp phải."""
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input từ người dùng
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    # Thêm tin nhắn người dùng vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gọi API Gemini và hiển thị phản hồi
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Tạo context từ lịch sử chat
            conversation_history = ""
            for msg in st.session_state.messages:
                role = "Người dùng" if msg["role"] == "user" else "Trợ lý"
                conversation_history += f"{role}: {msg['content']}\n\n"
            
            # Tạo prompt đầy đủ với system prompt và context
            full_prompt = f"""{SYSTEM_PROMPT}

LỊCH SỬ HỘI THOẠI:
{conversation_history}

Cô vừa hỏi: {prompt}

Hãy trả lời theo vai trò trợ lý thân thiện của giáo viên mầm non. Sử dụng emoji phù hợp, giọng điệu ấm áp, gần gũi."""
            
            # Gửi tin nhắn đến Gemini
            response = model.generate_content(full_prompt)
            full_response = response.text
            
            # Hiển thị phản hồi
            message_placeholder.markdown(full_response)
            
            # Lưu phản hồi vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"❌ Có lỗi xảy ra: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Sidebar với glass effect
with st.sidebar:
    st.markdown("### 🎯 Chế độ làm việc")
    
    # Thêm radio button để chọn chế độ
    mode = st.radio(
        "Chọn vai trò:",
        ["👶 Giáo viên Mầm Non", "🎓 Ban Giám hiệu"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if mode == "👶 Giáo viên Mầm Non":
        st.markdown("### 🎀 Công cụ hỗ trợ nhanh")
        st.markdown("#### 📚 Hoạt động học")
        
        if st.button("🎨 Hoạt động học chơi"):
            prompt = "Gợi ý hoạt động học chơi vui nhộn cho trẻ mầm non"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("🎭 Trò chơi phát triển"):
            prompt = "Ý tưởng trò chơi phát triển kỹ năng cho trẻ"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("🎵 Bài hát vận động"):
            prompt = "Bài hát và động tác cho trẻ mầm non"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### 💬 Phụ huynh")
        
        if st.button("👨‍👩‍👧 Tin nhắn phụ huynh"):
            prompt = "Mẫu tin nhắn gửi phụ huynh"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("📋 Báo cáo phát triển"):
            prompt = "Cách viết báo cáo phát triển của trẻ"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### 🎯 Xử lý tình huống")
        
        if st.button("😢 Trẻ khóc, quấy"):
            prompt = "Cách xử lý trẻ khóc và quấy phá"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("🤝 Kỹ năng xã hội"):
            prompt = "Dạy trẻ kỹ năng xã hội"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
    
    else:  # Chế độ Ban Giám hiệu
        st.markdown("### 📊 Quản lý nhà trường")
        st.markdown("#### 🎯 Vấn đề phổ biến")
        
        if st.button("📉 Chất lượng giảng dạy"):
            prompt = "Phân tích vấn đề chất lượng giảng dạy của một số tổ chuyên môn giảm sút"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("👥 Bất đồng thế hệ"):
            prompt = "Phân tích vấn đề bất đồng quan điểm giữa các nhóm giáo viên thế hệ khác nhau"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("📊 Tham gia hoạt động"):
            prompt = "Phân tích vấn đề mức độ tham gia hoạt động chung không đồng đều"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### 📝 Tài liệu hỗ trợ")
        
        if st.button("📋 Kế hoạch can thiệp"):
            prompt = "Viết kế hoạch can thiệp 1 trang cho vấn đề đang thảo luận"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("📊 Báo cáo phân tích"):
            prompt = "Xây dựng báo cáo phân tích tình huống chi tiết"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("✅ Checklist 30 ngày"):
            prompt = "Tạo checklist việc cần làm trong 30 ngày"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
        
        if st.button("📄 Tài liệu báo cáo"):
            prompt = "Tạo tài liệu để báo cáo cho giáo viên"
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Cuộc trò chuyện mới"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**💕 Tạo bởi LeHien**")
    st.markdown("*Dành tặng cô giáo mầm non*")

# Nút xóa lịch sử chat (giữ lại ở cuối cho backward compatibility)
if st.button("🗑️ Xóa lịch sử chat"):
    st.session_state.messages = []
    st.rerun()
