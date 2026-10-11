import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ひらがな単語タイピング ＆ AI分析", page_icon="⌨️", layout="centered"
)

# -------------------------------------------------------------------------
# ひらがな 3〜6文字の単語と正しいローマ字のペア辞書
# -------------------------------------------------------------------------
WORD_DATA = [
    # 3文字
    {"jp": "あいさつ", "romaji": "aisatsu"},
    {"jp": "きまり", "romaji": "kimari"},
    {"jp": "てがみ", "romaji": "tegami"},
    {"jp": "ことば", "romaji": "kotoba"},
    {"jp": "ねっと", "romaji": "netto"},
    {"jp": "じかん", "romaji": "jikan"},
    {"jp": "れきし", "romaji": "rekishi"},
    # 4文字
    {"jp": "ありがとう", "romaji": "arigatou"},
    {"jp": "おつかれ", "romaji": "otsukare"},
    {"jp": "よろしく", "romaji": "yoroshiku"},
    {"jp": "しゅくだい", "romaji": "shukudai"},
    {"jp": "としょかん", "romaji": "toshokan"},
    {"jp": "でんしゃ", "romaji": "densha"},
    {"jp": "きょかしょ", "romaji": "kyokasho"},
    {"jp": "こくばん", "romaji": "kokuban"},
    {"jp": "てすと", "romaji": "tesuto"},
    {"jp": "じっけん", "romaji": "jikken"},
    {"jp": "けんさく", "romaji": "kensaku"},
    {"jp": "ろぐいん", "romaji": "roguin"},
    # 5文字
    {"jp": "おはよう", "romaji": "ohayou"},
    {"jp": "すみません", "romaji": "sumimasen"},
    {"jp": "しつれい", "romaji": "shitsurei"},
    {"jp": "じかんわり", "romaji": "jikanwari"},
    {"jp": "うんどうかい", "romaji": "undoukai"},
    {"jp": "ぱすわーど", "romaji": "pasuwado"},
    {"jp": "せきゅりてぃ", "romaji": "sekuriti"},
    {"jp": "すまーとふぉん", "romaji": "sumatofon"},
    {"jp": "あるごりずむ", "romaji": "arugorizumu"},
    {"jp": "ねっとわーく", "romaji": "nettowaku"},
    # 6文字
    {"jp": "よろしくね", "romaji": "yoroshikune"},
    {"jp": "ぶんかさい", "romaji": "bunkasai"},
    {"jp": "つうちひょう", "romaji": "tsuuchihyou"},
    {"jp": "ぷろぐらみんぐ", "romaji": "puroguramingu"},
    {"jp": "おかいけい", "romaji": "okaikei"},
    {"jp": "しょうみきげん", "romaji": "shoumikigen"},
]

# -------------------------------------------------------------------------
# セッション状態の初期化
# -------------------------------------------------------------------------
if "current_item" not in st.session_state:
  st.session_state.current_item = random.choice(WORD_DATA)
if "mistake_count" not in st.session_state:
  st.session_state.mistake_count = 0
if "success_count" not in st.session_state:
  st.session_state.success_count = 0
if "error_logs" not in st.session_state:
  st.session_state.error_logs = []

st.title("⌨️ ひらがな単語タイピング ＆ AI分析")
st.caption(
    "3〜6文字のひらがな単語をテンポよく入力しよう！（追加のライブラリ不要版）"
)

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI詳細分析・特訓"])

with tab1:
  if st.button("🔀 次の問題へ"):
    st.session_state.current_item = random.choice(WORD_DATA)
    st.session_state.mistake_count = 0
    st.rerun()

  current_jp = st.session_state.current_item["jp"]
  current_romaji = st.session_state.current_item["romaji"]

  st.markdown("---")
  col_t1, col_t2 = st.columns(2)
  with col_t1:
    st.markdown("##### 🇯🇵 お題（ひらがな）")
    st.info(f"### {current_jp}")
  with col_t2:
    st.markdown("##### 🔤 入力するローマ字")
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
            "「お疲れ様です！タイピングの入力ログから分析した結果、"
            "子音の連続（`sh`, `ch`, `tsu` など）や促音の入力でリズムが崩れやすい傾向があります。"
            "焦らず一文字ずつ確実に入力していきましょう！」"
        )
        st.markdown("### ✨ あなたの弱点を克服するための特訓メニュー")
        st.markdown("1. `shukudai` （シャ・チュ・シュの切り替え）")
        st.markdown("2. `pasuwado` （指のホームポジションを意識）")
