import streamlit as st
import json
import openai
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Load ICD-10 descriptions
with open("icd10_descriptions.json") as f:
    icd_data = json.load(f)

# Streamlit UI setup
st.set_page_config(page_title="ICD-10 Explainer", page_icon="🧠")
st.title("🧠 ICD-10 Code Explainer Agent")

# User input
api_key = st.text_input("Enter your OpenAI API key", type="password")
code = st.text_input("Enter an ICD-10 Code (e.g., A000)").upper()

if st.button("Explain with GPT"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif code not in icd_data:
        st.warning("Code not found. Please check and try again.")
    else:
        description = icd_data[code]
        st.success(f"🩺 {code}: {description}")

        prompt = f"""
You're a helpful clinical explainer bot. A user provides an ICD-10 code and title. 
Respond with a clear, structured markdown explanation **without just restating the title**. Use the following format **exactly**:

### 🔍 What is this condition?
(Explain in layman terms)

### 📚 Why does it occur?
(Briefly explain causes or risk factors)

### 🧠 Symptoms and concerns
(List common signs, symptoms, or risks)

### 🩺 Common treatments
(Explain what treatments are generally used)

Avoid repeating the description. Be informative but concise.

ICD-10 Code: {code}  
ICD-10 Title: {description}
"""

        try:
            client = openai.OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                # model="gpt-4o",
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            explanation = response.choices[0].message.content
            st.markdown("### 🧠 GPT Explanation")
            st.markdown(explanation)  # this renders the markdown

        except openai.RateLimitError:
            st.error("⚠️ You've exceeded your OpenAI usage quota.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
