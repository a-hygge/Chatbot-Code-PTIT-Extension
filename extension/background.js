// Sự kiện khi extension được cài đặt
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension đã được cài đặt và sẽ tự động chèn chatbot vào trang web phù hợp.");
});