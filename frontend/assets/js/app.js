const API_URL = "http://localhost:8001";

// --- State ---
let currentUser = JSON.parse(localStorage.getItem("agri_user"));
let currentToken = localStorage.getItem("agri_token");
let currentLang = "en";

const translations = {
    en: {
        app_name: "AgriSathi",
        sidebar_dashboard: "Dashboard",
        sidebar_weather: "Weather",
        sidebar_assistant: "AI Assistant",
        sidebar_planner: "Crop Planner",
        sidebar_doctor: "Crop Doctor",
        sidebar_schemes: "Schemes & News",
        sidebar_roadmap: "Roadmap",
        sidebar_agrilocker: "AgriLocker",
        sidebar_logout: "Logout",
        dash_welcome: "Welcome Back, ",
        dash_subtitle: "Let's check your farm status today.",
        dash_weather_title: "Weather Today",
        dash_alerts_title: "Alerts",
        dash_market_title: "Market Price",
        dash_market_trend: "since yesterday",
        dash_schemes_title: "Government Schemes Status",
        news_search_placeholder: "Enter District (e.g. Kanchipuram)",
        news_search_btn: "Search",
        doc_upload_title: "Upload Leaf Image",
        doc_upload_desc: "Take a clear photo of the affected leaf (Paddy, Tomato, etc)",
        doc_select_btn: "Select Image",
    },
    ta: {
        app_name: "அக்ரிசாதி",
        sidebar_dashboard: "முகப்பு",
        sidebar_weather: "வானிலை",
        sidebar_assistant: "AI உதவியாளர்",
        sidebar_planner: "பயிர் திட்டம்",
        sidebar_doctor: "பயிர் மருத்துவர்",
        sidebar_schemes: "திட்டங்கள் & செய்திகள்",
        sidebar_roadmap: "வழிகாட்டி",
        sidebar_agrilocker: "ஆவணங்கள்",
        sidebar_logout: "வெளியேறு",
        dash_welcome: "வணக்கம், ",
        dash_subtitle: "இன்று உங்கள் பண்ணை நிலையை சரிபார்க்கலாம்.",
        dash_weather_title: "இன்றைய வானிலை",
        dash_alerts_title: "எச்சரிக்கைகள்",
        dash_market_title: "சந்தை விலை",
        dash_market_trend: "நேற்று முதல்",
        dash_schemes_title: "அரசு திட்டங்கள் நிலை",
        news_search_placeholder: "மாவட்டம் உள்ளிடவும் (எ.கா. காஞ்சிபுரம்)",
        news_search_btn: "தேடு",
        doc_upload_title: "இலை படத்தை பதிவேற்றவும்",
        doc_upload_desc: "பாதிக்கப்பட்ட இலையின் தெளிவான புகைப்படத்தை எடுக்கவும் (நெல், தக்காளி போன்றவை)",
        doc_select_btn: "படத்தை தேர்ந்தெடு",
    },
    ml: {
        app_name: "അഗ്രിസതി",
        sidebar_dashboard: "ഡാഷ്‌ബോർഡ്",
        sidebar_weather: "കാലാവസ്ഥ",
        sidebar_assistant: "AI അസിസ്റ്റന്റ്",
        sidebar_planner: "വിള ആസൂത്രണം",
        sidebar_doctor: "വിള ഡോക്ടർ",
        sidebar_schemes: "പദ്ധതികളും വാർത്തകളും",
        sidebar_roadmap: "വഴികാട്ടി",
        sidebar_agrilocker: "രേഖകൾ",
        sidebar_logout: "ലോഗ് ഔട്ട്",
        dash_welcome: "സ്വാഗതം, ",
        dash_subtitle: "ഇന്ന് നിങ്ങളുടെ കൃഷിസ്ഥലത്തിന്റെ അവസ്ഥ പരിശോധിക്കാം.",
        dash_weather_title: "ഇന്നത്തെ കാലാവസ്ഥ",
        dash_alerts_title: "മുന്നറിയിപ്പുകൾ",
        dash_market_title: "വിപണി വില",
        dash_market_trend: "ഇന്നലെ മുതൽ",
        dash_schemes_title: "സർക്കാർ പദ്ധതികളുടെ നില",
        news_search_placeholder: "ജില്ല നൽകുക (ഉദാ. കാഞ്ചീപുരം)",
        news_search_btn: "തിരയുക",
        doc_upload_title: "ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        doc_upload_desc: "രോഗബാധിത ഇലയുടെ വ്യക്തമായ ഫോട്ടോ എടുക്കുക (നെല്ല്, തക്കാളി തുടങ്ങിയവ)",
        doc_select_btn: "ചിത്രം തിരഞ്ഞെടുക്കുക",
    }
};

// --- Init ---
document.addEventListener("DOMContentLoaded", () => {
    if (currentUser) {
        showApp();
    } else {
        document.getElementById("section-auth").classList.remove("hidden");
    }
});

// --- Language ---
function changeLanguage(lang) {
    currentLang = lang;
    const t = translations[lang];
    if (!t) return;

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (t[key]) {
            el.innerText = t[key];
        }
    });

    // Also update AI chat language dropdown if exists to match preference, or keep separate?
    // User asked for "view change", AI chat language is likely for input/output processing.
    // We can sync them if needed, but for now let's keep the dashboard view consistent.
    const chatLang = document.getElementById("chat-lang");
    if (chatLang) {
        if (lang === 'ta') chatLang.value = 'ta'; // Assuming backend supports ta? The dropdown had en, ml, hi.
        // If not, we might want to add 'ta' or 'ml' to the chat dropdown if not present.
        // The original chat dropdown had: en, ml, hi.
        if (lang === 'ml') chatLang.value = 'ml';
        if (lang === 'en') chatLang.value = 'en';
    }
}

function toggleAuth(mode) {
    if (mode === 'register') {
        document.getElementById("form-login").classList.add("hidden");
        document.getElementById("form-register").classList.remove("hidden");
    } else {
        document.getElementById("form-register").classList.add("hidden");
        document.getElementById("form-login").classList.remove("hidden");
    }
}

// --- Auth ---
async function register() {
    const data = {
        full_name: document.getElementById("reg-name").value,
        phone_number: document.getElementById("reg-phone").value,
        village: document.getElementById("reg-village").value,
        state: document.getElementById("reg-state").value,
        password: document.getElementById("reg-pass").value,
    };

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (res.ok) {
            alert("Registration Successful based in India! Please login.");
            toggleAuth("login");
        } else {
            const err = await res.json();
            alert(err.detail);
        }
    } catch (e) { console.error(e); alert("Reg Error"); }
}

async function login() {
    const data = {
        phone_number: document.getElementById("login-phone").value,
        password: document.getElementById("login-pass").value,
    };

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            const result = await res.json();
            localStorage.setItem("agri_token", result.access_token);
            // Fetch full user details to store
            // For now just partial
            currentUser = { id: result.user_id, name: result.user_name };
            localStorage.setItem("agri_user", JSON.stringify(currentUser));
            showApp();
        } else {
            alert("Login Failed");
        }
    } catch (e) { console.error(e); }
}

function logout() {
    localStorage.removeItem("agri_user");
    localStorage.removeItem("agri_token");
    location.reload();
}

function showApp() {
    document.getElementById("section-auth").classList.add("hidden");
    document.getElementById("app-container").classList.remove("hidden");

    // Set User Info
    document.getElementById("user-name").innerText = currentUser.name;
    document.getElementById("dash-name").innerText = currentUser.name;
    document.getElementById("user-avatar").innerText = currentUser.name.charAt(0);

    // Initial Loads
    nav("dashboard");
    loadWeather();
    loadMarketPrice();
}

function loadMarketPrice() {
    const items = [
        { name: "Coconut (Kopra)", price: "₹125/kg", trend: "+2%" },
        { name: "Black Pepper", price: "₹510/kg", trend: "+1.5%" },
        { name: "Rubber (RSS4)", price: "₹155/kg", trend: "-0.5%" },
        { name: "Banana (Nendran)", price: "₹42/kg", trend: "+4%" },
        { name: "Cardamom", price: "₹1200/kg", trend: "+1%" }
    ];
    // Weekday-based rotation or random
    const item = items[Math.floor(Math.random() * items.length)];

    document.getElementById("dash-market-item").innerText = item.name;
    document.getElementById("dash-market-price").innerText = item.price;
    document.getElementById("dash-market-value").innerText = item.trend;
}

// --- Navigation ---
function nav(section) {
    // Hide all
    ["dashboard", "weather", "chat", "planner", "schemes", "roadmap", "agrilocker", "doctor"].forEach(id => {
        document.getElementById(`section-${id}`).classList.add("hidden");
    });
    // Show one
    document.getElementById(`section-${section}`).classList.remove("hidden");

    // ... existing sidebar update code ...
    document.querySelectorAll(".sidebar-item").forEach(el => el.classList.remove("active", "bg-agri-50", "text-agri-800"));

    if (section === 'schemes') loadSchemes();
    if (section === 'agrilocker') loadDocs();
}

// --- Doctor ---
async function analyzeLeaf() {
    const fileInp = document.getElementById("doctor-file");
    if (!fileInp.files[0]) return;

    const formData = new FormData();
    formData.append("file", fileInp.files[0]);

    // Show loading...
    document.getElementById("doctor-result").classList.remove("hidden");
    document.getElementById("doc-disease").innerText = "Analyzing...";
    document.getElementById("doc-desc").innerText = "Our AI is examining the leaf texture and color...";
    document.getElementById("doc-score").innerText = "Please Wait";
    document.getElementById("doc-pest").innerText = "--";

    try {
        const res = await fetch(`${API_URL}/doctor/analyze`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        document.getElementById("doc-disease").innerText = data.disease;
        document.getElementById("doc-score").innerText = `Health Score: ${data.health_score}/100`;
        document.getElementById("doc-desc").innerText = data.suggestion;
        document.getElementById("doc-pest").innerText = data.pesticide;

        // Color coding based on score
        const scoreEl = document.getElementById("doc-score");
        if (data.health_score > 80) {
            scoreEl.className = "bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold";
        } else if (data.health_score > 50) {
            scoreEl.className = "bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs font-bold";
        } else {
            scoreEl.className = "bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-bold";
        }

    } catch (e) { console.error(e); alert("Analysis Error"); }
}

// --- Weather ---
async function loadWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => fetchWeather(pos.coords.latitude, pos.coords.longitude),
            () => fetchWeather(10.8505, 76.2711) // Default: Kerala
        );
    } else {
        fetchWeather(10.8505, 76.2711);
    }
}

async function fetchWeather(lat, lon) {
    try {
        const res = await fetch(`${API_URL}/weather/current?lat=${lat}&lon=${lon}`);
        const data = await res.json();

        // Update Dashboard Widget
        document.getElementById("dash-temp").innerText = `${data.temp}°C`;
        document.getElementById("dash-weather-desc").innerText = data.condition;

        // Update Weather Section
        document.getElementById("weather-main-temp").innerText = `${data.temp}°`;
        document.getElementById("weather-main-cond").innerText = data.condition;
        document.getElementById("weather-hum").innerText = `${data.humidity}%`;
        document.getElementById("weather-wind").innerText = `${data.wind} km/h`;
        document.getElementById("weather-advice").innerText = data.advice;

        // Update Location (Sidebar)
        if (data.location) {
            document.getElementById("user-loc").innerText = data.location;
        }

        // Dynamic Alerts
        const cond = data.condition.toLowerCase();
        const alertCount = document.getElementById("dash-alert-count");
        const alertMsg = document.getElementById("dash-alert-msg");
        const alertIcon = document.getElementById("dash-alert-icon");

        if (cond.includes("rain") || cond.includes("storm") || cond.includes("thunder")) {
            alertCount.innerText = "1 Warning";
            alertCount.className = "text-xl font-bold text-red-500";
            alertMsg.innerText = "Rain expected. Check drainage.";
            alertIcon.className = "p-3 bg-red-50 rounded-lg text-red-500";
            alertIcon.innerHTML = '<i class="fas fa-exclamation-triangle text-xl"></i>';
        } else {
            alertCount.innerText = "No Warnings";
            alertCount.className = "text-xl font-bold text-green-600";
            alertMsg.innerText = "Conditions are favorable.";
            alertIcon.className = "p-3 bg-green-50 rounded-lg text-green-500";
            alertIcon.innerHTML = '<i class="fas fa-shield-alt text-xl"></i>';
        }

    } catch (e) { console.log("Weather error", e); }
}

// --- Chat ---
async function sendMessage() {
    const txt = document.getElementById("chat-input").value;
    if (!txt) return;

    const btn = document.querySelector("#section-chat button[onclick='sendMessage()']");
    const inp = document.getElementById("chat-input");

    addChatBubble(txt, 'user');
    inp.value = "";
    btn.disabled = true;
    inp.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    try {
        const res = await fetch(`${API_URL}/assistant/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: txt,
                language: document.getElementById("chat-lang").value
            })
        });
        const data = await res.json();
        addChatBubble(data.response, 'ai');

        if (data.audio_url) {
            const audio = new Audio(API_URL + data.audio_url);
            audio.play();
        }
    } catch (e) {
        addChatBubble("Error connecting to AI", 'ai');
    } finally {
        btn.disabled = false;
        inp.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

function addChatBubble(text, sender) {
    const parent = document.getElementById("chat-history");
    const div = document.createElement("div");
    div.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;

    const bubble = document.createElement("div");
    bubble.className = sender === 'user' ? 'chat-bubble-user p-3 max-w-xs text-sm shadow-sm' : 'chat-bubble-ai p-3 max-w-xs text-sm text-gray-700 shadow-sm';
    bubble.innerText = text;

    div.appendChild(bubble);
    parent.appendChild(div);
    parent.scrollTop = parent.scrollHeight;
}

// --- Voice ---
function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) { alert("Browser not supported"); return; }

    const recognition = new SpeechRecognition();
    recognition.lang = document.getElementById("chat-lang").value === 'ml' ? 'ml-IN' : 'en-US';
    recognition.start();

    recognition.onresult = (event) => {
        const txt = event.results[0][0].transcript;
        document.getElementById("chat-input").value = txt;
        sendMessage();
    };
}

// --- Planner ---
function autoFill() {
    // Randomize slightly for demo feel
    document.getElementById("ml-N").value = Math.floor(Math.random() * (120 - 60) + 60);
    document.getElementById("ml-P").value = Math.floor(Math.random() * (60 - 30) + 30);
    document.getElementById("ml-K").value = Math.floor(Math.random() * (50 - 20) + 20);
    document.getElementById("ml-ph").value = (Math.random() * (7.5 - 5.5) + 5.5).toFixed(1);
    document.getElementById("ml-rain").value = Math.floor(Math.random() * (300 - 100) + 100);
    document.getElementById("ml-temp").value = Math.floor(Math.random() * (35 - 20) + 20);
    document.getElementById("ml-hum").value = Math.floor(Math.random() * (90 - 60) + 60);
}

async function getRecommendation() {
    const data = {
        N: parseFloat(document.getElementById("ml-N").value),
        P: parseFloat(document.getElementById("ml-P").value),
        K: parseFloat(document.getElementById("ml-K").value),
        ph: parseFloat(document.getElementById("ml-ph").value),
        rainfall: parseFloat(document.getElementById("ml-rain").value),
        temperature: parseFloat(document.getElementById("ml-temp").value),
        humidity: parseFloat(document.getElementById("ml-hum").value),
    };

    try {
        const res = await fetch(`${API_URL}/cultivation/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await res.json();

        document.getElementById("ml-result").classList.remove("hidden");
        document.getElementById("ml-crop-name").innerText = result.crop;
        document.getElementById("ml-reason").innerText = result.reason;
    } catch (e) { alert("Prediction Error"); }
}

// --- Schemes ---
async function loadSchemes() {
    const res = await fetch(`${API_URL}/government/schemes`);
    const schemes = await res.json();
    const list = document.getElementById("schemes-list");
    list.innerHTML = "";
    schemes.forEach(s => {
        let statusColor = "bg-gray-100 text-gray-700";
        if (s.status.includes("Active")) statusColor = "bg-green-100 text-green-700";
        else if (s.status.includes("Open")) statusColor = "bg-blue-100 text-blue-700";
        else if (s.status.includes("Available")) statusColor = "bg-orange-100 text-orange-700";

        list.innerHTML += `
        <div class="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-l-green-500 flex flex-col justify-between">
            <div>
                <div class="flex justify-between items-start">
                    <h3 class="font-bold text-lg text-gray-800">${s.name}</h3>
                    <span class="${statusColor} text-xs px-2 py-1 rounded font-bold">${s.status}</span>
                </div>
                <p class="text-sm text-gray-600 mt-2 mb-4">${s.description}</p>
            </div>
            <a href="${s.link}" target="_blank" class="block w-full text-center bg-agri-50 text-agri-700 font-semibold py-2 rounded-lg hover:bg-agri-100 transition">
                ${s.action || "View Details"} <i class="fas fa-external-link-alt ml-1 text-xs"></i>
            </a>
        </div>`;
    });

    // Load News initially
    loadNews();
}

async function loadNews() {
    let loc = document.getElementById("news-location").value;
    if (!loc) loc = "India";

    // Show loading state
    const nList = document.getElementById("news-list");
    nList.innerHTML = "<p class='text-gray-500 text-sm'>Loading news for " + loc + "...</p>";

    try {
        const nRes = await fetch(`${API_URL}/government/news?location=${encodeURIComponent(loc)}`);
        const news = await nRes.json();

        nList.innerHTML = "";
        if (news.length === 0) {
            nList.innerHTML = "<p class='text-gray-500 text-sm'>No specific news found for this location.</p>";
            return;
        }

        news.forEach(n => {
            nList.innerHTML += `
            <a href="${n.url}" target="_blank" class="block group">
                <div class="flex items-center gap-4 p-4 bg-white rounded-xl shadow-sm border border-transparent hover:border-agri-500 hover:shadow-md transition cursor-pointer">
                     <div class="bg-blue-100 text-blue-600 w-12 h-12 rounded-lg flex items-center justify-center font-bold text-xl group-hover:bg-blue-200 transition">
                        <i class="fas fa-newspaper"></i>
                     </div>
                     <div>
                         <h4 class="font-bold text-gray-800 group-hover:text-agri-700 transition">${n.title}</h4>
                         <p class="text-xs text-gray-500">${n.date}</p>
                     </div>
                     <i class="fas fa-chevron-right ml-auto text-gray-300 group-hover:text-agri-500"></i>
                </div>
            </a>`;
        });
    } catch (e) {
        nList.innerHTML = "<p class='text-red-500 text-sm'>Error loading news.</p>";
    }
}

// --- Roadmap ---
async function generateRoadmap() {
    const goal = document.getElementById("roadmap-goal").value;
    const cont = document.getElementById("roadmap-container");
    cont.innerHTML = "<p class='text-center text-gray-500'>Generating roadmap... please wait...</p>";

    try {
        const res = await fetch(`${API_URL}/assistant/roadmap`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ goal: goal })
        });
        const data = await res.json();
        // Simple markdown parsing or just splitting by lines
        const lines = data.roadmap.split("\n");
        cont.innerHTML = "";

        lines.forEach((line, i) => {
            if (line.trim().length < 2) return;
            cont.innerHTML += `
             <div class="flex gap-4 items-start bg-white p-4 rounded-xl shadow-sm">
                 <div class="bg-agri-100 text-agri-800 font-bold w-8 h-8 rounded-full flex items-center justify-center shrink-0">${i + 1}</div>
                 <p class="text-gray-700">${line}</p>
                 <button class="text-gray-400 hover:text-green-500 ml-auto"><i class="fas fa-check-circle text-xl"></i></button>
             </div>`;
        });

    } catch (e) { cont.innerHTML = "Error generating roadmap."; }
}

// --- AgriLocker ---
async function loadDocs() {
    if (!currentUser) return;
    const res = await fetch(`${API_URL}/documents/list/${currentUser.id}`);
    const docs = await res.json();
    const tbody = document.getElementById("docs-list");
    tbody.innerHTML = "";

    docs.forEach(d => {
        tbody.innerHTML += `
         <tr class="hover:bg-gray-50">
             <td class="p-4 font-semibold text-gray-800 flex items-center gap-2">
                 <i class="fas fa-file-pdf text-red-500"></i> ${d.filename}
             </td>
             <td class="p-4 text-gray-600 hidden md:table-cell">${d.category}</td>
             <td class="p-4 text-gray-500 text-sm hidden md:table-cell">${new Date(d.upload_date).toLocaleDateString()}</td>
             <td class="p-4 text-right">
                 <a href="${API_URL}${d.file_path}" target="_blank" class="text-blue-500 hover:text-blue-700 mr-2"><i class="fas fa-download"></i></a>
                 <button onclick="deleteDoc(${d.id})" class="text-red-400 hover:text-red-700"><i class="fas fa-trash"></i></button>
             </td>
         </tr>`;
    });
}

async function uploadDoc() {
    const fileInp = document.getElementById("doc-file");
    const cat = document.getElementById("doc-cat").value;

    if (!fileInp.files[0]) return alert("Select File");

    const formData = new FormData();
    formData.append("file", fileInp.files[0]);
    formData.append("category", cat);
    formData.append("user_id", currentUser.id);

    try {
        const res = await fetch(`${API_URL}/documents/upload`, {
            method: "POST",
            body: formData
        });
        if (res.ok) {
            alert("Uploaded!");
            fileInp.value = "";
            loadDocs();
        } else alert("Upload Failed");
    } catch (e) { alert("Error"); }
}

async function deleteDoc(id) {
    if (!confirm("Delete this file?")) return;
    await fetch(`${API_URL}/documents/${id}`, { method: "DELETE" });
    loadDocs();
}
