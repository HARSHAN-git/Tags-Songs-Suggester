chrome.runtime.onMessage.addListener((message) => {
  if (message.tags || message.songs) {
    chrome.storage.local.set({
      tags: message.tags || [],
      songs: message.songs || []
    }, () => {
      loadSuggestions();
    });
  }
});

function loadSuggestions() {
  const songsList = document.getElementById("songsList");
  const tagsList = document.getElementById("tagsList");

  chrome.storage.local.get(["songs", "tags"], (result) => {
    const songs = result.songs || [];
    const tags = result.tags || [];

    songsList.innerHTML = songs.length
      ? songs.map(song => `<div class="song">${song}</div>`).join("")
      : "<em>No songs found</em>";

    tagsList.innerHTML = tags.length
      ? tags.map(tag => `<div class="tag">${tag}</div>`).join("")
      : "<em>No tags found</em>";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadSuggestions();
  document.getElementById("refreshBtn").addEventListener("click", loadSuggestions);
});