from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class GenerateRequest(BaseModel):
    model: str
    prompt: str

# Fetch MySQL configuration from environment variables
mysql_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

# Database query function
def fetch_from_database(prompt):
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        cursor.execute("SELECT response FROM responses WHERE prompt = %s", (prompt,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return "No matching response found in the database."
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Replace this with your actual LLAMA2 model initialization and usage
def generate_response(prompt):
    db_response = fetch_from_database(prompt)
    if db_response:
        return db_response
    return f"Generated response for prompt: {prompt}"

@app.post("/api/generate")
def generate(request: GenerateRequest):
    if request.model == "llama2":
        response = generate_response(request.prompt)
        return {"response": response}
    else:
        raise HTTPException(status_code=400, detail="Model not supported")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
