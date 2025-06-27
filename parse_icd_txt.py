
import json

input_file = "icd10cm_codes_2025.txt"
output_file = "icd10_descriptions.json"

icd_dict = {}

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            # Split on any whitespace (spaces, tabs), only at first space
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                code = parts[0].strip()
                desc = parts[1].strip()
                icd_dict[code] = desc

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(icd_dict, f, indent=2)

print(f"✅ Saved {len(icd_dict)} ICD-10 codes to {output_file}")
