/**
 * Web Audio API を用いた効果音シンセサイザー
 * 外部音声ファイル不要で動作
 */
class NenAudioManager {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
        this.initialized = true;
      }
    } catch (e) {
      console.warn('AudioContext not supported', e);
    }
  }

  resume() {
    this.init();
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }

  // 選択肢タップ音（軽快なクリスタルクリック音）
  playClick() {
    if (this.muted) return;
    this.resume();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    osc.type = 'sine';
    osc.frequency.setValueAtTime(587.33, now); // D5
    osc.frequency.exponentialRampToValueAtTime(880, now + 0.08); // A5

    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.12);
  }

  // 質問送り音
  playNext() {
    if (this.muted) return;
    this.resume();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(440, now);
    osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.15);

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.18);
  }

  // オーラチャージ音（低音の唸りとエネルギーの上昇）
  playAuraCharge() {
    if (this.muted) return;
    this.resume();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;

    // オシレーター1: サブベース
    const osc1 = this.ctx.createOscillator();
    const gain1 = this.ctx.createGain();
    osc1.type = 'sawtooth';
    osc1.frequency.setValueAtTime(65.4, now);
    osc1.frequency.exponentialRampToValueAtTime(130.8, now + 2.0);

    // フィルター
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(150, now);
    filter.frequency.exponentialRampToValueAtTime(800, now + 2.0);

    gain1.gain.setValueAtTime(0.01, now);
    gain1.gain.linearRampToValueAtTime(0.2, now + 1.2);
    gain1.gain.exponentialRampToValueAtTime(0.001, now + 2.3);

    osc1.connect(filter);
    filter.connect(gain1);
    gain1.connect(this.ctx.destination);

    osc1.start(now);
    osc1.stop(now + 2.3);
  }

  // 水見式発動音（神秘的な和音）
  playMizumishiki() {
    if (this.muted) return;
    this.resume();
    if (!this.ctx) return;

    const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]; // C5, E5, G5, C6, E6
    const now = this.ctx.currentTime;

    notes.forEach((freq, index) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const startTime = now + index * 0.12;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.001, startTime);
      gain.gain.linearRampToValueAtTime(0.12, startTime + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.0001, startTime + 1.8);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + 1.8);
    });
  }

  // 診断結果発表ファンファーレ（荘厳な響き）
  playResultFanfare() {
    if (this.muted) return;
    this.resume();
    if (!this.ctx) return;

    const chords = [
      { f: [261.63, 329.63, 392.00], t: 0, d: 0.3 },     // C
      { f: [293.66, 369.99, 440.00], t: 0.25, d: 0.3 },  // D
      { f: [329.63, 415.30, 493.88], t: 0.5, d: 0.35 },  // E
      { f: [523.25, 659.25, 783.99, 1046.50], t: 0.85, d: 1.8 } // High C Chord
    ];

    const now = this.ctx.currentTime;

    chords.forEach(chord => {
      chord.f.forEach(freq => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const startTime = now + chord.t;

        osc.type = chord.t === 0.85 ? 'triangle' : 'sine';
        osc.frequency.setValueAtTime(freq, startTime);

        gain.gain.setValueAtTime(0.001, startTime);
        gain.gain.linearRampToValueAtTime(0.08, startTime + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, startTime + chord.d);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(startTime);
        osc.stop(startTime + chord.d);
      });
    });
  }
}

const nenAudio = new NenAudioManager();
