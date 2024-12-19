# Chatbot Project with LLaMA2, Streamlit, FastAPI, and Docker

This project is a chatbot application leveraging **LLaMA2**, **Ollama**, **Streamlit**, **FastAPI**, and **Docker**. It integrates a generative AI model with a database-backed system to generate responses efficiently. This document provides an overview of the project's structure, the functionality of each component, and instructions for setup and usage.

---

## **Overview**

The chatbot consists of the following components:

1. **LLaMA2**: A state-of-the-art language model used to generate conversational responses.
2. **Streamlit**: Provides a user-friendly web interface for interacting with the chatbot.
3. **FastAPI**: Manages the backend API, connecting the chatbot logic to the front end and database.
4. **MySQL**: Stores pre-defined responses for prompts, enhancing efficiency.
5. **Docker**: Ensures a portable and consistent runtime environment.
6. **Supervisor**: Manages multiple processes (LLaMA2 server and Streamlit app) within the Docker container.

---

## **File Structure**

### **1. `run_llama2_server.py`**
   - **Purpose**: Contains the FastAPI application responsible for handling API requests and generating responses.
   - **Key Features**:
     - Fetches pre-defined responses from a MySQL database.
     - Generates AI responses using LLaMA2 when no database match is found.
   
### **2. `chatbot.py`**
   - **Purpose**: Implements the Streamlit application, providing an interactive interface for users to chat with the bot.
   - **Key Features**:
     - Accepts user input (prompts).
     - Displays responses generated by the FastAPI server.

### **3. `Dockerfile`**
   - **Purpose**: Defines the containerization setup for the chatbot.
   - **Key Features**:
     - Installs Python dependencies and system tools.
     - Set up a Supervisor to manage FastAPI and Streamlit processes.

### **4. `supervisor.conf`**
   - **Purpose**: Configures Supervisor to manage multiple processes in the Docker container.
   - **Key Features**:
     - Runs the FastAPI server (`run_llama2_server.py`).
     - Runs the Streamlit app (`chatbot.py`).

### **5. `requirements.txt`**
   - **Purpose**: Lists Python dependencies for the project.
   - **Key Dependencies**:
     - Streamlit, FastAPI, Uvicorn, MySQL Connector, LangChain, Streamlit Chat.

### **6. `.env`**
   - **Purpose**: Stores environment variables such as database credentials for security and ease of configuration.
   - **Key Variables**:
     - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_PORT`.

### **7. `README.md`** (This file)
   - **Purpose**: Provides an overview of the project, setup instructions, and functionality of each file.

---

## **Working on the Project**

### **1. Frontend**
   - The user interacts with the chatbot through a Streamlit-based web interface.
   - Input prompts are sent to the backend API hosted by FastAPI.

### **2. Backend**
   - FastAPI processes the prompt:
     - First, it queries the MySQL database for a pre-defined response.
     - If no match is found, it generates a response using LLaMA2.
   - The generated or fetched response is returned to the Streamlit app.

### **3. Deployment**
   - Docker ensures the application is deployed in a consistent environment.
   - Supervisor manages both the FastAPI server and the Streamlit application, ensuring they restart in case of failure.

---

## **Setup Instructions**

### **1. Prerequisites**
   - Docker installed on your system.
   - A MySQL database instance.
   - Environment variables configured in a `.env` file.

### **2. Steps to Run**
   1. **Clone the repository**:
      ```bash
      git clone <repository-url>
      cd <repository-folder>
      ```
   2. **Build the Docker image**:
      ```bash
      docker build -t chatbot_image.
      ```
   3. **Run the Docker container**:
      ```bash
      docker run -d -p 8000:8000 -p 8501:8501 --env-file .env chatbot_image
      ```
   4. **Access the chatbot**:
      - Open a browser and go to `http://localhost:8501`.

---

## **Key Features**

1. **Pre-defined Responses**:
   - Fetches responses from a MySQL database for faster and contextually accurate replies.

2. **Generative AI**:
   - LLaMA2 generates dynamic responses for prompts not found in the database.

3. **Streamlined Deployment**:
   - Docker simplifies deployment and ensures consistency.

4. **Multi-Process Management**:
   - Supervisor handles both the FastAPI backend and Streamlit frontend.

---

## **Future Enhancements**
   - Add user authentication for secure access.
   - Incorporate more advanced AI models.
   - Enhance the UI with additional features such as conversation history.

---

This project is a foundational framework for building robust chatbot applications. Contributions and suggestions for improvement are welcome!

