import random
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="日常単語タイピング＆AIコーチ", page_icon="⌨️", layout="centered"
)

# セッション状態の初期化
if "score_history" not in st.session_state:
    st.session_state.score_history = []
if "current_word" not in st.session_state:
    st.session_state.current_word = ""

# 日常単語のデータバンク（テーマ別）
WORD_BANK = {
    "日常の挨拶・会話": [
        "お疲れ様です",
        "ありがとうございます",
        "よろしくおねがいします",
        "ちょっと待ってください",
    ],
    "学校・生活": [
        "時間割を確認する",
        "宿題を提出する",
        "図書館で本を借りる",
        "電車に乗り遅れる",
    ],
    "ネット・SNS": [
        "パスワードを再設定する",
        "通知をオフにする",
        "アカウントを登録する",
        "検索エンジンで調べる",
    ],
}

st.title("⌨️ 日常単語タイピング ＆ AIアドバイザー")
st.caption(
    "個人情報の入力は不要です！毎日のちょっとしたスキマ時間でタイピングを上達させましょう。"
)

# タブの作成
tab1, tab2 = st.tabs(["🎯 タイピング実践", "🤖 AI弱点分析・特訓"])

with tab1:
  st.subheader("練習モードを選ぼう")
  selected_theme = st.selectbox(
      "テーマの選択", list(WORD_BANK.keys()), key="theme_select"
  )

  # お題の選択ボタン
  if st.button("新しいお題を出す"):
    st.session_state.current_word = random.choice(WORD_BANK[selected_theme])

  if st.session_state.current_word:
    st.info(f"💡 **いまのお題:** {st.session_state.current_word}")

    # タイピング入力欄
    user_input = st.text_input(
        "上の文字をローマ字（またはそのまま）で入力してEnter", key="typing_box"
    )

    if user_input:
      if user_input == st.session_state.current_word:
        st.success("🎉 正解です！お見事！")
        # 履歴の保存（簡易）
        st.session_state.score_history.append(
            {
                "word": st.session_state.current_word,
                "status": "Success",
            }
        )
      else:
        st.warning(
            f"⚠️ 入力内容が違います。（入力: {user_input} / お題:"
            f" {st.session_state.current_word}）"
        )

with tab2:
  st.subheader("🤖 AIによるタイピング診断＆特訓メニュー")

  if not st.session_state.score_history:
    st.info(
        "まずは「タイピング実践」タブでいくつか問題に挑戦してみましょう！"
    )
  else:
    st.write(
        f"これまでの練習回数: **{len(st.session_state.score_history)}回**"
    )

    # Gemini APIなどと連携してフィードバックを生成するイメージの場所
    if st.button("AIに弱点を分析してもらう"):
      with st.spinner("AIがあなたのタイピング傾向を分析中..."):
        # ここに `google-genai` を使ったAPI呼び出しを記述します
        # 例: 「以下の入力履歴から、苦手なローマ字の傾向を分析し、
        # 日常生活で使える新しい練習用の短い単語を3つ作ってください」
        st.markdown("---")
        st.markdown("### 💬 AIコーチからのアドバイス")
        st.write(
            "「お疲れ様です！子音と母音の切り替え（特に `shi` や `chi`"
            " など）で少しペースが落ちる傾向が見られます。"
            "指を大きく動かす練習を意識してみましょう！」"
        )
        st.markdown("### ✨ あなたのためのAI特訓単語リスト")
        st.markdown("1. `しょうゆをかける`")
        st.markdown("2. `ちゃのまでお茶を飲む`")
        st.markdown("3. `しんぶんしを読む`")
