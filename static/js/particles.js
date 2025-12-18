particlesJS("particles-js", {
  particles: {
    number: {
      value: 90,
      density: {
        enable: true,
        value_area: 900
      }
    },
    color: {
      value: "#93c5fd"
    },
    shape: {
      type: "circle"
    },
    opacity: {
      value: 0.6,
      random: true
    },
    size: {
      value: 3,
      random: true
    },
    line_linked: {
      enable: true,        // 🔥 GARIS LANGSUNG AKTIF
      distance: 150,
      color: "#60a5fa",
      opacity: 0.6,
      width: 1
    },
    move: {
      enable: true,
      speed: 1.2,
      random: true,
      out_mode: "out"
    }
  },

  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "grab"   // 🕸️ ketarik mouse
      },
      onclick: {
        enable: true,
        mode: "push"
      }
    },
    modes: {
      grab: {
        distance: 180,
        line_linked: {
          opacity: 0.9
        }
      }
    }
  },

  retina_detect: true
});
