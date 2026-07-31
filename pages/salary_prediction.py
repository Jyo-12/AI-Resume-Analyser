import streamlit as st
import pandas as pd
import plotly.express as px

from utils.salary_engine import (
    generate_salary_report,
    predict_salary,
    estimate_growth,
    salary_insights,
    compare_locations,
    compare_company_types
)

# ==========================================================
# SALARY PREDICTION PAGE
# ==========================================================

def salary_prediction_page():

    st.title("💰 AI Salary Prediction")

    st.markdown(
        """
        Predict your expected salary based on
        your resume, skills and experience.
        """
    )

    st.divider()

    # ------------------------------------------------------

    if "skills" not in st.session_state:

        st.warning(
            "Please analyze your resume first."
        )

        return

    candidate_skills = st.session_state["skills"]

    col1, col2 = st.columns(2)

    with col1:

        job_role = st.text_input(
            "Target Job Role",
            placeholder="Data Scientist"
        )

    with col2:

        education = st.selectbox(
            "Education",
            [
                "B.E",
                "B.Tech",
                "M.Tech",
                "B.Sc",
                "M.Sc",
                "MBA",
                "PhD",
                "Diploma"
            ]
        )

    experience = st.text_input(
        "Experience",
        placeholder="2 Years"
    )

    top_n = st.slider(
        "Top Salary Matches",
        3,
        15,
        10
    )

    if st.button(
        "💰 Predict Salary",
        use_container_width=True
    ):

        with st.spinner("Predicting salary..."):

            report = generate_salary_report(
                job_role,
                candidate_skills,
                experience,
                education
            )

            predictions = predict_salary(
                job_role,
                candidate_skills,
                experience,
                education,
                top_n
            )

            growth = estimate_growth(report)

            insights = salary_insights(report)

            location_compare = compare_locations(job_role)

            company_compare = compare_company_types(job_role)

            st.session_state["salary_report"] = report
            st.session_state["salary_predictions"] = predictions
            st.session_state["salary_growth"] = growth
            st.session_state["salary_insights"] = insights
            st.session_state["location_compare"] = location_compare
            st.session_state["company_compare"] = company_compare

    if "salary_report" not in st.session_state:

        return

    report = st.session_state["salary_report"]
    predictions = st.session_state["salary_predictions"]
    growth = st.session_state["salary_growth"]
    insights = st.session_state["salary_insights"]
    location_compare = st.session_state["location_compare"]
    company_compare = st.session_state["company_compare"]

    # ------------------------------------------------------

    st.subheader("🏆 Best Salary Prediction")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Predicted Salary",
        f"₹{report['predicted_salary_lpa']} LPA"
    )

    c2.metric(
        "Recommendation",
        f"{report['recommendation_score']}%"
    )

    c3.metric(
        "Skill Match",
        f"{report['skill_match']}%"
    )

    st.success(f"""

### {report['job_role']}

📍 Location : {report['location']}

🏢 Company : {report['company_type']}

🎓 Education : {report['education']}

💼 Employment : {report['employment_type']}

💰 Salary Category : {report['salary_category']}

""")

    st.divider()
    # ==========================================================
    # SALARY PREDICTION TABLE
    # ==========================================================

    st.subheader("📊 Salary Predictions")

    st.dataframe(

        predictions,

        use_container_width=True,

        hide_index=True

    )

    # ==========================================================
    # PREDICTED SALARY CHART
    # ==========================================================

    st.divider()

    st.subheader("📈 Predicted Salary Comparison")

    fig = px.bar(

        predictions,

        x="Location",

        y="Predicted_Salary_LPA",

        color="Recommendation_Score",

        text="Predicted_Salary_LPA",

        hover_data=[

            "Company_Type",

            "Experience"

        ]

    )

    fig.update_layout(

        height=450,

        xaxis_title="Location",

        yaxis_title="Salary (LPA)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # CAREER GROWTH
    # ==========================================================

    st.divider()

    st.subheader("🚀 Career Growth Forecast")

    growth_df = pd.DataFrame(

        {

            "Year": list(growth.keys()),

            "Salary (LPA)": list(growth.values())

        }

    )

    fig = px.line(

        growth_df,

        x="Year",

        y="Salary (LPA)",

        markers=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.dataframe(

        growth_df,

        hide_index=True,

        use_container_width=True

    )

    # ==========================================================
    # SALARY INSIGHTS
    # ==========================================================

    st.divider()

    st.subheader("💡 AI Salary Insights")

    for item in insights:

        st.info(item)

    # ==========================================================
    # MATCHED SKILLS
    # ==========================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Matched Skills")

        if report["matched_skills"]:

            for skill in report["matched_skills"]:

                st.success(skill)

        else:

            st.write("No matched skills.")

    with col2:

        st.subheader("📚 Skills To Improve")

        if report["missing_skills"]:

            for skill in report["missing_skills"]:

                st.warning(skill)

        else:

            st.success("No missing skills.")

    # ==========================================================
    # LOCATION COMPARISON
    # ==========================================================

    st.divider()

    st.subheader("🌍 Salary Comparison by Location")

    st.dataframe(

        location_compare,

        hide_index=True,

        use_container_width=True

    )

    fig = px.bar(

        location_compare,

        x="Location",

        y="Average_Salary_LPA",

        text="Average_Salary_LPA"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # COMPANY TYPE COMPARISON
    # ==========================================================

    st.divider()

    st.subheader("🏢 Salary by Company Type")

    st.dataframe(

        company_compare,

        hide_index=True,

        use_container_width=True

    )

    fig = px.pie(

        company_compare,

        names="Company_Type",

        values="Average_Salary_LPA"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    st.divider()

    report_lines = [

        "=" * 70,

        "AI SALARY PREDICTION REPORT",

        "=" * 70,

        "",

        f"Job Role : {report['job_role']}",

        f"Location : {report['location']}",

        f"Company Type : {report['company_type']}",

        f"Education : {report['education']}",

        f"Experience : {report['experience']}",

        "",

        f"Predicted Salary : ₹{report['predicted_salary_lpa']} LPA",

        f"Average Salary : ₹{report['average_salary_lpa']} LPA",

        f"Salary Range : ₹{report['minimum_salary_lpa']} - ₹{report['maximum_salary_lpa']} LPA",

        "",

        f"Recommendation Score : {report['recommendation_score']}%",

        f"Skill Match : {report['skill_match']}%",

        f"Salary Category : {report['salary_category']}",

        "",

        "Matched Skills"

    ]

    for skill in report["matched_skills"]:

        report_lines.append(f"✓ {skill}")

    report_lines.append("")
    report_lines.append("Missing Skills")

    for skill in report["missing_skills"]:

        report_lines.append(f"• {skill}")

    report_lines.append("")
    report_lines.append("AI Insights")

    for item in insights:

        report_lines.append(f"- {item}")

    report_lines.append("")
    report_lines.append("Career Growth")

    for year, value in growth.items():

        report_lines.append(f"{year} : ₹{value} LPA")

    report_lines.append("")
    report_lines.append("=" * 70)

    report_text = "\n".join(report_lines)

    st.download_button(

        "📥 Download Salary Report",

        report_text,

        file_name="Salary_Prediction_Report.txt",

        mime="text/plain",

        use_container_width=True

    )

    # ==========================================================
    # COMPLETION
    # ==========================================================

    st.divider()

    st.success(
        """
🎉 Salary prediction completed successfully!

You now have:

✅ Expected salary prediction

✅ Career growth forecast

✅ Salary insights

✅ Skill gap analysis

✅ Location-wise salary comparison

✅ Company-wise salary comparison

Use these insights to plan your career progression and target the most rewarding opportunities.
"""
    )