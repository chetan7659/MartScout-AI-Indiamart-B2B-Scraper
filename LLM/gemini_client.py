import google.generativeai as genai
from Helpers.config import GEMINI_API_KEY

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str, model_name="gemini-1.5-flash", temperature=0.7):
    """
    Queries the Gemini model with a given prompt.
    """
    try:
        model = genai.GenerativeModel(model_name)
        
        # Constructing the message with system context
        # Since Gemini 1.0 Pro doesn't strictly support system instructions as a separate parameter in the basic API yet (or it varies),
        # we can include it in the prompt or use the system_instruction argument if using 1.5.
        # Using 1.5 flash as default which supports system instructions usually, but to be safe and compatible:
        
        system_prompt = "You are an expert in Indiamart B2B products and market analysis."
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature
        )
        
        response = model.generate_content(full_prompt, generation_config=generation_config)
        
        if response.text:
            return response.text
        else:
            return "No response generated."
            
    except Exception as e:
        return f"Error contacting Gemini API: {e}"
