/**
 * HUNTER×HUNTER 念系統 深層心理テスト 設問プール（全60問）
 * 4つのフェーズ（Phase 1: 基礎認知, Phase 2: 対人葛藤, Phase 3: 心理防衛, Phase 4: 究極ジレンマ）
 * 6系統（強化・変化・放出・具現化・操作・特質）が完全均等（各系統40回ずつ+3選択肢）になるよう設計
 */

const QUESTION_POOL = [
  // =========================================================================
  // Phase 1: 基礎認知・日常スタイル (Q1 〜 Q15)
  // =========================================================================
  {
    id: 1, // [強化, 変化, 放出, 具現化]
    phase: 1,
    category: '日常の予期せぬ出来事',
    question: 'レストランで注文したものと全く違う料理が運ばれてきました。あなたはどうする？',
    options: [
      {
        text: '「これ頼んでないですよ！」とその場ですぐ店員に明るく伝える',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 0, manipulation: 0, specialization: -1 }
      },
      {
        text: '「まあこれも何かの縁かも」と面白がってそのまま食べてみる',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 1 }
      },
      {
        text: '「おーい店員さん！間違ってるぜ！」と少し大きな声で呼んで豪快に笑い飛ばす',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -1, specialization: -2 }
      },
      {
        text: '注文伝票やメニューの表記を再確認し、間違いの原因を冷静に確認してから交換を求める',
        scores: { enhancement: 0, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      }
    ]
  },
  {
    id: 2, // [変化, 放出, 具現化, 操作]
    phase: 1,
    category: '未知へのアプローチ',
    question: '初めて訪れた街で完全に道に迷ってしまいました。最初の行動は？',
    options: [
      {
        text: '迷ったこと自体を楽しみ、普段なら入らないような怪しい裏路地を散策してみる',
        scores: { enhancement: 0, emission: 0, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 1 }
      },
      {
        text: '近くにいる通行人やお店の人に声をかけて直接気さくに道を尋ねる',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -1, manipulation: 0, specialization: -2 }
      },
      {
        text: 'スマホの地図アプリを開き、現在地と目的地をピンポイントで照合・ルート再設計する',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '通ってきた目印や看板を思い出し、最も効率的かつ論理的に元の交差点へ引き返す',
        scores: { enhancement: -1, emission: -1, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 3, // [放出, 具現化, 操作, 特質]
    phase: 1,
    category: '生活空間と秩序',
    question: 'あなたのスマートフォンの中のアプリや写真の整理状態は？',
    options: [
      {
        text: '画面一面にアイコンや通知が溢れているが、普段使うものさえ動けば気にしない',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -3, manipulation: -3, specialization: -1 }
      },
      {
        text: 'カテゴリごとにフォルダ分けされ、通知バッジも消去して完璧に整頓されている',
        scores: { enhancement: -2, emission: -2, transmutation: -2, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '指の動線や使用頻度を計算し、片手操作で最短アクセスできるよう配置されている',
        scores: { enhancement: -1, emission: -1, transmutation: 0, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '自分だけの特殊な壁紙やウィジェット、他人が見たら意味不明な独自の世界観で構築している',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      }
    ]
  },
  {
    id: 4, // [具現化, 操作, 特質, 強化]
    phase: 1,
    category: '対人距離感',
    question: '他人に「あなたって本当に変わってるよね」と言われたとき、内心どう感じる？',
    options: [
      {
        text: '「変な目で見られたかも」と自分のマナーや振る舞いに粗がなかったか少し気にする',
        scores: { enhancement: -1, emission: 0, transmutation: -2, conjuration: 3, manipulation: 1, specialization: -2 }
      },
      {
        text: '「普通って何？」と心の中で相手の言葉の定義や基準の曖昧さを分析する',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '「ふふん、もっと言って」と独自の個性や美意識を認められたと感じて嬉しくなる',
        scores: { enhancement: -1, emission: 0, transmutation: 2, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '「えっ、どこが普通と違うんだろう？」と率直に不思議に思い、その場で聞き返す',
        scores: { enhancement: 3, emission: 1, transmutation: -1, conjuration: 0, manipulation: 0, specialization: -2 }
      }
    ]
  },
  {
    id: 5, // [操作, 特質, 強化, 変化]
    phase: 1,
    category: '意思決定の基準',
    question: '新作のゲームや趣味の道具を手に入れたとき、最初にすることは？',
    options: [
      {
        text: '全体のシステムや設定を把握し、一番効率のいい育成計画や攻略ルートを組み立てる',
        scores: { enhancement: -2, emission: -1, transmutation: 1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '誰もやっていない特殊な縛りプレイや、自分だけの独創的な楽しみ方を模索する',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '説明書やチュートリアルは飛ばして、まず実際に触ってガンガン動かしてみる',
        scores: { enhancement: 3, emission: 2, transmutation: 0, conjuration: -3, manipulation: -2, specialization: 0 }
      },
      {
        text: '隠し要素や裏技、裏コマンドがないか最初に探ってニヤニヤする',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: 0, manipulation: 1, specialization: 1 }
      }
    ]
  },
  {
    id: 6, // [特質, 強化, 変化, 放出]
    phase: 1,
    category: 'ルールの解釈',
    question: '夜中、車も人も全く通らない見通しの良い道路の赤信号。あなたなら？',
    options: [
      {
        text: '信号の規則よりも「今この空間における自分の意志」に従って静かに進む',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: -2, manipulation: -1, specialization: 3 }
      },
      {
        text: '誰もいなくても赤は赤！曲がったことは嫌だから青になるまで真っ直ぐ待つ',
        scores: { enhancement: 3, emission: -1, transmutation: -3, conjuration: 2, manipulation: 1, specialization: -2 }
      },
      {
        text: 'その瞬間の気分次第。渡る理由も待つ理由も適当にでっち上げて楽しむ',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 1 }
      },
      {
        text: '車が来ないことをチラッと確認して、「よし！」と小走りでパッと渡る',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -2, manipulation: 0, specialization: 0 }
      }
    ]
  },
  {
    id: 7, // [強化, 変化, 放出, 具現化]
    phase: 1,
    category: '道具へのこだわり',
    question: '普段持ち歩く財布やペン、鞄などを選ぶとき、もっとも重視する基準は？',
    options: [
      {
        text: '壊れにくさ、頑丈さ、使いやすさといった実用本位の性能',
        scores: { enhancement: 3, emission: 1, transmutation: -1, conjuration: 1, manipulation: 1, specialization: -2 }
      },
      {
        text: '他の人が持っていない一風変わった素材や、遊び心のあるギミック',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: 0, manipulation: -1, specialization: 2 }
      },
      {
        text: 'パッと見てテンションが上がる色合いや、気兼ねなくガンガン扱える手軽さ',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -2, manipulation: -2, specialization: -1 }
      },
      {
        text: '細部の縫製、機能美、使うほどに味が出る素材の品質と完成度',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 3, manipulation: 1, specialization: 2 }
      }
    ]
  },
  {
    id: 8, // [変化, 放出, 具現化, 操作]
    phase: 1,
    category: '会話と沈黙',
    question: '複数人で話していて不意に会話が途切れ、沈黙が流れたときどうする？',
    options: [
      {
        text: '誰かの発言をいじったり、少し際どい冗談を投げて反応を伺う',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -2, manipulation: 0, specialization: 2 }
      },
      {
        text: '思いついた他愛のない話題やギャグを大声で振って場を盛り上げる',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -2, manipulation: 0, specialization: -2 }
      },
      {
        text: '「何か面白いこと言わなきゃ」と内心少し緊張して無難な質問を探す',
        scores: { enhancement: 0, emission: -1, transmutation: -2, conjuration: 3, manipulation: 1, specialization: -2 }
      },
      {
        text: '誰が気まずそうにしているか観察し、その人が話しやすい話題を意図的に振る',
        scores: { enhancement: -1, emission: 0, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 9, // [放出, 具現化, 操作, 特質]
    phase: 1,
    category: '空間のポジショニング',
    question: '初めて入ったカフェやファミレスで自由に席を選べるとき、どこに座る？',
    options: [
      {
        text: '窓際やテラスなど、風通しがよく開放感のある明るい席',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -1, manipulation: -1, specialization: 0 }
      },
      {
        text: '壁際や隅の席など、周囲の視線が届きにくくパーソナルスペースが守れる場所',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '店全体が見渡せて、出入り口や店員の動線が把握しやすい席',
        scores: { enhancement: 0, emission: -1, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '他の席とは明らかに雰囲気が違う、一番独特な空気の漂う特別な席',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      }
    ]
  },
  {
    id: 10, // [具現化, 操作, 特質, 強化]
    phase: 1,
    category: '時間の使い方',
    question: '急に週末の予定がキャンセルになり、丸一日フリーになったときの最初の気分は？',
    options: [
      {
        text: '急な変更に少し戸惑いつつ、溜まっていた作業や部屋の整理に充てるスケジュールを組み直す',
        scores: { enhancement: -1, emission: -2, transmutation: -2, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '浮いた時間をどう活用すれば一番有意義か、タスクの優先順位を整理する',
        scores: { enhancement: -1, emission: -1, transmutation: 0, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '誰とも連絡を取らず、完全に一人の深い世界に浸れることに至福の安堵を覚える',
        scores: { enhancement: -2, emission: -3, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「よし！身体を動かしに行くか！」と即座に外へ飛び出す準備をする',
        scores: { enhancement: 3, emission: 2, transmutation: 0, conjuration: -2, manipulation: -2, specialization: -1 }
      }
    ]
  },
  {
    id: 11, // [操作, 特質, 強化, 変化]
    phase: 1,
    category: '自己開示の深度',
    question: '知り合って間もない人に「休日は何してるの？」と聞かれたら？',
    options: [
      {
        text: '当たり障りのない無難な回答をして、相手の話を聞く側にコントロールする',
        scores: { enhancement: -2, emission: -1, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 0 }
      },
      {
        text: '「人並みのことですよ」と濁し、本当のコアな探求・趣味は絶対に教えない',
        scores: { enhancement: -2, emission: -2, transmutation: 2, conjuration: 1, manipulation: 1, specialization: 3 }
      },
      {
        text: '最近ハマっていることや好きなことを包み隠さず熱心にそのまま語る',
        scores: { enhancement: 3, emission: 2, transmutation: -3, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '少しボケたり話を盛ったりして、相手をからかいながら面白おかしく話す',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -2, manipulation: 0, specialization: 1 }
      }
    ]
  },
  {
    id: 12, // [特質, 強化, 変化, 放出]
    phase: 1,
    category: '直感と衝動',
    question: '買い物中に、予算オーバーだけど強烈に惹かれるアイテムを見つけたら？',
    options: [
      {
        text: '「この出会いは運命だ」と独自の意味づけをして迷わず手に入れる',
        scores: { enhancement: 0, emission: 0, transmutation: 1, conjuration: 0, manipulation: -1, specialization: 3 }
      },
      {
        text: '「今買わなきゃ絶対後悔する！」と直感で即座にレジへ持っていく',
        scores: { enhancement: 3, emission: 1, transmutation: 0, conjuration: -3, manipulation: -3, specialization: 0 }
      },
      {
        text: '店員と値引き交渉を仕掛けるか、裏ルートやフリマで安く手に入らないか企む',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 1 }
      },
      {
        text: '「買っちゃえ買っちゃえ！」とテンション任せにパッと豪快に買う',
        scores: { enhancement: 1, emission: 3, transmutation: 1, conjuration: -3, manipulation: -3, specialization: -1 }
      }
    ]
  },
  {
    id: 13, // [強化, 変化, 放出, 具現化]
    phase: 1,
    category: '物語の好み',
    question: '映画や小説、ドラマを見るとき、もっとも感情移入しやすい登場人物は？',
    options: [
      {
        text: '不器用だけど熱い信念を持って愚直に立ち向かう主人公',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 0, manipulation: -2, specialization: -1 }
      },
      {
        text: '飄々としていて本心が読めないが、ここぞで魅せるトリックスター',
        scores: { enhancement: -2, emission: 0, transmutation: 3, conjuration: -1, manipulation: 0, specialization: 2 }
      },
      {
        text: '仲間思いで涙もろく、感情を爆発させて助けに来てくれる熱い親分肌',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '自らに厳しい戒律を課し、緻密な計画で復讐や理想を遂行するストイックな人物',
        scores: { enhancement: 0, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 1 }
      }
    ]
  },
  {
    id: 14, // [変化, 放出, 具現化, 操作]
    phase: 1,
    category: '日常のルーティン',
    question: '毎日の朝の支度やルーティンについてのあなたの感覚は？',
    options: [
      {
        text: 'その日の体調や気分に合わせて、起きてから柔軟に行動を決める',
        scores: { enhancement: 1, emission: 1, transmutation: 3, conjuration: -3, manipulation: -3, specialization: 1 }
      },
      {
        text: '大急ぎで支度して、勢いとノリで家を飛び出すことが多い',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -2, specialization: -1 }
      },
      {
        text: '起きる時間も手順も完全に固定化されており、崩れると気持ち悪い',
        scores: { enhancement: -1, emission: -2, transmutation: -3, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '朝のタイムスケジュールを分単位で組み立て、最短で準備を完了させる',
        scores: { enhancement: -2, emission: -1, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 15, // [放出, 具現化, 操作, 特質]
    phase: 1,
    category: '他者への共感の形',
    question: '友人が「仕事がつらい」と悩みを打ち明けてきたとき、あなたの自然な対応は？',
    options: [
      {
        text: '「よし、美味いもんでも食いに行って発散しようぜ！」と外へ連れ出す',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -1, specialization: -1 }
      },
      {
        text: '「大変だったね」と細かく状況を聞き、相手のストレス要因を丁寧に分析してあげる',
        scores: { enhancement: 0, emission: -1, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '何がつらい原因なのか論理的に整理し、転職や交渉などの具体的アクションを指示する',
        scores: { enhancement: -1, emission: -1, transmutation: -1, conjuration: 1, manipulation: 3, specialization: 0 }
      },
      {
        text: '「その苦しみも君の人生の深みになる」と本質的な視点を提示し、自立を見守る',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      }
    ]
  },

  // =========================================================================
  // Phase 2: 危機管理 & 対人葛藤 (Q16 〜 Q30)
  // =========================================================================
  {
    id: 16, // [具現化, 操作, 特質, 強化]
    phase: 2,
    category: '集団の膠着状態',
    question: 'チームの議論が平行線をたどり、誰も決め手を打てず重苦しい空気になったら？',
    options: [
      {
        text: '対立している論点をホワイトボード等に可視化し、客観的な比較表を作る',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: 'それぞれのキーマンの意見を個別に根回しして、自然な合意形成へ誘導する',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 0, manipulation: 3, specialization: 1 }
      },
      {
        text: '誰も触れていない盲点や、突拍子もない逆張りアイデアを投げて局面を一変させる',
        scores: { enhancement: -1, emission: 0, transmutation: 2, conjuration: -1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「あれこれ悩んでも始まらない！まずやってみよう！」と口火を切る',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: -2, manipulation: -1, specialization: 0 }
      }
    ]
  },
  {
    id: 17, // [操作, 特質, 強化, 変化]
    phase: 2,
    category: '友人の過ちへの介入',
    question: '大切な友人が、明らかに損をする危険な道へ進もうとしていたら？',
    options: [
      {
        text: 'その選択をするとどんな不利益が生じるか、客観的証拠と数字を並べて説得する',
        scores: { enhancement: -1, emission: -1, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '友人の覚悟を確かめ、「本人が選んだ道なら痛い目を見るのも本人の運命」と見守る',
        scores: { enhancement: 0, emission: -2, transmutation: 1, conjuration: 0, manipulation: -2, specialization: 3 }
      },
      {
        text: '正面から「それは絶対に間違ってる！」と本気で怒り、体を張って引き止める',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -1, manipulation: 0, specialization: -2 }
      },
      {
        text: 'あえて直接止めず、失敗したときに最小限の被害で済むよう裏で先回りして罠を外しておく',
        scores: { enhancement: -2, emission: -1, transmutation: 3, conjuration: 2, manipulation: 2, specialization: 2 }
      }
    ]
  },
  {
    id: 18, // [特質, 強化, 変化, 放出]
    phase: 2,
    category: '不当な非難への対応',
    question: '身に覚えのない悪口や根拠のない噂を流されていると知ったとき、どうする？',
    options: [
      {
        text: '「くだらない噂を流す暇な人たちだな」と鼻で笑い、完全に無視して相手にしない',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: 1, specialization: 3 }
      },
      {
        text: '「ふざけるな！」と怒りが沸き、噂の出どころを直接問い詰めに行く',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -1, manipulation: 0, specialization: -2 }
      },
      {
        text: 'その噂を利用して逆に相手をハメる罠や、面白おかしい偽情報を流し返す',
        scores: { enhancement: -2, emission: 0, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 2 }
      },
      {
        text: '「何言ってんだあいつら！」と仲間にぶちまけて、大騒ぎして発散する',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -2, manipulation: -1, specialization: -2 }
      }
    ]
  },
  {
    id: 19, // [強化, 変化, 放出, 具現化]
    phase: 2,
    category: '直前の突発トラブル',
    question: '超重要プレゼンや本番の10分前、機材トラブルで資料が使えなくなったら？',
    options: [
      {
        text: '「資料がなくても俺の言葉で直接伝えてやる！」と腹を括って熱弁する',
        scores: { enhancement: 3, emission: 1, transmutation: 0, conjuration: -3, manipulation: -2, specialization: 0 }
      },
      {
        text: '「機材トラブルも演出のうち」とアドリブの寸劇や会話形式に切り替えて場を沸かせる',
        scores: { enhancement: 0, emission: 1, transmutation: 3, conjuration: -2, manipulation: 0, specialization: 2 }
      },
      {
        text: '「おい誰か手伝え！」と周りを巻き込んで大急ぎで即席の対応策を叫びながら進める',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -1, specialization: -1 }
      },
      {
        text: '念のため用意していた印刷用紙やバックアップデータを即座に取り出して対処する',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      }
    ]
  },
  {
    id: 20, // [変化, 放出, 具現化, 操作]
    phase: 2,
    category: '苦手な相手との協業',
    question: '価値観が合わず苦手なタイプの人と、密にペアを組んで作業することになったら？',
    options: [
      {
        text: '相手の性格や弱点を観察し、相手が機嫌よく動いてくれるよう上手におだてて操る',
        scores: { enhancement: -3, emission: -2, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 1 }
      },
      {
        text: '「仕事は仕事」と割り切り、あえて相手の懐に飛び込んでフランクに接してみる',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -2, manipulation: 0, specialization: -2 }
      },
      {
        text: 'お互いの担当領域と納期、ルールを厳格に切り分け、最低限の業務連絡に留める',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '作業プロセスを完全にマニュアル化し、私情が挟まらない仕組みを作って遂行する',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 21, // [放出, 具現化, 操作, 特質]
    phase: 2,
    category: '孤立と信念',
    question: '自分が「絶対にこれが正しい」と確信している提案が、多数決で否決されたら？',
    options: [
      {
        text: '「なんでわかんねぇんだよ！」と不満をあからさまに口にして周囲に食ってかかる',
        scores: { enhancement: 2, emission: 3, transmutation: -2, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '自分の提案のどの部分に欠陥やリスクがあったのか、徹底的に再検証する',
        scores: { enhancement: -1, emission: -2, transmutation: -2, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: 'なぜ否決されたのか反対派の利害関係を分析し、次回通すための根回しと修正案を練る',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '「大衆には理解できない先見性だった」と内心で受け止め、一人でその道を極める',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: -1, specialization: 3 }
      }
    ]
  },
  {
    id: 22, // [具現化, 操作, 特質, 強化]
    phase: 2,
    category: '他者の対立への介入',
    question: '目の前で仲間同士が感情的な大ゲンカを始めたとき、あなたの最初の行動は？',
    options: [
      {
        text: 'お互いの主張を整理し、何が食い違いの原因なのか双方に冷静に確認する',
        scores: { enhancement: -1, emission: -1, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '双方の性格と弱点を突いて、これ以上争うと両者損をする論理を突きつけて鎮める',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '少し離れた場所から事の成り行きを静観し、人間の本質や人間関係の力学を観察する',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '二人の間に割って入り、「やめろ！仲間同士で喧嘩するな！」と体当たりで引き離す',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -2, manipulation: 0, specialization: -2 }
      }
    ]
  },
  {
    id: 23, // [操作, 特質, 強化, 変化]
    phase: 2,
    category: '他人の嘘への感知',
    question: '会話中、相手が明らかに自分に対して保身の嘘をついていると気づいたら？',
    options: [
      {
        text: '嘘をつかざるを得なかった相手の背景や利害関係を推測し、状況を掌握する',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '「この人はこういう人間か」と心の中で静かに達観し、深い関わりを持たない',
        scores: { enhancement: 0, emission: -2, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「それ、嘘ですよね？」と直接目を見てズバッと切り込む',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 0, manipulation: 0, specialization: -1 }
      },
      {
        text: '気づかないフリをして嘘に乗り、相手がさらにボロを出すのを面白がって観察する',
        scores: { enhancement: -2, emission: -1, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 2 }
      }
    ]
  },
  {
    id: 24, // [特質, 強化, 変化, 放出]
    phase: 2,
    category: '隠蔽と誠実',
    question: '自分の小さなミスが原因でトラブルが起きたが、誰も自分のミスだと気づいていないとき？',
    options: [
      {
        text: '「この事態がどう転ぶか」を達観して観察し、必要な時だけ静かに介入する',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '隠しているのが耐えられず、すぐに「すみません、私のミスです！」と名乗り出る',
        scores: { enhancement: 3, emission: 2, transmutation: -3, conjuration: 1, manipulation: -2, specialization: -2 }
      },
      {
        text: '誰にも気づかれないうちに、裏で完璧に修正して何事もなかったことにする',
        scores: { enhancement: -3, emission: -2, transmutation: 3, conjuration: 2, manipulation: 2, specialization: 0 }
      },
      {
        text: '「ヤバっ、俺のせいかも！」と焦って顔に出てしまい、すぐにバレる',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: -2, manipulation: -2, specialization: -2 }
      }
    ]
  },
  {
    id: 25, // [強化, 変化, 放出, 具現化]
    phase: 2,
    category: 'リーダーシップのスタイル',
    question: 'プロジェクトのリーダーとしてチームを率いるとき、あなたの基本スタンスは？',
    options: [
      {
        text: '自分が誰よりも先頭に立って汗を流し、行動と熱意でメンバーを引っ張る',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -1, manipulation: -1, specialization: 0 }
      },
      {
        text: '細かく指示せず、意外な発想やトリッキーなアイデアで状況を面白く牽引する',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: -2, manipulation: 0, specialization: 2 }
      },
      {
        text: '「みんなで最高の打ち上げ行くぞ！」と飲み食いや声掛けで士気を盛り上げる',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -1, specialization: -2 }
      },
      {
        text: 'リスクや例外処理のマニュアルを固め、誰がやってもミスが起きない仕組みを作る',
        scores: { enhancement: -2, emission: -3, transmutation: -2, conjuration: 3, manipulation: 2, specialization: 0 }
      }
    ]
  },
  {
    id: 26, // [変化, 放出, 具現化, 操作]
    phase: 2,
    category: '他者からの評価への反応',
    question: '他人から「本当に優秀で素晴らしいですね」と過剰に持ち上げられたとき？',
    options: [
      {
        text: '「もっと褒めていいですよ〜」とおどけて笑いに変え、本心を探る',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -1, manipulation: 1, specialization: 1 }
      },
      {
        text: '「よせやい！照れるだろ！」と大笑いして肩をバシッと叩く',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -2, manipulation: -1, specialization: -2 }
      },
      {
        text: '「何か裏があるのか？」「何か頼み事でもされるのか？」と警戒する',
        scores: { enhancement: -2, emission: -1, transmutation: 1, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '相手がなぜそう言ってきたのか、意図や今後の人間関係の立ち位置を計算する',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 27, // [放出, 具現化, 操作, 特質]
    phase: 2,
    category: '改善と期限のジレンマ',
    question: '納期の直前、既存の成果物より明らかに優れた新しいアイデアを閃いたら？',
    options: [
      {
        text: '「やっちゃえ！」とアドレナリン全開で仲間を巻き込んで一気に差し替える',
        scores: { enhancement: 2, emission: 3, transmutation: 1, conjuration: -3, manipulation: -3, specialization: 0 }
      },
      {
        text: '納期厳守が絶対。今回は既存のものを確実に納品し、新案は次回に回す',
        scores: { enhancement: -2, emission: -2, transmutation: -2, conjuration: 3, manipulation: 3, specialization: -2 }
      },
      {
        text: '既存のベースを崩さず、新しいアイデアのエッセンスだけを部分的に組み込む',
        scores: { enhancement: -1, emission: 0, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 0 }
      },
      {
        text: '新案が圧倒的に素晴らしいなら、納期延長の交渉を行ってでも最高峰を追求する',
        scores: { enhancement: 0, emission: -1, transmutation: 0, conjuration: 1, manipulation: 0, specialization: 3 }
      }
    ]
  },
  {
    id: 28, // [具現化, 操作, 特質, 強化]
    phase: 2,
    category: '許容できない境界線',
    question: '人間関係において、「これだけは絶対に許せない」と感じる行為は？',
    options: [
      {
        text: '約束や時間を平気で破り、不真面目に他人に迷惑をかけること',
        scores: { enhancement: 0, emission: -1, transmutation: -3, conjuration: 3, manipulation: 2, specialization: -1 }
      },
      {
        text: '自分の領域やプライベートに無遠慮に踏み込まれ、自由やペースを乱されること',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 2 }
      },
      {
        text: '型にはまった平凡な常識を押し付けられ、個性を否定されること',
        scores: { enhancement: 0, emission: 0, transmutation: 2, conjuration: -2, manipulation: -2, specialization: 3 }
      },
      {
        text: '裏切りや不誠実、仲間を陰で嘲笑うような卑怯な振る舞い',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: 0, manipulation: -1, specialization: -1 }
      }
    ]
  },
  {
    id: 29, // [操作, 特質, 強化, 変化]
    phase: 2,
    category: '臨時収入の使途',
    question: '宝くじなどで予期せぬ100万円の臨時収入が手に入ったら？',
    options: [
      {
        text: '将来のリスクに備えて全額貯金するか、堅実な資産運用に回す',
        scores: { enhancement: -2, emission: -2, transmutation: -2, conjuration: 2, manipulation: 3, specialization: -1 }
      },
      {
        text: '普段は絶対に手が出ないような、レアな逸品や特別な体験に投資する',
        scores: { enhancement: 0, emission: 0, transmutation: 2, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '欲しかったトレーニング器具や身体を鍛える道具を即座に買い揃える',
        scores: { enhancement: 3, emission: 1, transmutation: 0, conjuration: 0, manipulation: 0, specialization: -1 }
      },
      {
        text: 'ギャンブルやスリルある投資に突っ込んで、さらに増やせるか勝負してみる',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -3, manipulation: -2, specialization: 1 }
      }
    ]
  },
  {
    id: 30, // [特質, 強化, 変化, 放出]
    phase: 2,
    category: '約束のキャンセル',
    question: '楽しみにしていた友人との予定が、相手の身勝手な都合で当日ドタキャンされたら？',
    options: [
      {
        text: '「人間とはそういうもの」と静かに受け止め、その友人の器を心の中で測る',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「おいおい、そりゃねぇだろ！」と電話をかけて直接文句を言う',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: 0, manipulation: 0, specialization: -2 }
      },
      {
        text: '「急に暇ができた！」と瞬時に切り替え、一人でできる別の面白い悪巧みを探す',
        scores: { enhancement: 0, emission: 0, transmutation: 3, conjuration: -2, manipulation: -1, specialization: 2 }
      },
      {
        text: '「ふざけんな！」と怒りのメッセージを即座に連投して感情をぶつける',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: 0, manipulation: 0, specialization: -2 }
      }
    ]
  },

  // =========================================================================
  // Phase 3: 深層心理・防衛機制・無意識行動 (Q31 〜 Q45)
  // =========================================================================
  {
    id: 31, // [強化, 変化, 放出, 具現化]
    phase: 3,
    category: '自己嫌悪からの回復',
    question: '大きな失敗をして深い自己嫌悪に陥ったとき、あなたの立ち直り方は？',
    options: [
      {
        text: '筋トレやランニングで汗を流すか、ぐっすり寝て翌朝には気合いでリセットする',
        scores: { enhancement: 3, emission: 1, transmutation: -1, conjuration: -2, manipulation: -2, specialization: -1 }
      },
      {
        text: '他人に面白おかしく話せる自虐ネタやギャグとして昇華して笑い飛ばす',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -1, manipulation: 0, specialization: 1 }
      },
      {
        text: '信頼できる仲間に愚痴を聞いてもらい、感情を吐き出してスッキリする',
        scores: { enhancement: 0, emission: 3, transmutation: -2, conjuration: 0, manipulation: -1, specialization: -2 }
      },
      {
        text: 'なぜ失敗したのかノートに書き出し、原因と再発防止策を論理的に整理して心を落ち着かせる',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      }
    ]
  },
  {
    id: 32, // [変化, 放出, 具現化, 操作]
    phase: 3,
    category: '弱みの開示',
    question: '自分のコンプレックスや弱点について、普段どう扱っている？',
    options: [
      {
        text: '弱みを見せると付け込まれるので、絶対に他人には悟られないようポーカーフェイスを貫く',
        scores: { enhancement: -3, emission: -2, transmutation: 3, conjuration: 2, manipulation: 2, specialization: 1 }
      },
      {
        text: '隠そうとしても態度に出てしまうので、最初からオープンにして笑い話にする',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: -2, manipulation: -1, specialization: -2 }
      },
      {
        text: '弱点を克服するために人知れず厳しいトレーニングや勉強を重ねてカバーする',
        scores: { enhancement: 1, emission: 0, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '自分の弱点を補ってくれる人間を周囲に配置し、チームで補完する体制を組む',
        scores: { enhancement: -2, emission: -1, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      }
    ]
  },
  {
    id: 33, // [放出, 具現化, 操作, 特質]
    phase: 3,
    category: '涙と感情表出',
    question: '人前で涙を流すことに対して、あなたはどう感じている？',
    options: [
      {
        text: '感動した時や悔しい時は自然と涙が出るし、恥ずかしいとは思わない',
        scores: { enhancement: 1, emission: 3, transmutation: -3, conjuration: -1, manipulation: -2, specialization: -1 }
      },
      {
        text: '人前で泣くのは絶対に嫌。感情を取り乱す姿は絶対に見せたくない',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '人前で泣くのは合理的でないため、感情をコントロールして冷静を保つ',
        scores: { enhancement: -2, emission: -3, transmutation: -1, conjuration: 1, manipulation: 3, specialization: 0 }
      },
      {
        text: '涙を流している自分を、どこか頭の片隅で冷静に観察しているもう一人の自分がいる',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 1, manipulation: 1, specialization: 3 }
      }
    ]
  },
  {
    id: 34, // [具現化, 操作, 特質, 強化]
    phase: 3,
    category: '運命と偶然',
    question: '人生における「偶然の出会い」や「運命」についてどう考えている？',
    options: [
      {
        text: '偶然などなく、日々の緻密な積み重ねと準備が結果を引き寄せているだけだ',
        scores: { enhancement: 0, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '全ての事象には必ず理由と因果関係があり、偶然に見えるものも必然の確率だ',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '目に見えない大きな運命や宿命の引き寄せが、確実に自分を導いていると感じる',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 0, manipulation: -1, specialization: 3 }
      },
      {
        text: '運命なんてない！自分の力と努力、気合いで道を切り拓くものだ',
        scores: { enhancement: 3, emission: 1, transmutation: -1, conjuration: 1, manipulation: 1, specialization: -2 }
      }
    ]
  },
  {
    id: 35, // [操作, 特質, 強化, 変化]
    phase: 3,
    category: '秘密の守り方',
    question: '「誰にも言わないでね」と重大な秘密を打ち明けられたとき、どうする？',
    options: [
      {
        text: '状況次第では、自分や相手を守るためのカードとして使えるよう心に留めておく',
        scores: { enhancement: -3, emission: -2, transmutation: 2, conjuration: 0, manipulation: 3, specialization: 2 }
      },
      {
        text: '「ふーん」と聞き流し、自分に関係のない他人の秘密にはそもそも興味が持てない',
        scores: { enhancement: -1, emission: -1, transmutation: 2, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '約束だから絶対に誰にも言わない。墓場まで持っていく',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 3, manipulation: 1, specialization: 0 }
      },
      {
        text: '親しい仲間には「内緒だけどね…」と小声で教えたくなってしまう',
        scores: { enhancement: -1, emission: 1, transmutation: 3, conjuration: -2, manipulation: 0, specialization: -1 }
      }
    ]
  },
  {
    id: 36, // [特質, 強化, 変化, 放出]
    phase: 3,
    category: 'テリトリーへの侵犯',
    question: '自分の机や部屋の物を、家族や他人に勝手に触られたり動かされたら？',
    options: [
      {
        text: '自分の精神空間を汚されたように感じ、相手との見えない壁をさらに厚くする',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 1, manipulation: 1, specialization: 3 }
      },
      {
        text: '「おい！何で勝手に触るんだ！」とその場で怒鳴って抗議する',
        scores: { enhancement: 3, emission: 2, transmutation: -1, conjuration: 1, manipulation: 1, specialization: 0 }
      },
      {
        text: '二度と触られないよう、自分にしか解除できない特殊な鍵やトラップを仕掛ける',
        scores: { enhancement: -1, emission: -1, transmutation: 3, conjuration: 2, manipulation: 2, specialization: 2 }
      },
      {
        text: '「触るなっつったろーが！」と怒りを爆発させ、相手に直接文句を言いに行く',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: 1, manipulation: 1, specialization: -1 }
      }
    ]
  },
  {
    id: 37, // [強化, 変化, 放出, 具現化]
    phase: 3,
    category: '敗北の受容',
    question: 'ライバルとの一騎打ちで完膚なきまでに敗北した直後の心境は？',
    options: [
      {
        text: '悔しくてたまらない！「次は絶対にぶっ倒す！」と即座に特訓を始める',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 0, manipulation: -2, specialization: -1 }
      },
      {
        text: '「強いね〜流石だわ」と拍手しつつ、次は違うゲームやルールで勝負しようと企む',
        scores: { enhancement: -2, emission: 0, transmutation: 3, conjuration: -1, manipulation: 0, specialization: 2 }
      },
      {
        text: '「クソッ！」と大声を上げて悔しがり、仲間と酒を飲んで悔しさを晴らす',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -2, manipulation: -1, specialization: -2 }
      },
      {
        text: '相手の強さの秘密や戦術を徹底的に分析し、弱点を突くカウンター策をノートに書き留める',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 1 }
      }
    ]
  },
  {
    id: 38, // [変化, 放出, 具現化, 操作]
    phase: 3,
    category: '直感と論理の衝突',
    question: '自分の強烈な直感と、客観的なデータや論理が真っ向から対立したとき、どちらを信じる？',
    options: [
      {
        text: '「直感」と「データ」の双方が納得できる第3の妥協点や裏技を探す',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: 1, manipulation: 2, specialization: 0 }
      },
      {
        text: '「自分の腹の底の直感を信じないでどうする！」と本能のままに突き進む',
        scores: { enhancement: 2, emission: 3, transmutation: 0, conjuration: -3, manipulation: -3, specialization: 1 }
      },
      {
        text: '直感は錯覚の可能性があるため、客観的データと論理的根拠を厳格に信じる',
        scores: { enhancement: -3, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: -1 }
      },
      {
        text: 'データが導く最もリスクの少ない安全なシナリオを論理的に選択する',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 39, // [放出, 具現化, 操作, 特質]
    phase: 3,
    category: '自己規律とマイルール',
    question: 'あなたが自分自身に課している「マイルール」やこだわりについて？',
    options: [
      {
        text: 'ルールで自分を縛るのは大嫌い！その時その時で一番気持ちいい行動をする',
        scores: { enhancement: 1, emission: 3, transmutation: 2, conjuration: -3, manipulation: -3, specialization: 0 }
      },
      {
        text: '「道具の手入れ」「時間の使い方」「整理整頓」など細かな儀式が多数ある',
        scores: { enhancement: -1, emission: -2, transmutation: -2, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '生活リズムや日課をルーティン化し、効率を最大化するシステムを守っている',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '他人には到底理解されないであろう、自分独自の美学や絶対禁忌がある',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 2, manipulation: 0, specialization: 3 }
      }
    ]
  },
  {
    id: 40, // [具現化, 操作, 特質, 強化]
    phase: 3,
    category: '他者の承認への執着',
    question: '「他人から認められたい、褒められたい」という承認欲求についてどう思う？',
    options: [
      {
        text: '承認欲求に振り回されるのは愚か。自分が納得できる完璧な成果を出せているかが全てだ',
        scores: { enhancement: 0, emission: -2, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 2 }
      },
      {
        text: '他人の承認なんて気まぐれなもの。相手をコントロールするためのツールにすぎない',
        scores: { enhancement: -3, emission: -2, transmutation: 2, conjuration: 0, manipulation: 3, specialization: 1 }
      },
      {
        text: '自分の価値は自分で決める。誰にも自分の本質を測ることはできない',
        scores: { enhancement: 0, emission: -2, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: 'みんなに認められたら素直に嬉しいし、もっと頑張ろうと力が湧いてくる',
        scores: { enhancement: 3, emission: 2, transmutation: -1, conjuration: 0, manipulation: 0, specialization: -2 }
      }
    ]
  },
  {
    id: 41, // [操作, 特質, 強化, 変化]
    phase: 3,
    category: '他者からの理解不能性',
    question: '「あなたって何を考えているか分からない」と言われたとき、どう思う？',
    options: [
      {
        text: '「自分の論理構成や説明が不十分だったか？」と伝え方の改善点を考える',
        scores: { enhancement: -1, emission: -1, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '「理解されなくて当然」と全く動じず、孤高の立ち位置を保つ',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「えっ、全部顔に出てると思ってたのに！」と本気で驚く',
        scores: { enhancement: 3, emission: 2, transmutation: -3, conjuration: -1, manipulation: -2, specialization: -2 }
      },
      {
        text: '「狙い通り」と心の中でニヤリと微笑み、さらに煙に巻く',
        scores: { enhancement: -2, emission: -1, transmutation: 3, conjuration: 0, manipulation: 1, specialization: 2 }
      }
    ]
  },
  {
    id: 42, // [特質, 強化, 変化, 放出]
    phase: 3,
    category: '怒りのエネルギー',
    question: '激しい怒りが湧き上がったとき、そのエネルギーはどう処理される？',
    options: [
      {
        text: '怒りを冷徹な思索へと昇華させ、相手の存在を自己の世界から完全に消去する',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 1, manipulation: 1, specialization: 3 }
      },
      {
        text: '身体を動かしたり筋トレをして、汗と一緒に熱いエネルギーを燃やし尽くす',
        scores: { enhancement: 3, emission: 1, transmutation: -1, conjuration: -1, manipulation: -1, specialization: -1 }
      },
      {
        text: '冗談めかした皮肉やチクリとした嫌味で小出しにして、相手を精神的に翻弄する',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: -1, manipulation: 1, specialization: 1 }
      },
      {
        text: '大声を出す、物に当たるなど、即座に身体の外へ大爆発させて発散する',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: -2, manipulation: -1, specialization: -2 }
      }
    ]
  },
  {
    id: 43, // [強化, 変化, 放出, 具現化]
    phase: 3,
    category: '孤独への耐性',
    question: '誰とも話さず一人きりで長期間過ごすことについて、どう感じる？',
    options: [
      {
        text: '仲間と会えないのは退屈。早くみんなで集まって何かしたい',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '気まぐれに誰かと遊んだり、急に一人になったり、その日の気分で切り替えたい',
        scores: { enhancement: 0, emission: 0, transmutation: 3, conjuration: -1, manipulation: -2, specialization: 1 }
      },
      {
        text: '寂しくて耐えられない！すぐに誰かに電話したりメッセージを送る',
        scores: { enhancement: 0, emission: 3, transmutation: -2, conjuration: -2, manipulation: -1, specialization: -3 }
      },
      {
        text: '一人の時間こそが至高。誰にも邪魔されず自分の世界・研究に没頭できて心地よい',
        scores: { enhancement: -2, emission: -3, transmutation: 1, conjuration: 3, manipulation: 1, specialization: 2 }
      }
    ]
  },
  {
    id: 44, // [変化, 放出, 具現化, 操作]
    phase: 3,
    category: '過去の失敗への態度',
    question: '過去にやらかしてしまった痛恨の失敗や黒歴史を思い出したとき？',
    options: [
      {
        text: '他人に面白おかしく話せる鉄板ネタや持ちギャグとして昇華している',
        scores: { enhancement: 0, emission: 1, transmutation: 3, conjuration: -1, manipulation: 0, specialization: 1 }
      },
      {
        text: '「あちゃー！」と叫んで頭を抱えるが、すぐ「まあ終わったことだ！」と豪快に笑い飛ばす',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -2, manipulation: -2, specialization: -1 }
      },
      {
        text: '思い出すたびに胃が痛くなり、何が原因だったのか何度も一人で反省・検証する',
        scores: { enhancement: -2, emission: -1, transmutation: -2, conjuration: 3, manipulation: 1, specialization: 0 }
      },
      {
        text: '二度と同じミスを起こさないよう、行動マニュアルを改訂してルール化する',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      }
    ]
  },
  {
    id: 45, // [放出, 具現化, 操作, 特質]
    phase: 3,
    category: '他者の才能への感情',
    question: '同年代で圧倒的な才能を発揮している天才を目の当たりにしたとき？',
    options: [
      {
        text: '「すげえやつがいる！」と興奮し、直接話しかけて仲良くなろうとする',
        scores: { enhancement: 1, emission: 3, transmutation: 0, conjuration: -1, manipulation: 0, specialization: -1 }
      },
      {
        text: 'その才能の緻密な技法や裏付けを徹底的に研究し、技術を自分にインストールする',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: 'その才能を自分のプロジェクトにどう活用・マネジメントできるか画策する',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '自分には自分の唯一無二の役割があるため、他人と自分を比較すること自体がない',
        scores: { enhancement: 0, emission: -2, transmutation: 0, conjuration: 0, manipulation: 0, specialization: 3 }
      }
    ]
  },

  // =========================================================================
  // Phase 4: 道徳ジレンマ・究極の選択・世界観 (Q46 〜 Q60)
  // =========================================================================
  {
    id: 46, // [具現化, 操作, 特質, 強化]
    phase: 4,
    category: '究極の救済ジレンマ',
    question: '沈みゆく船で救命ボートの定員が足りません。あなたならどう判断する？',
    options: [
      {
        text: 'ボート以外の浮力材を周囲の資材から即座に組み立て、全員助かる第3の道を模索する',
        scores: { enhancement: 1, emission: 0, transmutation: 1, conjuration: 3, manipulation: 1, specialization: 2 }
      },
      {
        text: '年齢や生存確率、能力などの客観的基準を定め、最も生存率が高まる合理的な選別を行う',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: 'この惨劇の意味を静かに見つめ、運命の導くままに自身の覚悟を決める',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '目の前の仲間や弱者を全員ボートに乗せ、自分は最後まで船に残って戦う',
        scores: { enhancement: 3, emission: 2, transmutation: -3, conjuration: 0, manipulation: -2, specialization: -1 }
      }
    ]
  },
  {
    id: 47, // [操作, 特質, 強化, 変化]
    phase: 4,
    category: '手段と目的の清濁',
    question: '大義ある目的を達成するためなら、多少の嘘や汚い手段を使うことは許される？',
    options: [
      {
        text: 'ルールや法に抵触しない範囲で、リスクとリターンを計算して合理的に判断する',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 2, manipulation: 3, specialization: 0 }
      },
      {
        text: '世間の善悪基準ではなく、「自分の魂や美学に背かないか」だけが唯一の判断基準だ',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '絶対に許されない。どんなに正当な目的でも、卑怯な手段を使ったら終わりだ',
        scores: { enhancement: 3, emission: 1, transmutation: -3, conjuration: 2, manipulation: -2, specialization: -2 }
      },
      {
        text: '勝てば官軍。目的が達成できるなら、使える手札は何でも使うのが当然だ',
        scores: { enhancement: -3, emission: -1, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 2 }
      }
    ]
  },
  {
    id: 48, // [特質, 強化, 変化, 放出]
    phase: 4,
    category: '人生最大の恐怖',
    question: 'あなたが人生において「最も恐ろしい」と感じる状態はどれ？',
    options: [
      {
        text: '自分の自由を奪われ、他人に思考や生き方を完全にコントロールされること',
        scores: { enhancement: 0, emission: 0, transmutation: 2, conjuration: 1, manipulation: 1, specialization: 3 }
      },
      {
        text: '自分の信念を曲げ、嘘と妥協にまみれて生きること',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 1, manipulation: -1, specialization: 1 }
      },
      {
        text: '退屈で何の刺激もなく、変化のない日常に閉じ込められること',
        scores: { enhancement: 0, emission: 1, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 2 }
      },
      {
        text: '誰とも心を通わせられず、仲間をすべて失って一人ぼっちになること',
        scores: { enhancement: 0, emission: 3, transmutation: -1, conjuration: 0, manipulation: -1, specialization: -3 }
      }
    ]
  },
  {
    id: 49, // [強化, 変化, 放出, 具現化]
    phase: 4,
    category: '裏切りへの報復',
    question: '最も深く信頼していた仲間に裏切られ、大損害を被ったとき、あなたが下す決断は？',
    options: [
      {
        text: '直接相手の前に立ち、「なぜ裏切った！」と拳を交えて真意を問い詰める',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: -1, manipulation: 0, specialization: -2 }
      },
      {
        text: '感情を表に出さず、何倍もの代償を相手が最も痛烈に感じる形で静かにやり返す',
        scores: { enhancement: -2, emission: -1, transmutation: 3, conjuration: 1, manipulation: 2, specialization: 2 }
      },
      {
        text: '「ふざけんな！」と激怒し、仲間を集めて相手を徹底的に糾弾する',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '相手が二度と立ち上がれないよう、法や制度の力を使って完璧に追い詰めて処罰する',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 1 }
      }
    ]
  },
  {
    id: 50, // [変化, 放出, 具現化, 操作]
    phase: 4,
    category: '真の強さの定義',
    question: 'あなたにとって「真に強い人間」とはどんな人物？',
    options: [
      {
        text: 'どんな状況にも柔軟に適応し、決して本心を掴ませずに生き残る機知に富んだ人間',
        scores: { enhancement: -2, emission: 0, transmutation: 3, conjuration: 0, manipulation: 1, specialization: 2 }
      },
      {
        text: '仲間を守るためなら命を投げ出し、どんな強敵にも恐れず立ち向かう情熱的な人間',
        scores: { enhancement: 2, emission: 3, transmutation: -2, conjuration: -1, manipulation: -2, specialization: -2 }
      },
      {
        text: '自らの感情を完全に律し、揺るぎない規律と完璧な技術を磨き上げた人間',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '感情に流されず、冷徹に大局を見極めてすべてをコントロールできる知性ある人間',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      }
    ]
  },
  {
    id: 51, // [放出, 具現化, 操作, 特質]
    phase: 4,
    category: '安全と自由の選択',
    question: '「退屈だが完全に安全で約束された生活」と「危険に満ちているが完全な自由」、選ぶなら？',
    options: [
      {
        text: '仲間とスリルを分かち合えるなら、危険でも刺激的な自由を選ぶ！',
        scores: { enhancement: 2, emission: 3, transmutation: 2, conjuration: -3, manipulation: -3, specialization: 1 }
      },
      {
        text: '「安全な生活」を強固に築き、その安全地帯の中で少しずつ自由を広げていく',
        scores: { enhancement: -2, emission: -2, transmutation: -2, conjuration: 3, manipulation: 2, specialization: -1 }
      },
      {
        text: '「安全」に見える場所のシステムを掌握し、自分がルールを作って自由に支配する',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 2 }
      },
      {
        text: '世の中の安全や自由という枠組み自体を超越した、自分だけの別の境地を目指す',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      }
    ]
  },
  {
    id: 52, // [具現化, 操作, 特質, 強化]
    phase: 4,
    category: '感情と理性の衝突',
    question: '「情義（大切な仲間への恩）」と「合理（全体の最大の利益）」が正面衝突したとき、下す決断は？',
    options: [
      {
        text: '感情と理性の双方の損失を最小限に抑える、極めて緻密な救済プロトコルを組む',
        scores: { enhancement: -1, emission: -1, transmutation: 0, conjuration: 3, manipulation: 2, specialization: 1 }
      },
      {
        text: '胸を痛めつつも「合理」を取る。感情に流されて全体を危機に晒すのは指導者失格だ',
        scores: { enhancement: -3, emission: -3, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: 'その選択によって自身が背負う業（カルマ）を受け止め、独自の覚悟で決断する',
        scores: { enhancement: 0, emission: -1, transmutation: 0, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '迷うことなく「情義」を取る！理屈のために仲間を見捨てるくらいなら破滅した方がマシだ',
        scores: { enhancement: 3, emission: 2, transmutation: -2, conjuration: -1, manipulation: -3, specialization: -2 }
      }
    ]
  },
  {
    id: 53, // [操作, 特質, 強化, 変化]
    phase: 4,
    category: '死ぬ直前の後悔',
    question: 'あなたが人生の最後に「これだけは後悔したくない」と思うことは？',
    options: [
      {
        text: '「自分の手で環境と秩序をコントロールしきれず、他人に振り回されたこと」',
        scores: { enhancement: -2, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '「他人の作った敷いたレールを歩み、自分だけの唯一無二の生を全うできなかったこと」',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 0, manipulation: 0, specialization: 3 }
      },
      {
        text: '「やりたいことに全力で挑戦せず、安全に逃げてしまったこと」',
        scores: { enhancement: 3, emission: 1, transmutation: 1, conjuration: -2, manipulation: -2, specialization: 1 }
      },
      {
        text: '「退屈な常識人として終わり、人生のスリルや面白さを味わい尽くせなかったこと」',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 2 }
      }
    ]
  },
  {
    id: 54, // [特質, 強化, 変化, 放出]
    phase: 4,
    category: '禁断の真実の独占',
    question: '世界の根幹に関わる重大な秘密（真実）を、あなた一人だけが知ってしまったら？',
    options: [
      {
        text: 'その真実の深淵を一人で静かに探求し、自身の精神の糧として生涯秘匿する',
        scores: { enhancement: -1, emission: -2, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '隠し事は嫌だ。信頼できる仲間全員にすぐに打ち明けて共有する',
        scores: { enhancement: 3, emission: 2, transmutation: -3, conjuration: -1, manipulation: -2, specialization: -2 }
      },
      {
        text: '誰にも言わず、その真実を利用して自分が一番面白く有利に生きるために活用する',
        scores: { enhancement: -3, emission: -2, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 2 }
      },
      {
        text: '「とんでもないことを知っちまった！」と仲間を呼んで大騒ぎする',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -2, manipulation: -2, specialization: -2 }
      }
    ]
  },
  {
    id: 55, // [強化, 変化, 放出, 具現化]
    phase: 4,
    category: '人生というゲーム',
    question: 'もし人生を一言のゲームジャンルで表すなら、あなたにとって何が一番しっくりくる？',
    options: [
      {
        text: '【アクション・格闘】自分の身体と魂を限界までぶつけ合って勝利するゲーム',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: -2, manipulation: -2, specialization: -1 }
      },
      {
        text: '【心理戦・トランプ】ブラフと駆け引きで相手の裏をかき、スリルを味わうゲーム',
        scores: { enhancement: -2, emission: 0, transmutation: 3, conjuration: -1, manipulation: 1, specialization: 1 }
      },
      {
        text: '【マルチプレイ・協力バトル】仲間と力を合わせてド派手な大技でボスを倒すゲーム',
        scores: { enhancement: 1, emission: 3, transmutation: -1, conjuration: -1, manipulation: -1, specialization: -2 }
      },
      {
        text: '【クラフト・収集】自らの手で完璧な装備や世界を作り上げていくゲーム',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 3, manipulation: 1, specialization: 2 }
      }
    ]
  },
  {
    id: 56, // [変化, 放出, 具現化, 操作]
    phase: 4,
    category: '赦しの条件',
    question: '一度裏切った相手を、あなたが「心からもう一度許す」ための絶対条件は？',
    options: [
      {
        text: '許したフリをしておく方が、今後の展開で自分にメリットがあると判断したとき',
        scores: { enhancement: -3, emission: -2, transmutation: 3, conjuration: 0, manipulation: 2, specialization: 1 }
      },
      {
        text: '相手が心底から頭を下げて謝罪し、誠意ある涙や行動を見せてくれたとき',
        scores: { enhancement: 2, emission: 3, transmutation: -2, conjuration: -1, manipulation: -2, specialization: -2 }
      },
      {
        text: '裏切りによる損害が金銭や数字で完全に補填され、再発防止の誓約が交わされたとき',
        scores: { enhancement: -2, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 0 }
      },
      {
        text: '相手が二度と裏切れないよう、完全にこちらが弱みや主導権を握ったとき',
        scores: { enhancement: -2, emission: -2, transmutation: 1, conjuration: 1, manipulation: 3, specialization: 1 }
      }
    ]
  },
  {
    id: 57, // [放出, 具現化, 操作, 特質]
    phase: 4,
    category: '存在の痕跡',
    question: 'あなたがこの世界に最後に遺したい「自分の生きた証」とは？',
    options: [
      {
        text: '仲間たちの心の中に刻まれた「あいつは最高に熱くて頼れるやつだった」という記憶',
        scores: { enhancement: 2, emission: 3, transmutation: -2, conjuration: 0, manipulation: -1, specialization: -2 }
      },
      {
        text: '自分が心血を注いで完成させた、完璧で不朽の作品やシステム・道具',
        scores: { enhancement: -1, emission: -2, transmutation: -1, conjuration: 3, manipulation: 2, specialization: 2 }
      },
      {
        text: '自分が創り上げた強固な組織や仕組みが、後世まで自律して稼働し続けること',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 1 }
      },
      {
        text: '時代や歴史の流れそのものを塗り替えるような、圧倒的な思想やパラダイムシフト',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 1, manipulation: 1, specialization: 3 }
      }
    ]
  },
  {
    id: 58, // [具現化, 操作, 特質, 強化]
    phase: 4,
    category: '孤独の本質',
    question: 'あなたにとって「孤独」とはどのようなもの？',
    options: [
      {
        text: '誰にも邪魔されず、自分の精神と技を最も純粋に研ぎ澄ますことができる神聖な領域',
        scores: { enhancement: -1, emission: -3, transmutation: 1, conjuration: 3, manipulation: 1, specialization: 2 }
      },
      {
        text: '自分の領域を整え、次なる戦略や計画を緻密に組み立てるための作戦室',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 1, manipulation: 3, specialization: 0 }
      },
      {
        text: '自己の深淵と宇宙の真理を探求するための、かけがえのない思索の時',
        scores: { enhancement: -2, emission: -3, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '一人は寂しいけれど、自分を鍛え直すための試練の場',
        scores: { enhancement: 3, emission: 1, transmutation: -2, conjuration: 1, manipulation: 0, specialization: -1 }
      }
    ]
  },
  {
    id: 59, // [操作, 特質, 強化, 変化]
    phase: 4,
    category: '直面する運命への覚悟',
    question: '誰も助けてくれない、逃げ場のない絶体絶命の危機に一人で追い詰められたら？',
    options: [
      {
        text: '手持ちの全リソースと制約を極限まで計算し、0.1%の生還ルートを緻密に実行する',
        scores: { enhancement: -1, emission: -2, transmutation: 0, conjuration: 2, manipulation: 3, specialization: 1 }
      },
      {
        text: '恐怖を完全に遮断し、自身の宿命を達観しながら研ぎ澄まされた未知の力を解放する',
        scores: { enhancement: 0, emission: -1, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '「死なば諸共！」と全オーラと気力を絞り出し、最後の1滴まで真っ向勝負する',
        scores: { enhancement: 3, emission: 2, transmutation: -1, conjuration: -1, manipulation: -2, specialization: 0 }
      },
      {
        text: '敵の油断を誘う命懸けのハッタリや嘘を仕掛け、一瞬の隙を突いて脱出・逆転する',
        scores: { enhancement: -2, emission: -1, transmutation: 3, conjuration: 0, manipulation: 1, specialization: 2 }
      }
    ]
  },
  {
    id: 60, // [特質, 強化, 変化, 放出]
    phase: 4,
    category: '魂のコアバリュー',
    question: 'あなたが人生で最も誇りに思える「自分自身のあり方」は？',
    options: [
      {
        text: '唯一無二の孤高の存在として、自分だけの特別な真理とカリスマを体現すること',
        scores: { enhancement: -1, emission: -1, transmutation: 1, conjuration: 1, manipulation: 0, specialization: 3 }
      },
      {
        text: '何があっても自分を偽らず、嘘をつかずに真っ直ぐ生き抜くこと',
        scores: { enhancement: 3, emission: 1, transmutation: -3, conjuration: 1, manipulation: -2, specialization: -1 }
      },
      {
        text: '誰の敷いたルールにも縛られず、自由奔放に人生を遊び尽くすこと',
        scores: { enhancement: -1, emission: 0, transmutation: 3, conjuration: -2, manipulation: -2, specialization: 2 }
      },
      {
        text: '仲間や愛する人のために熱い情熱を燃やし、決して見捨てずに守り抜くこと',
        scores: { enhancement: 1, emission: 3, transmutation: -2, conjuration: 0, manipulation: -1, specialization: -2 }
      }
    ]
  }
];
