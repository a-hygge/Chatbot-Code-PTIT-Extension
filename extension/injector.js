(function() {
  const CHAT_ID = 'huongdan-nghiepvu-container';
  const TOGGLE_BUTTON_ID = 'chat-toggle-button';

  if (document.getElementById(TOGGLE_BUTTON_ID)) return;

  const toggleButton = document.createElement('div');
  toggleButton.id = TOGGLE_BUTTON_ID;
  toggleButton.textContent = 'HD';
  document.body.appendChild(toggleButton);

  const chatContainer = document.createElement('div');
  chatContainer.id = CHAT_ID;
  chatContainer.className = 'chat-container';
  
  chatContainer.innerHTML = `
    <div id="chat-header">
      <span class="header-title">Hướng dẫn nghiệp vụ</span>
      <div class="header-controls">
        <div id="chat-new-btn" class="header-btn" title="Trò chuyện mới">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
        </div>
        <div id="chat-minimize-btn" class="header-btn" title="Thu nhỏ/Phóng to">
          <svg class="minimize-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          <svg class="maximize-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: none;"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
        </div>
        <div id="chat-close-btn" class="header-btn" title="Đóng">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </div>
      </div>
    </div>
    <div id="chat-messages"></div>
    <form id="chat-form">
      <input type="text" id="user-input" placeholder="Nhập câu hỏi..." required />
      <button type="submit">➤</button>
    </form>
    <div class="resizer resizer-se"></div>
    <div class="resizer resizer-sw"></div>
    <div class="resizer resizer-ne"></div>
    <div class="resizer resizer-nw"></div>
  `;
  document.body.appendChild(chatContainer);

  const messagesEl = document.getElementById("chat-messages");
  const formEl = document.getElementById("chat-form");
  const inputEl = document.getElementById("user-input");
  const newChatBtn = document.getElementById('chat-new-btn');
  const minimizeBtn = document.getElementById('chat-minimize-btn');
  const closeBtn = document.getElementById('chat-close-btn');
  const minimizeIcon = minimizeBtn.querySelector('.minimize-icon');
  const maximizeIcon = minimizeBtn.querySelector('.maximize-icon');

  toggleButton.addEventListener('click', () => {
    chatContainer.classList.toggle('visible');
    if (chatContainer.classList.contains('minimized')) {
      chatContainer.classList.remove('minimized');
      minimizeIcon.style.display = 'block';
      maximizeIcon.style.display = 'none';
    }
  });

  closeBtn.addEventListener('click', () => { chatContainer.classList.remove('visible'); });

  minimizeBtn.addEventListener('click', () => {
    chatContainer.classList.toggle('minimized');
    const isMinimized = chatContainer.classList.contains('minimized');
    minimizeIcon.style.display = isMinimized ? 'none' : 'block';
    maximizeIcon.style.display = isMinimized ? 'block' : 'none';
  });

  newChatBtn.addEventListener('click', () => {
    messagesEl.innerHTML = '';
    appendMessage("Xin chào! Tôi có thể hướng dẫn nghiệp vụ cho bạn về Code PTIT?", "bot", true);
    if (chatContainer.classList.contains('minimized')) {
        chatContainer.classList.remove('minimized');
        minimizeIcon.style.display = 'block';
        maximizeIcon.style.display = 'none';
    }
  });

  const BACKEND_URL = "http://localhost:5000/api/chat";

  function appendMessage(text, sender, isBot = false) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}-message`;
    if(isBot) wrapper.classList.add('bot-message-wrapper');
    const bubble = document.createElement("div");
    bubble.className = isBot ? 'bot-message' : 'user-message-bubble';
    if (sender === 'bot') { bubble.innerHTML = parseMarkdown(text); } else { bubble.textContent = text; }
    wrapper.appendChild(bubble);
    if (isBot) { const img = document.createElement("img"); img.src = chrome.runtime.getURL("icon.png"); img.className = "avatar"; wrapper.appendChild(img); }
    messagesEl.appendChild(wrapper);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
  
  function displayVideos(videos) {
    if (!videos || videos.length === 0) return null;
    const videosContainer = document.createElement("div");
    videosContainer.className = "videos-container";
    const header = document.createElement("h4");
    header.textContent = "VIDEO HƯỚNG DẪN LIÊN QUAN";
    videosContainer.appendChild(header);
    const videosList = document.createElement("ul");
    videos.forEach(video => {
        const item = document.createElement("li");
        if (video.thumbnail) { const img = document.createElement("img"); img.src = video.thumbnail; img.className = "video-thumbnail"; item.appendChild(img); }
        const videoInfo = document.createElement("div");
        videoInfo.className = "video-info";
        const link = document.createElement("a");
        link.href = video.link; link.textContent = video.title || "Video không có tiêu đề"; link.target = "_blank"; videoInfo.appendChild(link);
        if (video.description) { const desc = document.createElement("div"); desc.className = "video-description"; desc.textContent = video.description; videoInfo.appendChild(desc); }
        item.appendChild(videoInfo);
        videosList.appendChild(item);
    });
    videosContainer.appendChild(videosList);
    return videosContainer;
  }

  function parseMarkdown(md) {
    if (!md) return "Không có phản hồi";
    md = md.replace(/^## (.*$)/gim, '<strong>$1</strong>');
    md = md.replace(/^### (.*$)/gim, '<strong>$1</strong>');
    md = md.replace(/```([\s\S]*?)```/g, '<pre class="code-block"><code>$1</code></pre>');
    md = md.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    md = md.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    md = md.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    md = md.replace(/\n/g, '<br>');
    return md;
  }

  async function sendMessage(question) {
    appendMessage(question, "user");
    inputEl.value = "";
    appendMessage("⏳ Đang xử lý...", "bot", true);
    try {
        const res = await fetch(BACKEND_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) });
        if (!res.ok) throw new Error(`Lỗi HTTP: ${res.status}`);
        const data = await res.json();
        messagesEl.removeChild(messagesEl.lastChild);
        appendMessage(data.text, "bot", true);
        if (data.videos && data.videos.length > 0) {
            const videosElement = displayVideos(data.videos);
            if (videosElement) { messagesEl.appendChild(videosElement); messagesEl.scrollTop = messagesEl.scrollHeight; }
        }
    } catch (error) {
        messagesEl.removeChild(messagesEl.lastChild);
        appendMessage("Lỗi kết nối máy chủ. Vui lòng đảm bảo server Python đã được khởi động và cấu hình CORS.", "bot", true);
        console.error("API Error:", error);
    }
  }

  formEl.addEventListener("submit", (e) => { e.preventDefault(); const q = inputEl.value.trim(); if (q) sendMessage(q); });
  inputEl.addEventListener("keypress", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); formEl.dispatchEvent(new Event("submit")); }});
  appendMessage("Xin chào! Tôi có thể hướng dẫn nghiệp vụ cho bạn về Code PTIT?", "bot", true);
  
  const chatHeader = document.getElementById("chat-header");
  chatHeader.addEventListener("mousedown", (e) => { if (e.target.closest('.header-btn') || e.target.classList.contains('resizer')) return; const rect = chatContainer.getBoundingClientRect(); const initialX = e.clientX - rect.left; const initialY = e.clientY - rect.top; let isDragging = true; function onMouseMove(e) { if (!isDragging) return; let newX = e.clientX - initialX; let newY = e.clientY - initialY; newX = Math.max(0, Math.min(newX, window.innerWidth - rect.width)); newY = Math.max(0, Math.min(newY, window.innerHeight - rect.height)); chatContainer.style.left = `${newX}px`; chatContainer.style.top = `${newY}px`; chatContainer.style.right = 'auto'; chatContainer.style.bottom = 'auto'; } function onMouseUp() { isDragging = false; document.removeEventListener('mousemove', onMouseMove); document.removeEventListener('mouseup', onMouseUp); } document.addEventListener('mousemove', onMouseMove); document.addEventListener('mouseup', onMouseUp); });

  function initResize(e) {
    const resizer = e.target;
    let startX = e.clientX;
    let startY = e.clientY;
    const initialRect = chatContainer.getBoundingClientRect();

    function doResize(e) {
      let newWidth, newHeight, newLeft = initialRect.left, newTop = initialRect.top;
      
      if (resizer.classList.contains('resizer-se')) {
        newWidth = initialRect.width + (e.clientX - startX);
        newHeight = initialRect.height + (e.clientY - startY);
      } else if (resizer.classList.contains('resizer-sw')) {
        newWidth = initialRect.width - (e.clientX - startX);
        newHeight = initialRect.height + (e.clientY - startY);
        newLeft = initialRect.left + (e.clientX - startX);
      } else if (resizer.classList.contains('resizer-ne')) {
        newWidth = initialRect.width + (e.clientX - startX);
        newHeight = initialRect.height - (e.clientY - startY);
        newTop = initialRect.top + (e.clientY - startY);
      } else if (resizer.classList.contains('resizer-nw')) {
        newWidth = initialRect.width - (e.clientX - startX);
        newHeight = initialRect.height - (e.clientY - startY);
        newLeft = initialRect.left + (e.clientX - startX);
        newTop = initialRect.top + (e.clientY - startY);
      }
      
      chatContainer.style.width = newWidth + 'px';
      chatContainer.style.height = newHeight + 'px';
      chatContainer.style.left = newLeft + 'px';
      chatContainer.style.top = newTop + 'px';
      chatContainer.style.bottom = 'auto';
      chatContainer.style.right = 'auto';
    }

    function stopResize() {
      window.removeEventListener('mousemove', doResize);
      window.removeEventListener('mouseup', stopResize);
    }

    window.addEventListener('mousemove', doResize);
    window.addEventListener('mouseup', stopResize);
  }

  chatContainer.querySelectorAll('.resizer').forEach(resizer => {
    resizer.addEventListener('mousedown', initResize);
  });
})();