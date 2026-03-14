const API_BASE = "https://studingwell-com.vercel.app";
let timeLeft = 25 * 60;
let timerId = null;

// Initialize user data on page load
document.addEventListener("DOMContentLoaded", () => {
    const name = localStorage.getItem("username") || "Student";
    const userDisplay = document.getElementById("user-display");
    const avatar = document.getElementById("avatar");

    if (userDisplay) userDisplay.innerText = name;
    if (avatar) avatar.innerText = name[0].toUpperCase();
});

// AI Chat Function
async function ask() {
    const inp = document.getElementById("user-input");
    const win = document.getElementById("chat-window");
    const text = inp.value.trim();

    if (!text) return;

    // Display user message
    win.innerHTML += `
        <div class="flex justify-end message-anim">
            <div class="bg-indigo-600 text-white p-4 rounded-2xl rounded-tr-none max-w-2xl text-sm shadow-md">
                ${text}
            </div>
        </div>`;
    
    inp.value = "";
    win.scrollTop = win.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: text })
        });

        if (!res.ok) throw new Error("Server response error");

        const data = await res.json();
        
        // Display AI message
        win.innerHTML += `
            <div class="flex justify-start message-anim">
                <div class="bg-gray-100 p-4 rounded-2xl rounded-tl-none max-w-2xl text-sm shadow-sm">
                    ${data.answer.replace(/\n/g, '<br>')}
                </div>
            </div>`;
        
        // Re-render LaTeX math formulas
        if (window.MathJax) {
            MathJax.typesetPromise();
        }
        
        win.scrollTop = win.scrollHeight;

    } catch (e) {
        console.error(e);
        win.innerHTML += `<div class="text-red-500 text-center text-xs">Error: Could not reach the AI.</div>`;
    }
}

// Focus Timer Functions
function toggleTimer() {
    const btn = document.getElementById("t-btn");
    if (timerId) {
        clearInterval(timerId);
        timerId = null;
        btn.innerText = "Start";
    } else {
        timerId = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            if (timeLeft <= 0) {
                clearInterval(timerId);
                alert("Time is up! Take a break.");
                resetTimer();
            }
        }, 1000);
        btn.innerText = "Pause";
    }
}

function updateTimerDisplay() {
    const m = Math.floor(timeLeft / 60);
    const s = timeLeft % 60;
    const timerElement = document.getElementById("timer");
    if (timerElement) {
        timerElement.innerText = `${m}:${s < 10 ? '0' + s : s}`;
    }
}

function resetTimer() {
    timeLeft = 25 * 60;
    updateTimerDisplay();
}

// Auth and Logout
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// Enter key support
const inputField = document.getElementById("user-input");
if (inputField) {
    inputField.onkeypress = (e) => {
        if (e.key === "Enter") ask();
    };
}