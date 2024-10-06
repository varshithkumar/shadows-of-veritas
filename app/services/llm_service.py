# backend/app/services/llm_service.py
import os
from openai import AsyncOpenAI
import openai
import json
from dotenv import load_dotenv
import asyncio

load_dotenv()

MAX_RETRIES = 3

PROMPT = """
Generate a concise detective case in JSON format with the following structure:

[Start of JSON]
{
  "title": "Case Title",
  "description": "Case Description",
  "characters": [
    {
      "name": "Character Name",
      "background": "Character Background",
      "dialogues": [
        {
          "text": "Dialogue text",
          "options": [
            {
              "response": "Player's response",
              "next_dialogue_id": "Next dialogue ID"
            }
          ]
        }
      ]
    }
  ],
  "clues": [
    {
      "description": "Clue Description",
      "location": "Clue Location"
    }
  ]
}
[End of JSON]

Please provide only the JSON data between [Start of JSON] and [End of JSON], without any additional text.
"""


openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_case():
    prompt = PROMPT
    max_retries = MAX_RETRIES
    # Use the new method for chat completion
    for attempt in range(max_retries):
        try:            
          response = await asyncio.to_thread(
              openai.chat.completions.create,
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "user", "content": prompt}
              ],
              max_tokens=500,
              temperature=0.7,
          )

          output = response.choices[0].message.content
          # Extract the JSON between the delimiters, if used
          start_delimiter = "[Start of JSON]"
          end_delimiter = "[End of JSON]"
          if start_delimiter in output and end_delimiter in output:
              json_str = output.split(start_delimiter)[1].split(end_delimiter)[0].strip()
          else:
              json_str = output.strip()
          # Ensure the output is valid JSON
          try:
              case_data = json.loads(json_str)
          except json.JSONDecodeError as e:
              raise ValueError(f"Invalid JSON output from LLM: {e}")
          return case_data
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"JSON decoding failed on attempt {attempt + 1}: {e}. Retrying...")
                continue
            else:
                raise ValueError(f"Failed to parse JSON after {max_retries} attempts: {e}\nOutput received: {output}")
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")
    raise ValueError("Failed to generate valid JSON from the LLM.")
