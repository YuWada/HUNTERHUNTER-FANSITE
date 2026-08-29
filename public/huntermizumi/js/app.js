/**
 * 念能力 系統診断 メインアプリケーション
 * 動的適応型ルーティング（60問プールから15問を出題） & 6系統多次元得失点スコアリング
 */

class NenApp {
  constructor() {
    this.totalQuestionsToAnswer = 15;
    this.currentStep = 0; // 0 〜 14

    // 出題履歴スタック: { question: Object, selectedOptionIndex: number }[]
    this.history = [];

    // 出題済み質問IDのSet（重複防止）
    this.usedQuestionIds = new Set();

    // 累積スコア（6系統）
    this.scores = {
      enhancement: 0,
      transmutation: 0,
      emission: 0,
      conjuration: 0,
      manipulation: 0,
      specialization: 0
    };

    this.resultData = null;

    // DOM要素
    this.screens = {
      intro: document.getElementById('screen-intro'),
      quiz: document.getElementById('screen-quiz'),
      mizumishiki: document.getElementById('screen-mizumishiki'),
      result: document.getElementById('screen-result')
    };

    this.initEvents();
  }

  initEvents() {
    // スタートボタン
    const btnStart = document.getElementById('btn-start');
    if (btnStart) {
      btnStart.addEventListener('click', () => {
        nenAudio.playClick();
        this.startQuiz();
      });
    }

    // 戻るボタン
    const btnPrev = document.getElementById('btn-prev-q');
    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        nenAudio.playClick();
        this.prevQuestion();
      });
    }

    // サウンド切り替えボタン
    const btnSound = document.getElementById('btn-sound-toggle');
    if (btnSound) {
      btnSound.addEventListener('click', () => {
        const isMuted = nenAudio.toggleMute();
        btnSound.textContent = isMuted ? '🔇 サウンド OFF' : '🔊 サウンド ON';
        btnSound.classList.toggle('muted', isMuted);
      });
    }

    // 再診断ボタン
    const btnRetry = document.getElementById('btn-retry');
    if (btnRetry) {
      btnRetry.addEventListener('click', () => {
        nenAudio.playClick();
        this.resetQuiz();
      });
    }

    // X (Twitter) シェアボタン
    const btnShareX = document.getElementById('btn-share-x');
    if (btnShareX) {
      btnShareX.addEventListener('click', () => {
        this.shareToX();
      });
    }

    // 結果コピーボタン
    const btnCopyResult = document.getElementById('btn-copy-result');
    if (btnCopyResult) {
      btnCopyResult.addEventListener('click', () => {
        this.copyResultToClipboard();
      });
    }
  }

  // 画面の切り替え
  showScreen(screenName) {
    Object.keys(this.screens).forEach(key => {
      if (this.screens[key]) {
        this.screens[key].classList.toggle('active', key === screenName);
      }
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // クイズ開始
  startQuiz() {
    this.currentStep = 0;
    this.history = [];
    this.usedQuestionIds.clear();
    this.resetScores();

    // 最初の質問を選定
    const firstQ = this.pickNextQuestion(1);
    this.history.push({ question: firstQ, selectedOptionIndex: null });
    this.usedQuestionIds.add(firstQ.id);

    this.showScreen('quiz');
    this.renderCurrentQuestion();
  }

  // スコア初期化
  resetScores() {
    this.scores = {
      enhancement: 0,
      transmutation: 0,
      emission: 0,
      conjuration: 0,
      manipulation: 0,
      specialization: 0
    };
  }

  /**
   * 現在のフェーズと回答傾向に応じて最適な質問をプールから抽出する動的ルーティング
   * @param {number} phase フェーズ番号 (1, 2, 3, 4)
   * @returns {Object} 質問オブジェクト
   */
  pickNextQuestion(phase) {
    // 該当フェーズでまだ使っていない質問を抽出
    const candidates = QUESTION_POOL.filter(
      q => q.phase === phase && !this.usedQuestionIds.has(q.id)
    );

    if (candidates.length === 0) {
      // フォールバック：全プールで未使用のもの
      const fallback = QUESTION_POOL.filter(q => !this.usedQuestionIds.has(q.id));
      return fallback[Math.floor(Math.random() * fallback.length)] || QUESTION_POOL[0];
    }

    // Phase 1: ランダムまたはバランスよく抽出
    if (phase === 1) {
      return candidates[Math.floor(Math.random() * candidates.length)];
    }

    // ランダム要素を強化: 30%の確率で完全にランダムな質問を選ぶ
    if (Math.random() < 0.3) {
      return candidates[Math.floor(Math.random() * candidates.length)];
    }

    // Phase 2〜4: 現在のスコア上位系統や競合系統にアプローチする設問を重み付け抽出
    // 現在のスコアを計算
    const currentScores = this.getCurrentAccumulatedScores();
    const sortedTypes = Object.keys(currentScores).sort(
      (a, b) => currentScores[b] - currentScores[a]
    );
    const topType1 = sortedTypes[0];
    const topType2 = sortedTypes[1];

    // topType1 と topType2 のスコア差が大きい選択肢を含む質問を優先（差分を際立たせる）
    let bestQuestion = candidates[0];
    let maxVariance = -1;

    candidates.forEach(q => {
      let variance = 0;
      q.options.forEach(opt => {
        const s1 = opt.scores[topType1] || 0;
        const s2 = opt.scores[topType2] || 0;
        variance += Math.abs(s1 - s2);
      });
      // 少しランダム性を加えて偏りを防ぐ
      const scoreWeight = variance + Math.random() * 10;
      if (scoreWeight > maxVariance) {
        maxVariance = scoreWeight;
        bestQuestion = q;
      }
    });

    return bestQuestion;
  }

  // 現在までの確定済みスコアを計算
  getCurrentAccumulatedScores() {
    const scores = {
      enhancement: 0,
      transmutation: 0,
      emission: 0,
      conjuration: 0,
      manipulation: 0,
      specialization: 0
    };

    for (let i = 0; i < this.currentStep; i++) {
      const item = this.history[i];
      if (item && item.selectedOptionIndex !== null) {
        const opt = item.question.options[item.selectedOptionIndex];
        if (opt && opt.scores) {
          Object.keys(opt.scores).forEach(key => {
            scores[key] += opt.scores[key];
          });
        }
      }
    }
    return scores;
  }

  // 現在の質問を描画
  renderCurrentQuestion() {
    const currentItem = this.history[this.currentStep];
    if (!currentItem) return;

    const q = currentItem.question;
    const progressFill = document.getElementById('quiz-progress-fill');
    const qNumber = document.getElementById('quiz-q-number');
    const qCategory = document.getElementById('quiz-category');
    const qText = document.getElementById('quiz-question-text');
    const optionsContainer = document.getElementById('quiz-options-container');
    const btnPrev = document.getElementById('btn-prev-q');

    const total = this.totalQuestionsToAnswer;
    const current = this.currentStep + 1;

    if (progressFill) {
      progressFill.style.width = `${(current / total) * 100}%`;
    }
    if (qNumber) {
      qNumber.textContent = `QUESTION ${current} / ${total}`;
    }
    if (qCategory) {
      qCategory.textContent = q.category;
    }
    if (qText) {
      qText.textContent = q.question;
    }

    // 戻るボタンの表示・非表示
    if (btnPrev) {
      btnPrev.style.visibility = this.currentStep > 0 ? 'visible' : 'hidden';
    }

    // 選択肢のレンダリング
    if (optionsContainer) {
      optionsContainer.innerHTML = '';
      q.options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';

        if (currentItem.selectedOptionIndex === idx) {
          btn.classList.add('selected');
        }

        btn.innerHTML = `
          <span class="option-marker">${String.fromCharCode(65 + idx)}</span>
          <span class="option-text">${opt.text}</span>
        `;

        btn.addEventListener('click', () => {
          nenAudio.playClick();
          this.selectOption(idx);
        });

        optionsContainer.appendChild(btn);
      });
    }

    // カードのフェードインアニメーション
    const card = document.getElementById('quiz-card');
    if (card) {
      card.classList.remove('fade-in');
      void card.offsetWidth;
      card.classList.add('fade-in');
    }
  }

  // 選択肢決定
  selectOption(optionIndex) {
    const currentItem = this.history[this.currentStep];
    const prevSelectedIndex = currentItem.selectedOptionIndex;
    currentItem.selectedOptionIndex = optionIndex;

    // もし過去の選択肢を変更した場合、以降の履歴を再構築するために後続を切り詰める
    if (prevSelectedIndex !== null && prevSelectedIndex !== optionIndex) {
      while (this.history.length > this.currentStep + 1) {
        const popped = this.history.pop();
        this.usedQuestionIds.delete(popped.question.id);
      }
    }

    if (this.currentStep < this.totalQuestionsToAnswer - 1) {
      setTimeout(() => {
        nenAudio.playNext();
        this.currentStep++;

        // 次の質問が履歴になければ新しく抽出
        if (this.currentStep >= this.history.length) {
          // フェーズ判定 (1〜3問: Phase 1, 4〜7問: Phase 2, 8〜11問: Phase 3, 12〜15問: Phase 4)
          let nextPhase = 1;
          if (this.currentStep >= 11) nextPhase = 4;
          else if (this.currentStep >= 7) nextPhase = 3;
          else if (this.currentStep >= 3) nextPhase = 2;

          const nextQ = this.pickNextQuestion(nextPhase);
          this.history.push({ question: nextQ, selectedOptionIndex: null });
          this.usedQuestionIds.add(nextQ.id);
        }

        this.renderCurrentQuestion();
      }, 180);
    } else {
      // 15問すべて回答完了 -> 水見式演出へ
      setTimeout(() => {
        this.finishQuiz();
      }, 250);
    }
  }

  // 前の質問に戻る
  prevQuestion() {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.renderCurrentQuestion();
    }
  }

  // クイズ完了・水見式演出と結果集計
  finishQuiz() {
    this.calculateFinalScores();
    this.showScreen('mizumishiki');
    nenAudio.playAuraCharge();

    const container = document.getElementById('mizumishiki-view');
    const dominantType = this.resultData.dominantType;

    setTimeout(() => {
      nenAudio.playMizumishiki();
    }, 1500);

    nenVisualizer.startMizumishikiAnimation(container, dominantType, () => {
      nenAudio.playResultFanfare();
      this.showScreen('result');
      this.renderResult();
    });
  }

  // 最終スコア集計ロジック（多次元得失点方式 & 正規化）
  calculateFinalScores() {
    this.resetScores();

    this.history.forEach(item => {
      if (item && item.selectedOptionIndex !== null) {
        const opt = item.question.options[item.selectedOptionIndex];
        if (opt && opt.scores) {
          Object.keys(opt.scores).forEach(key => {
            if (key !== 'specialization') {
              this.scores[key] += opt.scores[key] * 1.1;
            } else {
              this.scores[key] += opt.scores[key];
            }
          });
        }
      }
    });

    // 最小スコアを調べて正の領域へシフト（Base shift）
    const values = Object.values(this.scores);
    const minVal = Math.min(...values);
    const shift = minVal < 0 ? Math.abs(minVal) + 5 : 5;

    const shiftedScores = {};
    let totalShifted = 0;
    Object.keys(this.scores).forEach(key => {
      shiftedScores[key] = Math.max(0.1, this.scores[key] + shift);
      totalShifted += shiftedScores[key];
    });

    // 各系統の適合度（パーセンテージ 0〜100%）
    const percentages = {};
    let sumPct = 0;
    Object.keys(shiftedScores).forEach(key => {
      const pct = Math.round((shiftedScores[key] / totalShifted) * 100);
      percentages[key] = pct;
      sumPct += pct;
    });

    // 100%に微調整
    const diff = 100 - sumPct;
    if (diff !== 0) {
      const highestKey = Object.keys(this.scores).reduce((a, b) => this.scores[a] > this.scores[b] ? a : b);
      percentages[highestKey] += diff;
    }

    // 主系統（最高生スコア）
    let dominantType = 'enhancement';
    let maxRaw = -999;
    Object.keys(this.scores).forEach(key => {
      if (this.scores[key] > maxRaw) {
        maxRaw = this.scores[key];
        dominantType = key;
      }
    });

    // 副系統（2番目）
    let subType = null;
    let secondRaw = -999;
    Object.keys(this.scores).forEach(key => {
      if (key !== dominantType && this.scores[key] > secondRaw) {
        secondRaw = this.scores[key];
        subType = key;
      }
    });

    this.resultData = {
      rawScores: { ...this.scores },
      percentages,
      dominantType,
      subType,
      dominantData: NEN_TYPES[dominantType],
      subData: subType ? NEN_TYPES[subType] : null
    };
  }

  // 診断結果画面のレンダリング
  renderResult() {
    const data = this.resultData;
    if (!data) return;

    const dominant = data.dominantData;

    // 1. メインヘッダー
    const auraBadge = document.getElementById('res-aura-badge');
    const title = document.getElementById('res-type-title');
    const ruby = document.getElementById('res-type-ruby');
    const hisokaWord = document.getElementById('res-hisoka-word');
    const summary = document.getElementById('res-summary');
    const description = document.getElementById('res-description');

    if (auraBadge) {
      auraBadge.textContent = `${dominant.name} (${dominant.english})`;
      auraBadge.style.backgroundColor = dominant.color;
      auraBadge.style.boxShadow = `0 0 15px ${dominant.glow}`;
    }
    if (title) {
      title.textContent = dominant.name;
      title.style.color = dominant.color;
      title.style.textShadow = `0 0 20px ${dominant.glow}`;
    }
    if (ruby) ruby.textContent = dominant.ruby;
    if (hisokaWord) {
      hisokaWord.textContent = `ヒソカのオーラ別性格分析：『${dominant.hisokaQuote}』♦`;
    }
    if (summary) summary.textContent = dominant.summary;
    if (description) {
      description.innerHTML = dominant.description.replace(/\n/g, '<br><br>');
    }

    // 2. 長所・短所
    const strengthsList = document.getElementById('res-strengths');
    const weaknessesList = document.getElementById('res-weaknesses');

    if (strengthsList) {
      strengthsList.innerHTML = dominant.strengths.map(s => `<li>${s}</li>`).join('');
    }
    if (weaknessesList) {
      weaknessesList.innerHTML = dominant.weaknesses.map(w => `<li>${w}</li>`).join('');
    }

    // 3. 六性図レーダーチャート
    const canvas = document.getElementById('res-hex-canvas');
    if (canvas) {
      nenVisualizer.drawHexRadar(canvas, data.percentages, data.dominantType);
    }

    // 4. キャラクター紹介
    const charList = document.getElementById('res-characters-list');
    if (charList) {
      charList.innerHTML = dominant.characters.map(char => `
        <div class="character-card" style="border-left-color: ${dominant.color}">
          <div class="char-header">
            <h4 class="char-name">${char.name}</h4>
            <span class="char-ability">${char.ability}</span>
          </div>
          <p class="char-desc">${char.desc}</p>
        </div>
      `).join('');
    }

    // 5. オリジナル念能力提案（回答ハッシュに基づく選出）
    const abilityContainer = document.getElementById('res-original-ability');
    if (abilityContainer && dominant.originalAbilities && dominant.originalAbilities.length > 0) {
      // ユーザーの回答履歴からシード値を計算して、一意かつ個性的な能力を選出
      let hash = 0;
      this.history.forEach((h, i) => {
        hash += (h.selectedOptionIndex + 1) * (i + 7) * 31;
      });
      const abilityIndex = Math.abs(hash) % dominant.originalAbilities.length;
      const ability = dominant.originalAbilities[abilityIndex];
      this.resultData.originalAbility = ability;

      abilityContainer.innerHTML = `
        <div class="original-ability-card" style="--card-color: ${dominant.color}">
          <div class="ability-card-top">
            <div class="ability-badge">深層心理から導き出されたオリジナル念能力</div>
            <span class="ability-index-label">全${dominant.originalAbilities.length}種中 No.${abilityIndex + 1}</span>
          </div>
          <h3 class="ability-name">${ability.name}</h3>
          <p class="ability-desc">${ability.desc}</p>
          <div class="ability-subnote">※あなたの無意識の行動心理と潜在オーラパターンから構築された専用の能力です。</div>
        </div>
      `;
    }

    // 6. 相性分析
    const compBest = document.getElementById('res-comp-best');
    const compWorst = document.getElementById('res-comp-worst');

    if (compBest) {
      compBest.innerHTML = `
        <div class="comp-label best">◎ 最高の相棒：${dominant.compatibility.best}</div>
        <p class="comp-desc">${dominant.compatibility.bestReason}</p>
      `;
    }
    if (compWorst) {
      compWorst.innerHTML = `
        <div class="comp-label worst">▲ 衝突注意：${dominant.compatibility.worst}</div>
        <p class="comp-desc">${dominant.compatibility.worstReason}</p>
      `;
    }
  }

  // X (旧Twitter) へシェア
  shareToX() {
    if (!this.resultData) return;
    const dominant = this.resultData.dominantData;
    const p = this.resultData.percentages;
    const ability = this.resultData.originalAbility;
    const text = `【電脳ハンター協会：よく当たる念能力系統診断ヒソカ×水見式】
念能力：　${ability.name}
${ability.desc}

判定系統：${dominant.name}（${dominant.english}）
ヒソカの分析：『${dominant.hisokaQuote}』
${dominant.summary}

▼ 六性図 オーラ適性分布
強化系: ${p.enhancement}%
変化系: ${p.transmutation}%
放出系: ${p.emission}%
具現化系: ${p.conjuration}%
操作系: ${p.manipulation}%
特質系: ${p.specialization}%

電脳ハンター協会
https://hunterhunter-fansite.pages.dev/

#念能力診断 #ヒソカの水見式 #ハンターハンター #HUNTERxHUNTER`;
    const url = 'https://hunterhunter-fansite.pages.dev/';
    const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(shareUrl, '_blank');
  }

  // クリップボードにコピー
  copyResultToClipboard() {
    if (!this.resultData) return;
    const dominant = this.resultData.dominantData;
    const p = this.resultData.percentages;
    const ability = this.resultData.originalAbility;
    const text = `【電脳ハンター協会：よく当たる念能力系統診断ヒソカ×水見式】
念能力：　${ability.name}
${ability.desc}

判定系統：${dominant.name}（${dominant.english}）
ヒソカの分析：『${dominant.hisokaQuote}』
${dominant.summary}

▼ 六性図 オーラ適性分布
強化系: ${p.enhancement}%
変化系: ${p.transmutation}%
放出系: ${p.emission}%
具現化系: ${p.conjuration}%
操作系: ${p.manipulation}%
特質系: ${p.specialization}%

電脳ハンター協会
https://hunterhunter-fansite.pages.dev/`;

    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('btn-copy-result');
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = '✅ コピーしました！';
        setTimeout(() => {
          btn.innerHTML = orig;
        }, 2000);
      }
    }).catch(err => {
      console.error('Copy failed', err);
    });
  }

  // リセット
  resetQuiz() {
    this.currentStep = 0;
    this.history = [];
    this.usedQuestionIds.clear();
    this.resetScores();
    this.resultData = null;
    this.showScreen('intro');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new NenApp();
});
