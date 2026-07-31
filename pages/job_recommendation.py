import streamlit as st
import pandas as pd
import plotly.express as px

from utils.job_engine import (
    generate_job_report,
    format_job_report,
    search_jobs
)


# ==========================================================
# JOB RECOMMENDATION PAGE
# ==========================================================

def job_recommendation_page():

    st.title("💼 AI Job Recommendation")

    st.markdown(
        """
        Discover the best matching jobs based on your resume,
        skills, education and experience.
        """
    )

    st.divider()

    # ------------------------------------------------------
    # Resume Validation
    # ------------------------------------------------------

    if "skills" not in st.session_state:

        st.warning(
            "Please analyze your resume first."
        )

        return

    skills = st.session_state["skills"]

    # ------------------------------------------------------
    # Candidate Information
    # ------------------------------------------------------

    st.subheader("Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        experience = st.number_input(

            "Years of Experience",

            min_value=0,

            max_value=40,

            value=0

        )

    with col2:

        education = st.selectbox(

            "Highest Qualification",

            [

                "B.E",

                "B.Tech",

                "M.Tech",

                "B.Sc",

                "M.Sc",

                "MBA",

                "PhD",

                "Diploma",

                "Other"

            ]

        )

    st.divider()

    # ------------------------------------------------------
    # Generate Recommendation
    # ------------------------------------------------------

    if st.button(

        "🚀 Generate Job Recommendations",

        use_container_width=True

    ):

        with st.spinner(

            "Finding the best jobs..."

        ):

            report = generate_job_report(

                candidate_skills=skills,

                candidate_experience=experience,

                candidate_education=education,

                top_n=10

            )

            dashboard = format_job_report(report)

        st.session_state["job_dashboard"] = dashboard

    if "job_dashboard" not in st.session_state:

        return

    dashboard = st.session_state["job_dashboard"]

    summary = dashboard["summary"]

    best_job = dashboard["best_job"]

    recommendations = dashboard["recommendations"]

    statistics = dashboard["statistics"]

    career_advice = dashboard["career_advice"]

    roadmap = dashboard["roadmap"]

    skill_gap = dashboard["skill_gap"]

    # ------------------------------------------------------
    # Dashboard Metrics
    # ------------------------------------------------------

    st.subheader("Recommendation Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Jobs Found",

        summary["total_jobs"]

    )

    c2.metric(

        "Average Match",

        f"{summary['average_score']} %"

    )

    c3.metric(

        "Best Match",

        f"{summary['highest_score']} %"

    )

    st.divider()

    # ------------------------------------------------------
    # Best Job Card
    # ------------------------------------------------------

    st.subheader("🏆 Best Job Match")

    st.success(

        f"""
### {best_job['job_title']}

**Company:** {best_job['company']}

**Location:** {best_job['location']}

**Salary:** {best_job['salary']}

**Experience:** {best_job['experience']}

**Employment Type:** {best_job['employment_type']}

**Match Score:** {best_job['overall_score']} %

**Confidence:** {best_job['confidence']}
"""
    )

    st.divider()
    # ==========================================================
    # SEARCH RECOMMENDED JOBS
    # ==========================================================

    st.subheader("🔍 Search Recommended Jobs")

    search_keyword = st.text_input(
        "Search by Job Title, Company or Location"
    )

    display_jobs = recommendations

    if search_keyword.strip():

        display_jobs = search_jobs(
            search_keyword,
            recommendations
        )

    # ==========================================================
    # JOB RECOMMENDATION TABLE
    # ==========================================================

    st.divider()

    st.subheader("💼 Recommended Jobs")

    if len(display_jobs) == 0:

        st.warning("No matching jobs found.")

    else:

        jobs_df = pd.DataFrame([
            {
                "Job Title": job["job_title"],
                "Company": job["company"],
                "Location": job["location"],
                "Salary": job["salary"],
                "Experience": job["experience"],
                "Match %": job["overall_score"],
                "Confidence": job["confidence"]
            }

            for job in display_jobs
        ])

        st.dataframe(

            jobs_df,

            hide_index=True,

            use_container_width=True

        )

    # ==========================================================
    # MATCH SCORE CHART
    # ==========================================================

    st.divider()

    st.subheader("📊 Job Match Scores")

    chart_df = pd.DataFrame([

        {

            "Job": job["job_title"],

            "Score": job["overall_score"]

        }

        for job in display_jobs

    ])

    fig = px.bar(

        chart_df,

        x="Job",

        y="Score",

        text="Score",

        color="Score"

    )

    fig.update_layout(

        height=450,

        xaxis_title="Job Title",

        yaxis_title="Match Score (%)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # CAREER ADVICE
    # ==========================================================

    st.divider()

    st.subheader("🎯 Personalized Career Advice")

    for advice in career_advice:

        st.info(advice)

    # ==========================================================
    # SKILL GAP ANALYSIS
    # ==========================================================

    st.divider()

    st.subheader("📈 Skill Gap Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Completion",

            f"{skill_gap['completion_percentage']}%"

        )

    with col2:

        st.metric(

            "Matched Skills",

            len(skill_gap["matched"])

        )

    st.markdown("### ✅ Matched Skills")

    if skill_gap["matched"]:

        cols = st.columns(4)

        for i, skill in enumerate(skill_gap["matched"]):

            with cols[i % 4]:

                st.success(skill)

    else:

        st.warning("No matched skills found.")

    st.markdown("### ❌ Missing Required Skills")

    if skill_gap["missing_required"]:

        cols = st.columns(4)

        for i, skill in enumerate(skill_gap["missing_required"]):

            with cols[i % 4]:

                st.error(skill)

    else:

        st.success("No required skill gaps!")

    st.markdown("### ⭐ Missing Preferred Skills")

    if skill_gap["missing_preferred"]:

        cols = st.columns(4)

        for i, skill in enumerate(skill_gap["missing_preferred"]):

            with cols[i % 4]:

                st.warning(skill)

    else:

        st.success("All preferred skills matched.")

    # ==========================================================
    # IMPROVEMENT ROADMAP
    # ==========================================================

    st.divider()

    st.subheader("🛣️ Improvement Roadmap")

    for step in roadmap:

        st.write(f"✅ {step}")
    # ==========================================================
    # RECOMMENDATION STATISTICS
    # ==========================================================

    st.divider()

    st.subheader("📊 Recommendation Statistics")

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Highest Score",
        f"{statistics['highest_score']}%"
    )

    s2.metric(
        "Average Score",
        f"{statistics['average_score']}%"
    )

    s3.metric(
        "Lowest Score",
        f"{statistics['lowest_score']}%"
    )

    confidence_df = pd.DataFrame({

        "Confidence": [

            "Excellent",
            "Strong",
            "Moderate",
            "Weak",
            "Poor"

        ],

        "Jobs": [

            statistics["excellent"],
            statistics["strong"],
            statistics["moderate"],
            statistics["weak"],
            statistics["poor"]

        ]

    })

    fig = px.pie(

        confidence_df,

        names="Confidence",

        values="Jobs",

        title="Recommendation Confidence Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # DETAILED JOB CARDS
    # ==========================================================

    st.divider()

    st.subheader("📋 Detailed Job Recommendations")

    for index, job in enumerate(display_jobs, start=1):

        with st.expander(

            f"{index}. {job['job_title']} ({job['overall_score']}%)",

            expanded=False

        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**🏢 Company:** {job['company']}")

                st.write(f"**📍 Location:** {job['location']}")

                st.write(f"**💰 Salary:** {job['salary']}")

                st.write(f"**💼 Employment:** {job['employment_type']}")

            with col2:

                st.write(f"**🎯 Match Score:** {job['overall_score']} %")

                st.write(f"**📈 Confidence:** {job['confidence']}")

                st.write(f"**🧑‍💻 Experience:** {job['experience']}")

                st.write(f"**🎓 Education:** {job['education']}")

            st.markdown("### ✅ Matched Required Skills")

            if job["matched_required"]:

                st.write(", ".join(job["matched_required"]))

            else:

                st.write("None")

            st.markdown("### ⭐ Matched Preferred Skills")

            if job["matched_preferred"]:

                st.write(", ".join(job["matched_preferred"]))

            else:

                st.write("None")

            st.markdown("### ❌ Missing Required Skills")

            if job["missing_required"]:

                st.write(", ".join(job["missing_required"]))

            else:

                st.success("No missing required skills.")

            st.markdown("### ⚠ Missing Preferred Skills")

            if job["missing_preferred"]:

                st.write(", ".join(job["missing_preferred"]))

            else:

                st.success("No missing preferred skills.")

            st.markdown("### 💡 Recommendation Reason")

            for reason in job["recommendation_reason"]:

                st.info(reason)

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    st.divider()

    report_text = []

    report_text.append("=" * 60)
    report_text.append("AI JOB RECOMMENDATION REPORT")
    report_text.append("=" * 60)
    report_text.append("")

    report_text.append(
        f"Total Recommendations : {summary['total_jobs']}"
    )

    report_text.append(
        f"Average Match Score : {summary['average_score']}%"
    )

    report_text.append(
        f"Highest Match Score : {summary['highest_score']}%"
    )

    report_text.append("")

    report_text.append("BEST MATCH")

    report_text.append(
        f"Job : {best_job['job_title']}"
    )

    report_text.append(
        f"Company : {best_job['company']}"
    )

    report_text.append(
        f"Location : {best_job['location']}"
    )

    report_text.append(
        f"Match Score : {best_job['overall_score']}%"
    )

    report_text.append("")

    report_text.append("CAREER ADVICE")

    for advice in career_advice:

        report_text.append(f"- {advice}")

    report_text.append("")

    report_text.append("IMPROVEMENT ROADMAP")

    for step in roadmap:

        report_text.append(step)

    report_text.append("")
    report_text.append("=" * 60)

    report_string = "\n".join(report_text)

    st.download_button(

        label="📥 Download Job Recommendation Report",

        data=report_string,

        file_name="Job_Recommendation_Report.txt",

        mime="text/plain",

        use_container_width=True

    )

    # ==========================================================
    # COMPLETION MESSAGE
    # ==========================================================

    st.divider()

    st.success(
        """
🎉 Job recommendations generated successfully!

You can now continue with:

✅ Course Recommendation

✅ Salary Prediction

✅ Interview Preparation

✅ AI Career Coach
"""
    )