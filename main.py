import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

def extract_fields_from_file(file_path: str, fields: list[str]) -> dict:
    """
    Reads an unstructured markdown file and uses Google Gemini SDK to extract specified fields.

    Args:
        file_path (str): Path to the markdown file containing product details.
        fields (list[str]): List of field names to extract from the file.

    Returns:
        dict: A dictionary mapping each field to its extracted value.
    """
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment. Please set it in your .env file.")

    # Read the source file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Prepare system instruction and user prompt
    system_instruction = (
        "You are a helpful assistant that extracts specified fields from an unstructured product description. "
        "Return the output strictly as a JSON object with keys matching the field names."
    )
    user_prompt = (
        f"Extract the following fields from the product details below:\n"
        f"Fields: {fields}\n\n"
        f"Product Details:\n{content}"
    )

    # Call Gemini to generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
        contents=user_prompt
    )

    # Normalize response text: strip markdown code fences if present
    raw = response.text.strip()
    if raw.startswith('```'):
        lines = raw.splitlines()
        if lines and lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        raw = '\n'.join(lines)

    # Parse JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from Gemini response: {response.text}")

    return data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract specified fields from a markdown file using Gemini SDK."
    )
    parser.add_argument(
        "-f", "--file", type=str, default="prod1info.md",
        help="Path to the markdown file containing product details (default: prod1info.md)"
    )
    parser.add_argument(
        "-k", "--keys", type=str, nargs='+', required=True,
        help="List of field names to extract from the file."
    )
    args = parser.parse_args()

    result = extract_fields_from_file(args.file, args.keys)

    # Print human-readable output
    if len(args.keys) == 1:
        key = args.keys[0]
        value = result.get(key)
        if value is None:
            print(f"Field '{key}' not found.")
        else:
            print(value)
    else:
        # Multiple fields: list each
        for k in args.keys:
            val = result.get(k)
            print(f"{k}: {val if val is not None else 'Not found'}")
