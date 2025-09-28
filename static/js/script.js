// Staggered fade-up + subtle 3D tilt on hover
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".master-card");

  // Staggered entrance
  cards.forEach((card, i) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(40px)";
    setTimeout(() => {
      card.style.transition = "opacity .8s ease, transform .8s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, i * 160);
  });

  // Gentle tilt on pointer move
  cards.forEach((card) => {
    const maxTilt = 6; // degrees
    const frame = card.querySelector(".image-frame");

    function handleMove(e){
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;  // 0..1
      const y = (e.clientY - rect.top) / rect.height;  // 0..1
      const rx = (y - 0.5) * -2 * maxTilt;             // rotateX
      const ry = (x - 0.5) *  2 * maxTilt;             // rotateY
      card.style.transform = `translateY(-6px) rotateX(${rx}deg) rotateY(${ry}deg)`;
      if (frame) frame.style.filter = "brightness(1.03)";
    }
    function reset(){
      card.style.transform = "translateY(0) rotateX(0) rotateY(0)";
      if (frame) frame.style.filter = "none";
    }

    card.addEventListener("mousemove", handleMove);
    card.addEventListener("mouseleave", reset);
    card.addEventListener("touchstart", () => card.classList.add("no-tilt"), {passive:true});
    card.addEventListener("touchend", () => card.classList.remove("no-tilt"));
  });
});
