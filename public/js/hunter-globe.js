import createGlobe from './vendor/cobe/cobe.esm.js';

const canvas = document.querySelector('#hunter-globe');
const stage = canvas?.closest('.globe-stage');

if (canvas && stage) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let phi = 3.2;
  let visible = true;
  let globe;

  const markers = [
    { location: [35.6762, 139.6503], size: 0.055 },
    { location: [40.7128, -74.006], size: 0.035 },
    { location: [51.5072, -0.1276], size: 0.032 },
    { location: [-33.8688, 151.2093], size: 0.032 },
    { location: [1.3521, 103.8198], size: 0.03 },
  ];

  const arcs = [
    { from: [35.6762, 139.6503], to: [40.7128, -74.006] },
    { from: [35.6762, 139.6503], to: [-33.8688, 151.2093] },
    { from: [51.5072, -0.1276], to: [1.3521, 103.8198] },
  ];

  let currentSize = 0;
  
  const render = () => {
    const rect = stage.getBoundingClientRect();
    const size = Math.max(320, Math.round(rect.width));
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    // サイズが同じなら再生成しない（ResizeObserverの無限ループによる停止を防ぐ）
    if (currentSize === size) return;
    currentSize = size;

    globe?.destroy();
    globe = createGlobe(canvas, {
      devicePixelRatio: dpr,
      width: size * dpr,
      height: size * dpr,
      phi,
      theta: 0.2,
      dark: 1,
      diffuse: 1.25,
      mapSamples: 12000,
      mapBrightness: 4.2,
      mapBaseBrightness: 0.05,
      baseColor: [0.13, 0.16, 0.1],
      markerColor: [0.72, 0.9, 0.18],
      glowColor: [0.13, 0.18, 0.08],
      arcColor: [0.9, 0.25, 0.18],
      arcWidth: 0.42,
      arcHeight: 0.22,
      markerElevation: 0.015,
      opacity: 0.9,
      scale: 1.02,
      markers,
      arcs,
      onRender: state => {
        phi += 0.003;
        state.phi = phi;
      },
    });
  };

  let resizeTimer;
  const observer = new ResizeObserver(() => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(render, 120);
  });

  const visibilityObserver = new IntersectionObserver(entries => {
    visible = entries[0]?.isIntersecting ?? true;
  }, { threshold: 0.01 });

  observer.observe(stage);
  visibilityObserver.observe(stage);
  render();

  window.addEventListener('pagehide', () => {
    observer.disconnect();
    visibilityObserver.disconnect();
    globe?.destroy();
  }, { once: true });
}
