import re
import json
import openai


# Paste your API key here
# openai.api_key = "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"


client = openai.OpenAI(api_key="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")  # or use environment variable

# Load OCR text
with open("../backend/detected_text_output.txt", "r") as file:
    raw_text = file.read()

prompt = f"""
Here is the raw OCR text from a medicine bottle. Please extract useful information and return it as a JSON object in the following structure:

{{
  "pillName": "Name of the medication (e.g., Metformin)",
  "dosage": "Number of pills taken per intake (as an integer, e.g., 2 for 'take 2 tablets')",
  "frequency": "Number of times the medication is to be taken per day (as an integer, e.g., 2 for '2 times daily')",
  "swallowed": false,
  "time1": "First time the medication should be taken (in HH:MM 24hr format if specified)",
  "time2": "Second time the medication should be taken (if applicable)"
  "quantity" : "Number of tablets in the bottle"
}}

IMPORTANT:
- 'dosage' is the number of tablets per intake (like 'Take 1 tablet'), NOT the strength (like '500mg').
- Ignore any number followed by 'mg' or 'mg.' — that is strength, not dosage.
- If the frequency is mentioned as 'up to 2 times daily' or '2 times per day', then 'frequency' should be 2.
- Only include 'time1' or 'time2' if specific clock times are mentioned (like '9am' or '18:00').
- If 'tablet' is singular and the text says 'take 1 tablet', then 'dosage' should be 1.
- SPECIFY BOTH TIMES TO NULL UNLESS THERE IS SOMETING CLEAR TO EXIST AS A TIME LIKE '9:00' OR '18:00'
- Look for number next to symbols such as QTY or quanity for the quantity number 
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