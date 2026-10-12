const status = document.getElementById("status");
const progress = document.getElementById("progress");
const percent = document.getElementById("percent");
const time = document.getElementById("time");

const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const step4 = document.getElementById("step4");
const step5 = document.getElementById("step5");

let value = 0;

const messages = [
    "Uploading Video...",
    "Detecting Objects...",
    "Tracking Objects...",
    "Applying Blur...",
    "Rendering Final Video..."
];

const timer = setInterval(() => {

    value++;

    progress.style.width = value + "%";
    percent.innerText = value + "%";

    const remaining = Math.max(0, 25 - Math.floor(value / 4));
    time.innerText = remaining + " sec";

    if (value >= 5) {
        step1.style.color = "#00ff88";
    }

    if (value >= 20) {
        status.innerText = messages[1];
        step2.style.color = "#00ff88";
    }

    if (value >= 40) {
        status.innerText = messages[2];
        step3.style.color = "#00ff88";
    }

    if (value >= 60) {
        status.innerText = messages[3];
        step4.style.color = "#00ff88";
    }

    if (value >= 85) {
        status.innerText = messages[4];
        step5.style.color = "#00ff88";
    }

    if (value >= 100) {

        clearInterval(timer);

        window.location.href = "result.html";

    }

}, 100);