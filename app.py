import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Trợ lý Quản lý Giáo dục", 
    page_icon="🎓", 
    layout="wide"
)

st.markdown("""
<style>
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
    
    [data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
    }
    
    [data-testid="stChatMessage"] {
        background: transparent !important;
    }
    
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] h1,
    [data-testid="stChatMessageContent"] h2,
    [data-testid="stChatMessageContent"] h3,
    [data-testid="stChatMessageContent"] li {
        color: #333 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
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
    
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    h1, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)
#code by trungnam 
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
        📚 Trợ lý Quản lý Giáo dục 🎓
    </h1>
    <p style='color: white; font-size: 1.3em; margin: 15px 0 0 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);'>
        Hỗ trợ Ban Giám hiệu phân tích và giải quyết vấn đề quản lý nhà trường
    </p>
</div>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Có lỗi xảy ra: {str(e)}")
    st.stop()

SYSTEM_PROMPT = """Bạn là trợ lý quản lý giáo dục chuyên nghiệp, hỗ trợ Ban Giám hiệu nhà trường.

NHIỆM VỤ CỦA BẠN:
- Phân tích các vấn đề quản lý giáo dục một cách chuyên sâu, có cấu trúc
- Đưa ra giải pháp cụ thể, khả thi, dựa trên nghiên cứu quản lý hiện đại
- Hỗ trợ xây dựng kế hoạch hành động chi tiết
- Tạo tài liệu báo cáo chuyên nghiệp

PHONG CÁCH GIAO TIẾP:
- Chuyên nghiệp, rõ ràng, có cấu trúc bullet points
- Sử dụng icon phù hợp: 📚 📊 🎯 💡 ✅ 📋 👥 🏫
- Đưa ra lựa chọn cụ thể cho người dùng
- Phân tích nguyên nhân trước khi đưa giải pháp

KHI NGƯỜI DÙNG CHỌN VẤN ĐỀ:
1. Liệt kê 4-5 nguyên nhân có thể
2. Đưa ra 3 hướng hỗ trợ cụ thể
3. Khi được yêu cầu, cung cấp 5 biện pháp chi tiết

KHI ĐƯỢC YÊU CẦU TẠO TÀI LIỆU:
- Kế hoạch: Format rõ ràng, có mục tiêu, hoạt động, thời gian
- Báo cáo: Cấu trúc đầy đủ với tình huống, nguyên nhân, giải pháp
- Checklist: Chia theo tuần, cụ thể, có trách nhiệm

LUÔN GIỮ THÁI ĐỘ: Tôn trọng, hỗ trợ, không phán xét."""

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    welcome_message = """👋 Xin chào Ban Giám hiệu!

Tôi là trợ lý quản lý giáo dục. Nhà trường đang gặp 3 vấn đề nổi bật gần đây. Bạn muốn phân tích vấn đề nào trước?

**1. Chất lượng giảng dạy của một số tổ chuyên môn giảm sút**

**2. Bất đồng quan điểm giữa các nhóm giáo viên thế hệ khác nhau**

**3. Mức độ tham gia hoạt động chung không đồng đều**

---

Hãy chọn số **1, 2, 3** hoặc mô tả vấn đề khác bạn đang gặp phải."""
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Kiểm tra xem có message mới từ button sidebar không
if "pending_response" not in st.session_state:
    st.session_state.pending_response = False

# Hiển thị tất cả messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý AI response nếu có message mới từ button
if st.session_state.pending_response and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if last_message["role"] == "user":
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                conversation_history = ""
                for msg in st.session_state.messages:
                    role = "Người dùng" if msg["role"] == "user" else "Trợ lý"
                    conversation_history += f"{role}: {msg['content']}\n\n"
                
                full_prompt = f"""{SYSTEM_PROMPT}

LỊCH SỬ HỘI THOẠI:
{conversation_history}

Ban Giám hiệu vừa hỏi: {last_message['content']}

Hãy trả lời theo vai trò trợ lý quản lý giáo dục chuyên nghiệp. Phân tích vấn đề và đưa ra các lựa chọn hỗ trợ cụ thể."""
                
                # Streaming response
                response = model.generate_content(full_prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_message = f"Có lỗi xảy ra: {str(e)}"
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        
        st.session_state.pending_response = False
        st.rerun()

# Xử lý input từ chat
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            conversation_history = ""
            for msg in st.session_state.messages:
                role = "Người dùng" if msg["role"] == "user" else "Trợ lý"
                conversation_history += f"{role}: {msg['content']}\n\n"
            
            full_prompt = f"""{SYSTEM_PROMPT}

LỊCH SỬ HỘI THOẠI:
{conversation_history}

Ban Giám hiệu vừa hỏi: {prompt}

Hãy trả lời theo vai trò trợ lý quản lý giáo dục chuyên nghiệp. Phân tích vấn đề và đưa ra các lựa chọn hỗ trợ cụ thể."""
            
            # Streaming response
            response = model.generate_content(full_prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"Có lỗi xảy ra: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

with st.sidebar:
    st.markdown("### 🎒 Công cụ quản lý")
    st.markdown("---")
    
    st.markdown("#### 🏫 Vấn đề phổ biến")
    
    if st.button("📊 Chất lượng giảng dạy"):
        prompt = "Phân tích vấn đề: Chất lượng giảng dạy của một số tổ chuyên môn giảm sút"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    if st.button("👥 Bất đồng thế hệ"):
        prompt = "Phân tích vấn đề: Bất đồng quan điểm giữa các nhóm giáo viên thế hệ khác nhau"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    if st.button("🎯 Tham gia hoạt động"):
        prompt = "Phân tích vấn đề: Mức độ tham gia hoạt động chung không đồng đều"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### 📝 Tài liệu hỗ trợ")
    
    if st.button("📋 Kế hoạch can thiệp"):
        prompt = "Viết kế hoạch can thiệp 1 trang cho vấn đề đang thảo luận"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    if st.button("📈 Báo cáo phân tích"):
        prompt = "Xây dựng báo cáo phân tích tình huống chi tiết"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    if st.button("✅ Checklist 30 ngày"):
        prompt = "Tạo checklist việc cần làm trong 30 ngày"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    if st.button("📄 Tài liệu báo cáo GV"):
        prompt = "Tạo tài liệu để báo cáo cho giáo viên"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_response = True
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Cuộc trò chuyện mới"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**💝 Tạo bởi LeHien**")
    st.markdown("**🌸TN Dành tặng cô giáo mầm non**")
