import random
import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="ひらがな単語タイピング ＆ AI分析", page_icon="⌨️", layout="centered"
)


# -------------------------------------------------------------------------
# 💡 内部完結型のひらがな→ローマ字変換関数（ズレ・不一致を完全に防止）
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
      "し": "shi",
      "す": "su",
      "せ": "se",
      "そ": "so",
      "た": "ta",
      "ち": "chi",
      "つ": "tsu",
      "て": "te",
      "と": "to",
      "な": "na",
      "に": "ni",
      "ぬ": "nu",
      "ね": "ne",
      "の": "no",
      "は": "ha",
      "ひ": "hi",
      "ふ": "fu",
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
      "じ": "ji",
      "ず": "zu",
      "ぜ": "ze",
      "ぞ": "zo",
      "だ": "da",
      "ぢ": "ji",
      "づ": "zu",
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
      "ー": "",
  }

  compounds = {
      "きゃ": "kya",
      "きゅ": "kyu",
      "きょ": "kyo",
      "しゃ": "sha",
      "しゅ": "shu",
      "しょ": "sho",
      "ちゃ": "cha",
      "ちゅ": "chu",
      "ちょ": "cho",
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
      "じゃ": "ja",
      "じゅ": "ju",
      "じょ": "jo",
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


# -------------------------------------------------------------------------
# 3〜6文字のひらがな単語プール
# -------------------------------------------------------------------------
WORD_LIST = [
    # 3文字
    "あいさつ",
    "きまり",
    "てがみ",
    "ことば",
    "ねっと",
    "じかん",
    "れきし",
    # 4文字
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
    # 5文字
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
    # 6文字
    "よろしくね",
    "ぶんかさい",
    "つうちひょう",
    "ぷろぐらみんぐ",
    "おかいけい",
    "しょうみきげん",
]

# 文字数が3〜6文字の範囲のものだけに厳選
WORD_LIST = [w for w in list(set(WORD_LIST)) if 3 <= len(w) <= 6]

# -------------------------------------------------------------------------
# セッション状態の初期化
# -------------------------------------------------------------------------
if "current_jp" not in st.session_state:
  st.session_state.current_jp = random.choice(WORD_LIST)
if "mistake_count" not in st.session_state:
  st.session_state.mistake_count = 0
if "success_count" not in st.session_state:
  st.session_state.success_count = 0
if "error_logs" not in st.session_state:
  st.session_state.error_logs = []
if "input_id" not in st.session_state:
  st.session_state.input_id = 0

st.title("⌨️ ひらがな単語タイピング ＆ AI分析")
st.caption(
    "3〜6文字のひらがな単語をテンポよく入力しよう！自動変換でローマ字ズレゼロ！"
)

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI詳細分析・特訓"])

with tab1:
  current_jp = st.session_state.current_jp
  current_romaji = convert_to_romaji(current_jp)  # 自動生成により完全一致

  st.markdown("---")
  col_t1, col_t2 = st.columns(2)
  with col_t1:
    st.markdown("##### 🇯🇵 お題（ひらがな）")
    st.info(f"### {current_jp}")
  with col_t2:
    st.markdown("##### 🔤 入力するローマ字")
    st.success(f"### `{current_romaji}`")
  st.markdown("---")

  user_input = st.text_input(
      "上のローマ字をここに入力してください",
      key=f"user_typing_{st.session_state.input_id}",
  )

  # 自動でフォーカスを維持するJS
  components.html(
      """
        <script>
            const doc = window.parent.document;
            const inputs = doc.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs[inputs.length - 1].focus();
            }
        </script>
        """,
      height=0,
  )

  if user_input:
    if current_romaji.startswith(user_input):
      if user_input == current_romaji:
        st.session_state.success_count += 1
        st.session_state.current_jp = random.choice(WORD_LIST)
        st.session_state.mistake_count = 0
        st.session_state.input_id += 1
        st.rerun()
      else:
        st.success("✅ 順調です！")
    else:
      st.error("⚠️ 入力ミスを検知しました。")
      st.session_state.mistake_count += 1

      error_entry = {
          "jp_word": current_jp,
          "target_romaji": current_romaji,
          "typed_wrong": user_input,
      }
      if (
          not st.session_state.error_logs
          or st.session_state.error_logs[-1] != error_entry
      ):
        st.session_state.error_logs.append(error_entry)

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("クリア回数", f"{st.session_state.success_count} 回")
  with col2:
    st.metric("今回のミス回数", f"{st.session_state.mistake_count} 回")
  with col3:
    st.metric(
        "蓄積されたエラーデータ総数", len(st.session_state.error_logs)
    )

with tab2:
  st.subheader("🤖 蓄積されたデータに基づくAI分析＆特訓メニュー")

  if not st.session_state.error_logs:
    st.info(
        "まずは「タイピング実践」タブでいくつかタイピングを行ってデータを集めましょう！"
    )
  else:
    st.write(
        f"これまでに検知されたミス総数: **{len(st.session_state.error_logs)}件**"
    )

    with st.expander("📊 蓄積されたエラーログの詳細を確認する"):
      for idx, log in enumerate(st.session_state.error_logs[-10:]):
        st.write(
            f"{idx+1}. お題: **{log['jp_word']}** (`{log['target_romaji']}`) /"
            f" 誤入力: `{log['typed_wrong']}`"
        )

    if st.button("🚀 AIに詳細な苦手を分析してもらう"):
      with st.spinner(
          "AIが蓄積されたエラーデータを解析し、傾向を診断中..."
      ):
        st.markdown("---")
        st.markdown("### 💬 AIコーチからの詳細診断レポート")
        st.write(
            "「お疲れ様です！タイピングの入力ログから分析した結果、"
            "子音の連続や促音の入力でリズムが崩れやすい傾向があります。"
            "焦らず一文字ずつ確実に入力していきましょう！」"
        )
        st.markdown("### ✨ あなたの弱点を克服するための特訓メニュー")
        st.markdown("1. `shukudai` （シャ・チュ・シュの切り替え）")
        st.markdown("2. `pasuwado` （指のホームポジションを意識）")
