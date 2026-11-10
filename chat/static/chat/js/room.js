// Live chat for one room over a WebSocket.
// Django renders the message history; this script handles everything after that.

const roomName = JSON.parse(document.getElementById("room-name").textContent);
const myUsername = JSON.parse(document.getElementById("username").textContent);

const chatLog = document.getElementById("chat-log");
const input = document.getElementById("chat-input");
const sendButton = document.getElementById("chat-send");
const statusNote = document.getElementById("chat-status");

// Use wss:// when the page is served over https://, otherwise ws://
const wsScheme = location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${wsScheme}://${location.host}/ws/chat/${roomName}/`);

function scrollToBottom() {
  chatLog.scrollTop = chatLog.scrollHeight;
}

// Same "HH:MM" format the server uses for the history.
function formatTime(isoString) {
  return new Date(isoString).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

// Build "username: content · time" using textContent only,
// so any HTML a user types is shown as plain text (no XSS).
function appendMessage(data) {
  const emptyNote = document.getElementById("empty-note");
  if (emptyNote) emptyNote.remove();

  const row = document.createElement("div");
  row.className = "message";
  if (data.username === myUsername) row.classList.add("own");

  const name = document.createElement("span");
  name.className = "username";
  name.textContent = data.username;

  const time = document.createElement("span");
  time.className = "time";
  time.textContent = `· ${formatTime(data.timestamp)}`;

  row.append(name, document.createTextNode(`: ${data.content} `), time);
  chatLog.appendChild(row);
  scrollToBottom();
}

function sendMessage() {
  const message = input.value.trim();
  if (!message || socket.readyState !== WebSocket.OPEN) return;
  socket.send(JSON.stringify({ message }));
  input.value = "";
  input.focus();
}

// --- WebSocket events ---
socket.addEventListener("message", (event) => {
  appendMessage(JSON.parse(event.data));
});

socket.addEventListener("close", () => {
  statusNote.hidden = false;
  input.disabled = true;
  sendButton.disabled = true;
});

// --- UI events ---
sendButton.addEventListener("click", sendMessage);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});

// Start at the newest message in the history.
scrollToBottom();
