import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# Google Gemini API 設定（環境変数を使用推奨）
genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.0-flash-lite")

# タイトル
st.title("✈️ 旅行プランニングアシスタント")
st.write("あなたの希望に合わせた旅行プランをAIが提案します。")

# 入力フォーム
with st.form("travel_form"):
    destination = st.text_input("行きたい場所（都市名・国名など）", placeholder="例: 京都, パリ")
    budget = st.number_input("予算（円）", min_value=10000, step=5000)
    days = st.slider("旅行日数（日）", min_value=1, max_value=30, value=5)
    interests = st.text_area("興味のあるアクティビティやテーマ", placeholder="例: 美術館巡り、食べ歩き、自然、温泉")
    submit = st.form_submit_button("旅行プランを作成")

# 結果表示
if submit and destination and budget and interests:
    with st.spinner("旅行プランを生成中..."):
        prompt = f"""
        あなたは旅行プランナーです。以下の条件に合った旅行プランを日本語で提案してください。

        - 行き先: {destination}
        - 予算: {budget}円
        - 日数: {days}日
        - 興味: {interests}

        以下の情報を含めてください：
        - 日別スケジュール（1日ごとに簡潔に）
        - おすすめの観光地やアクティビティ
        - 宿泊施設の種類（ホテル、旅館など）
        - 交通手段（移動方法）
        - 概算費用の内訳（宿泊、交通、アクティビティ、食費など）
        """

        response = model.generate_content(prompt)
        plan_text = response.text

        # 表示
        st.subheader("📋 あなたの旅行プラン")
        st.markdown(plan_text)

        # 費用内訳の抽出と可視化（簡易版）
        st.subheader("💰 費用の目安（内訳）")
        if "宿泊" in plan_text:
            try:
                costs = {
                    "宿泊": int(budget * 0.4),
                    "交通": int(budget * 0.3),
                    "アクティビティ": int(budget * 0.2),
                    "食費": int(budget * 0.1),
                }

                fig = go.Figure(data=[go.Pie(labels=list(costs.keys()), values=list(costs.values()))])
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("費用の内訳を可視化できませんでした。")

        # オプション：地図との連携（streamlit-folium などで拡張可能）

elif submit:
    st.warning("全ての項目を入力してください。")

s
