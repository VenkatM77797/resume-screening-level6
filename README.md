# Applicant Tracking System (ATS)

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
-![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![PyPDF2](https://img.shields.io/badge/PyPDF2-FF6F00?style=for-the-badge&logo=python&logoColor=white)

--------------------------------------------------

## Folder Structure

resume-screening-level6/
├── resume_screening_level6.py
├── requirements.txt
├── README.md
└── resumes/          (optional for sample PDFs)

--------------------------------------------------

<img width="2537" height="1393" alt="image" src="https://github.com/user-attachments/assets/9c767113-7979-4b0c-8678-90c024ab1795" /># Simple Resume Screening ATS (Level 6)

## How to Run

1. Install dependencies
``` bash
pip install -r requirements.txt
``` 
--------------------------------------------------

2. Run the Streamlit App
``` bash
streamlit run resume_screening_level6.py
OR
python -m streamlit run resume_screening_level6.py
```
--------------------------------------------------

3. Open in Browser
``` bash
http://localhost:8501
``` 
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

Venkat Mandarapu  




