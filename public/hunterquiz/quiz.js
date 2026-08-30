(function() {
  // DOM Elements
  const screenStart = document.getElementById('screen-start');
  const screenQuiz = document.getElementById('screen-quiz');
  const screenResult = document.getElementById('screen-result');
  
  const btnStart = document.getElementById('btn-start');
  const btnRetry = document.getElementById('btn-retry');
  const btnShareX = document.getElementById('btn-share-x');
  const btnShareCopy = document.getElementById('btn-share-copy');
  
  const progressFill = document.getElementById('progress-fill');
  const stageText = document.getElementById('stage-text');
  const questionCountText = document.getElementById('question-count-text');
  const questionText = document.getElementById('question-text');
  const choicesContainer = document.getElementById('choices-container');
  
  const resCorrects = document.getElementById('result-corrects');
  const resScore = document.getElementById('result-score');
  const resRank = document.getElementById('result-rank');
  const resDesc = document.getElementById('result-desc');

  // Game State
  let allQuestions = [];
  let usedQuestions = new Set();
  
  let currentStage = 1; 
  let totalQuestionsAnswered = 0; 
  let questionsInCurrentStage = 0; 
  let correctsInCurrentStage = 0;
  
  let totalCorrects = 0;
  let totalScore = 0;

  const TOTAL_QUESTIONS = 25;
  const QUESTIONS_PER_STAGE = 5;
  const SHARE_URL = "https://hunterhunter-fansite.pages.dev/";

  // Rank Descriptions
  const rankDescriptions = {
    triple: "世界でも10人といない、複数の分野において歴史的な大発見や世界的偉業を成し遂げた最高峰のハンター。君の知識はもはや伝説級だ！",
    double: "シングルハンターの称号を持ちつつ、自ら育てた後輩もシングルを獲得するほどの優れた育成者。君の知識は確かなものだ。",
    single: "特定の分野において華々しい業績を残した者に与えられる称号。君のHUNTER×HUNTERに対する情熱と知識は本物だ！",
    pro: "怪物・財宝・秘境など、未知なるものを追い求める世界一過酷で世界一儲かる職業。君はすでに一人前のハンターだ。",
    rookie: "表のハンター試験には合格したが、念能力を学ぶ「裏試験」はここからが本番。気を抜かずにさらなる高みを目指そう！",
    exam3: "「三次試験あたりから死傷者が激増するんだよなァ…」。実力はあるが、ここから先は一瞬の油断が命取りになるレベルだ。",
    exam1: "会場の雰囲気にも飲まれがちなルーキー。ベテラン受験者による「新人潰し」の標的にされないよう気をつけるんだな。",
    civilian: "念の存在すら知らない一般市民。ハンターの世界は危険すぎる、一般社会で平和に暮らすのが一番だ。"
  };

  // Decrypt and Parse CSV
  function initData() {
    if (typeof ENCRYPTED_QUIZ_DATA === 'undefined') return;
    const key = 42;
    let decodedStr = atob(ENCRYPTED_QUIZ_DATA);
    let uintArray = new Uint8Array(decodedStr.length);
    for (let i = 0; i < decodedStr.length; i++) {
      uintArray[i] = decodedStr.charCodeAt(i) ^ key;
    }
    const decoder = new TextDecoder('utf-8');
    const csvStr = decoder.decode(uintArray);
    
    const lines = csvStr.split('\n').map(l => l.trim()).filter(l => l);
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',');
      if (cols.length >= 7) {
        allQuestions.push({
          q: cols[0], c: cols[1],
          w: [cols[2], cols[3], cols[4], cols[5]],
          lv: parseInt(cols[6], 10) || 1
        });
      }
    }
  }

  function shuffle(array) {
    let currentIndex = array.length, randomIndex;
    while (currentIndex != 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
  }

  function getEligibleQuestions() {
    let minLv = 1, maxLv = 2;
    switch(currentStage) {
      case 1: case 2: minLv = 1; maxLv = 2; break;
      case 3: case 4: minLv = 2; maxLv = 3; break;
      case 5: case 6: minLv = 3; maxLv = 4; break;
      case 7: case 8: minLv = 3; maxLv = 5; break;
      default: minLv = 4; maxLv = 5; break; 
    }
    
    let candidates = allQuestions.filter(q => q.lv >= minLv && q.lv <= maxLv && !usedQuestions.has(q.q));
    if (candidates.length === 0) {
      candidates = allQuestions.filter(q => !usedQuestions.has(q.q));
    }
    return candidates;
  }

  function showScreen(screenEl) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    screenEl.classList.add('active');
  }

  function startGame() {
    usedQuestions.clear();
    currentStage = 1;
    totalQuestionsAnswered = 0;
    questionsInCurrentStage = 0;
    correctsInCurrentStage = 0;
    totalCorrects = 0;
    totalScore = 0;
    showScreen(screenQuiz);
    nextQuestion();
  }

  function nextQuestion() {
    if (totalQuestionsAnswered >= TOTAL_QUESTIONS) {
      finishGame();
      return;
    }
    
    if (questionsInCurrentStage >= QUESTIONS_PER_STAGE) {
      if (correctsInCurrentStage === QUESTIONS_PER_STAGE) {
        currentStage += 2;
      } else {
        currentStage += 1;
      }
      if (currentStage > 10) currentStage = 10;
      questionsInCurrentStage = 0;
      correctsInCurrentStage = 0;
    }
    
    const candidates = getEligibleQuestions();
    if (candidates.length === 0) {
      finishGame();
      return;
    }
    
    const qObj = candidates[Math.floor(Math.random() * candidates.length)];
    usedQuestions.add(qObj.q);
    renderQuestion(qObj);
  }

  function renderQuestion(qObj) {
    stageText.textContent = `段階 ${currentStage}`;
    questionCountText.textContent = `${totalQuestionsAnswered + 1} / ${TOTAL_QUESTIONS} 問目`;
    progressFill.style.width = `${((totalQuestionsAnswered) / TOTAL_QUESTIONS) * 100}%`;
    
    questionText.textContent = qObj.q;
    choicesContainer.innerHTML = '';
    
    let choices = [
      { text: qObj.c, isCorrect: true },
      { text: qObj.w[0], isCorrect: false },
      { text: qObj.w[1], isCorrect: false },
      { text: qObj.w[2], isCorrect: false },
      { text: qObj.w[3], isCorrect: false }
    ];
    
    // 5択をシャッフル
    shuffle(choices);

    // 1/15 chance for silence (always at the bottom)
    if (Math.random() < (1 / 15)) {
      choices.push({ text: "答えは沈黙!!", isCorrect: false });
    }
    
    choices.forEach(c => {
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.textContent = c.text;
      btn.onclick = () => handleAnswer(c.isCorrect, btn);
      choicesContainer.appendChild(btn);
    });
  }

  function handleAnswer(isCorrect, btnEl) {
    const allBtns = choicesContainer.querySelectorAll('.choice-btn');
    allBtns.forEach(b => b.disabled = true);
    
    btnEl.classList.add('clicked');
    
    totalQuestionsAnswered++;
    questionsInCurrentStage++;
    
    if (isCorrect) {
      correctsInCurrentStage++;
      totalCorrects++;
      totalScore += currentStage;
    }
    
    setTimeout(() => {
      nextQuestion();
    }, 400);
  }

  function finishGame() {
    progressFill.style.width = `100%`;
    showScreen(screenResult);
    
    resCorrects.textContent = `${totalCorrects} / ${TOTAL_QUESTIONS}`;
    resScore.textContent = `${totalScore} 点`;
    
    let rankName = "";
    let descText = "";
    resRank.className = "rank-title";
    
    if (totalScore === 125) {
      rankName = "トリプルハンター";
      descText = rankDescriptions.triple;
      resRank.classList.add("rank-triple");
    } else if (totalScore >= 120) {
      rankName = "ダブルハンター";
      descText = rankDescriptions.double;
      resRank.classList.add("rank-double");
    } else if (totalScore >= 110) {
      rankName = "シングルハンター";
      descText = rankDescriptions.single;
      resRank.classList.add("rank-single");
    } else if (totalScore >= 100) {
      rankName = "プロハンター";
      descText = rankDescriptions.pro;
    } else if (totalScore >= 85) {
      rankName = "新人ハンター";
      descText = rankDescriptions.rookie;
    } else if (totalScore >= 60) {
      rankName = "ハンター試験三次試験レベル";
      descText = rankDescriptions.exam3;
    } else if (totalScore >= 30) {
      rankName = "ハンター試験新人受験者レベル";
      descText = rankDescriptions.exam1;
    } else {
      rankName = "一般人レベル";
      descText = rankDescriptions.civilian;
    }
    
    resRank.textContent = rankName;
    resDesc.textContent = descText;
  }

  function buildShareText() {
    const rank = resRank.textContent;
    return `【HUNTER試験 ドキドキ５択クイズ】\n私の結果は『${rank}』でした！\n\n正解数: ${totalCorrects}/25問\n獲得スコア: ${totalScore}点\n\n#HUNTER試験 #ハンターハンタークイズ\n`;
  }

  btnStart.addEventListener('click', startGame);
  btnRetry.addEventListener('click', startGame);
  
  btnShareX.addEventListener('click', () => {
    const text = encodeURIComponent(buildShareText() + SHARE_URL);
    window.open(`https://twitter.com/intent/tweet?text=${text}`, '_blank');
  });
  
  btnShareCopy.addEventListener('click', () => {
    const text = buildShareText() + SHARE_URL;
    navigator.clipboard.writeText(text).then(() => {
      alert("結果をクリップボードにコピーしました！");
    }).catch(err => {
      console.error("Copy failed", err);
      alert("コピーに失敗しました。");
    });
  });

  initData();
})();
