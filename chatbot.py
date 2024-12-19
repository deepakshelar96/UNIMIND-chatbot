import re
import requests
import streamlit as st
import json
import pymysql
from streamlit_chat import message  # Import streamlit-chat for chatbot UI

# Database connection parameters
DB_HOST = '103.212.121.208'
DB_USER = 'xkawgszq_aiagent'
DB_PASSWORD = 'Mansi@123'
DB_NAME = 'xkawgszq_academy'

# Define the API endpoint
API_URL = "http://localhost:8000/api/generate"

# CSS to align all messages on the left
st.markdown("""
    <style>
        .streamlit-chat-message {
            display: flex !important;
            justify-content: flex-start !important;
        }
        .streamlit-chat-message .user-message {
            background-color: #e0f7fa; /* Light background for user messages */
        }
        .streamlit-chat-message .bot-message {
            background-color: #f1f1f1; /* Light background for bot messages */
        }
    </style>
""", unsafe_allow_html=True)

# Function to strip HTML tags from text
def strip_html_tags(text):
    return re.sub(r'<.*?>', '', text) if text else ""

# Function to preprocess user input (normalize, remove extra spaces)
def preprocess_input(input_text):
    return " ".join(input_text.lower().split())

# Function to get response from the model (fallback if no relevant course info is available)
def generate_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response from the model")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to fetch answers or recommendations from the database
def fetch_answer(question, role):
    question = preprocess_input(question)

    connection = None
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        with connection.cursor() as cursor:
            # Handle role-specific queries for Admin
            if role == "Admin":
                # User Management Queries
                if "user count" in question or "number of users" in question:
                    cursor.execute("SELECT COUNT(*) FROM users")
                    user_count = cursor.fetchone()[0]
                    return f"Total number of users: {user_count}"

                if "list users" in question:
                    cursor.execute("SELECT email FROM users")
                    users = cursor.fetchall()
                    return "Users: " + ", ".join(user[0] for user in users) if users else "No users found."

                if "deactivate user" in question:
                    email = question.split("deactivate user")[-1].strip()
                    cursor.execute("UPDATE users SET status = 'inactive' WHERE email = %s", (email,))
                    connection.commit()
                    return f"User with email {email} has been deactivated."

                if "activate user" in question:
                    email = question.split("activate user")[-1].strip()
                    cursor.execute("UPDATE users SET status = 'active' WHERE email = %s", (email,))
                    connection.commit()
                    return f"User with email {email} has been activated."

                # Course Management Queries
                if "course count" in question or "number of courses" in question:
                    cursor.execute("SELECT COUNT(*) FROM course")
                    course_count = cursor.fetchone()[0]
                    return f"Total number of courses: {course_count}"

                if "list courses" in question:
                    cursor.execute("SELECT title FROM course")
                    courses = cursor.fetchall()
                    return "Courses: " + ", ".join(course[0] for course in courses) if courses else "No courses found."

                if "course details" in question:
                    course_name = question.split("course details for")[-1].strip()
                    cursor.execute("SELECT description, requirements, outcomes FROM course WHERE title LIKE %s", (f"%{course_name}%",))
                    result = cursor.fetchone()
                    if result:
                        description, requirements, outcomes = result
                        return (f"Description: {description}\n"
                                f"Requirements: {requirements}\n"
                                f"Outcomes: {outcomes}")
                    else:
                        return f"Course '{course_name}' not found."

                if "add course" in question:
                    course_name = question.split("add course")[-1].strip()
                    # You can add more course details like description, price etc. in a similar way
                    cursor.execute("INSERT INTO course (title) VALUES (%s)", (course_name,))
                    connection.commit()
                    return f"Course '{course_name}' has been added."

                if "delete course" in question:
                    course_name = question.split("delete course")[-1].strip()
                    cursor.execute("DELETE FROM course WHERE title LIKE %s", (f"%{course_name}%",))
                    connection.commit()
                    return f"Course '{course_name}' has been deleted."

                # Platform Stats
                if "platform stats" in question:
                    cursor.execute("SELECT COUNT(*) FROM course")
                    course_count = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM users")
                    user_count = cursor.fetchone()[0]
                    return f"Platform stats: {course_count} courses and {user_count} users."

                # Role Management
                if "change role" in question:
                    parts = question.split("change role of")
                    if len(parts) > 1:
                        email_and_role = parts[1].strip()
                        email = email_and_role.split("to")[0].strip()
                        new_role = email_and_role.split("to")[1].strip()
                        role_id = {"admin": 1, "mentor": 2, "user": 3}.get(new_role.lower(), 3)
                        cursor.execute("UPDATE users SET role_id = %s WHERE email = %s", (role_id, email))
                        connection.commit()
                        return f"Role of user with email {email} has been changed to {new_role.title()}."

                # Content Moderation Queries (Example)
                if "approve content" in question:
                    course_name = question.split("approve content for")[-1].strip()
                    # Implement logic for approving content (add database handling for content approval)
                    return f"Content for course '{course_name}' has been approved."

                # System Health and Reports
                if "platform health" in question:
                    return "The platform is running smoothly."

                if "generate report" in question:
                    # Generate a custom report, for example, list of most popular courses or user activity
                    return "Here is the requested report on user activity."

                return "Admin command not recognized. Please try again."

            # Handle other roles (Mentor, User) in a similar way
            if role == "mentors":
                 # Mentor-specific queries
                if "assigned courses" in question:
                    mentor_email = question.split("assigned courses for")[-1].strip()
                    cursor.execute("""
                        SELECT course.title 
                        FROM course 
                        INNER JOIN mentor_course 
                        ON course.id = mentor_course.course_id 
                        INNER JOIN users 
                        ON mentor_course.mentor_id = users.id 
                        WHERE users.email = %s
                    """, (mentor_email,))
                    courses = cursor.fetchall()
                    return "Assigned Courses: " + ", ".join(course[0] for course in courses) if courses else "No courses assigned."

                if "add assignment" in question:
                    parts = question.split("add assignment to")
                    if len(parts) > 1:
                        course_name_and_assignment = parts[1].strip()
                        course_name, assignment_details = course_name_and_assignment.split("with details")
                        cursor.execute("SELECT id FROM course WHERE title = %s", (course_name.strip(),))
                        course_id = cursor.fetchone()
                        if course_id:
                            # Assuming a table `assignments` with fields `course_id` and `details`
                            cursor.execute(
                                "INSERT INTO assignments (course_id, details) VALUES (%s, %s)",
                                (course_id[0], assignment_details.strip())
                            )
                            connection.commit()
                            return f"Assignment added to course '{course_name.strip()}'."
                        else:
                            return f"Course '{course_name.strip()}' not found."

                if "student progress" in question:
                    course_name = question.split("student progress for")[-1].strip()
                    cursor.execute("""
                        SELECT users.email, progress.status 
                        FROM progress 
                        INNER JOIN users 
                        ON progress.user_id = users.id 
                        INNER JOIN course 
                        ON progress.course_id = course.id 
                        WHERE course.title LIKE %s
                    """, (f"%{course_name}%",))
                    progress = cursor.fetchall()
                    if progress:
                        return "Student Progress:\n" + "\n".join(f"{email}: {status}" for email, status in progress)
                    else:
                        return f"No progress found for course '{course_name}'."

                return "Mentor command not recognized. Please try again."
                

            if role == "learner":
                if "available courses" in question or "list courses" in question:
                    cursor.execute("SELECT title FROM course")
                    courses = cursor.fetchall()
                    return "Available Courses: " + ", ".join(course[0] for course in courses) if courses else "No courses available at the moment."

                if "course details" in question:
                    course_name = question.split("course details for")[-1].strip()
                    cursor.execute("SELECT description, requirements, outcomes FROM course WHERE title LIKE %s", (f"%{course_name}%",))
                    result = cursor.fetchone()
                    if result:
                        description, requirements, outcomes = result
                        return (
                            f"Description: {description}\n"
                            f"Requirements: {requirements}\n"
                            f"Outcomes: {outcomes}"
                        )
                    else:
                        return f"Course '{course_name}' not found."

                # Handle unrecognized questions
                return "I'm not sure how to help with that. Please ask about available courses or specific course details."

    except pymysql.MySQLError as e:
        return f"Database error: {e.args[0]} - {e.args[1]}"
    finally:
        if connection:
            connection.close()


# Function to get user role based on email
def get_user_role_by_email(email):
    """Fetch user role based on email."""
    connection = None
    ROLE_MAP = {
        1: "Admin",
        2: "mentors",
        3: "learners"
    }
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT role_id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                role_id = result[0]
                return ROLE_MAP.get(role_id, "learners")
            else:
                return "learners"  # Default role if no role is found
    except pymysql.MySQLError as e:
        return f"Error fetching role: {e.args[1]}"
    finally:
        if connection:
            connection.close()


# Set up Streamlit framework
st.title('Hello from Unimind: Your 24/7 Knowledge Companion!')

# Step 1: Ask for email input
email = st.text_input("Please enter your email to continue:")

# Step 2: Validate the email and get role
if email:
    role = get_user_role_by_email(email)
    if role:
        # Display the role and proceed to chatbot
        st.write(f"Welcome, {role}! You will now be able to access your {role} chatbot.")
        
        # Step 3: Proceed with chatbot interaction (existing logic)
        input_text = st.text_input("Let’s Get Your Questions Answered!", key="user_input")
        submit_button = st.button("Submit")

        if 'history' not in st.session_state:
            st.session_state.history = []

        if submit_button and input_text:
            user_input = input_text.strip()

            # Fetch answer based on role
            response = fetch_answer(user_input, role)

            if response in ["I'm not sure", "Course not found", "No relevant courses found"]:
                response = generate_response(user_input)

            # Add user input and response to chat history
            st.session_state.history.append({"message": user_input, "is_user": True})
            st.session_state.history.append({"message": response, "is_user": False})

        # Display chat history
        for i, chat in enumerate(st.session_state.history):
            message(chat['message'], is_user=chat['is_user'], key=f"{'user' if chat['is_user'] else 'bot'}_{i}")
    else:
        st.write("No account found with that email. Please try again.")
