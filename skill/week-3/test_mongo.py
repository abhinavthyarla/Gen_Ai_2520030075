
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=15000
    )

    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")

    db = client["llm_monitoring"]

    db["api_usage"].insert_one({
        "provider": "test",
        "status": "success"
    })

    print("Test record inserted successfully!")

except Exception as e:
    print("ERROR:", type(e).__name__, e)

finally:
    if "client" in locals():
        client.close()
