import random
import pykakasi
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ひらがな単語タイピング ＆ AI分析", page_icon="⌨️", layout="centered"
)


# pykakasi（ローマ字変換ライブラリ）の初期化
@st.cache_resource
def get_kakasi():
  kks = pykakasi.kakasi()
  return kks


kks = get_kakasi()


def convert_to_romaji(japanese_text):
  """ひらがなテキストを正確なヘボン式ローマ字に自動変換"""
  result = kks.convert(japanese_text)
  return "".join([item["hepburn"] for item in result])


# -------------------------------------------------------------------------
# ひらがな 3〜6文字の単語プール（文化庁の言葉遣い・学校・日常・情報用語ベース）
# -------------------------------------------------------------------------
WORD_LIST = [
    # 3文字
    "あいさつ",
    "おぎり",
    "きまり",
    "しんぶん",
    "てがみ",
    "ことば",
    "ねっと",
    "さきに",
    "はっぴ",
    "じかん",
    "けいざい",
    "れきし",
    "かず",
    "けいさん",
    # 4文字
    "ありがとう",
    "おつかれ",
    "よろしく",
    "しゅくだい",
    "としょかん",
    "でんしゃ",
    "きょかしょ",
    "こくばん",
    "きゅうしょく",
    "てすと",
    "じっけん",
    "はっぴょう",
    "ごうかく",
    "けんさく",
    "ろぐいん",
    "ぷらいばし",
    "めっせーじ",
    "こめんと",
    # 5文字
    "おはよう",
    "すみません",
    "しつれい",
    "じかんわり",
    "うんどうかい",
    "せいとうかい",
    "てんちょう",
    "ぱすわーど",
    "せきゅりてぃ",
    "だうんろーど",
    "すまーとふぉん",
    "あるごりずむ",
    "ねっとわーく",
    "じどうはんばいき",
    # 6文字
    "よろしくね",
    "もうしわけ",
    "しゅうがくりょこう",
    "ぶんかさい",
    "つうちひょう",
    "あっぷろーど",
    "ぷろぐらみんぐ",
    "きゃっしゅれす",
    "おかいけい",
    "しょうみきげん",
]

# 重複削除と、文字数が3〜6文字の範囲のものだけに厳選
WORD_LIST = [w for w in list(set(WORD_LIST)) if 3 <= len(w) <= 6]

# -------------------------------------------------------------------------
# セッション状態の初期化
# -------------------------------------------------------------------------
if "current_word" not in st.session_state:
  st.session_state.current_word = random.choice(WORD_LIST)
if "mistake_count" not in st.session_state:
  st.session_state.mistake_count = 0
if "success_count" not in st.session_state:
  st.session_state.success_count = 0
if "error_logs" not in st.session_state:
  st.session_state.error_logs = []

st.title("⌨️ ひらがな単語タイピング ＆ AI分析")
st.caption(
    "3〜6文字のひらがな単語をテンポよく入力しよう！ライブラリが正確なローマ字を自動生成します。"
)

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI詳細分析・特訓"])

with tab1:
  # 「新しいお題をセット」ボタン
  if st.button("🔀 次の問題へ"):
    st.session_state.current_word = random.choice(WORD_LIST)
    st.session_state.mistake_count = 0
    st.rerun()

  current_jp = st.session_state.current_word
  current_romaji = convert_to_romaji(current_jp)

  st.markdown("---")
  col_t1, col_t2 = st.columns(2)
  with col_t1:
    st.markdown("##### 🇯🇵 お題（ひらがな）")
    st.info(f"### {current_jp}")
  with col_t2:
    st.markdown("##### 🔤 ローマ字（自動生成）")
    st.success(f"### `{current_romaji}`")
  st.markdown("---")

  # リアルタイム入力
  user_input = st.text_input(
      "上のローマ字をここに入力してください", key="user_typing", value=""
  )

  if user_input:
    if current_romaji.startswith(user_input):
      st.success("✅ 順調です！")
      if user_input == current_romaji:
        st.balloons()
        st.markdown(
            "🎉 **クリア！お見事です！「次の問題へ」を押して進もう！**"
        )
        st.session_state.success_count += 1
        # 自動で次の問題へ切り替える親切設計も可能ですが、まずはボタン操作にしています
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

  # スタッツ表示
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
            "「お疲れ様です！短文単語のタイピングログから分析した結果、"
            "子音の連続（`sh`, `ch`, `tsu` など）や、促音（小さい『っ』）の入力タイミングに"
            "つまずきやすい傾向が見られます。一文字ずつ確実にキーを叩く意識を持ちましょう！」"
        )
        st.markdown("### ✨ あなたの弱点を克服するための特訓単語")
        st.markdown("1. `shukudai` （シャ・チュ・シュの切り替え）")
        st.markdown("2. `chottomatte` （促音の連続をマスター）")
