import streamlit as st
import pandas as pd
import tempfile

from rank import (
    load_candidates,
    build_candidate_df,
    build_skills_df,
    build_career_df,
    build_skill_features,
    build_career_features,
    build_behavior_features,
    build_exp_features,
    build_final_ranking
)

st.set_page_config(
    page_title="Subbu's Home Batch",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:linear-gradient(
        135deg,
        #0B1220 0%,
        #111827 50%,
        #1E293B 100%
    );
}

.main-title{
    text-align:center;
    font-size:72px;
    font-weight:900;
    color:white;
}

.sub-title{
    text-align:center;
    font-size:28px;
    color:#D1D5DB;
}

.hero{
    padding:30px;
    border-radius:25px;
    background:#1F2937;
    border:1px solid #374151;
    margin-bottom:25px;
}

.card{
    background:#1F2937;
    padding:20px;
    border-radius:20px;
    border:1px solid #374151;
    min-height:180px;
}

.card h3{
    color:white;
}

.card p{
    color:#D1D5DB;
    font-size:18px;
}

.stButton > button{
    width:100%;
    height:70px;
    font-size:24px;
    font-weight:bold;
    border-radius:15px;
}

.footer{
    text-align:center;
    color:#9CA3AF;
    margin-top:40px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<div class="main-title">
🏆 Subbu's Home Batch
</div>

<div class="sub-title">
AI Powered Candidate Ranking System
</div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    <h3>📂 Input</h3>
    <p>
    Upload Candidate Dataset<br><br>
    JSON<br>
    JSONL
    </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h3>⚙ Ranking Engine</h3>
    <p>
    Skill Score<br>
    Career Score<br>
    Behavioral Score<br>
    Experience Score
    </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h3>📊 Output</h3>
    <p>
    Top 100 Candidates<br>
    Ranked Results<br>
    Download CSV
    </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader(
    "Upload Candidate Dataset",
    type=["json","jsonl"]
)

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Run Ranking"
    ):

        with st.spinner(
            "Processing Candidates..."
        ):

            suffix = ".jsonl"

            if uploaded_file.name.endswith(".json"):
                suffix = ".json"

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                input_path = temp_file.name

            candidates = load_candidates(
                input_path
            )

            candidate_df = build_candidate_df(
                candidates
            )

            skills_df = build_skills_df(
                candidates
            )

            career_df = build_career_df(
                candidates
            )

            skill_features = build_skill_features(
                skills_df
            )

            career_features = build_career_features(
                career_df
            )

            behavior_features = build_behavior_features(
                candidate_df
            )

            exp_features = build_exp_features(
                candidate_df
            )

            ranked_df = build_final_ranking(

                candidate_df,

                skill_features,

                career_features,

                behavior_features,

                exp_features
            )

            output_df = pd.DataFrame({

                "candidate_id":
                    ranked_df["candidate_id"],

                "rank":
                    ranked_df["rank"],

                "score":
                    ranked_df["final_score"].round(6),

                "reasoning":
                    ranked_df["reasoning"]
            })

            st.success(
                "Ranking Completed Successfully"
            )

            m1,m2,m3 = st.columns(3)

            with m1:
                st.metric(
                    "Candidates",
                    len(output_df)
                )

            with m2:
                st.metric(
                    "Top Rank",
                    "1"
                )

            with m3:
                st.metric(
                    "Status",
                    "Success"
                )

            st.divider()

            st.subheader(
                "🏅 Top Ranked Candidates"
            )

            st.dataframe(
                output_df,
                use_container_width=True,
                height=700
            )

            csv = output_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download submission.csv",
                data=csv,
                file_name="submission.csv",
                mime="text/csv",
                use_container_width=True
            )

st.markdown("""
<div class="footer">
Subbu's Home Batch • RedRob AI Challenge
</div>
""", unsafe_allow_html=True)