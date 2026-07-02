import json
import pandas as pd
import numpy as np
import argparse

# ==================================================
# LOAD DATA
# ==================================================

def load_candidates(file_path):

    candidates = []

    if file_path.endswith(".jsonl"):

        with open(file_path, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if line:
                    candidates.append(
                        json.loads(line)
                    )

    elif file_path.endswith(".json"):

        with open(file_path, "r", encoding="utf-8") as f:

            candidates = json.load(f)

    else:
        raise ValueError(
            "Input must be .json or .jsonl"
        )

    print(
        f"Loaded {len(candidates):,} candidates"
    )

    return candidates


# ==================================================
# BUILD candidate_df
# ==================================================

def build_candidate_df(candidates):

    rows = []

    for c in candidates:

        profile = c["profile"]

        signals = c["redrob_signals"]

        rows.append({

            "candidate_id":
                c["candidate_id"],

            "title":
                profile.get(
                    "current_title",
                    ""
                ),

            "headline":
                profile.get(
                    "headline",
                    ""
                ),

            "industry":
                profile.get(
                    "current_industry",
                    ""
                ),

            "country":
                profile.get(
                    "country",
                    ""
                ),

            "years_exp":
                profile.get(
                    "years_of_experience",
                    0
                ),

            "open_to_work":
                signals.get(
                    "open_to_work_flag",
                    False
                ),

            "github_score":
                signals.get(
                    "github_activity_score",
                    0
                ),

            "response_rate":
                signals.get(
                    "recruiter_response_rate",
                    0
                ),

            "notice_period":
                signals.get(
                    "notice_period_days",
                    180
                ),

            "saved_by_recruiters":
                signals.get(
                    "saved_by_recruiters_30d",
                    0
                ),

            "search_appearances":
                signals.get(
                    "search_appearance_30d",
                    0
                ),

            "profile_views":
                signals.get(
                    "profile_views_received_30d",
                    0
                )

        })

    candidate_df = pd.DataFrame(rows)

    print(
        "candidate_df:",
        candidate_df.shape
    )

    return candidate_df


# ==================================================
# BUILD skills_df
# ==================================================

def build_skills_df(candidates):

    rows = []

    for c in candidates:

        cid = c["candidate_id"]

        for skill in c.get("skills", []):

            rows.append({

                "candidate_id":
                    cid,

                "skill_name":
                    skill.get(
                        "name",
                        ""
                    ),

                "proficiency":
                    skill.get(
                        "proficiency",
                        ""
                    ),

                "endorsements":
                    skill.get(
                        "endorsements",
                        0
                    ),

                "duration_months":
                    skill.get(
                        "duration_months",
                        0
                    )

            })

    skills_df = pd.DataFrame(rows)

    print(
        "skills_df:",
        skills_df.shape
    )

    return skills_df


# ==================================================
# BUILD career_df
# ==================================================

def build_career_df(candidates):

    rows = []

    for c in candidates:

        cid = c["candidate_id"]

        for role in c.get(
            "career_history",
            []
        ):

            rows.append({

                "candidate_id":
                    cid,

                "title":
                    role.get(
                        "title",
                        ""
                    ),

                "company":
                    role.get(
                        "company",
                        ""
                    ),

                "industry":
                    role.get(
                        "industry",
                        ""
                    ),

                "duration_months":
                    role.get(
                        "duration_months",
                        0
                    ),

                "is_current":
                    role.get(
                        "is_current",
                        False
                    )

            })

    career_df = pd.DataFrame(rows)

    print(
        "career_df:",
        career_df.shape
    )

    return career_df  

# ==================================================
# SKILL CONFIG
# ==================================================

CORE_SKILLS = {
    "BM25",
    "Elasticsearch",
    "OpenSearch",
    "Qdrant",
    "Pinecone",
    "Weaviate",
    "FAISS",
    "Embeddings",
    "Sentence Transformers",
    "Semantic Search",
    "Vector Search"
}

BONUS_SKILLS = {
    "Learning to Rank",
    "RAG",
    "LangChain",
    "LlamaIndex",
    "LoRA",
    "QLoRA",
    "PEFT"
}

FOUNDATION_SKILLS = {
    "Python",
    "PyTorch",
    "TensorFlow",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "scikit-learn"
}


# ==================================================
# TITLE SCORE
# ==================================================

TITLE_SCORE = {

    "Search Engineer": 10,
    "Recommendation Systems Engineer": 10,

    "NLP Engineer": 9,
    "Senior NLP Engineer": 9,

    "AI Engineer": 8,
    "Senior AI Engineer": 8,
    "Lead AI Engineer": 8,

    "Applied ML Engineer": 8,

    "Machine Learning Engineer": 8,
    "Senior Machine Learning Engineer": 8,
    "Staff Machine Learning Engineer": 8,

    "ML Engineer": 7,
    "Junior ML Engineer": 6,

    "AI Research Engineer": 6,

    "Data Scientist": 5,
    "Senior Data Scientist": 5,

    "AI Specialist": 4,

    "Data Engineer": 2,
    "Analytics Engineer": 2
}

NEGATIVE_TITLES = {

    "Marketing Manager",
    "HR Manager",
    "Sales Executive",
    "Accountant",
    "Business Analyst",
    "Project Manager",
    "Customer Support",
    "Content Writer",
    "Civil Engineer",
    "Mechanical Engineer",
    "Graphic Designer",
    "Operations Manager"
}


# ==================================================
# EXPERIENCE SCORE
# ==================================================

def exp_score(x):

    if 5 <= x <= 9:
        return 1.0

    elif 4 <= x < 5:
        return 0.7

    elif 9 < x <= 12:
        return 0.7

    elif 3 <= x < 4:
        return 0.4

    else:
        return 0.2


# ==================================================
# SKILL FEATURES
# ==================================================

def build_skill_features(skills_df):

    candidate_skills = (
        skills_df
        .groupby("candidate_id")["skill_name"]
        .apply(set)
        .reset_index()
    )

    def compute_skill_score(skill_set):

        core_count = len(
            skill_set & CORE_SKILLS
        )

        bonus_count = len(
            skill_set & BONUS_SKILLS
        )

        foundation_count = len(
            skill_set & FOUNDATION_SKILLS
        )

        score = (

            core_count * 5 +

            bonus_count * 3 +

            foundation_count * 1
        )

        return score

    candidate_skills["skill_score"] = (
        candidate_skills["skill_name"]
        .apply(compute_skill_score)
    )

    return candidate_skills[
        [
            "candidate_id",
            "skill_score"
        ]
    ]


# ==================================================
# CAREER FEATURES
# ==================================================

def build_career_features(career_df):

    current_jobs = career_df[
        career_df["is_current"] == True
    ].copy()

    current_jobs["career_score"] = (

        current_jobs["title"]

        .map(TITLE_SCORE)

        .fillna(0)
    )

    current_jobs["duration_bonus"] = (

        current_jobs["duration_months"] / 12

    ).clip(upper=5)

    current_jobs["career_score"] += (
        current_jobs["duration_bonus"]
    )

    current_jobs.loc[

        current_jobs["title"].isin(
            NEGATIVE_TITLES
        ),

        "career_score"

    ] = -3

    return current_jobs[
        [
            "candidate_id",
            "career_score"
        ]
    ]


# ==================================================
# BEHAVIOR FEATURES
# ==================================================

def build_behavior_features(candidate_df):

    behavior = candidate_df.copy()

    behavior["notice_score"] = (

        180 - behavior["notice_period"]

    ) / 180

    behavior["otw_score"] = (

        behavior["open_to_work"]

        .astype(float)
    )

    behavior.loc[

        behavior["open_to_work"] == False,

        "otw_score"

    ] = -0.5

    norm_cols = [

        "github_score",
        "saved_by_recruiters",
        "search_appearances",
        "profile_views"
    ]

    for col in norm_cols:

        mn = behavior[col].min()
        mx = behavior[col].max()

        if mx == mn:

            behavior[col + "_norm"] = 0

        else:

            behavior[col + "_norm"] = (

                behavior[col] - mn

            ) / (mx - mn)

    behavior["behavior_score"] = (

        behavior["github_score_norm"] * 0.25 +

        behavior["response_rate"] * 0.25 +

        behavior["saved_by_recruiters_norm"] * 0.20 +

        behavior["search_appearances_norm"] * 0.15 +

        behavior["notice_score"] * 0.10 +

        behavior["otw_score"] * 0.05
    )

    return behavior[
        [
            "candidate_id",
            "behavior_score"
        ]
    ]


# ==================================================
# EXPERIENCE FEATURES
# ==================================================

def build_exp_features(candidate_df):

    exp_df = candidate_df[
        [
            "candidate_id",
            "years_exp"
        ]
    ].copy()

    exp_df["exp_score"] = (

        exp_df["years_exp"]

        .apply(exp_score)
    )

    return exp_df[
        [
            "candidate_id",
            "exp_score"
        ]
    ]
# ==================================================
# REASONING
# ==================================================

def generate_reason(title):

    title = str(title)

    if "Search" in title:
        return "Strong search and retrieval background with highly relevant ranking skills."

    elif "Recommendation" in title:
        return "Recommendation systems experience aligns closely with candidate matching and ranking."

    elif "NLP" in title:
        return "NLP expertise with retrieval and embedding related experience."

    elif "Machine Learning" in title:
        return "Strong machine learning background with relevant AI skills."

    elif "AI Engineer" in title:
        return "AI engineering experience and relevant production ML exposure."

    elif "Applied ML" in title:
        return "Applied ML experience with practical ranking and retrieval relevance."

    return "Relevant AI and machine learning profile with strong overall signals."


# ==================================================
# FINAL RANKING
# ==================================================

def build_final_ranking(
    candidate_df,
    skill_features,
    career_features,
    behavior_features,
    exp_features
):

    final_df = (
        skill_features

        .merge(
            career_features,
            on="candidate_id",
            how="left"
        )

        .merge(
            behavior_features,
            on="candidate_id",
            how="left"
        )

        .merge(
            exp_features,
            on="candidate_id",
            how="left"
        )
    )

    final_df["career_score"] = (
        final_df["career_score"]
        .fillna(0)
    )

    final_df["behavior_score"] = (
        final_df["behavior_score"]
        .fillna(0)
    )

    final_df["exp_score"] = (
        final_df["exp_score"]
        .fillna(0)
    )

    final_df["final_score"] = (

        final_df["skill_score"] * 0.35 +

        final_df["career_score"] * 0.35 +

        final_df["behavior_score"] * 20 * 0.20 +

        final_df["exp_score"] * 10 * 0.10
    )

    ranked = (

        final_df

        .sort_values(
            "final_score",
            ascending=False
        )

        .head(100)

        .reset_index(drop=True)
    )

    ranked = ranked.merge(

        candidate_df[
            [
                "candidate_id",
                "title",
                "headline",
                "years_exp"
            ]
        ],

        on="candidate_id",
        how="left"
    )

    ranked["reasoning"] = (

        ranked["title"]

        .apply(generate_reason)
    )

    ranked["rank"] = (
        ranked.index + 1
    )

    return ranked


# ==================================================
# SUBMISSION
# ==================================================

def create_submission(
    ranked_df,
    output_file
):

    submission = pd.DataFrame({

        "candidate_id":
            ranked_df["candidate_id"],

        "rank":
            ranked_df["rank"],

        "score":
            ranked_df["final_score"].round(6),

        "reasoning":
            ranked_df["reasoning"]

    })

    submission.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSubmission saved: {output_file}"
    )

    print(
        f"Rows: {len(submission)}"
    )


# ==================================================
# MAIN
# ==================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidates",
        required=True
    )

    parser.add_argument(
        "--out",
        default="submission.csv"
    )

    args = parser.parse_args()

    print("\nLoading candidates...")

    candidates = load_candidates(
        args.candidates
    )

    print("\nBuilding DataFrames...")

    candidate_df = build_candidate_df(
        candidates
    )

    skills_df = build_skills_df(
        candidates
    )

    career_df = build_career_df(
        candidates
    )

    print("\nBuilding Features...")

    skill_features = (
        build_skill_features(
            skills_df
        )
    )

    career_features = (
        build_career_features(
            career_df
        )
    )

    behavior_features = (
        build_behavior_features(
            candidate_df
        )
    )

    exp_features = (
        build_exp_features(
            candidate_df
        )
    )

    print("\nRanking Candidates...")

    ranked_df = build_final_ranking(

        candidate_df,

        skill_features,

        career_features,

        behavior_features,

        exp_features
    )

    create_submission(
        ranked_df,
        args.out
    )

    print("\nDone.")


if __name__ == "__main__":

    main()