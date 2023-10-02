import os
import datetime
from metaphor_python import Metaphor
import streamlit as st
from userInfo import UserInfo
from helpers import join_tags


metaphor = Metaphor(os.getenv('METAPHOR_KEY'))

ROLE_TAGS = {
    "Machine Learning": ["#hiring", "#mlhiring", "#ml"],
    "Software Engineer": ["#hiring","#softwarejobs"]
}


def build_query(ui, start_date, end_date, result_type, top_n_jobs):
    search_type='keyword'
    use_autoprompt=True
    query = f"{ui.role_type} {ui.location} {ui.user_experience} years of experience {result_type}"
    if result_type == "Posts":
        search_type = 'neural'
        query = (f"Hiring or Openings for {ui.role_type} in {ui.location} {result_type}"
                 f"activity")
        query += join_tags(ROLE_TAGS[ui.role_type])

    response = metaphor.search(
        query=query,
        num_results=top_n_jobs,
        start_published_date=str(start_date),
        end_published_date=str(end_date),
        type=search_type,
        include_domains=['linkedin.com'],
        use_autoprompt=use_autoprompt
    )
    for res in response.results:
        st.markdown(f"[{res.title}]({res.url})")


def run():
    st.title("Job Search Inputs")

    # User inputs
    role_type = st.selectbox("Select Role", ["Machine Learning", "Software Engineer"])
    # role_type = st.text_input("Enter Role Type", "")
    user_availability = st.selectbox("Select User Availability", ["Full-time", "Part-time", "Contract"])
    user_experience = st.number_input("Select User Experience (in years)", min_value=0, value=3, step=1)

    location = st.text_input("Enter Location", "india")
    notice_period = st.number_input("Enter Notice Period (in days)", min_value=0, value=30, step=30)

    # Date range input
    st.header("Jobs Published between Dates")
    start_date = st.date_input("Start Date", format='YYYY-MM-DD',value=datetime.date(2023, 8, 1))
    end_date = st.date_input("End Date", format='YYYY-MM-DD')
    # Ask for top N jobs
    top_n_jobs = st.slider("Select the number of jobs you want to see", min_value=1, max_value=100, value=10)
    result_type = st.selectbox("Select Result type", ["Posts", "Jobs"])
    if st.button("Submit"):
        # Thank you message
        st.success("Thank you for providing your details, search in progress....please wait")
        ui = UserInfo()
        ui.role_type = role_type
        ui.user_availability = user_availability
        ui.user_experience = user_experience
        ui.location = location
        ui.notice_period = notice_period
        build_query(ui, start_date, end_date, result_type, top_n_jobs)


if __name__ == '__main__':
    run()
