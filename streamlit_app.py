import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="小学校ローマ字タイピング", page_icon="⌨️", layout="centered"
)


# -------------------------------------------------------------------------
# 💡 小学校の教科書で習うローマ字（訓令式ベース）に変換する関数
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
      "し": "si",  # 訓令式（小学校教科書）
      "す": "su",
      "せ": "se",
      "そ": "so",
      "た": "ta",
      "ち": "ti",  # 訓令式
      "つ": "tu",  # 訓令式
      "て": "te",
      "と": "to",
      "な": "na",
      "に": "ni",
      "ぬ": "nu",
      "ね": "ne",
      "の": "no",
      "は": "ha",
      "ひ": "hi",
      "ふ": "hu",  # 訓令式
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
      "じ": "zi",  # 訓令式
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
      "ー": "",
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


# -------------------------------------------------------------------------
# 3〜6文字のひらがな単語プール
# -------------------------------------------------------------------------
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

# タイトル表示
st.title("⌨️ 小学校のローマ字タイピング")
st.caption(
    "小学校の教科書に合わせたローマ字表記（si, ti, tu, hu, zi 等）で練習できます。"
)

tab1
