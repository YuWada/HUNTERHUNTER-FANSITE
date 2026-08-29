/**
 * 六性図レーダーチャート & 水見式アニメーション描画マネージャー
 */

class NenVisualizer {
  constructor() {
    this.animationId = null;
  }

  /**
   * 六性図（レーダーチャート）をCanvasに描画
   * @param {HTMLCanvasElement} canvas
   * @param {Object} percentages 各系統の割合 { enhancement: 30, transmutation: 20, ... }
   * @param {string} dominantType 主系統ID
   */
  drawHexRadar(canvas, percentages, dominantType) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Canvas解像度設定
    const rect = canvas.getBoundingClientRect();
    const size = Math.min(rect.width || 340, rect.height || 340);
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.scale(dpr, dpr);

    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size * 0.36;

    // 系統の並び順（上から時計回り）
    const types = NEN_HEX_ORDER; // ['enhancement', 'transmutation', 'conjuration', 'specialization', 'manipulation', 'emission']
    const totalVertices = types.length;

    // 角度計算（上を0度とする）: -90度からスタート
    const getAngle = (i) => -Math.PI / 2 + (i * 2 * Math.PI) / totalVertices;

    // アニメーション進行度 (0.0 -> 1.0)
    let progress = 0;
    const startTime = performance.now();
    const duration = 1200; // 1.2秒

    const render = (currentTime) => {
      const elapsed = currentTime - startTime;
      progress = Math.min(elapsed / duration, 1.0);
      // イージング（easeOutCubic）
      const ease = 1 - Math.pow(1 - progress, 3);

      ctx.clearRect(0, 0, size, size);

      // 1. 背景の同心六角形グリッド描画
      const gridLevels = [0.25, 0.5, 0.75, 1.0];
      gridLevels.forEach((level) => {
        ctx.beginPath();
        for (let i = 0; i < totalVertices; i++) {
          const angle = getAngle(i);
          const x = centerX + Math.cos(angle) * (radius * level);
          const y = centerY + Math.sin(angle) * (radius * level);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = level === 1.0 ? 'rgba(255, 255, 255, 0.25)' : 'rgba(255, 255, 255, 0.08)';
        ctx.lineWidth = level === 1.0 ? 1.5 : 1;
        ctx.stroke();
      });

      // 2. 軸線描画
      for (let i = 0; i < totalVertices; i++) {
        const angle = getAngle(i);
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // 3. データポリゴンの描画
      const primaryColor = NEN_TYPES[dominantType]?.color || '#ff4757';
      ctx.beginPath();
      const points = [];
      for (let i = 0; i < totalVertices; i++) {
        const typeKey = types[i];
        const val = (percentages[typeKey] || 0) / 100; // 0.0 ~ 1.0
        const currentVal = val * ease;
        const angle = getAngle(i);
        // 最低でも少し内側になるように下限設定
        const dist = radius * Math.max(currentVal, 0.1);
        const x = centerX + Math.cos(angle) * dist;
        const y = centerY + Math.sin(angle) * dist;
        points.push({ x, y, typeKey, val });
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();

      // グラデーション塗りつぶし
      const grad = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, radius);
      grad.addColorStop(0, primaryColor + '66'); // 40% opacity
      grad.addColorStop(1, primaryColor + '22'); // 13% opacity
      ctx.fillStyle = grad;
      ctx.fill();

      // ポリゴンの輪郭
      ctx.strokeStyle = primaryColor;
      ctx.lineWidth = 2.5;
      ctx.shadowColor = primaryColor;
      ctx.shadowBlur = 10;
      ctx.stroke();
      ctx.shadowBlur = 0; // リセット

      // 4. データポイント頂点の光る円描画
      points.forEach(pt => {
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 4.5, 0, Math.PI * 2);
        ctx.fillStyle = NEN_TYPES[pt.typeKey].color;
        ctx.shadowColor = NEN_TYPES[pt.typeKey].color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.shadowBlur = 0;
      });

      // 5. 各頂点ラベル・パーセンテージ描画
      for (let i = 0; i < totalVertices; i++) {
        const typeKey = types[i];
        const typeData = NEN_TYPES[typeKey];
        const angle = getAngle(i);
        const labelDist = radius + 26;
        const lx = centerX + Math.cos(angle) * labelDist;
        const ly = centerY + Math.sin(angle) * labelDist;

        ctx.font = 'bold 12px "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // 主系統の場合は強調
        const isDominant = typeKey === dominantType;
        ctx.fillStyle = isDominant ? typeData.color : '#e0e0e0';
        if (isDominant) {
          ctx.shadowColor = typeData.color;
          ctx.shadowBlur = 6;
        }
        ctx.fillText(typeData.name, lx, ly - 7);
        ctx.shadowBlur = 0;

        // パーセンテージ表示
        const pctVal = Math.round((percentages[typeKey] || 0) * ease);
        ctx.font = '11px sans-serif';
        ctx.fillStyle = isDominant ? '#ffffff' : '#888888';
        ctx.fillText(`${pctVal}%`, lx, ly + 8);
      }

      if (progress < 1.0) {
        requestAnimationFrame(render);
      }
    };

    requestAnimationFrame(render);
  }

  /**
   * 水見式のアニメーションを開始
   * @param {HTMLElement} container 水見式表示用DOM要素
   * @param {string} dominantType 判定された念系統
   * @param {Function} onComplete 完了時コールバック
   */
  startMizumishikiAnimation(container, dominantType, onComplete) {
    if (!container) return;
    container.innerHTML = '';
    container.className = `mizumishiki-stage type-${dominantType}`;

    const typeData = NEN_TYPES[dominantType];

    // 水見式HTML構造生成
    const stage = document.createElement('div');
    stage.className = 'mizumishiki-inner';
    stage.innerHTML = `
      <div class="mizumishiki-aura-aura" style="--aura-color: ${typeData.color}"></div>
      <div class="glass-wrapper">
        <div class="glass-rim"></div>
        <div class="glass-body">
          <div class="water-surface">
            <div class="leaf ${typeData.mizumishiki.type}">
              <div class="leaf-vein"></div>
            </div>
            <div class="water-effect-layer ${typeData.mizumishiki.type}"></div>
          </div>
          <div class="water-fill ${typeData.mizumishiki.type}">
            <div class="water-inner-glow"></div>
            <div class="water-particles-container"></div>
          </div>
        </div>
        <div class="glass-base"></div>
      </div>
      <div class="mizumishiki-aura-hands">
        <div class="hand hand-left"></div>
        <div class="hand hand-right"></div>
      </div>
      <div class="mizumishiki-status-text">オーラを集中させています...</div>
    `;

    container.appendChild(stage);

    const statusText = stage.querySelector('.mizumishiki-status-text');
    const waterFill = stage.querySelector('.water-fill');
    const leaf = stage.querySelector('.leaf');
    const effectLayer = stage.querySelector('.water-effect-layer');
    const particles = stage.querySelector('.water-particles-container');

    // フェーズ1: オーラ発動 (0.8秒後)
    setTimeout(() => {
      stage.classList.add('phase-aura');
      if (statusText) statusText.textContent = '「煉」を展開中… オーラが水に干渉しています';
    }, 800);

    // フェーズ2: 水見式異変発動 (2.0秒後)
    setTimeout(() => {
      stage.classList.add('phase-reaction', `effect-${typeData.mizumishiki.type}`);
      if (statusText) {
        statusText.innerHTML = `<span class="reaction-highlight" style="color:${typeData.color}">${typeData.mizumishiki.title}</span>`;
      }

      // 系統ごとの固有パーティクル生成
      this.generateParticles(particles, typeData.mizumishiki.type, typeData.color);
    }, 2200);

    // フェーズ3: 判定完了 (4.2秒後)
    setTimeout(() => {
      stage.classList.add('phase-complete');
      if (onComplete) onComplete();
    }, 4200);
  }

  /**
   * 系統ごとの水見式パーティクル生成
   */
  generateParticles(container, effectType, color) {
    if (!container) return;
    const count = effectType === 'overflow' ? 30 : 20;

    for (let i = 0; i < count; i++) {
      const p = document.createElement('div');
      p.className = `m-particle ${effectType}`;
      p.style.setProperty('--p-color', color);
      p.style.left = `${10 + Math.random() * 80}%`;
      p.style.top = `${20 + Math.random() * 60}%`;
      p.style.animationDelay = `${Math.random() * 1.5}s`;
      p.style.animationDuration = `${1 + Math.random() * 2}s`;
      container.appendChild(p);
    }
  }
}

const nenVisualizer = new NenVisualizer();
