# skill-gap-analyzer
Python-based Skill Gap Analyzer that compares candidate skills with job-role requirements and prioritizes missing skills.
# 🚀 AI Skill Gap Analyzer

## 📌 Project Overview

AI Skill Gap Analyzer is an AI-powered application that analyzes a user's skills and compares them with the skills required for a target job role.

The system identifies missing skills and categorizes them based on priority. It also provides a roadmap to help users improve their skills for their desired career.

---

Skill-Gap-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── skill_extractor.py
│   ├── analyzer.py
│   └── roadmap.py
│
├── data/
│   └── skills.csv
│
└── screenshots/
    ├── home.png
    ├── analysis.png
    ├── missing-skills.png
    └── roadmap.png

## 🎯 Problem Statement

Students and job seekers often do not know which skills they are missing for a particular job role.

This project helps users identify the gap between their current skills and the skills required by industry job roles.

---

## 🎯 Objective

The main objectives of this project are:

- Analyze the user's existing skills.
- Identify skills required for a target job role.
- Find missing skills.
- Categorize missing skills based on priority.
- Provide a personalized learning roadmap.
- Help students prepare for placements and careers.

---

## ✨ Features

- 📄 Resume/skill analysis
- 🔍 Skill extraction
- 🎯 Job-role based skill comparison
- ❌ Missing skill detection
- 🔴 High / 🟡 Medium / 🟢 Low priority classification
- 📚 Learning roadmap generation
- 📊 Skill gap analysis
- 💻 User-friendly interface

---

## 🛠️ Technologies Used

- Python
- Machine Learning
- Natural Language Processing (NLP)
- Pandas
- NumPy
- Scikit-learn
- Git
- GitHub
- 🧪 Testing

The project was tested using different skill sets and job roles.

Example

Existing Skills:

Python
Machine Learning
Deep Learning
Git
PyTorch
Docker

Missing Skills:

🔴 High Priority
Data Structures
🟡 Medium Priority
Natural Language Processing
REST API
TensorFlow
🟢 Low Priority
Cloud Computing
MLOps
⚠️ Limitations
Skill detection depends on the available skill dataset.
The system may not identify every possible skill.
Job requirements can change over time.
Learning recommendations may need further personalization.
The current system may have limited job-role coverage.

🔮 Future Improvements
Add more job roles.
Improve NLP-based skill extraction.
Add AI-powered resume analysis.
Integrate real-time job postings.
Add personalized course recommendations.
Add LinkedIn profile analysis.
Add cloud deployment.
Improve recommendation accuracy.
Add user authentication and profiles.

👩‍💻 Author

Aishwarya M C

🎓 AIML Engineering Student
📍 Aditya College of Engineering and Technology
🎯 Aspiring AI Engineer / Software Developer

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.


---

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Skill Analysis

![Skill Analysis](screenshots/analysis.png)

### Missing Skills

![Missing Skills](screenshots/missing-skills.png)

### Learning Roadmap

![Learning Roadmap](screenshots/roadmap.png) 

COMPARE Python,SQL vs ML Engineer
Start the program:
cd skill-gap-analyzer
python3 main.py
Select:
1. Analyze skills
Enter the details:
Candidate name:        [press Enter]
Target role:           Machine Learning Engineer
Candidate skills:      Python, SQL
The application normalizes the skills and compares them with the role profile.
Comparison result
Required skills for Machine Learning Engineer:

Python
SQL
NumPy
Pandas
Statistics
Machine Learning
Scikit-learn
Git
Matched required skills:

Python
SQL
Missing required skills:

NumPy
Pandas
Statistics
Machine Learning
Scikit-learn
Git
Missing optional skills:

Deep Learning
TensorFlow or PyTorch
Docker
Cloud fundamentals
Match calculation
Only required skills affect the score:

Matched required skills / Total required skills × 100
2 / 8 × 100 = 25.00%
Assessment:

Needs Improvement
Priority ordering
The application prioritizes gaps using the project’s educational rule:

High priority: foundational machine-learning concepts
Medium priority: supporting tools
Low priority: optional deployment and cloud skills
Result:

HIGH PRIORITY:
1. Machine Learning
2. Statistics
3. Scikit-learn

MEDIUM PRIORITY:
4. NumPy
5. Pandas
6. Git

LOW PRIORITY:
7. Deep Learning
8. TensorFlow or PyTorch
9. Docker
10. Cloud fundamentals

---

## ⚙️ Installation / Setup

### 1. Clone the repository

```bash
git clone [YOUR_GITHUB_REPOSITORY_URL]
