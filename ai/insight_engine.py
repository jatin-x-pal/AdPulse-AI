from ai.openai_client import get_openai_client
from ai.prompt_builder import build_analysis_prompt

def generate_marketing_insights(metrics: dict, audiences: list, forecast: list) -> str:
    """Calls the OpenAI completions endpoint with our generated prompt."""
    client = get_openai_client()
    if not client:
        return "Error: OPENAI_API_KEY environment variable not set. Please add it to your `.env` file."
        
    prompt = build_analysis_prompt(metrics, audiences, forecast)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior digital marketing analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with OpenAI API: {str(e)}"
