# 🏆 Subbu's Home Batch – RedRob Candidate Ranking System

## Team

**Team Name:** Subbu's Home Batch

### Members

- Pekala Harsha Vardhan (Team Lead)
- Munagala Praveen Naga Kumar
- Pathivada Rahul
- Gollu Hritwik Rupesh

---

## Problem Statement

Build a reproducible candidate ranking system that selects and ranks the Top 100 candidates from a candidate dataset.

The system must:

- Process candidate profiles
- Score candidates using predefined ranking logic
- Generate a valid submission CSV
- Run completely offline during inference
- Produce reproducible results

---

## Methodology

The ranking system uses a deterministic rule-based scoring approach.

### 1. Skill Score

Candidates are scored based on:

- Core Skills
- Bonus Skills
- Foundation Skills

Weights:

- Core Skills → Highest weight
- Bonus Skills → Medium weight
- Foundation Skills → Lower weight

---

### 2. Career Score

Current and recent job titles are mapped to role relevance scores.

Examples:

- Search Engineer
- Recommendation Systems Engineer
- NLP Engineer
- AI Engineer
- Machine Learning Engineer

Higher relevance roles receive higher scores.

---

### 3. Behavioral Score

Behavioral signals include:

- GitHub Activity
- Recruiter Response Rate
- Search Appearances
- Saved By Recruiters
- Notice Period
- Open To Work Status

These signals help prioritize active and recruiter-attractive candidates.

---

### 4. Experience Score

Experience is evaluated using years of professional experience.

Preferred range:

- 5–9 years

Candidates inside the target range receive higher scores.

---

### Final Score

Final ranking score is computed using weighted aggregation:

- Skill Score
- Career Score
- Behavioral Score
- Experience Score

Candidates are sorted in descending order and Top 100 are selected.

---

## Repository Structure

```text
.
├── app.py
├── rank.py
├── requirements.txt
├── submission_metadata.yaml
├── submission_v1.csv
└── .streamlit/
```

---

## Reproducibility

Generate submission file:

```bash
python rank.py --candidates candidates.jsonl --out submission.csv
```

Output:

```text
submission.csv
```

---

## Sandbox Demo

Streamlit Demo:

[(https://redrobai-subbus-home-batch.streamlit.app/)]

The sandbox allows:

- Upload candidate dataset
- Run ranking
- View Top Candidates
- Download submission.csv

---

## Compute Environment

- OS: Windows 11
- Python: 3.10.11
- RAM: 8 GB
- CPU: Intel x64 Processor
- GPU Required: No

---

## AI Usage Disclosure

ChatGPT was used for:

- Understanding submission requirements
- Clarifying challenge expectations
- Debugging implementation issues

No AI model is used during ranking or inference.

---

## Declaration

This repository contains the final reproducible implementation used for the RedRob Hackathon submission.