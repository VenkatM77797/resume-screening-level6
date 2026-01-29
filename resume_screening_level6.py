import io
import pandas as pd
import streamlit as st
import PyPDF2
from datetime import datetime

# -----------------------------
# SKILL BANK (edit anytime)
# -----------------------------
SKILL_BANK = sorted(set([
    # Data / Analytics
    "excel", "advanced excel", "pivot tables", "vlookup", "power bi", "tableau",
    "data analysis", "data analytics", "data visualization", "reporting", "dashboards",
    "statistics", "a/b testing",

    # SQL / DB
    "sql", "mysql", "postgresql", "sqlite", "joins", "stored procedures",

    # Python / ML
    "python", "python3", "pandas", "numpy", "scikit-learn", "machine learning",
    "deep learning", "nlp", "tensorflow", "pytorch",

    # Cloud / Dev / Tools
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
    "linux", "jira",

    # Soft
    "communication", "problem solving", "teamwork", "stakeholder management",
]))

# Map variants -> canonical form
ALIASES = {
    "python3": "python",
    "advanced excel": "excel",
    "pivot tables": "excel",
    "vlookup": "excel",
    "postgresql": "sql",
    "mysql": "sql",
    "github": "git",
}

CURRENT_YEAR = datetime.now().year


# -----------------------------
# Helpers
# -----------------------------
def read_pdf_bytes(file_bytes: bytes) -> str:
    """Extract text from uploaded PDF bytes."""
    text = ""
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    for p in reader.pages:
        text += (p.extract_text() or "") + "\n"
    return text.lower()

def normalize(text: str) -> str:
    """Normalize text and apply alias replacements."""
    t = text.lower().replace("–", "-").replace("—", "-")
    for k, v in ALIASES.items():
        t = t.replace(k, v)
    return t

def extract_skills(text: str, skills: list[str]) -> list[str]:
    found = []
    for s in skills:
        if s in text:
            found.append(s)
    return sorted(set(found))

def extract_skills_from_jd(jd_text: str) -> list[str]:
    jd = normalize(jd_text)
    found = []
    for s in SKILL_BANK:
        s_norm = ALIASES.get(s, s)
        if s_norm in jd:
            found.append(s_norm)
    return sorted(set(found))

def estimate_experience_years(text: str) -> int:
    """
    Conservative experience estimate:
    - Look only at years 2000..current
    - Use the MOST RECENT year seen (often relates to work timeline)
    - Experience = current_year - most_recent_year
    - Cap at 6 to avoid crazy numbers from education dates
    """
    years = []
    for y in range(2000, CURRENT_YEAR + 1):
        if str(y) in text:
            years.append(y)
    if len(years) >= 1:
        most_recent = max(years)
        return min(max(CURRENT_YEAR - most_recent, 0), 6)
    return 0

def experience_bucket(years: int) -> str:
    if years <= 1:
        return "Junior (0–1)"
    if years <= 4:
        return "Mid (2–4)"
    return "Senior (5+)"

def experience_score(years: int) -> float:
    # 0..6 -> 0..100
    years = max(0, min(years, 6))
    return round((years / 6) * 100, 2)

def must_missing(found_skills: list[str], must_have: list[str]) -> list[str]:
    return [s for s in must_have if s not in found_skills]

def final_decision(jd_match_pct: float, missing_must: list[str]) -> str:
    """
    Realistic ATS decision:
    - Very low JD match -> reject
    - Missing 2+ must-have -> reject
    - Missing 1 must-have OR mid JD match -> review
    - Else eligible
    """
    if jd_match_pct < 20:
        return "REJECT"
    if len(missing_must) >= 2:
        return "REJECT"
    if len(missing_must) == 1 or jd_match_pct < 50:
        return "REVIEW"
    return "ELIGIBLE"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Realistic ATS (Level 6)", layout="wide")
st.title("Realistic Resume Screening ATS (Level 6)")
st.caption("Paste JD → choose MUST/NICE → upload PDFs → get ranked results + shortlist + explanations + CSV download.")

with st.sidebar:
    st.header("Controls")
    cutoff = st.slider("Score cutoff (min score for shortlist)", 0, 100, 60)
    top_n = st.slider("Top-N shortlist size", 1, 50, 10)
    show_decisions = st.multiselect(
        "Show decisions",
        ["ELIGIBLE", "REVIEW", "REJECT"],
        default=["ELIGIBLE", "REVIEW", "REJECT"]
    )
    strict_mode = st.checkbox("Strict mode (JD match required)", value=True)
    st.caption("Strict mode: if JD Match is 0%, candidate becomes REJECT with score 0.")

st.subheader("1) Paste Job Description (JD)")
jd_text = st.text_area("Job Description", height=180, placeholder="Paste the job description here...")

extracted = extract_skills_from_jd(jd_text) if jd_text.strip() else []

colA, colB = st.columns(2)
with colA:
    st.write("**Skills detected from JD (auto):**")
    if extracted:
        st.success(", ".join(extracted))
    else:
        st.info("Paste JD to auto-detect skills. You can also choose MUST/NICE manually.")

with colB:
    st.write("**Select MUST-HAVE and NICE-TO-HAVE**")
    options = extracted if extracted else [ALIASES.get(s, s) for s in SKILL_BANK]

    default_must = []
    for s in ["python", "sql", "excel"]:
        if s in options:
            default_must.append(s)

    must_have = st.multiselect("MUST-HAVE skills", options, default=default_must)
    nice_to_have = st.multiselect(
        "NICE-TO-HAVE skills",
        options,
        default=[s for s in ["pandas", "power bi", "communication"] if s in options and s not in must_have]
    )

# Clean lists
must_have = sorted(set([s.lower().strip() for s in must_have if s.strip()]))
nice_to_have = sorted(set([s.lower().strip() for s in nice_to_have if s.strip() and s not in must_have]))
all_skills = sorted(set(must_have + nice_to_have))

st.subheader("2) Upload resume PDFs")
uploads = st.file_uploader("Upload one or more PDF resumes", type=["pdf"], accept_multiple_files=True)

if not uploads:
    st.stop()

if not all_skills:
    st.error("Please select at least 1 skill in MUST/NICE (or paste a JD).")
    st.stop()

# JD skills baseline (if user pasted JD, use extracted; else use selected skills)
jd_skills = extracted if extracted else all_skills

results = []
explanations = {}

for f in uploads:
    raw_text = read_pdf_bytes(f.read())
    text = normalize(raw_text)

    found = extract_skills(text, all_skills)
    missing_must = must_missing(found, must_have)

    # JD match
    jd_found = [s for s in jd_skills if s in found]
    jd_missing = [s for s in jd_skills if s not in found]
    jd_match_pct = round((len(jd_found) / len(jd_skills)) * 100, 2) if jd_skills else 0.0

    # Nice match
    nice_found = [s for s in nice_to_have if s in found]
    nice_match_pct = round((len(nice_found) / len(nice_to_have)) * 100, 2) if nice_to_have else 0.0

    # Experience
    exp_years = estimate_experience_years(text)
    exp_bucket = experience_bucket(exp_years)
    exp_sc = experience_score(exp_years)

    # -----------------------------
    # Realistic scoring
    # JD dominates, then experience, then nice-to-have
    # -----------------------------
    base_score = (0.75 * jd_match_pct) + (0.15 * exp_sc) + (0.10 * nice_match_pct)

    # Hard rule (strict mode): if no JD match at all -> reject
    decision = final_decision(jd_match_pct, missing_must)
    if strict_mode and jd_match_pct == 0:
        decision = "REJECT"
        final_score = 0.0
    else:
        # Must-have penalties (ATS-like)
        if len(missing_must) == 1:
            base_score *= 0.85
        elif len(missing_must) >= 2:
            base_score *= 0.60

        final_score = round(base_score, 2)

    # Explanation
    expl = []
    if must_have:
        if not missing_must:
            expl.append("✅ All MUST-HAVE skills found.")
        else:
            expl.append(f"⚠️ Missing MUST-HAVE: {', '.join(missing_must)}")

    expl.append(f"📌 JD Match: {jd_match_pct}% (found: {', '.join(jd_found) if jd_found else 'none'})")

    if jd_missing:
        expl.append(f"➖ Missing JD skills: {', '.join(jd_missing[:12])}" + (" ..." if len(jd_missing) > 12 else ""))

    expl.append(f"🧭 Experience: {exp_years} yrs → {exp_bucket}")

    if nice_to_have:
        expl.append(f"✨ Nice-to-have match: {nice_match_pct}% (found: {', '.join(nice_found) if nice_found else 'none'})")

    expl.append(f"✅ Final Decision: {decision}")
    explanations[f.name] = "\n".join(expl)

    results.append({
        "Resume": f.name,
        "Decision": decision,
        "Score": final_score,
        "JD Match %": jd_match_pct,
        "Experience (yrs)": exp_years,
        "Experience Level": exp_bucket,
        "Found Skills": ", ".join(found),
        "Missing Must-Have": ", ".join(missing_must),
    })

df = pd.DataFrame(results).sort_values("Score", ascending=False).reset_index(drop=True)
df.insert(0, "Rank", df.index + 1)

# Filters
filtered = df[df["Decision"].isin(show_decisions)].copy()
filtered = filtered[filtered["Score"] >= cutoff].copy()
filtered = filtered.head(top_n).reset_index(drop=True)

st.subheader("Ranked Results")
st.dataframe(df, use_container_width=True)

st.subheader(f"Shortlist (Decision in {show_decisions}, Score ≥ {cutoff}, Top {top_n})")
st.dataframe(filtered, use_container_width=True)

st.subheader("Explain Score (ATS-style)")
for name in df["Resume"].tolist():
    with st.expander(f"Why this score? → {name}"):
        st.text(explanations.get(name, "No explanation available."))

# Downloads
csv_full = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Full Results (CSV)", data=csv_full, file_name="ats_results_full.csv", mime="text/csv")

csv_short = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download Shortlist (CSV)", data=csv_short, file_name="ats_shortlist.csv", mime="text/csv")
