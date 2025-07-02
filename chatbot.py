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

def generate_prompt(question: str, has_video: bool = False) -> str:
    """Tạo prompt cho AI dựa trên câu hỏi và có video hay không"""
    if has_video:
        prompt = f"""
        Bạn là một chuyên gia tư vấn về hệ thống Code PTIT, vai trò của bạn là hỗ trợ các giảng viên.
        Một giảng viên đang có câu hỏi sau: "{question}"
        
        Nhiệm vụ của bạn là cung cấp một câu trả lời **tóm tắt, ngắn gọn** các bước chính để giảng viên có thể thực hiện được yêu cầu. 
        Chỉ nêu các ý chính, không cần đi vào chi tiết từng nút bấm vì đã có video hướng dẫn chi tiết.
        Hãy trình bày câu trả lời một cách rõ ràng, chuyên nghiệp. Dùng markdown.
        QUAN TRỌNG: Câu trả lời phải hoàn toàn bằng tiếng Việt và thật súc tích.
        """
    else:
        prompt = f"""
        Bạn là một chuyên gia tư vấn về hệ thống Code PTIT (Canvas LMS), vai trò của bạn là hỗ trợ các giảng viên.
        Một giảng viên đang có câu hỏi sau: "{question}"
        
        Nhiệm vụ của bạn là cung cấp câu trả lời CHI TIẾT, cụ thể về cách thực hiện yêu cầu trên hệ thống Code PTIT.
        Hãy đưa ra hướng dẫn từng bước, bao gồm:
        - Các bước thực hiện cụ thể
        - Vị trí của các menu, nút bấm
        - Lưu ý quan trọng khi thực hiện
        
        Hãy trình bày câu trả lời một cách rõ ràng, chuyên nghiệp. Dùng markdown.
        QUAN TRỌNG: Câu trả lời phải hoàn toàn bằng tiếng Việt và chi tiết.
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

def find_relevant_videos(question: str, videos: List[Dict]) -> List[Dict]:
    """Tìm 1 video phù hợp nhất dựa trên câu hỏi và nội dung video"""
    if not videos:
        return []
    
    video_descriptions = []
    for i, video in enumerate(videos):
        title = video.get('title', '')
        description = video.get('description', '')
        video_descriptions.append(f"{i+1}. Tiêu đề: {title}\n   Mô tả: {description}")
    
    video_list_text = "\n".join(video_descriptions)
    
    selection_prompt = f"""
    Bạn là chuyên gia phân tích nội dung video giáo dục về hệ thống Code PTIT.
    Câu hỏi của người dùng: "{question}"
    
    Danh sách video có sẵn:
    {video_list_text}
    
    Hãy phân tích câu hỏi và so sánh với tiêu đề + mô tả của từng video để tìm video phù hợp NHẤT.
    Chỉ xuất ra số thứ tự của video (ví dụ: 5), không giải thích gì thêm.
    Nếu KHÔNG CÓ video nào thực sự phù hợp với câu hỏi, xuất ra số 0.
    
    Lưu ý: Chỉ chọn video khi có độ tương đồng cao về nội dung, không chọn video chung chung.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(selection_prompt, generation_config={"temperature": 0.1})
        selected_index = int(response.text.strip()) - 1
        
        if 0 <= selected_index < len(videos):
            return [videos[selected_index]]
        else:
            return []
    except Exception as e:
        print(f"Lỗi khi chọn video bằng AI: {e}")
        return find_relevant_videos_fallback(question, videos)

def find_relevant_videos_fallback(question: str, videos: List[Dict]) -> List[Dict]:
    """Phương pháp dự phòng để tìm video phù hợp"""
    question_lower = question.lower()
    scored_videos = []
    
    for video in videos:
        title = video.get('title', '').lower()
        description = video.get('description', '').lower()
        content = title + " " + description
        
        score = 0
        question_words = question_lower.split()
        
        for word in question_words:
            if len(word) > 2:  
                score += content.count(word) * 2  
                if word in title:
                    score += 3  
        
        if score > 0:
            scored_videos.append((score, video))
    
    if scored_videos:
        scored_videos.sort(key=lambda x: x[0], reverse=True)
        if scored_videos[0][0] >= 4:
            return [scored_videos[0][1]]
    
    return []

def process_question(question: str) -> Dict:
    print(f"Bắt đầu xử lý câu hỏi: '{question}'")
    videos = load_video_data()
    
    relevant_videos = find_relevant_videos(question, videos)
    
    for video in relevant_videos:
        video['thumbnail'] = get_youtube_thumbnail(video.get('link', ''))
    
    print(f"   -> Đã chọn {len(relevant_videos)} video phù hợp nhất.")
    
    has_video = len(relevant_videos) > 0
    prompt = generate_prompt(question, has_video)
    response_text = call_gemini_api(prompt)
    
    response = {"text": response_text, "videos": relevant_videos}
    print("Hoàn tất xử lý.")
    return response


if __name__ == "__main__":
    print("--- CHẠY THỬ NGHIỆM MODULE CHATBOT ---")
    
    sample_questions = [
        "Làm sao tạo bài tập mới?",
        "Làm thế nào để tạo nhóm học cho sinh viên?",
        "Làm sao để đăng tài liệu lên khóa học?",
        "Làm cách nào để thiết lập lịch cho lớp học?",
        "Cách chấm điểm bài tập như thế nào?",
        "Làm sao để tạo rubric đánh giá?",
        "Cách upload video bài giảng?",
        "Làm thế nào để gửi thông báo cho sinh viên?"
    ]

    for q in sample_questions:
        print("\n" + "="*50)
        print(f" CÂU HỎI: {q}")
        response = process_question(q)
        print("\n CÂU TRẢ LỜI TỪ AI:")
        print(response['text'])
        
        if response['videos']:
            print("\n VIDEO HƯỚDẪN LIÊN QUAN:")
            for video in response['videos']:
                print(f"  - Tiêu đề: {video['title']}")
                print(f"    Link: {video['link']}")
        else:
            print("\n Không tìm thấy video hướng dẫn liên quan.")
        print("="*50)