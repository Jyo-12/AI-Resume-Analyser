import streamlit as st
import pandas as pd
import plotly.express as px

from utils.course_engine import (
    generate_course_report,
    format_course_report
)

# ==========================================================
# COURSE RECOMMENDATION PAGE
# ==========================================================

def course_recommendation_page():

    st.title("📚 AI Course Recommendation")

    st.markdown(
        """
        Discover the best learning resources based on your
        resume skills and career goals.
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

    st.subheader("Career Goal")

    desired_career = st.text_input(

        "Desired Career",

        placeholder="Example : Data Scientist"

    )

    st.subheader("Skills You Want To Learn")

    missing_skill_text = st.text_area(

        "Missing Skills",

        placeholder="Machine Learning, Docker, AWS, Deep Learning"

    )

    missing_skills = [

        skill.strip()

        for skill in missing_skill_text.split(",")

        if skill.strip()

    ]

    top_courses = st.slider(

        "Number of Recommendations",

        3,

        15,

        5

    )

    if st.button(

        "🚀 Recommend Courses",

        use_container_width=True

    ):

        with st.spinner(

            "Finding the best courses..."

        ):

            report = generate_course_report(

                candidate_skills,

                missing_skills,

                desired_career,

                top_courses

            )

            dashboard = format_course_report(

                report

            )

        st.session_state["course_dashboard"] = dashboard

    if "course_dashboard" not in st.session_state:

        return

    dashboard = st.session_state["course_dashboard"]

    best_course = dashboard["best_course"]

    recommendations = dashboard["recommendations"]

    learning_path = dashboard["learning_path"]

    weekly_plan = dashboard["weekly_plan"]

    statistics = dashboard["statistics"]

    estimated_hours = dashboard["estimated_hours"]

    # ------------------------------------------------------

    st.subheader("📊 Recommendation Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Courses",

        statistics["total_courses"]

    )

    c2.metric(

        "Average",

        f"{statistics['average_score']}%"

    )

    c3.metric(

        "Highest",

        f"{statistics['highest_score']}%"

    )

    c4.metric(

        "Study Hours",

        estimated_hours

    )

    st.divider()

    # ------------------------------------------------------

    st.subheader("🏆 Best Course")

    st.success(

f"""
### {best_course['course_name']}

Platform : {best_course['platform']}

Difficulty : {best_course['difficulty']}

Duration : {best_course['duration']}

Career Path : {best_course['career_path']}

Recommendation Score : {best_course['recommendation_score']} %

Certificate : {best_course['certificate']}
"""

    )
    st.divider()

    # ==========================================================
    # COURSE RECOMMENDATIONS
    # ==========================================================

    st.subheader("📚 Recommended Courses")

    course_df = pd.DataFrame([

        {

            "Course": course["course_name"],

            "Platform": course["platform"],

            "Difficulty": course["difficulty"],

            "Duration": course["duration"],

            "Score": course["recommendation_score"]

        }

        for course in recommendations

    ])

    st.dataframe(

        course_df,

        hide_index=True,

        use_container_width=True

    )

    # ==========================================================
    # RECOMMENDATION SCORE CHART
    # ==========================================================

    st.divider()

    st.subheader("📈 Recommendation Scores")

    fig = px.bar(

        course_df,

        x="Course",

        y="Score",

        text="Score",

        color="Score"

    )

    fig.update_layout(

        height=450,

        xaxis_title="Course",

        yaxis_title="Recommendation Score (%)"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
    # COURSE DETAILS
    # ==========================================================

    st.divider()

    st.subheader("📖 Course Details")

    for index, course in enumerate(recommendations, start=1):

        with st.expander(

            f"{index}. {course['course_name']} ({course['recommendation_score']}%)",

            expanded=False

        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Platform:** {course['platform']}")

                st.write(f"**Difficulty:** {course['difficulty']}")

                st.write(f"**Duration:** {course['duration']}")

                st.write(f"**Certificate:** {course['certificate']}")

            with col2:

                st.write(f"**Career Path:** {course['career_path']}")

                st.write(f"**Recommendation Score:** {course['recommendation_score']}%")

                st.write(f"**Skill Match:** {course['skill_match_percentage']}%")

                st.write(f"**Course URL:** {course['course_url']}")

            st.markdown("### ✅ Existing Skills")

            if course["matched_skills"]:

                st.success(", ".join(course["matched_skills"]))

            else:

                st.write("None")

            st.markdown("### ⭐ New Skills You'll Learn")

            if course["new_skills"]:

                st.info(", ".join(course["new_skills"]))

            else:

                st.write("No additional skills")

            st.markdown("### 💡 Why This Course?")

            for reason in course["reason"]:

                st.write(f"✅ {reason}")

    # ==========================================================
    # LEARNING PATH
    # ==========================================================

    st.divider()

    st.subheader("🛣️ Personalized Learning Path")

    path_df = pd.DataFrame(learning_path)

    if not path_df.empty:

        st.dataframe(

            path_df,

            hide_index=True,

            use_container_width=True

        )

    # ==========================================================
    # WEEKLY STUDY PLAN
    # ==========================================================

    st.divider()

    st.subheader("📅 Weekly Study Plan")

    weekly_df = pd.DataFrame(weekly_plan)

    if not weekly_df.empty:

        st.dataframe(

            weekly_df,

            hide_index=True,

            use_container_width=True

        )

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    st.divider()

    report_lines = []

    report_lines.append("=" * 70)

    report_lines.append("AI COURSE RECOMMENDATION REPORT")

    report_lines.append("=" * 70)

    report_lines.append("")

    report_lines.append(

        f"Best Course : {best_course['course_name']}"

    )

    report_lines.append(

        f"Platform : {best_course['platform']}"

    )

    report_lines.append(

        f"Recommendation Score : {best_course['recommendation_score']}%"

    )

    report_lines.append("")

    report_lines.append("TOP RECOMMENDATIONS")

    report_lines.append("")

    for i, course in enumerate(recommendations, start=1):

        report_lines.append(

            f"{i}. {course['course_name']}"

        )

        report_lines.append(

            f"Platform : {course['platform']}"

        )

        report_lines.append(

            f"Difficulty : {course['difficulty']}"

        )

        report_lines.append(

            f"Score : {course['recommendation_score']}%"

        )

        report_lines.append("")

    report_lines.append("LEARNING PATH")

    report_lines.append("")

    for step in learning_path:

        report_lines.append(

            f"Step {step['step']} : {step['course_name']}"

        )

    report_lines.append("")

    report_lines.append(

        f"Estimated Study Time : {estimated_hours} Hours"

    )

    report_lines.append("")

    report_text = "\n".join(report_lines)

    st.download_button(

        label="📥 Download Course Report",

        data=report_text,

        file_name="Course_Recommendation_Report.txt",

        mime="text/plain",

        use_container_width=True

    )

    # ==========================================================
    # COMPLETION
    # ==========================================================

    st.divider()

    st.success(
        """
🎉 Course recommendations generated successfully!

Complete these recommended courses to strengthen your profile,
improve your ATS score, and become more competitive for your
target career.
"""
    )