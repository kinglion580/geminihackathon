# Repository Guidelines

## Project Structure & Module Organization
Core automation lives in root-level scripts: `ai_act_cli.py` is the interactive Rich-based assistant, `query_ai_act.py` runs semantic search with Gemini File Search, `setup_ai_act_store.py` provisions the store, and `download_gdpr.py` scrapes GDPR references. Legal sources reside under `articles/` (individual article text files plus the consolidated `EU_AI_Act_Full_Text.txt`), while `store_info.txt` caches the remote store identifier created during setup. Keep additional assets alongside their producing scripts, and place any future tests inside `tests/` to mirror the module they cover.

## set up knowledge base
'setup_ai_act_store.py' supports to buld a knowledge base for EU AI Act and GDPR.
Before building the knowledge base, please check if there is an existing knowledge base that we can use.
If there is an existing knowledge base, please delete it and build a new one.
Please upload always all the files in the folder 'articles' to the knowledge base. 
If you find article that are similar to the articles in the folder 'articles', please do not upload them to the knowledge base.

## Build, Test, and Development Commands
Use Python 3.11+ with a virtual environment: `python -m venv .venv && source .venv/bin/activate`. Install runtime tooling with `pip install google-genai rich requests beautifulsoup4`. Provision the vector store through `python setup_ai_act_store.py`, inspect the CLI locally using `python ai_act_cli.py`, and issue single-shot questions via `python query_ai_act.py "What are prohibited AI practices?"`. Re-run `python download_gdpr.py` only if fresh GDPR content is needed because it performs 100 HTTP requests.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation, descriptive snake_case function names (`build_manual_context`) and PascalCase classes (`AIActAgent`). Keep constants uppercase near the top of each module and load secrets from environment variables before instantiating `genai.Client`. Favor Rich panels and Markdown blocks for any new terminal output so the UX remains consistent, and add docstrings to new public methods describing arguments and failure modes.

## Testing Guidelines
There are no automated tests yet, so add pytest-based coverage as you extend the fallback retrieval logic. Place specs under `tests/` using the `test_<module>.py` naming pattern and run them with `pytest -q`. For now, manual verification still matters: script a smoke check (`python ai_act_cli.py`, ask `Article 5 prohibitions`) and a fallback-path check (`python query_ai_act.py "List foundation model duties"` after temporarily revoking File Search).

## Commit & Pull Request Guidelines
The repository currently lacks Git history, so adopt conventional-commit prefixes (`feat:`, `fix:`, `docs:`) and keep subject lines under ~72 characters, present tense, e.g., `feat: add citation preview trimming`. Every PR should include a concise summary of the scenario, reproduction or validation commands, screenshots when UI output changes, and note whether Gemini credentials or article files were touched. Reference related policy tickets or issue IDs in the description to tie compliance changes back to their source.

## Security & Configuration Tips
Never commit live API keys; read them from `GEMINI_API_KEY` in the shell and consider `.env` + `python-dotenv` if you need local overrides. When working with `store_info.txt`, treat it as ephemeral—regenerate through `setup_ai_act_store.py` if secrets rotate. Scrapers should respect rate limits (keep the built-in `time.sleep(0.5)` delay) and log HTTP failures without dumping full payloads.

## Search in knowledge base 
The 'ai_act_cli.py' is a terminal-based agent for querying the EU AI Act (Regulation 2024/1689) and GDPR. Please use the knowledge base to answer the questions.
The agent is an expert legal assistant on the EU AI Act (Regulation 2024/1689) and GDPR. 
        
        CONTEXT DOCUMENT (Full Text of the Regulation):
        ================================================================================
        {full_text}
        ================================================================================
        
        Your goal is to provide accurate, comprehensive answers based ONLY on the provided context document above.
        
        Guidelines:
        1. ALWAYS cite specific Articles and paragraphs (e.g., "Article 5(1)").
        2. If the answer is not in the document, state that clearly.
        3. Be precise with legal definitions.
        4. Use structured formatting (bullet points, bold text).
