const chat = document.getElementById("chat");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const statusLabel = document.getElementById("status");

let sessionId = null;

function addBubble(text, role) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  chat.appendChild(bubble);
  chat.scrollTop = chat.scrollHeight;
}

async function checkHealth() {
  const res = await fetch("/api/health");
  const data = await res.json();
  statusLabel.textContent = data.has_api_key
    ? "API key detected. Ready to chat."
    : "Set GOOGLE_API_KEY to enable the demo.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addBubble(message, "user");
  input.value = "";
  statusLabel.textContent = "Thinking...";

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId, user_id: "demo-user" }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Request failed");
    }

    const data = await res.json();
    sessionId = data.session_id;
    addBubble(data.reply || "(No response)", "agent");
    statusLabel.textContent = "Ready";
  } catch (err) {
    statusLabel.textContent = err.message;
    addBubble("Sorry, I hit an error. Check the API key or try again.", "agent");
  }
});

document.getElementById("scrollToDemo").addEventListener("click", () => {
  document.getElementById("demo").scrollIntoView({ behavior: "smooth" });
});

document.getElementById("scrollToDetails").addEventListener("click", () => {
  document.getElementById("details").scrollIntoView({ behavior: "smooth" });
});

checkHealth();
