import random
import streamlit as st

st.set_page_config(
    page_title="日常単語タイピング ＆ AIコーチ", page_icon="⌨️", layout="centered"
)

# 日常単語のデータバンク
WORD_BANK = {
    "日常の挨拶・会話": [
        "ohotsukaresama",
        "arigatou",
        "yoroshiku",
        "chottomate",
    ],
    "学校・生活": [
        "jikanwari",
        "shukudai",
        "toshokan",
        "densha",
    ],
    "ネット・SNS": [
        "pasuwado",
        "tsuchi",
        "akanunto",
        "kensaku",
    ],
}

# セッション状態の初期化
if "current_word" not in st.session_state:
  st.session_state.current_word = "ohotsukaresama"  # 初期値
if "mistake_count" not in st.session_state:
  st.session_state.mistake_count = 0
if "error_logs" not in st.session_state:
  st.session_state.error_logs = []

st.title("⌨️ リアルタイムタイピング ＆ AIアドバイザー")
st.caption("個人情報不要！1文字打つごとにリアルタイムでフィードバックします。")

tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI弱点分析・特訓"])

with tab1:
  st.subheader("練習モードを選ぼう")
  selected_theme = st.selectbox(
      "テーマの選択", list(WORD_BANK.keys()), key="theme_select"
  )

  if st.button("新しいお題をセット"):
    st.session_state.current_word = random.choice(WORD_BANK[selected_theme])
    st.session_state.mistake_count = 0
    st.rerun()

  target = st.session_state.current_word

  st.markdown("### 📝 お題（ローマ字入力）")
  st.info(f"**{target}**")

  # リアルタイム入力を受け付けるテキスト入力
  # (on_change やキー変更ごとに即座に評価される)
  user_input = st.text_input(
      "ここにローマ字を入力してください", key="user_typing", value=""
  )

  if user_input:
    # リアルタイムのプレフィックス（前方一致）チェック
    if target.startswith(user_input):
      st.success("✅ 順調です！この調子！")
      if user_input == target:
        st.balloons()
        st.markdown("🎉 **クリア！お見事です！**")
    else:
      st.error(
          "⚠️ 入力が違います！タイピングミスが発生しています。"
      )
      st.session_state.mistake_count += 1
      # どのような入力で間違えたかを蓄積（AI分析用）
      st.session_state.error_logs.append(
          {"target": target, "typed": user_input}
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
        # ここに Gemini API (google-genai) を組み込んでエラーログを送信する
        st.markdown("---")
        st.markdown("### 💬 AIコーチからの分析レポート")
        st.write(
            "「お疲れ様です！子音の連続や母音の切り替え部分でミスの傾向が見られます。"
            "特にキーの押し間違いが多い箇所を重点的に練習しましょう。」"
        )
        st.markdown("### ✨ あなたのための特訓単語")
        st.markdown(
            "1. `shukudai` （シャ・チュ・シュの音の切り替えを意識）"
        )
        st.markdown(
            "2. `toshokan` （指のホームポジションを意識した高速入力）"
        )
