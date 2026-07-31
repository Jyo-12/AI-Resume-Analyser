import streamlit as st
import pandas as pd
import plotly.express as px

from utils.interview_engine import (
    recommend_interview_questions,
    interview_readiness_score,
    readiness_level,
    interview_preparation_summary,
    interview_skill_gap_analysis,
    recommend_best_questions,
)


# ==========================================================
# INTERVIEW PREPARATION PAGE
# ==========================================================

def interview_preparation_page():
    st.title("🎯 AI Interview Preparation")

    st.markdown(
        """
Prepare for your dream job with AI-powered interview questions,
skill-gap analysis and interview readiness insights.
"""
    )

    st.divider()

    # ------------------------------------------------------
    # Session State Check for Skills
    # ------------------------------------------------------
    if "skills" not in st.session_state:
        st.warning("Please analyze your resume first.")
        return

    candidate_skills = st.session_state["skills"]

    # ------------------------------------------------------
    # User Inputs
    # ------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        job_role = st.text_input(
            "Target Job Role",
            placeholder="Data Scientist"
        )

    with col2:
        difficulty = st.selectbox(
            "Difficulty",
            ["All", "Easy", "Medium", "Hard"]
        )

    question_type = st.selectbox(
        "Question Type",
        [
            "All",
            "Technical",
            "Coding",
            "Scenario",
            "Behavioral",
            "HR",
            "Aptitude",
        ]
    )

    total_questions = st.slider(
        "Number of Questions",
        5,
        50,
        20
    )

    # ------------------------------------------------------
    # Action Button
    # ------------------------------------------------------
    if st.button("🚀 Generate Interview Plan", use_container_width=True):
        if not job_role.strip():
            st.error("Please enter a Target Job Role to generate your interview plan.")
            return

        with st.spinner("Preparing interview roadmap..."):
            selected_difficulty = None if difficulty == "All" else difficulty
            selected_type = None if question_type == "All" else question_type

            questions = recommend_interview_questions(
                job_role=job_role,
                candidate_skills=candidate_skills,
                difficulty=selected_difficulty,
                question_type=selected_type,
                top_n=total_questions,
            )

            readiness_score = interview_readiness_score(
                job_role, candidate_skills, selected_difficulty
            )

            readiness = readiness_level(readiness_score)

            summary = interview_preparation_summary(
                job_role, candidate_skills
            )

            gap_analysis = interview_skill_gap_analysis(
                job_role, candidate_skills
            )

            best_questions = recommend_best_questions(
                job_role, candidate_skills, top_n=5
            )

            st.session_state["interview_questions"] = questions
            st.session_state["interview_summary"] = summary
            st.session_state["gap_analysis"] = gap_analysis
            st.session_state["readiness_score"] = readiness_score
            st.session_state["readiness_level"] = readiness
            st.session_state["best_questions"] = best_questions
            st.session_state["target_job_role"] = job_role

    # ------------------------------------------------------
    # Guard Check for Results
    # ------------------------------------------------------
    if "interview_questions" not in st.session_state:
        return

    questions = st.session_state["interview_questions"]
    summary = st.session_state.get("interview_summary", {})
    gap = st.session_state.get("gap_analysis", {})
    readiness_score = st.session_state.get("readiness_score", 0)
    readiness_level_text = st.session_state.get("readiness_level", "N/A")
    best_questions = st.session_state.get("best_questions")
    current_role = st.session_state.get("target_job_role", job_role)

    # ==========================================================
    # DASHBOARD METRICS
    # ==========================================================
    st.subheader("📊 Interview Readiness Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Readiness", f"{readiness_score}%")
    c2.metric("Level", readiness_level_text)
    c3.metric("Coverage", f"{summary.get('Coverage', 0)}%")
    c4.metric("Questions", len(questions) if isinstance(questions, pd.DataFrame) else 0)

    st.divider()

    # ==========================================================
    # OVERVIEW
    # ==========================================================
    st.subheader("📈 Preparation Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"""
### 🎯 Preparation Status

**{summary.get('Preparation_Status', 'In Progress')}**
"""
        )

        matched_skills_count = (
            len(gap.get("Matched_Skills", []))
            if isinstance(gap.get("Matched_Skills"), list)
            else summary.get("Matched_Skills", 0)
        )
        missing_skills_count = (
            len(gap.get("Missing_Skills", []))
            if isinstance(gap.get("Missing_Skills"), list)
            else summary.get("Missing_Skills", 0)
        )

        st.metric("Matched Skills", matched_skills_count)
        st.metric("Missing Skills", missing_skills_count)

    with col2:
        gauge_df = pd.DataFrame(
            {
                "Metric": ["Coverage", "Gap"],
                "Percentage": [
                    gap.get("Coverage", 0),
                    gap.get("Gap", 0),
                ],
            }
        )

        fig = px.bar(
            gauge_df,
            x="Metric",
            y="Percentage",
            color="Metric",
            text="Percentage",
        )

        fig.update_layout(height=350, yaxis_title="Percentage")

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # TOP RECOMMENDED QUESTIONS
    # ==========================================================
    st.subheader("⭐ Top Recommended Questions")

    if isinstance(best_questions, pd.DataFrame) and best_questions.empty:
        st.warning("No interview questions found for the selected job role.")
    elif isinstance(best_questions, pd.DataFrame):
        for index, row in best_questions.iterrows():
            with st.expander(
                f"⭐ Question {index+1} • Score : {row.get('Recommendation_Score', 0)}%",
                expanded=(index == 0),
            ):
                st.markdown(f"### ❓ {row.get('Question', '')}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Skill :** {row.get('Skill', '')}")
                    st.write(f"**Difficulty :** {row.get('Difficulty', '')}")

                with col2:
                    st.write(f"**Question Type :** {row.get('Question_Type', '')}")
                    st.write(f"**Skill Match :** {row.get('Skill_Match_%', 0)}%")

                st.markdown("### ✅ Expected Key Points")
                st.success(row.get("Expected_Key_Points", "N/A"))

                st.markdown("### 💬 Sample Answer")
                st.info(row.get("Sample_Answer", "N/A"))

                st.markdown("### 🎯 Matched Skills")
                matched = row.get("Matched_Skills", [])
                if matched:
                    st.success(", ".join(matched) if isinstance(matched, list) else str(matched))
                else:
                    st.write("None")

                st.markdown("### 📚 Missing Skills")
                missing = row.get("Missing_Skills", [])
                if missing:
                    st.warning(", ".join(missing) if isinstance(missing, list) else str(missing))
                else:
                    st.success("No missing skills.")

    # ==========================================================
    # ALL RECOMMENDED QUESTIONS
    # ==========================================================
    st.divider()

    st.subheader("📚 Complete Interview Question Bank")

    if isinstance(questions, pd.DataFrame) and not questions.empty:
        req_cols = [
            "Skill",
            "Difficulty",
            "Question_Type",
            "Recommendation_Score",
            "Skill_Match_%",
        ]
        available_cols = [c for c in req_cols if c in questions.columns]
        display_df = questions[available_cols].copy()

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
        )

        # ==========================================================
        # RECOMMENDATION SCORE CHART
        # ==========================================================
        st.divider()

        st.subheader("📈 Question Recommendation Scores")

        score_chart = questions.copy()
        score_chart["Question_No"] = [
            f"Q{i}" for i in range(1, len(score_chart) + 1)
        ]

        fig = px.bar(
            score_chart,
            x="Question_No",
            y="Recommendation_Score" if "Recommendation_Score" in score_chart.columns else None,
            color="Difficulty" if "Difficulty" in score_chart.columns else None,
            text="Recommendation_Score" if "Recommendation_Score" in score_chart.columns else None,
            hover_data=[c for c in ["Skill", "Question_Type"] if c in score_chart.columns],
        )

        fig.update_layout(
            height=450,
            xaxis_title="Interview Questions",
            yaxis_title="Recommendation Score (%)",
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================================================
        # SEARCH QUESTIONS
        # ==========================================================
        st.divider()

        st.subheader("🔍 Search Interview Questions")

        search_text = st.text_input(
            "Search Question", placeholder="Search by keyword..."
        )

        if search_text and "Question" in questions.columns:
            filtered = questions[
                questions["Question"].str.contains(
                    search_text, case=False, na=False
                )
            ]
        else:
            filtered = questions

        st.write(f"**Total Questions : {len(filtered)}**")

        # ==========================================================
        # EXPANDABLE QUESTION CARDS
        # ==========================================================
        for i, row in filtered.reset_index(drop=True).iterrows():
            with st.expander(
                f"Question {i+1} • {row.get('Skill', 'General')} • {row.get('Difficulty', 'N/A')}"
            ):
                st.markdown(f"### ❓ {row.get('Question', '')}")
                st.write(f"**Recommendation Score:** {row.get('Recommendation_Score', 0)}%")
                st.write(f"**Question Type:** {row.get('Question_Type', '')}")
                st.write(f"**Skill Match:** {row.get('Skill_Match_%', 0)}%")

                st.markdown("### ✅ Expected Key Points")
                st.success(row.get("Expected_Key_Points", "N/A"))

                st.markdown("### 💬 Sample Answer")
                st.info(row.get("Sample_Answer", "N/A"))

    st.divider()

    # ==========================================================
    # SKILL GAP ANALYSIS
    # ==========================================================
    st.subheader("🧠 Interview Skill Gap Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Coverage", f"{gap.get('Coverage', 0)}%")

    with col2:
        st.metric("Gap", f"{gap.get('Gap', 0)}%")

    coverage_df = pd.DataFrame(
        {
            "Category": ["Coverage", "Gap"],
            "Percentage": [gap.get("Coverage", 0), gap.get("Gap", 0)],
        }
    )

    fig = px.pie(
        coverage_df,
        names="Category",
        values="Percentage",
        hole=0.45,
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==========================================================
    # REQUIRED SKILLS
    # ==========================================================
    st.divider()

    st.subheader("📚 Required Interview Skills")

    req_skills = gap.get("Required_Skills", [])
    if req_skills:
        required_df = pd.DataFrame({"Required Skills": req_skills})
        st.dataframe(
            required_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No required skills available.")

    # ==========================================================
    # MATCHED AND MISSING SKILLS
    # ==========================================================
    st.divider()

    col1, col2 = st.columns(2)

    matched_list = gap.get("Matched_Skills", [])
    missing_list = gap.get("Missing_Skills", [])

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_list:
            for skill in matched_list:
                st.success(skill)
        else:
            st.info("No matched skills.")

    with col2:
        st.subheader("⚠ Missing Skills")
        if missing_list:
            for skill in missing_list:
                st.warning(skill)
        else:
            st.success("Excellent! No missing skills.")

    # ==========================================================
    # STRONG VS WEAK SKILL VISUALIZATION
    # ==========================================================
    st.divider()

    chart_df = pd.DataFrame(
        {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [len(matched_list), len(missing_list)],
        }
    )

    fig = px.bar(
        chart_df,
        x="Category",
        y="Count",
        color="Category",
        text="Count",
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

    # ==========================================================
    # INTERVIEW ROADMAP
    # ==========================================================
    st.divider()

    st.subheader("🛣 Personalized Interview Roadmap")

    roadmap = []
    for priority, skill in enumerate(missing_list, start=1):
        roadmap.append(
            {
                "Priority": priority,
                "Skill": skill,
                "Action": f"Study {skill}, solve interview questions and build one project.",
            }
        )

    roadmap_df = pd.DataFrame(roadmap)

    if roadmap_df.empty:
        st.success("Your interview roadmap is complete.")
    else:
        st.dataframe(
            roadmap_df,
            use_container_width=True,
            hide_index=True,
        )

    # ==========================================================
    # WEEKLY PREPARATION PLAN
    # ==========================================================
    st.divider()

    st.subheader("📅 Weekly Preparation Plan")

    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekly_plan = []
    for i, day in enumerate(week_days):
        if i < len(missing_list):
            topic = missing_list[i]
        else:
            topic = "Mock Interview Practice"

        weekly_plan.append({"Day": day, "Focus": topic})

    weekly_df = pd.DataFrame(weekly_plan)

    st.dataframe(
        weekly_df,
        hide_index=True,
        use_container_width=True,
    )

    # ==========================================================
    # PREPARATION SUMMARY
    # ==========================================================
    st.divider()

    st.subheader("📈 Preparation Summary")

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Coverage",
                "Gap",
                "Matched Skills",
                "Missing Skills",
            ],
            "Value": [
                summary.get("Coverage", 0),
                summary.get("Gap", 0),
                summary.get("Matched_Skills", len(matched_list)),
                summary.get("Missing_Skills", len(missing_list)),
            ],
        }
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
    )

    fig = px.bar(
        summary_df,
        x="Metric",
        y="Value",
        color="Metric",
        text="Value",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(
        f"""
### 🎯 Current Interview Status

**Preparation Status:** {summary.get('Preparation_Status', 'In Progress')}

**Readiness Level:** {summary.get('Readiness_Level', readiness_level_text)}

Keep improving the missing skills and continue practicing interview questions every day.
"""
    )

    st.divider()

    # ==========================================================
    # MOCK INTERVIEW PLANNER
    # ==========================================================
    st.subheader("🎤 AI Mock Interview Planner")

    if isinstance(questions, pd.DataFrame) and not questions.empty:
        mock_df = questions.copy()
        mock_df.insert(0, "Question_No", range(1, len(mock_df) + 1))
        mock_df["Candidate_Score"] = 0
        mock_df["Max_Score"] = 10
        mock_df["Status"] = "Not Attempted"

        valid_cols = [
            c for c in ["Question_No", "Skill", "Difficulty", "Question_Type", "Status"]
            if c in mock_df.columns
        ]

        st.dataframe(
            mock_df[valid_cols],
            hide_index=True,
            use_container_width=True,
        )

        total_questions_count = len(mock_df)
        max_score = total_questions_count * 10
    else:
        total_questions_count = 0
        max_score = 0

    # ==========================================================
    # MOCK INTERVIEW SUMMARY
    # ==========================================================
    st.divider()

    st.subheader("📊 Mock Interview Summary")

    obtained_score = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Questions", total_questions_count)
    col2.metric("Maximum Score", max_score)
    col3.metric("Current Score", obtained_score)

    # ==========================================================
    # AI COACHING
    # ==========================================================
    st.divider()

    st.subheader("🤖 AI Interview Coach")

    confidence = summary.get("Coverage", 0)

    if confidence >= 90:
        confidence_level = "Very High"
    elif confidence >= 80:
        confidence_level = "High"
    elif confidence >= 70:
        confidence_level = "Moderate"
    elif confidence >= 60:
        confidence_level = "Low"
    else:
        confidence_level = "Very Low"

    c1, c2 = st.columns(2)
    c1.metric("Confidence Score", f"{confidence}%")
    c2.metric("Confidence Level", confidence_level)

    # ==========================================================
    # COACHING TIPS
    # ==========================================================
    st.divider()

    st.subheader("💡 Personalized Coaching Tips")

    if confidence >= 90:
        tips = [
            "Revise company-specific interview rounds.",
            "Continue solving advanced interview questions.",
            "Review your projects before interviews.",
            "Practice leadership and behavioral questions.",
        ]
    elif confidence >= 75:
        tips = [
            "Practice SQL and Python daily.",
            "Strengthen system design knowledge.",
            "Improve STAR-based behavioral answers.",
            "Practice explaining projects clearly.",
        ]
    elif confidence >= 60:
        tips = [
            "Focus on missing technical skills.",
            "Practice coding interview questions.",
            "Attend mock interviews.",
            "Improve communication skills.",
        ]
    else:
        tips = [
            "Complete core technical topics first.",
            "Study interview fundamentals.",
            "Revise resume projects.",
            "Practice HR interview questions every day.",
        ]

    for tip in tips:
        st.info(tip)

    # ==========================================================
    # RECOMMENDED NEXT STEPS
    # ==========================================================
    st.divider()

    st.subheader("🚀 Next Preparation Steps")

    if missing_list:
        for i, skill in enumerate(missing_list, start=1):
            st.success(f"{i}. Learn **{skill}** and solve interview questions.")
    else:
        st.success("Excellent! You have covered all required interview skills.")

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================
    st.divider()

    report_lines = [
        "=" * 70,
        "AI INTERVIEW PREPARATION REPORT",
        "=" * 70,
        "",
        f"Target Role : {current_role}",
        "",
        f"Readiness Score : {readiness_score}%",
        f"Readiness Level : {readiness_level_text}",
        "",
        f"Coverage : {summary.get('Coverage', 0)}%",
        f"Gap : {summary.get('Gap', 0)}%",
        "",
        f"Preparation Status : {summary.get('Preparation_Status', 'In Progress')}",
        "",
        "Matched Skills",
    ]

    for skill in matched_list:
        report_lines.append(f"✓ {skill}")

    report_lines.append("")
    report_lines.append("Missing Skills")

    for skill in missing_list:
        report_lines.append(f"• {skill}")

    report_lines.append("")
    report_lines.append("Coaching Tips")

    for tip in tips:
        report_lines.append(f"- {tip}")

    report_lines.append("")
    report_lines.append("Weekly Plan")

    for _, row in weekly_df.iterrows():
        report_lines.append(f"{row['Day']} : {row['Focus']}")

    report_lines.append("")
    report_lines.append("=" * 70)

    report_text = "\n".join(report_lines)

    st.download_button(
        "📥 Download Interview Report",
        report_text,
        file_name="Interview_Preparation_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # ==========================================================
    # FINAL SUMMARY
    # ==========================================================
    st.divider()

    st.success(
        f"""
## 🎉 Interview Preparation Completed Successfully!

### 📌 Current Readiness

**Role:** {current_role}

**Readiness:** {readiness_score}%

**Preparation Status:** {summary.get('Preparation_Status', 'In Progress')}

**Coverage:** {summary.get('Coverage', 0)}%

**Missing Skills Count:** {len(missing_list)}

### 🚀 You're now ready to:

✅ Practice technical interviews

✅ Prepare HR interview answers

✅ Revise your projects

✅ Improve weak interview topics

✅ Take mock interviews

Best wishes for your upcoming interviews! 🌟
"""
    )