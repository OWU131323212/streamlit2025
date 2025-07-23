import streamlit as st
import plotly.graph_objects as go
import random

# タイトル
st.title("✈️ 旅行プランニングアシスタント（ローカル版）")
st.write("あなたの希望に合わせた簡単な旅行プランを自動で提案します。")

# 入力フォーム
with st.form("travel_form"):
    destination = st.text_input("行きたい場所（都市名・国名など）", placeholder="例: 京都, パリ")
    budget = st.number_input("予算（円）", min_value=10000, step=5000)
    days = st.slider("旅行日数（日）", min_value=1, max_value=30, value=5)
    interests = st.text_area("興味のあるアクティビティやテーマ", placeholder="例: 美術館巡り、食べ歩き、自然、温泉")
    submit = st.form_submit_button("旅行プランを作成")

# 旅行プランの自動生成関数（簡易的）
def generate_simple_plan(destination, budget, days, interests):
    interest_keywords = interests.split("、")
    sample_activities = {
        "美術館": "地元の美術館を訪問",
        "食": "地元グルメを食べ歩き",
        "自然": "自然公園でハイキング",
        "温泉": "温泉でゆっくり休養",
        "ショッピング": "ショッピングエリアを散策",
        "歴史": "歴史的建造物を巡る",
    }

    schedule = []
    for day in range(1, days + 1):
        activity = random.choice(interest_keywords)
        matched = next((v for k, v in sample_activities.items() if k in activity), f"{destination}で自由行動")
        schedule.append(f"**Day {day}:** {matched}")

    # 宿泊施設タイプと交通手段（サンプル）
    hotel_type = random.choice(["ビジネスホテル", "旅館", "民宿", "ゲストハウス"])
    transport = random.choice(["電車", "バス", "レンタカー", "飛行機"])

    # 概算費用（仮の比率）
    costs = {
        "宿泊": int(budget * 0.4),
        "交通": int(budget * 0.3),
        "アクティビティ": int(budget * 0.2),
        "食費": int(budget * 0.1),
    }

    return schedule, hotel_type, transport, costs

# 結果表示
if submit and destination and budget and interests:
    with st.spinner("旅行プランを作成中..."):
        schedule, hotel_type, transport, costs = generate_simple_plan(destination, budget, days, interests)

        # 表示
        st.subheader("📋 あなたの旅行プラン")
        st.markdown(f"**行き先**: {destination}  \n**日数**: {days}日  \n**宿泊施設**: {hotel_type}  \n**移動手段**: {transport}")
        st.markdown("### 日別スケジュール")
        for item in schedule:
            st.markdown(f"- {item}")

        # 費用の内訳チャート
        st.subheader("💰 費用の目安（内訳）")
        fig = go.Figure(data=[go.Pie(labels=list(costs.keys()), values=list(costs.values()))])
        st.plotly_chart(fig, use_container_width=True)

elif submit:
    st.warning("全ての項目を入力してください。")
