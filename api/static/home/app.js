(function () {
  const canvas = document.getElementById("particles");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let particles = [];
  let w = 0;
  let h = 0;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }

  function initParticles() {
    const count = Math.min(80, Math.floor((w * h) / 18000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 1.8 + 0.4,
      dx: (Math.random() - 0.5) * 0.35,
      dy: (Math.random() - 0.5) * 0.35,
      opacity: Math.random() * 0.5 + 0.15,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);

    particles.forEach((p, i) => {
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0 || p.x > w) p.dx *= -1;
      if (p.y < 0 || p.y > h) p.dy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(34, 211, 238, ${p.opacity})`;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const q = particles[j];
        const dist = Math.hypot(p.x - q.x, p.y - q.y);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(167, 139, 250, ${0.12 * (1 - dist / 120)})`;
          ctx.stroke();
        }
      }
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", () => {
    resize();
    initParticles();
  });

  resize();
  initParticles();
  draw();

  const reveals = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.12 }
  );
  reveals.forEach((el) => observer.observe(el));

  const demoBtn = document.getElementById("demo-btn");
  const demoOutput = document.getElementById("demo-output");

  if (demoBtn && demoOutput) {
    demoBtn.addEventListener("click", async () => {
      demoBtn.disabled = true;
      demoOutput.className = "demo-output loading";
      demoOutput.textContent = "GET /api/health/ …";

      try {
        const res = await fetch("/api/health/");
        const data = await res.json();
        demoOutput.className = "demo-output";
        demoOutput.textContent = JSON.stringify(data, null, 2);
      } catch {
        demoOutput.className = "demo-output error";
        demoOutput.textContent = "Erreur : impossible de joindre l'API.";
      } finally {
        demoBtn.disabled = false;
      }
    });
  }
})();
