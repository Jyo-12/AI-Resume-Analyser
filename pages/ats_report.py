import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.ats_engine import generate_ats_report


# ==========================================================
# ATS REPORT PAGE
# ==========================================================

def ats_report_page():

    st.title("📄 AI ATS Resume Report")

    st.markdown(
        """
        Analyze your resume using our AI-powered ATS engine.
        View resume score, strengths, weaknesses and optimization tips.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # Check Resume
    # --------------------------------------------------------

    if "resume_text" not in st.session_state:

        st.warning("⚠ Please upload and analyze a resume first.")

        return

    resume_text = st.session_state["resume_text"]

    report = generate_ats_report(resume_text)

    # --------------------------------------------------------
    # Overall ATS Score
    # --------------------------------------------------------

    score = report["overall_score"]

    c1, c2 = st.columns([1, 2])

    with c1:

        st.metric(
            "ATS Score",
            f"{score}/100"
        )

    with c2:

        if score >= 85:
            st.success("Excellent ATS Compatibility")

        elif score >= 70:
            st.info("Good Resume")

        elif score >= 50:
            st.warning("Needs Improvement")

        else:
            st.error("Poor ATS Compatibility")

    st.divider()

    # --------------------------------------------------------
    # ATS Gauge
    # --------------------------------------------------------

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            number={"suffix": "/100"},

            title={"text": "ATS Compatibility Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "green"},

                "steps": [

                    {"range": [0, 40], "color": "#ffcccc"},

                    {"range": [40, 70], "color": "#ffe699"},

                    {"range": [70, 100], "color": "#c6efce"}

                ]

            }

        )

    )

    st.plotly_chart(

        gauge,

        use_container_width=True

    )

    st.divider()

    # --------------------------------------------------------
    # Score Breakdown
    # --------------------------------------------------------

    st.subheader("📊 Score Breakdown")

    breakdown = pd.DataFrame({

        "Category": [

            "Contact",

            "Sections",

            "Education",

            "Skills",

            "Experience",

            "Projects",

            "Certifications",

            "Keywords"

        ],

        "Score": [

            report["contact_score"],

            report["section_score"],

            report["education_score"],

            report["skill_score"],

            report["experience_score"],

            report["project_score"],

            report["certification_score"],

            report["keyword_score"]

        ]

    })

    fig = px.bar(

        breakdown,

        x="Category",

        y="Score",

        color="Score",

        text="Score"

    )

    fig.update_layout(

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.dataframe(

        breakdown,

        use_container_width=True,

        hide_index=True

    )
    # ==========================================================
    # CONTACT INFORMATION
    # ==========================================================

    st.divider()

    st.subheader("📞 Contact Information")

    contact = report["contact_info"]

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "📧 Email",
            value=contact.get("email", "") or "Not Found",
            disabled=True
        )

        st.text_input(
            "📱 Phone",
            value=contact.get("phone", "") or "Not Found",
            disabled=True
        )

    with col2:

        st.text_input(
            "💼 LinkedIn",
            value=contact.get("linkedin", "") or "Not Found",
            disabled=True
        )

        st.text_input(
            "🐙 GitHub",
            value=contact.get("github", "") or "Not Found",
            disabled=True
        )

    # ==========================================================
    # RESUME SECTIONS
    # ==========================================================

    st.divider()

    st.subheader("📂 Resume Sections Detected")

    sections = report["found_sections"]

    if sections:

        cols = st.columns(3)

        for index, section in enumerate(sections):

            with cols[index % 3]:

                st.success(f"✅ {section.title()}")

    else:

        st.error("No standard resume sections detected.")

    # ==========================================================
    # SKILLS
    # ==========================================================

    st.divider()

    st.subheader("💻 Technical Skills Detected")

    skills = report["detected_skills"]

    if len(skills):

        skill_columns = st.columns(4)

        for index, skill in enumerate(sorted(skills)):

            with skill_columns[index % 4]:

                st.info(skill)

    else:

        st.warning("No technical skills detected.")

    # ==========================================================
    # ATS KEYWORDS
    # ==========================================================

    st.divider()

    st.subheader("🔑 ATS Keywords Matched")

    keywords = report["matched_keywords"]

    if len(keywords):

        keyword_cols = st.columns(4)

        for index, keyword in enumerate(sorted(keywords)):

            with keyword_cols[index % 4]:

                st.success(keyword)

    else:

        st.error("No ATS keywords matched.")

    # ==========================================================
    # STRENGTHS
    # ==========================================================

    st.divider()

    st.subheader("💪 Resume Strengths")

    strengths = report["strengths"]

    if strengths:

        for item in strengths:

            st.success(f"✅ {item}")

    else:

        st.info("No major strengths detected.")

    # ==========================================================
    # IMPROVEMENTS
    # ==========================================================

    st.divider()

    st.subheader("📝 Suggested Improvements")

    improvements = report["improvements"]

    if improvements:

        for item in improvements:

            st.warning(f"⚠ {item}")

    else:

        st.success("Excellent resume. No major improvements required.")

    # ==========================================================
    # SUMMARY CARD
    # ==========================================================

    st.divider()

    st.subheader("📋 ATS Summary")

    summary = f"""
Overall ATS Score : {report['overall_score']}/100

Contact Score : {report['contact_score']}

Section Score : {report['section_score']}

Education Score : {report['education_score']}

Skill Score : {report['skill_score']}

Experience Score : {report['experience_score']}

Project Score : {report['project_score']}

Certification Score : {report['certification_score']}

Keyword Score : {report['keyword_score']}
"""

    st.code(summary)

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    st.download_button(

        label="📥 Download ATS Report",

        data=summary,

        file_name="ATS_Report.txt",

        mime="text/plain"

    )

    # ==========================================================
    # FINAL MESSAGE
    # ==========================================================

    st.divider()

    st.success(
        """
🎉 ATS analysis completed successfully.

You can now proceed to:

• 💼 Job Recommendation

• 📚 Course Recommendation

• 💰 Salary Prediction

• 🎤 Interview Preparation

• 🤖 AI Career Coach
"""
    )