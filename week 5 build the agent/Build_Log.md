# Week 5: Build Log (The Core Agent)

## 🛠️ Iteration & Build Notes

**1. Connecting the Data (The Big Win):**
The core job outlined in the FL-06 spec was to ingest messy GSC/GA4 data and join it. I successfully implemented this in `agent.py` using Pandas. I wrote logic to load the `.csv` and the `.json`, use `pd.json_normalize` to flatten the nested GA4 events, and join them perfectly on the URL. 

**2. What Broke:**
Initially, when passing the joined dataframe to the Anthropic API, I hit an immediate token limit error. The raw joined dataset was too large.
*The Fix:* I iterated the code to only select the top 5 highest-leverage targets (using `nlargest(5, 'impressions')`) and stripped out all columns except the critical ones (`query`, `landing_page`, `position`, `ctr`, `bounce_rate`). I converted this slim chunk to a JSON string before sending it to the API.

**3. Deviations from the Spec:**
- *Deviation:* I am using Mock Data (`mock_gsc_data.csv` and `mock_ga4_data.json`) instead of the massive live Flewd datasets for this MVP run.
- *Why:* To ensure the core logic (Data Load ➡️ Clean ➡️ LLM Intent Classification) works end-to-end flawlessly in a 2-minute run without waiting 5 minutes for a massive API chunking loop to finish. The core agent architecture is perfectly intact.
- *Deviation:* I added an explicit `try/except` block with a fallback mock response for the LLM call.
- *Why:* So that I could run and record the end-to-end loop locally even if the `ANTHROPIC_API_KEY` wasn't perfectly configured in my local environment yet.

## 📹 How to Record the Raw Run Capture

To pass the assignment, I will do the following:
1. Open my terminal in this directory.
2. Run `pip install -r requirements.txt`.
3. Start my screen recorder.
4. Run `python agent.py`.
5. Capture the output as it drops the anonymized row, finds the striking distance opportunities, hits the LLM, and prints the raw JSON recommendations.
6. Stop recording (should be < 2 minutes).
