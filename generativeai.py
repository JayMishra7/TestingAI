import google.generativeai as genai
import re

# --- CONFIGURATION ---
# Replace with your actual Google AI Studio API Key
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

genai.configure(api_key=GOOGLE_API_KEY)

# --- THE SYSTEM INSTRUCTIONS (From Component 1 above) ---
SYSTEM_PROMPT = """
**Role:** You are the "Strategic Visual Architect," an expert AI agent designed to help users create professional-grade image generation prompts.
**Core directive:** Do not just write a prompt. You must guide the user through a strict 3-step decision funnel. Maintain state and wait for input.

**PHASE 1: INGESTION & STRATEGY (Wait for initial input)**
1. Receive raw idea.
2. Generate 4 Distinct Strategic Archetypes (Vibes): A (Cinematic), B (Emotional), C (Commercial), D (Creative).
3. **OUTPUT:** Present options A-D. Ask user to reply with a letter. STOP.

**PHASE 2: CURATED RECIPES (Wait for Letter selection)**
1. Receive letter selection.
2. Generate 3 complete "Style Recipes" (combinations of Lighting, Fashion, Angle, Vibe) based *only* on that archetype.
3. **OUTPUT:** Present recipes 1-3. Ask user to reply with a number. STOP.

**PHASE 3: FINAL COMPILATION (Wait for Number selection)**
1. Receive number selection.
2. Combine original idea with the chosen recipe details.
3. Construct a highly detailed image prompt with technical parameters.
4. **OUTPUT:** Provide final prompt inside a markdown code block (```) ONLY.
"""

# --- INITIALIZE GEMINI MODEL ---
# Using gemini-1.5-pro for better instruction following in multi-turn steps
model = genai.GenerativeModel(
    'gemini-1.5-pro-latest',
    system_instruction=SYSTEM_PROMPT,
    generation_config={"temperature": 0.7} # Slightly creative but structured
)

# Start the chat session
chat_session = model.start_chat(history=[])

# --- HELPER FUNCTION FOR TURNS ---
def run_turn(user_input, turn_name):
    print(f"\n--- User Input ({turn_name}) ---> {user_input}")
    response = chat_session.send_message(user_input)
    print(f"\n<--- Gem App Response ({turn_name}) ---\n{response.text}\n")
    return response.text

# --- MOCK IMAGE GENERATION FUNCTION ---
def generate_image_from_text(prompt_text):
    """
    In a real app, you would send 'prompt_text' to an API like:
    - Vertex AI Imagen (google-cloud-aiplatform)
    - OpenAI DALL-E 3
    - Midjourney API wrapper
    This function simulates that call.
    """
    print("\n==========================================")
    print("⚡ SENDING FINAL PROMPT TO IMAGE MODEL ⚡")
    print("==========================================")
    print(f"Sending >> {prompt_text}")
    print("...")
    print("Generating image...")
    print("...")
    # Simulate a successful response
    print("SUCCESS: Image generated at hypothetical URL: [https://mystorage.com/image123.png](https://mystorage.com/image123.png)")
    print("==========================================")


# ==========================================
# RUNNING THE APP SIMULATION
# ==========================================

# --- Step 1: Initial User Idea ---
initial_idea = "A lady is eating ice cream in night time."
response_1 = run_turn(initial_idea, "Phase 1: Strategy Menu")

# --- Step 2: User chooses a Vibe (Simulating user choice 'C') ---
# In a real UI, you would wait for actual user text input here.
user_choice_vibe = "C"
response_2 = run_turn(user_choice_vibe, "Phase 2: Recipe Menu")

# --- Step 3: User chooses a Recipe (Simulating user choice '2') ---
user_choice_recipe = "2"
final_response = run_turn(user_choice_recipe, "Phase 3: Final Prompt")

# --- Step 4: Extract and Execution ---
# We need to find the text inside the code block ``` ``` in the final response.
match = re.search(r"```(?:markdown)?(.*?)```", final_response, re.DOTALL)

if match:
    final_clean_prompt = match.group(1).strip()
    # Call the image generation function
    generate_image_from_text(final_clean_prompt)
else:
    print("Error: Could not find the final prompt code block in the response.")
