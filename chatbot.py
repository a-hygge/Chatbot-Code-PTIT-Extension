# chatbot.py
import json
import os
import google.generativeai as genai
from typing import Dict, List
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Lỗi: Không tìm thấy GOOGLE_API_KEY trong file .env")
genai.configure(api_key=GOOGLE_API_KEY)

def get_youtube_thumbnail(video_url: str) -> str:
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return ""
    try:
        if "youtu.be" in video_url:
             video_id = urlparse(video_url).path.strip('/')
        else:
             query = urlparse(video_url).query
             video_id = parse_qs(query).get("v", [None])[0]
        
        if video_id:
            return f"http://i3.ytimg.com/vi/{video_id}/mqdefault.jpg"
    except Exception as e:
        print(f"Không thể lấy ID video từ URL '{video_url}': {e}")
        return ""
    return ""

def load_video_data(filepath: str = "playlist_videos.json") -> List[Dict]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi tải dữ liệu video: {e}")
        return []

def classify_task(question: str) -> str:
    classification_prompt = f"""
    Bạn là một trình phân loại nhiệm vụ cho nền tảng giáo dục Code PTIT. 
    Dựa trên câu hỏi sau, hãy xác định chức năng nào liên quan nhất. 
    Chỉ xuất ra một tên nhiệm vụ duy nhất trong danh sách dưới đây, không thêm giải thích.
    Danh sách nhiệm vụ: calendar, groups, sections, bigbluebutton, outcomes_rubrics, question_banks, student_guide, grading_groups, rubrics, announcements_discussions, grading_feedback, registration, assignments, modules, materials, terms, batch_students, random_questions, copy_content, course_thumbnail, course_creation, general
    Câu hỏi: "{question}"
    Nhiệm vụ:
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(classification_prompt, generation_config={"temperature": 0.0})
    return response.text.strip().lower()

def generate_prompt(task: str, question: str) -> str:
    prompt = f"""
    Bạn là một chuyên gia tư vấn về hệ thống Code PTIT, vai trò của bạn là hỗ trợ các giảng viên.
    Một giảng viên đang có câu hỏi sau: "{question}"
    Câu hỏi này đã được phân loại vào chức năng: "{task}"
    Nhiệm vụ của bạn là cung cấp một câu trả lời **tóm tắt, ngắn gọn** các bước chính để giảng viên có thể thực hiện được yêu cầu. 
    Chỉ nêu các ý chính, không cần đi vào chi tiết từng nút bấm.
    Hãy trình bày câu trả lời một cách rõ ràng, chuyên nghiệp. Dùng markdown.
    QUAN TRỌNG: Câu trả lời phải hoàn toàn bằng tiếng Việt và thật súc tích.
    """
    return prompt

def call_gemini_api(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config={"temperature": 0.2})
        return response.text
    except Exception as e:
        print(f"Lỗi khi gọi API Gemini: {e}")
        return "Đã xảy ra lỗi khi kết nối đến dịch vụ AI. Vui lòng thử lại sau."

def find_relevant_videos(task: str, videos: List[Dict]) -> List[Dict]:
    task_keywords = {
        "calendar": ["calendar", "lịch"], "groups": ["group", "nhóm học"], "assignments": ["assignment", "bài tập"],
        "modules": ["module", "nội dung khóa học"], "materials": ["tài liệu", "bài giảng"], "general": ["Code PTIT"]
    }
    keywords_to_search = task_keywords.get(task, [task])
    relevant_videos = []
    for video in videos:
        text_to_search = (video.get("title", "") + " " + video.get("description", "")).lower()
        if any(keyword.lower() in text_to_search for keyword in keywords_to_search):
            relevant_videos.append(video)
    return relevant_videos

def process_question(question: str) -> Dict:
    print(f"Bắt đầu xử lý câu hỏi: '{question}'")
    videos = load_video_data()
    task = classify_task(question)
    print(f"   -> Nhiệm vụ: '{task}'")
    
    relevant_videos = find_relevant_videos(task, videos)
    
    for video in relevant_videos:
        video['thumbnail'] = get_youtube_thumbnail(video.get('link', ''))
    
    print(f"   -> Tìm thấy {len(relevant_videos)} video, đã thêm thumbnail.")
    
    prompt = generate_prompt(task, question)
    response_text = call_gemini_api(prompt)
    
    response = {"text": response_text, "videos": relevant_videos}
    print("Hoàn tất xử lý.")
    return response

# --- PHẦN 4: KHỐI THỰC THI THỬ NGHIỆM ---

if __name__ == "__main__":
    # Phần này chỉ chạy khi bạn thực thi file này trực tiếp (python chatbot.py)
    # Dùng để kiểm tra nhanh logic của chatbot.
    print("--- CHẠY THỬ NGHIỆM MODULE CHATBOT ---")
    
    sample_questions = [
        "Làm sao tạo bài tập mới?",
        "Làm thế nào để tạo nhóm học cho sinh viên?",
        "Làm sao để đăng tài liệu lên khóa học?",
        "Làm cách nào để thiết lập lịch cho lớp học?"
    ]

    for q in sample_questions:
        print("\n" + "="*50)
        print(f"📚 CÂU HỎI: {q}")
        response = process_question(q)
        print("\n📝 CÂU TRẢ LỜI TỪ AI:")
        print(response['text'])
        
        if response['videos']:
            print("\n🎬 VIDEO HƯỚDẪN LIÊN QUAN:")
            for video in response['videos']:
                print(f"  - Tiêu đề: {video['title']}")
                print(f"    Link: {video['link']}")
        else:
            print("\n🎬 Không tìm thấy video hướng dẫn liên quan.")
        print("="*50)