# Simple Resume Screening ATS (Level 6)

This project is a simple Applicant Tracking System (ATS) built using Python and Streamlit.

It allows recruiters or hiring managers to paste a Job Description (JD), upload resume PDFs, and automatically score candidates based on JD match percentage.

The resumes are ranked and classified into ELIGIBLE, REVIEW, or REJECT categories.

--------------------------------------------------

## Features

- Paste Job Description text
- Upload multiple PDF resumes
- Automatic PDF resume parsing
- JD Match % scoring based on word overlap
- Candidate classification:
  - ELIGIBLE
  - REVIEW
  - REJECT
- Ranking of resumes based on match score
- CSV download of results

--------------------------------------------------

## Tech Stack

- Python
- Streamlit
- Pandas
- PyPDF2

--------------------------------------------------

## Folder Structure

resume-screening-level6/
├── resume_screening_level6.py
├── requirements.txt
├── README.md
└── resumes/          (optional for sample PDFs)

--------------------------------------------------

## How to Run

1. Install dependencies

pip install -r requirements.txt

--------------------------------------------------

2. Run the Streamlit App

streamlit run resume_screening_level6.py

--------------------------------------------------

3. Open in Browser

http://localhost:8501

--------------------------------------------------

## How It Works

1. Paste the Job Description in the input box
2. Upload one or more resume PDF files
3. The system calculates JD Match % for each resume
4. Resumes are ranked from highest to lowest match score

--------------------------------------------------

## Decision Logic

Match Score ≥ 50%  → ELIGIBLE  
Match Score 20–49% → REVIEW  
Match Score < 20%  → REJECT  

--------------------------------------------------

## Sample Output

Rank #1  
Resume: Resume_1.pdf  
Decision: ELIGIBLE  
JD Match %: 78.25  

Rank #2  
Resume: Resume_2.pdf  
Decision: REVIEW  
JD Match %: 42.10  

Rank #3  
Resume: Resume_3.pdf  
Decision: REJECT  
JD Match %: 10.50  

--------------------------------------------------

## Why This Project

Recruiters often receive hundreds of resumes for a single job opening.

This project helps automate the resume screening process by providing:

- Fast JD-resume matching
- Candidate shortlisting support
- Simple and explainable scoring logic

--------------------------------------------------

## Future Improvements

- Skill-based weighting instead of word matching
- Semantic similarity using embeddings
- Experience estimation improvements
- Support for DOCX resumes
- Deployment on Streamlit Cloud

--------------------------------------------------

## Author

Built by Venkat Mandarapu  
Resume Screening ATS Project (Level 6)



