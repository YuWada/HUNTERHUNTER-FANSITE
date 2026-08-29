import createGlobe from './vendor/cobe/cobe.esm.js';

let canvas = document.querySelector('#hunter-globe');
const stage = canvas?.closest('.globe-stage');

if (canvas && stage) {
  // アクセスするたびに初期の角度（自転の開始位置）をランダムにする
  let phi = Math.random() * Math.PI * 2; 
  let globe;
  let visible = true;

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
  let animationFrame; // アニメーションループ用の変数
  
  const render = () => {
    const rect = stage.getBoundingClientRect();
    const size = Math.max(320, Math.round(rect.width));
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    if (Math.abs(currentSize - size) < 5) return; 
    currentSize = size;
    
    if (globe) {
      globe.destroy();
      cancelAnimationFrame(animationFrame); // 既存のループを停止
      
      // Cobeはcanvasの周りにラッパーdivを自動生成するため、stageの中身を完全に空にしてリセットする
      stage.innerHTML = '';
      
      canvas = document.createElement('canvas');
      canvas.id = 'hunter-globe';
      canvas.style.width = '100%';
      canvas.style.height = '100%';
      canvas.style.display = 'block';
      stage.appendChild(canvas);
    }

    // Vanilla JSのCobeには onRender が存在しないため、オプションから外す
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
    });

    // 自分で requestAnimationFrame を回して update を呼ぶのが Vanilla JS での正しいアニメーション手法
    const loop = () => {
      if (visible) {
        // 回転速度を 1/3 (0.003 -> 0.001) に変更
        phi += 0.001;
        if (globe) globe.update({ phi });
      }
      animationFrame = requestAnimationFrame(loop);
    };
    loop();
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
