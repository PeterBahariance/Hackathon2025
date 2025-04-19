import re
import json
import openai


# Paste your API key here
# openai.api_key = "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"


client = openai.OpenAI(api_key="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")  # or use environment variable

# Load OCR text
with open("detected_text_output.txt", "r") as file:
    raw_text = file.read()

prompt = f"""
Here is the raw OCR text from a medicine bottle. Please extract useful information and return it as a structured JSON object with keys like medication, dosage, instructions, patient_name, expiration_date, etc.

OCR Text:
---
{raw_text}
---
"""

# Call GPT using the new client
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a medical assistant that extracts structured data from messy scanned text."},
        {"role": "user", "content": prompt}
    ]
)

# Print and save output
parsed_output = response.choices[0].message.content
print(parsed_output)

clean_output = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", parsed_output).strip()

try:
    # Try loading to confirm it's valid JSON
    structured_data = json.loads(clean_output)

    # Save clean JSON
    with open("../backend/output_from_gpt.json", "w") as f:
        json.dump(structured_data, f, indent=2)

    print("✅ JSON cleaned and saved successfully.")

except json.JSONDecodeError as e:
    print("❌ GPT returned invalid JSON:\n")
    print(parsed_output)