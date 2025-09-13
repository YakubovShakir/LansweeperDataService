import os

from classes.AIClient import AIClient

api_base_url = "http://10.112.20.31:8080"
auth_token = os.getenv("AI_API_AUTH_TOKEN")
if auth_token is None:
    raise Exception("Missing AI_API_AUTH_TOKEN")

model = "RuadaptQwen2.5-32B-instruct"

ai_client = AIClient(api_base_url, auth_token, model)
