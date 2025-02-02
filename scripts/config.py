from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
server_url = os.getenv('SERVER_URL')

print(f"API Key: {api_key}")
print(f"Server URL: {server_url}")