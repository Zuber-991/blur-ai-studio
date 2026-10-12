// ==============================
// BlurAI Studio Result Page
// ==============================

// AI Report
document.getElementById("command").textContent =
    localStorage.getItem("command") || "Not Specified";

document.getElementById("blur").textContent =
    localStorage.getItem("blur") || "Gaussian Blur";

// Get videos
const originalVideo = localStorage.getItem("originalVideo");
const outputVideo = localStorage.getItem("outputVideo");

console.log("Original:", originalVideo);
console.log("Output:", outputVideo);

// -----------------------------
// Original Video
// -----------------------------
const originalPlayer = document.getElementById("originalVideo");

if (originalVideo) {
    originalPlayer.src = originalVideo;
    originalPlayer.controls = true;
    originalPlayer.preload = "auto";

    originalPlayer.onloadeddata = () => {
        console.log("Original video loaded");
    };

    originalPlayer.onerror = () => {
        console.log("Cannot load original video");
    };

    originalPlayer.load();
}

// -----------------------------
// Processed Video
// -----------------------------
const blurredPlayer = document.getElementById("blurredVideo");

if (outputVideo) {
    blurredPlayer.src = outputVideo;
    blurredPlayer.controls = true;
    blurredPlayer.preload = "auto";

    blurredPlayer.onloadeddata = () => {
        console.log("Blurred video loaded");
    };

    blurredPlayer.onerror = (e) => {
        console.log("Cannot load blurred video", e);
        alert("Unable to load processed video.");
    };

    blurredPlayer.load();
}

// -----------------------------
// Download
// -----------------------------
document.getElementById("download").onclick = function () {

    if (!outputVideo) {
        alert("No processed video found.");
        return;
    }

    const link = document.createElement("a");
    link.href = outputVideo;
    link.download = "BlurAI_Result.mp4";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};