# poller.py

import requests
import time
import json
import os
import dotenv

dotenv.load_dotenv()

class EndpointPoller:
    def __init__(self, base_url="https://xpt548ceab.execute-api.us-east-1.amazonaws.com/dev"):
        self.api_key = os.getenv('API_KEY')
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def run(self, query, topic, debate_type, side, type_of_argument, save_file_path=None):
        response = self.start_process(query, topic, debate_type, side, type_of_argument)
        self.execution_arn = json.loads(response['body'])["executionArn"]
        final_result = self.get_status(
            self.execution_arn,
        )
        final_result = json.loads(json.loads(final_result['output'])['body'])

        if save_file_path and "html_output" in final_result:
            with open(save_file_path, "w", encoding="utf-8") as f:
                f.write(final_result["html_output"])

        return final_result

    def start_process(self, query, topic, debate_type, side, type_of_argument):
        endpoint = f"{self.base_url}/polling-serverless-dev-startProcess"
        payload = {
            "topic": topic,
            "debate_type": debate_type,
            "side": side,
            "query": query,
            "type_of_argument": type_of_argument
        }

        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_status(self, execution_arn, max_attempts=30, delay=10, ):
        endpoint = f"{self.base_url}/polling-serverless-dev-getStatus"
        payload = {"executionArn": execution_arn}

        for attempt in range(max_attempts):
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "SUCCEEDED":
                return data

            if data.get("status") == "FAILED":
                raise Exception("Process failed")

            time.sleep(delay)

        raise TimeoutError(f"Process did not complete after {max_attempts * delay} seconds")


# Example usage
if __name__ == "__main__":
    poller = EndpointPoller()
    import argparse

    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, help='Topic of the debate')
    parser.add_argument('--debate_type', type=str, help='Type of debate for generating cards', default="parliamentary")
    parser.add_argument('--side', type=str, help='Side of the debater (e.g. affirmative or negative) with respect to the topic. If none, its not specified.', default=None)
    parser.add_argument('--query', type=str, help='Query to search for evidence')
    parser.add_argument('--type_of_argument', type=str, help='Type of argument to generate cards for', default="any_type")
    args = parser.parse_args()

    # result = poller.run(
    #     topic=args.topic,
    #     debate_type=args.debate_type,
    #     side=args.side,
    #     query=args.query,
    #     type_of_argument=args.type_of_argument
    # )

    # Start process
    result = poller.run(
        topic="Australia should significantly increase its investment in nuclear energy",
        debate_type="parliamentary",
        side="affirmative",
        query="Impact of energy shortage in Australia",
        type_of_argument="impact"
    )