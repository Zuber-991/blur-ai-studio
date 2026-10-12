console.log("BlurAI Studio Loaded");

// Card hover effect
const cards = document.querySelectorAll(".card");

cards.forEach(card => {

card.addEventListener("mouseenter",()=>{

card.style.boxShadow="0 0 30px #7c3aed";

});

card.addEventListener("mouseleave",()=>{

card.style.boxShadow="none";

});

});

// Upload button
document.getElementById("uploadBtn").onclick=()=>{

window.location.href="upload.html";

};

// Get Started button
document.getElementById("getStarted").onclick=()=>{

window.location.href="upload.html";

};

// Watch Demo button
document.getElementById("demoBtn").onclick=()=>{

const video=document.getElementById("demoVideo");

video.play();

video.scrollIntoView({
behavior:"smooth"
});

};