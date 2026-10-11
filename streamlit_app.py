import random
import streamlit as st

st.set_page_config(
    page_title="日常単語タイピング ＆ AIコーチ", page_icon="⌨️", layout="centered"
)

# 日常単語のデータバンク（日本語とローマ字のペア）
WORD_BANK = {
    "日常の挨拶・会話": [
        {"jp": "お疲れ様です", "romaji": "ohotsukaresama"},
        {"jp": "ありがとうございます", "romaji": "arigatou"},
        {"jp": "よろしくお願いします", "romaji": "yoroshiku"},
        {"jp": "ちょっと待ってください", "romaji": "chottomate"},
    ],
    "学校・生活": [
        {"jp": "時間割を確認する", "romaji": "jikanwari"},
        {"jp": "宿題を提出する", "romaji": "shukudai"},
        {"jp": "図書館で本を借りる", "romaji": "toshokan"},
        {"jp": "電車に乗り遅れる", "romaji": "densha"},
    ],
    "ネット・SNS": [
        {"jp": "パスワードを再設定する", "romaji": "pasuwado"},
        {"jp": "通知をオフにする", "romaji": "tsuchi"},
        {"jp": "アカウントを登録する", "romaji": "akanunto"},
        {"jp": "検索エンジンで調べる", "romaji": "kensaku"},
    ],
}

# セッション状態の初期化
if "current_item" not in st.session_state:
  st.session_state.current_item = WORD_BANK["日常の挨拶・会話"][0]
if "mistake_count" not in st.session_state:
  st.session_state.mistake_count = 0
if "error_logs" not in st.session_state:
  st.session_state.error_logs = []

st.title("⌨️ リアルタイムタイピング ＆ AIアドバイザー")
st.caption("個人情報不要！日本語の意味を確認しながらローマ字入力の練習ができます。")

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI弱点分析・特訓"])

with tab1:
  st.subheader("練習モードを選ぼう")
  selected_theme = st.selectbox(
      "テーマの選択", list(WORD_BANK.keys()), key="theme_select"
  )

  if st.button("新しいお題をセット"):
    st.session_state.current_item = random.choice(WORD_BANK[selected_theme])
    st.session_state.mistake_count = 0
    st.rerun()

  current_jp = st.session_state.current_item["jp"]
  current_romaji = st.session_state.current_item["romaji"]

  # 日本語とローマ字を並べて表示
  st.markdown("---")
  col_t1, col_t2 = st.columns(2)
  with col_t1:
    st.markdown("##### 🇯🇵 意味（日本語）")
    st.info(f"### {current_jp}")
  with col_t2:
    st.markdown("##### 🔤 入力するローマ字")
    st.success(f"### `{current_romaji}`")
  st.markdown("---")

  # リアルタイム入力を受け付けるテキスト入力
  user_input = st.text_input(
      "上のローマ字をここに入力してください", key="user_typing", value=""
  )

  if user_input:
    # リアルタイムのプレフィックス（前方一致）チェック
    if current_romaji.startswith(user_input):
      st.success("✅ 順調です！この調子！")
      if user_input == current_romaji:
        st.balloons()
        st.markdown("🎉 **クリア！お見事です！次の問題も挑戦しよう！**")
    else:
      st.error(
          "⚠️ 入力が違います！タイピングミスが発生しています。"
      )
      st.session_state.mistake_count += 1
      st.session_state.error_logs.append(
          {"target": current_romaji, "typed": user_input}
      )

  # 現在のスタッツ表示
  col1, col2 = st.columns(2)
  with col1:
    st.metric("現在のミス回数", f"{st.session_state.mistake_count} 回")
  with col2:
    st.metric("蓄積されたエラーデータ数", len(st.session_state.error_logs))

with tab2:
  st.subheader("🤖 AIによるタイピング診断＆特訓メニュー")

  if not st.session_state.error_logs:
    st.info(
        "まずは「タイピング実践」タブでタイピングを行ってデータを集めましょう！"
    )
  else:
    st.write(
        f"これまでに検知されたミス総数:"
        f" **{len(st.session_state.error_logs)}件**"
    )

    if st.button("AIにミスの傾向を分析してもらう"):
      with st.spinner("AIがミスの傾向を分析中..."):
        # ここに Gemini API (google-genai) を組み込む予定地
        st.markdown("---")
        st.markdown("### 💬 AIコーチからの分析レポート")
        st.write(
            "「お疲れ様です！子音の連続や母音の切り替え部分でミスの傾向が見られます。"
            "特にキーの押し間違いが多い箇所を重点的に練習しましょう。」"
        )
        st.markdown("### ✨ あなたのための特訓単語")
        st.markdown("1. `shukudai` （シャ・チュ・シュの音の切り替え）")
        st.markdown("2. `toshokan` （ホームポジションを意識した入力）")
