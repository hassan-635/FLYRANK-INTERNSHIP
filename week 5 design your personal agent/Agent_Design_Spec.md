# Week 5: Design Your Personal Agent

## 1. Job to be Done
**The Agent:** The Semantic SEO Opportunity Scorer.
**The Job:** Given raw Google Search Console (GSC) and Google Analytics 4 (GA4) data from the FlyRank Hackathon dataset, the agent will analyze the performance data, classify the underlying search intent of the queries, and output a ranked list of the top 5 highest-leverage content actions (e.g., "Rewrite Title", "Merge Pages") based on expected business impact rather than simple search volume.

## 2. The User and Usage Frequency
**User:** Me (Backend/Data Intern working on the FlyRank brief).
**Frequency:** Run once a week during the content strategy sprint to prioritize work.

## 3. Tools and Data Needed (Access Plan)
- **Data Source 1:** GSC Site & URL Impressions (CSV exports, provided in the hackathon brief).
- **Data Source 2:** GA4 Raw Event Export (JSON nested format).
- **Tool 1 (Data Processor):** A Python Pandas script to load the data, flatten the `snake_case` GA4 JSON, and join the GSC and GA4 datasets on the *Landing Page URL* (since GA4 lacks query data).
- **Tool 2 (Intent Classifier):** An LLM API connection to classify queries into 4 specific semantic buckets: Comparison, Replacement, Risk/Safety, or Use-case.

## 4. Draft Instructions (System Prompt)
> "You are a Senior SEO Data Scientist. I am providing you with a joined dataset containing Google Search Console impression data and GA4 engagement data. 
> Your goal is to prioritize content actions by business impact.
> 1. Ignore rows where the query field is blank (anonymized data).
> 2. Identify 'Striking Distance' pages (pages ranking in positions 3–15).
> 3. Identify High-Impression / Low-CTR anomalies.
> 4. Classify the semantic intent of the top queries for these pages into: Comparison, Replacement, Risk, or Use-case.
> 5. Output a JSON array containing the Top 5 most urgent content recommendations, including the URL, the identified problem (e.g., 'Intent Mismatch'), and the recommended action (e.g., 'Rewrite Title')."

## 5. Five Eval Cases (Pre-Build)
Before the agent is considered successful, it must pass these 5 scenarios based on the FL-03 standard:
1. **The Striking Distance:** Input is a page with 10k impressions, position 4.2, and CTR 1%. **Expected Output:** High-priority recommendation for a Title/Meta description rewrite.
2. **The Anonymized Row:** Input contains a row with high traffic but a blank/null search query. **Expected Output:** The agent ignores the row or flags it as anonymized without attempting to classify its "intent".
3. **The Intent Mismatch:** Input is a page ranking #2 for "safe alternatives to epsom salt", but GA4 shows an 85% bounce rate and zero purchases. **Expected Output:** High-priority recommendation stating "Content intent mismatch - page is likely transactional but query is informational."
4. **The Cannibalization:** Input shows two different URLs (`/magnesium-benefits` and `/benefits-of-magnesium`) both ranking position 8 for the same query cluster. **Expected Output:** Recommendation to consolidate/merge the pages.
5. **The Winner:** Input is a page ranking Position 1 with a 35% CTR and high conversion rate. **Expected Output:** Agent ignores this page completely. Do not fix what isn't broken.

## 6. Risks and Guardrails
- **Risk:** Hallucinating traffic data to justify a narrative. 
  - **Guardrail:** The agent must only use the numbers provided in the Python DataFrame context. If a metric is missing, it must output "Insufficient Data" rather than guessing.
- **Risk:** Violating client confidentiality. 
  - **Guardrail:** The script will strip out raw Personal Identifiable Information (PII) from the GA4 export *before* passing the aggregated data chunks to the LLM API.

## 7. Build Platform Choice & Justification
**Platform Chosen:** A Scripted Agent (Python + Pandas + Anthropic API).
**Justification against alternatives:** I initially considered a Claude Project or a Custom ChatGPT. However, the brief states the GA4 export contains ~1,700 nested JSON events per day and GSC has ~8,000 rows. Dropping 10,000+ rows of raw, unjoined CSV/JSON text into a standard chat window will either hit token limits, cause massive hallucinations, or crash. 
As a backend intern, writing a local Python script is free and highly scalable. Pandas can easily flatten the GA4 JSON and join the data on the URL in milliseconds. The script will then send only the *aggregated, filtered* anomalies to the Anthropic API for semantic classification. This leverages code for what code does best (math and joins) and AI for what AI does best (semantic reasoning).
