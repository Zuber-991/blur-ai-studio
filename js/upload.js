const videoInput = document.getElementById("videoInput");
const imageInput = document.getElementById("imageInput");

const videoPreview = document.getElementById("videoPreview");
const imagePreview = document.getElementById("imagePreview");

// Preview Video
videoInput.onchange = () => {
    const file = videoInput.files[0];

    if (file) {
        videoPreview.src = URL.createObjectURL(file);
        videoPreview.style.display = "block";
    }
};

// Preview Image
imageInput.onchange = () => {
    const file = imageInput.files[0];

    if (file) {
        imagePreview.src = URL.createObjectURL(file);
        imagePreview.style.display = "block";
    }
};

// Start AI Processing
document.getElementById("startBtn").onclick = async () => {

    if (videoInput.files.length === 0) {
        alert("Please upload a video.");
        return;
    }

    const btn = document.getElementById("startBtn");

    btn.disabled = true;
    btn.innerHTML = "Processing...";

    const formData = new FormData();

    formData.append("video", videoInput.files[0]);

    if (imageInput.files.length > 0) {
        formData.append("reference", imageInput.files[0]);
    }

    formData.append("command", document.getElementById("command").value);
    formData.append("blur", document.getElementById("blurStyle").value);

    try {

        const response = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error);
            btn.disabled = false;
            btn.innerHTML = "🚀 Start AI Processing";
            return;
        }

        // Save Original Video
        localStorage.setItem(
            "originalVideo",
            URL.createObjectURL(videoInput.files[0])
        );

        // Save Output Video
        localStorage.setItem(
            "outputVideo",
            "http://127.0.0.1:5000" + data.video
        );

        localStorage.setItem(
            "command",
            document.getElementById("command").value
        );

        localStorage.setItem(
            "blur",
            document.getElementById("blurStyle").value
        );

        window.location.href = "processing.html";

    } catch (err) {

        console.error(err);

        alert("Cannot connect to Flask Backend");

        btn.disabled = false;
        btn.innerHTML = "🚀 Start AI Processing";

    }

};