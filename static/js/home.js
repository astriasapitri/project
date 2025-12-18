const counters = document.querySelectorAll('.count');

counters.forEach(counter => {
  const target = +counter.dataset.target;
  let current = 0;

  const update = () => {
    current += target / 50;
    if (current < target) {
      counter.textContent = current.toFixed(1);
      requestAnimationFrame(update);
    } else {
      counter.textContent = target;
    }
  };
  update();
});
