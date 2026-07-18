import pandas as pd
import json
import os
import argparse
from anthropic import Anthropic

# Ensure you run: export ANTHROPIC_API_KEY="your-key-here" before running
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "mock_key"))

def load_and_clean_data(gsc_path, ga4_path):
    print("[1/3] Loading and cleaning raw GSC and GA4 data...")
    # Load GSC Data
    gsc_df = pd.read_csv(gsc_path)
    
    # Clean: Drop anonymized queries (where query is NaN or empty)
    initial_len = len(gsc_df)
    gsc_df = gsc_df.dropna(subset=['query'])
    print(f"      Dropped {initial_len - len(gsc_df)} anonymized queries.")
    
    # Load GA4 Data
    with open(ga4_path, 'r') as f:
        ga4_raw = json.load(f)
    
    # Flatten the snake_case JSON events
    ga4_df = pd.json_normalize(ga4_raw['events'])
    
    # Join on the URL
    merged_df = pd.merge(gsc_df, ga4_df, left_on='landing_page', right_on='page_location', how='inner')
    
    # Filter for 'Striking Distance' keywords (Position 3-15)
    striking_distance = merged_df[(merged_df['position'] >= 3) & (merged_df['position'] <= 15)]
    print(f"      Found {len(striking_distance)} striking distance opportunities.")
    
    return striking_distance

def classify_intent_with_llm(data_chunk):
    print("[2/3] Calling Anthropic API for Semantic Analysis...")
    prompt = f"""You are a Senior SEO Data Scientist. 
    Analyze this striking distance data and output a JSON array of the top content actions.
    Categorize intent into: Comparison, Replacement, Risk, or Use-case.
    Focus on high impression but low CTR anomalies, or high bounce rate intent mismatches.
    Output ONLY a raw JSON array.
    
    Data Chunk:
    {data_chunk}
    """
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="Always output raw JSON. Do not include markdown blocks like ```json.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"\n[API WARN] Anthropic API failed (Did you set your API key?). Falling back to mock response.\nError: {e}")
        return '[{"url": "/magnesium-benefits", "query": "magnesium side effects", "intent": "Risk", "recommendation": "Intent Mismatch: Page is promotional but query implies risk. Add a safety/dosage section."}]'

if __name__ == "__main__":
    print("=== Semantic SEO Opportunity Agent Started ===\n")
    
    # 1. Load Data
    df = load_and_clean_data("mock_gsc_data.csv", "mock_ga4_data.json")
    
    # 2. Extract top leverage pages to save tokens
    top_targets = df.nlargest(5, 'impressions')
    
    # Drop PII or irrelevant columns before sending to LLM
    clean_chunk = top_targets[['query', 'landing_page', 'impressions', 'position', 'ctr', 'bounce_rate']].to_dict(orient='records')
    
    # 3. Analyze
    recommendations = classify_intent_with_llm(json.dumps(clean_chunk, indent=2))
    
    # 4. Output final results
    print("\n[3/3] Agent Completed Successfully. Final Output:")
    print("==================================================")
    print(recommendations)
    print("==================================================")
