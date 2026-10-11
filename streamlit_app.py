import json
import random
import google.generativeai as genai
import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="小学校ローマ字タイピング ＆ AI分析", page_icon="⌨️", layout="centered"
)


# -------------------------------------------------------------------------
# 💡 小学校の教科書に合わせたローマ字に変換する関数
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

# セッション初期化
if "error_logs" not in st.session_state:
  st.session_state.error_logs = [
      {
          "jp_word": "しゅくだい",
          "target_romaji": "syukudai",
          "typed_wrong": "sukudai",
      }
  ]

st.title("⌨️ 小学校のローマ字タイピング ＆ AI分析")
st.caption(
    "小学校の教科書に合わせたローマ字表記（si, ti, tu, hu, zi 等）で練習できます。"
)

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI詳細分析・特訓"])

with tab1:
  words_with_romaji = [
      {"jp": w, "romaji": convert_to_romaji(w)} for w in WORD_LIST
  ]
  words_json = json.dumps(words_with_romaji, ensure_ascii=False)

  html_code = (
      """
    <div style="font-family: sans-serif; padding: 10px; max-width: 600px; margin: auto;">
        <div style="display: flex; gap: 20px; margin-bottom: 15px;">
            <div style="flex: 1; background: #e8f4fd; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; color: #555; margin-bottom: 5px;">お題（ひらがな）</div>
                <div id="jp-display" style="font-size: 26px; font-weight: bold; color: #004085;">-</div>
            </div>
            <div style="flex: 1; background: #e2fcd6; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 12px; color: #555; margin-bottom: 5px;">教科書通りのローマ字</div>
                <div id="romaji-display" style="font-size: 22px; font-weight: bold; color: #155724; font-family: monospace;">-</div>
            </div>
        </div>

        <div style="margin-bottom: 10px;">
            <input type="text" id="typing-input" placeholder="ここに入力してね..." 
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
        const wordList = """
      + words_json
      + """;
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
                feedback.innerText = '✅ 正解！次の問題へ進みます！';
                
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
                feedback.innerText = '✅ 順調です！';
            } else {
                mistakeCount++;
                mistakeCntEl.innerText = mistakeCount;
                feedback.style.color = '#dc3545';
                feedback.innerText = '⚠️ 入力ミスです！もう一度確認してね';
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
  )

  components.html(html_code, height=300)

with tab2:
  st.subheader("🤖 Geminiによる苦手分析＆特訓メニュー作成")
  st.write(
      "これまでのタイピングの誤りデータを基に、Geminiが個別の苦手分野を自動分析します。"
  )

  # st.secrets から Gemini APIキーを取得
  gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")

  if not gemini_api_key:
    st.warning(
        "⚠️ GEMINI_API_KEY が設定されていません。StreamlitのSecretsに"
        " `GEMINI_API_KEY` を登録してください。"
    )
  else:
    if st.button("🚀 Geminiに苦手を分析してもらう"):
      try:
        client = genai.Client(api_key=gemini_api_key)
        with st.spinner("Geminiがエラーログを解析し、特訓メニューを作成中..."):
          prompt = f"""
                    あなたは小学校の親しみやすいタイピング指導のAIコーチです。
                    以下の児童のローマ字タイピングにおける誤りデータを分析し、
                    1. 児童がどのような傾向で間違えているかをやさしく解説してください。
                    2. その苦手克服に向けた具体的な特訓アドバイスや練習問題の提案を出力してください。

                    誤りデータ:
                    {json.dumps(st.session_state.error_logs, ensure_ascii=False)}
                    """

          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=prompt,
          )

          ai_report = response.text
          st.markdown("---")
          st.markdown("### 💬 Geminiコーチからの詳細診断レポート")
          st.write(ai_report)

      except Exception as e:
        st.error(f"APIの呼び出し中にエラーが発生しました: {e}")
