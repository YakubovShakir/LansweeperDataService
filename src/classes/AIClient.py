import requests
import json


class AIClient:

    def __init__(
        self,
        api_base_url: str,
        auth_token: str,
        model: str,
    ):

        self.__api_base_url = api_base_url
        self.__auth_token = auth_token
        self.__model = model

        self.__header = {
            "Accept": "*/*",
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.__auth_token,
        }

    def build_prompt_body(
        self,
        system_role: str,
        user_messages: list,
        max_response_tokens: int,
        temperature: float,
    ):
        builded_user_messages = AIClient.build_user_mesages(user_messages)

        messages = [{"role": "system", "content": system_role}]

        for msg in builded_user_messages:
            messages.append(msg)

        return {
            "model": self.__model,
            "messages": messages,
            "max_tokens": max_response_tokens,
            "temperature": temperature,
        }

    def send_quick_prompt(
        self,
        system_role: str,
        user_messages: list,
        max_response_tokens: int,
        temperature: float,
    ):
        """
        Prompt without context
        """

        AIClient.validate_temperature(temperature)

        payload = self.build_prompt_body(
            system_role, user_messages, max_response_tokens, temperature
        )
        response = requests.post(
            self.__api_base_url + "/v1/chat/completions",
            headers=self.__header,
            json=payload,
        )

        AIClient.validate_repsonse_code(response)

        parsed_repsonse = json.loads(response.text)
        answer = parsed_repsonse["choices"][0]["message"]["content"]

        return answer

    @staticmethod
    def validate_repsonse_code(response):
        if response.status_code < 200 and response.status_code >= 300:
            raise Exception("Something went wrong, error: ", response.text)

    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        if not temperature >= 0 and temperature <= 1:
            raise Exception("Temperature must be in range from 0 to 1")
        return True

    @staticmethod
    def build_user_mesages(messages: list):
        return [{"role": "user", "content": message} for message in messages]
