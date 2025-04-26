import json
from abacusai import ApiClient
from config import settings

# Initialize Abacus.AI client with API key
client = ApiClient(api_key=settings.ABACUS_AI_API_KEY)

async def get_llm_response(question: str) -> dict:
    """
    Fetches a structured JSON response from Abacus.AI for a travel-related question.
    """

    prompt = f"""
You are a travel assistant. Provide ONLY a structured JSON response to the following question.
DO NOT include any text, comments, or code blocks — just valid JSON.
Question: {question}
Response format:
{{
  "visa_requirements": "...",
  "passport_requirements": "...",
  "additional_documents": "...",
  "travel_advisories": "..."
}}
Make sure it's concise, accurate, and pure JSON without backticks or extra formatting.
"""

    try:
        # Call Abacus.AI
        response = client.evaluate_prompt(
            prompt=prompt,
            system_message="You are a helpful travel assistant",
            llm_name="OPENAI_GPT4O"
        )

        print("response", response.content)

        # Try parsing directly
        try:
            response_json = json.loads(response.content)

            # Validate the keys
            required_keys = [
                "visa_requirements",
                "passport_requirements",
                "additional_documents",
                "travel_advisories"
            ]
            if not all(key in response_json for key in required_keys):
                raise ValueError("Response missing required fields")

            return response_json

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from Abacus.AI")
        except ValueError as e:
            raise ValueError(f"Response validation failed: {str(e)}")

    except Exception as e:
        raise Exception(f"Failed to get response from Abacus.AI: {str(e)}")
