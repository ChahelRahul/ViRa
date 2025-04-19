const weddingDate = new Date("June 21, 2025 15:00:00").getTime();
setInterval(() => {
  const now = new Date().getTime();
  const diff = weddingDate - now;
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);
  document.getElementById("days").innerText = days;
  document.getElementById("hours").innerText = hours;
  document.getElementById("minutes").innerText = minutes;
  document.getElementById("seconds").innerText = seconds;
}, 1000);

let slideIndex = 0;
const slides = document.getElementsByClassName("slide");
function showSlide(n) {
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex = (n + slides.length) % slides.length;
  slides[slideIndex].style.display = "block";
}
function plusSlides(n) {
  showSlide(slideIndex + n);
}
document.addEventListener("DOMContentLoaded", () => showSlide(slideIndex));