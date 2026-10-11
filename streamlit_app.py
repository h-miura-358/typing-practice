import json
import random
import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="ローマ字タイピング ＆ 苦手克服トレーニング",
    page_icon="⌨️",
    layout="centered",
)


# -------------------------------------------------------------------------
# 💡 ローマ字変換ロジック
# -------------------------------------------------------------------------
def convert_to_romaji(hira_text):
  mapping = {
      "あ": "a",
      "い": "i",
      "う": "u",
      "え": "e",
      "お": "o",
      "か": "ka",
      "き": "ki",
      "く": "ku",
      "け": "ke",
      "こ": "ko",
      "さ": "sa",
      "し": "si",
      "す": "su",
      "せ": "se",
      "そ": "so",
      "た": "ta",
      "ち": "ti",
      "つ": "tu",
      "て": "te",
      "と": "to",
      "な": "na",
      "に": "ni",
      "ぬ": "nu",
      "ね": "ne",
      "の": "no",
      "は": "ha",
      "ひ": "hi",
      "ふ": "hu",
      "へ": "he",
      "ほ": "ho",
      "ま": "ma",
      "み": "mi",
      "む": "mu",
      "め": "me",
      "も": "mo",
      "や": "ya",
      "ゆ": "yu",
      "よ": "yo",
      "ら": "ra",
      "り": "ri",
      "る": "ru",
      "れ": "re",
      "ろ": "ro",
      "わ": "wa",
      "を": "wo",
      "ん": "n",
      "が": "ga",
      "ぎ": "gi",
      "ぐ": "gu",
      "げ": "ge",
      "ご": "go",
      "ざ": "za",
      "じ": "zi",
      "ず": "zu",
      "ぜ": "ze",
      "ぞ": "zo",
      "だ": "da",
      "ぢ": "di",
      "づ": "du",
      "で": "de",
      "ど": "do",
      "ば": "ba",
      "び": "bi",
      "ぶ": "bu",
      "べ": "be",
      "ぼ": "bo",
      "ぱ": "pa",
      "ぴ": "pi",
      "ぷ": "pu",
      "ぺ": "pe",
      "ぽ": "po",
      "ー": "-",
  }

  compounds = {
      "きゃ": "kya",
      "きゅ": "kyu",
      "きょ": "kyo",
      "しゃ": "sya",
      "しゅ": "syu",
      "しょ": "syo",
      "ちゃ": "tya",
      "ちゅ": "tyu",
      "ちょ": "tyo",
      "てぃ": "thi",
      "でぃ": "dhi",
      "とぅ": "twu",
      "どぅ": "dwu",
      "にゃ": "nya",
      "にゅ": "nyu",
      "にょ": "nyo",
      "ひゃ": "hya",
      "ひゅ": "hyu",
      "ひょ": "hyo",
      "みゃ": "mya",
      "みゅ": "myu",
      "みょ": "myo",
      "りゃ": "rya",
      "りゅ": "ryu",
      "りょ": "ryo",
      "ぎゃ": "gya",
      "ぎゅ": "gyu",
      "ぎょ": "gyo",
      "じゃ": "zya",
      "じゅ": "zyu",
      "じょ": "zyo",
      "びゃ": "bya",
      "びゅ": "byu",
      "びょ": "byo",
      "ぴゃ": "pya",
      "ぴゅ": "pyu",
      "ぴょ": "pyo",
  }

  res = ""
  i = 0
  n = len(hira_text)
  while i < n:
    if i + 1 < n and hira_text[i : i + 2] in compounds:
      res += compounds[hira_text[i : i + 2]]
      i += 2
    elif hira_text[i] == "っ" and i + 1 < n:
      next_char = hira_text[i + 1]
      sub_conv = mapping.get(next_char, "")
      if sub_conv:
        res += sub_conv[0]
      i += 1
    elif hira_text[i] in mapping:
      res += mapping[hira_text[i]]
      i += 1
    else:
      res += hira_text[i]
      i += 1
  return res


# 通常の練習用ワードリスト
WORD_LIST = [
    "あいさつ",
    "きまり",
    "てがみ",
    "ことば",
    "ねっと",
    "じかん",
    "れきし",
    "ありがとう",
    "おつかれ",
    "よろしく",
    "しゅくだい",
    "としょかん",
    "でんしゃ",
    "きょかしょ",
    "こくばん",
    "てすと",
    "じっけん",
    "けんさく",
    "ろぐいん",
    "おはよう",
    "すみません",
    "しつれい",
    "じかんわり",
    "うんどうかい",
    "ぱすわーど",
    "せきゅりてぃ",
    "すまーとふぉん",
    "あるごりずむ",
    "ねっとわーく",
    "よろしくね",
    "ぶんかさい",
    "つうちひょう",
    "ぷろぐらみんぐ",
    "おかいけい",
    "しょうみきげん",
]
WORD_LIST = [w for w in list(set(WORD_LIST)) if 3 <= len(w) <= 6]

# セッション初期化（間違いの記録用）
if "error_logs" not in st.session_state:
  st.session_state.error_logs = ["しゅくだい", "しつれい", "せきゅりてぃ"]

st.title("⌨️ ローマ字タイピングトレーニング")
st.caption("標準的なローマ字入力によるタイピング実践および復習アプリです。")

tab1, tab2 = st.tabs(["🎯 通常トレーニング", "🔁 苦手克服モード"])

# -------------------------------------------------------------------------
# タブ1: 通常トレーニング
# -------------------------------------------------------------------------
with tab1:
  st.subheader("🎯 タイピング実践")
  words_with_romaji = [
      {"jp": w, "romaji": convert_to_romaji(w)} for w in WORD_LIST
  ]
  words_json = json.dumps(words_with_romaji, ensure_ascii=False)

  html_code = f"""
    <div style="font-family: sans-serif; padding: 10px; max-width: 600px; margin: auto;">
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: #e8f4fd; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; color: #555; margin-bottom: 5px;">出題（ひらがな）</div>
                <div id="jp-display" style="font-size: 26px; font-weight: bold; color: #004085;">-</div>
            </div>
            <div style="flex: 1; background: #e2fcd6; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; color: #555; margin-bottom: 5px;">ローマ字表記</div>
                <div id="romaji-display" style="font-size: 22px; font-weight: bold; color: #155724; font-family: monospace;">-</div>
            </div>
        </div>

        <div style="margin-bottom: 10px;">
            <input type="text" id="typing-input" placeholder="ここに入力..." 
                style="width: 100%; padding: 14px; font-size: 20px; border: 2px solid #ccc; border-radius: 6px; box-sizing: border-box; outline: none;"
                autocomplete="off" autocapitalize="off" spellcheck="false">
        </div>

        <div id="feedback" style="font-size: 16px; font-weight: bold; height: 25px; margin-bottom: 10px;"></div>

        <div style="display: flex; justify-content: space-around; background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">
            <div>クリア回数: <span id="success-cnt" style="font-weight: bold; color: #007bff;">0</span> 回</div>
            <div>ミス回数: <span id="mistake-cnt" style="font-weight: bold; color: #dc3545;">0</span> 回</div>
        </div>
    </div>

    <script>
        const wordList = {words_json};
        let currentItem = wordList[Math.floor(Math.random() * wordList.length)];
        
        let successCount = 0;
        let mistakeCount = 0;

        const jpDisplay = document.getElementById('jp-display');
        const romajiDisplay = document.getElementById('romaji-display');
        const typingInput = document.getElementById('typing-input');
        const feedback = document.getElementById('feedback');
        const successCntEl = document.getElementById('success-cnt');
        const mistakeCntEl = document.getElementById('mistake-cnt');

        function updateScreen() {
            jpDisplay.innerText = currentItem.jp;
            romajiDisplay.innerText = currentItem.romaji;
            typingInput.value = '';
        }

        updateScreen();
        typingInput.focus();

        window.addEventListener('focus', () => typingInput.focus());
        document.addEventListener('click', () => typingInput.focus());

        typingInput.addEventListener('input', (e) => {
            const val = typingInput.value;
            
            if (currentItem.romaji === val) {
                successCount++;
                successCntEl.innerText = successCount;
                feedback.style.color = '#28a745';
                feedback.innerText = '✅ 正解！次の問題へ進みます';
                
                let nextItem;
                do {
                    nextItem = wordList[Math.floor(Math.random() * wordList.length)];
                } while (nextItem.jp === currentItem.jp && wordList.length > 1);
                
                currentItem = nextItem;
                setTimeout(() => {
                    feedback.innerText = '';
                    updateScreen();
                }, 400);

            } else if (currentItem.romaji.startsWith(val)) {
                feedback.style.color = '#17a2b8';
                feedback.innerText = '✅ 順調です';
            } else {
                mistakeCount++;
                mistakeCntEl.innerText = mistakeCount;
                feedback.style.color = '#dc3545';
                feedback.innerText = '⚠️ 入力ミスです。確認してください';
                typingInput.value = '';
            }
        });

        setInterval(() => {
            if (document.activeElement !== typingInput) {
                typingInput.focus();
            }
        }, 200);
    </script>
    """

  components.html(html_code, height=300)

# -------------------------------------------------------------------------
# タブ2: 苦手克服モード
# -------------------------------------------------------------------------
with tab2:
  st.subheader("🔁 苦手克服モード（ミスした単語の集中特訓）")
  st.write("これまでのトレーニングで誤答した単語に絞って演習を行います。")

  if not st.session_state.error_logs:
    st.success("🎉 現在、記録されたミスのデータはありません。")
  else:
    st.info(f"対象ワード: {', '.join(st.session_state.error_logs)}")

    error_words_with_romaji = [
        {"jp": w, "romaji": convert_to_romaji(w)}
        for w in st.session_state.error_logs
    ]
    error_words_json = json.dumps(error_words_with_romaji, ensure_ascii=False)

    review_html_code = f"""
        <div style="font-family: sans-serif; padding: 10px; max-width: 600px; margin: auto;">
            <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                <div style="flex: 1; background: #fff3cd; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; color: #555; margin-bottom: 5px;">復習出題（ひらがな）</div>
                    <div id="rev-jp-display" style="font-size: 26px; font-weight: bold; color: #856404;">-</div>
                </div>
                <div style="flex: 1; background: #d4edda; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; color: #555; margin-bottom: 5px;">ローマ字表記</div>
                    <div id="rev-romaji-display" style="font-size: 22px; font-weight: bold; color: #155724; font-family: monospace;">-</div>
                </div>
            </div>

            <div style="margin-bottom: 10px;">
                <input type="text" id="rev-typing-input" placeholder="ここに入力..." 
                    style="width: 100%; padding: 14px; font-size: 20px; border: 2px solid #ccc; border-radius: 6px; box-sizing: border-box; outline: none;"
                    autocomplete="off" autocapitalize="off" spellcheck="false">
            </div>

            <div id="rev-feedback" style="font-size: 16px; font-weight: bold; height: 25px; margin-bottom: 10px;"></div>

            <div style="display: flex; justify-content: space-around; background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center;">
                <div>クリア回数: <span id="rev-success-cnt" style="font-weight: bold; color: #28a745;">0</span> 回</div>
                <div>ミス回数: <span id="rev-mistake-cnt" style="font-weight: bold; color: #dc3545;">0</span> 回</div>
            </div>
        </div>

        <script>
            const errorWordList = {error_words_json};
            let revCurrentItem = errorWordList[Math.floor(Math.random() * errorWordList.length)];
            
            let revSuccessCount = 0;
            let revMistakeCount = 0;

            const revJpDisplay = document.getElementById('rev-jp-display');
            const revRomajiDisplay = document.getElementById('rev-romaji-display');
            const revTypingInput = document.getElementById('rev-typing-input');
            const revFeedback = document.getElementById('rev-feedback');
            const revSuccessCntEl = document.getElementById('rev-success-cnt');
            const revMistakeCntEl = document.getElementById('rev-mistake-cnt');

            function updateRevScreen() {
                revJpDisplay.innerText = revCurrentItem.jp;
                revRomajiDisplay.innerText = revCurrentItem.romaji;
                revTypingInput.value = '';
            }

            updateRevScreen();
            revTypingInput.focus();

            window.addEventListener('focus', () => revTypingInput.focus());
            document.addEventListener('click', () => revTypingInput.focus());

            revTypingInput.addEventListener('input', (e) => {
                const val = revTypingInput.value;
                
                if (revCurrentItem.romaji === val) {
                    revSuccessCount++;
                    revSuccessCntEl.innerText = revSuccessCount;
                    revFeedback.style.color = '#28a745';
                    revFeedback.innerText = '✅ 正解です';
                    
                    let nextItem;
                    do {
                        nextItem = errorWordList[Math.floor(Math.random() * errorWordList.length)];
                    } while (nextItem.jp === revCurrentItem.jp && errorWordList.length > 1);
                    
                    revCurrentItem = nextItem;
                    setTimeout(() => {
                        revFeedback.innerText = '';
                        updateRevScreen();
                    }, 400);

                } else if (revCurrentItem.romaji.startsWith(val)) {
                    revFeedback.style.color = '#17a2b8';
                    revFeedback.innerText = '✅ 順調です';
                } else {
                    revMistakeCount++;
                    revMistakeCntEl.innerText = revMistakeCount;
                    revFeedback.style.color = '#dc3545';
                    revFeedback.innerText = '⚠️ 入力ミスです。確認してください';
                    revTypingInput.value = '';
                }
            });

            setInterval(() => {
                if (document.activeElement !== revTypingInput) {
                    revTypingInput.focus();
                }
            }, 200);
        </script>
        """

    components.html(review_html_code, height=300)

    if st.button("🧹 ミス記録をリセット"):
      st.session_state.error_logs = []
      st.rerun()
