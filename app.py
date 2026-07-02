import streamlit as st
import pandas as pd
import tempfile
import subprocess

st.set_page_config(
    page_title="Subbu's Home Batch",
    page_icon="🏆",
    layout="wide"
)

# ==================================================
# STYLING
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #0f172a 100%
    );
}

.block-container {
    padding-top: 1rem;
    max-width: 1400px;
}

.main-title {
    text-align:center;
    font-size:72px;
    font-weight:900;
    color:white;
}

.sub-title {
    text-align:center;
    font-size:28px;
    color:#cbd5e1;
    margin-bottom:20px;
}

.hero-card {
    background:rgba(255,255,255,0.08);
    padding:30px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.15);
    margin-bottom:20px;
}

[data-testid="metric-container"] {
    background:rgba(255,255,255,0.08);
    border-radius:15px;
    padding:15px;
    border:1px solid rgba(255,255,255,0.15);
}

.stButton > button {
    width:100%;
    height:60px;
    font-size:22px;
    font-weight:bold;
    border-radius:12px;
}

.footer {
    text-align:center;
    color:#94a3b8;
    font-size:18px;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero-card">
    <div class="main-title">
        🏆 Subb's Home Batch
    </div>
    <div class="sub-title">
        AI-Powered Candidate Ranking System
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# INFO CARDS
# ==================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        """
        ### 📂 Input

        Upload:

        • candidates.jsonl

        • sample_candidates.json
        """
    )

with c2:
    st.info(
        """
        ### ⚙️ Engine

        • Skill Scoring

        • Career Scoring

        • Behavioral Signals

        • Experience Scoring
        """
    )

with c3:
    st.info(
        """
        ### 📊 Output

        • Top 100 Candidates

        • Ranking Score

        • Submission CSV
        """
    )

st.divider()

# ==================================================
# FILE UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload Candidate Dataset",
    type=["json", "jsonl"]
)

# ==================================================
# RUN
# ==================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Run Ranking"
    ):

        with st.spinner(
            "Ranking Candidates..."
        ):

            suffix = ".jsonl"

            if uploaded_file.name.endswith(".json"):
                suffix = ".json"

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_input:

                temp_input.write(
                    uploaded_file.getbuffer()
                )

                input_path = temp_input.name

            output_path = "submission.csv"

            cmd = [
                "python",
                "rank.py",
                "--candidates",
                input_path,
                "--out",
                output_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                st.error(
                    "Ranking Failed"
                )

                st.code(
                    result.stderr
                )

            else:

                df = pd.read_csv(
                    output_path
                )

                st.success(
                    "Ranking Completed Successfully"
                )

                # ==================================
                # METRICS
                # ==================================

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "Candidates Returned",
                        len(df)
                    )

                with m2:
                    st.metric(
                        "Top Rank",
                        1
                    )

                with m3:
                    st.metric(
                        "Status",
                        "Success"
                    )

                st.divider()

                st.markdown(
                    """
                    <h2 style='color:white'>
                    🏅 Top Ranked Candidates
                    </h2>
                    """,
                    unsafe_allow_html=True
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=700
                )

                with open(
                    output_path,
                    "rb"
                ) as f:

                    st.download_button(
                        label="📥 Download submission.csv",
                        data=f,
                        file_name="submission.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

st.markdown("""
<div class="footer">
Subb's Home Batch • RedRob Candidate Ranking System
</div>
""", unsafe_allow_html=True)