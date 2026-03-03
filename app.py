from flask import Flask, render_template, request
import json
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

# Load skills
with open("skills.json") as f:
    skills_data = json.load(f)
    required_skills = [skill.lower() for skill in skills_data["required_skills"]]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # Get form data
    user_skills = request.form["skills"].split(",")
    job_role = request.form["job_role"]

    # Clean user skills
    user_skills = [skill.strip().lower() for skill in user_skills]

    # Match skills
    matched = []
    for skill in user_skills:
        if skill in required_skills:
            matched.append(skill)

    # Calculate score
    if len(required_skills) > 0:
        score = int((len(matched) / len(required_skills)) * 100)
    else:
        score = 0

    # Feedback logic
    if score >= 75:
        feedback = "Excellent profile! You are interview ready."
    elif score >= 50:
        feedback = "Good profile. Improve a few more relevant skills."
    else:
        feedback = "Consider adding more relevant skills to strengthen your resume."

    # (Optional) Add to blockchain
    blockchain.chain.append({
        "job_role": job_role,
        "matched_skills": matched,
        "score": score
    })

    return render_template(
        "result.html",
        matched=matched,
        score=score,
        job_role=job_role,
        feedback=feedback
    )

if __name__ == "__main__":
    app.run(debug=True)