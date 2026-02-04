---
source_url: http://geminicli.com/docs/cli/model-routing
source_type: llms-txt
content_hash: sha256:d58e841eaeb23b7c231665dcb8219bfdd828fbe704ab3370624adb38e668a862
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"ee517f83c5c9de91334fb54cd13de145d7dea07828f7b2d6b2d6253bd233e333"'
last_modified: '2025-12-17T22:33:12Z'
---

# Untitled

## Model routing

Gemini CLI includes a model routing feature that automatically switches to a
fallback model in case of a model failure. This feature is enabled by default
and provides resilience when the primary model is unavailable.

## How it works

Model routing is managed by the `ModelAvailabilityService`, which monitors model
health and automatically routes requests to available models based on defined
policies.

1.  **Model failure:** If the currently selected model fails (e.g., due to quota
    or server errors), the CLI will iniate the fallback process.

2.  **User consent:** Depending on the failure and the model's policy, the CLI
    may prompt you to switch to a fallback model (by default always prompts
    you).

3.  **Model switch:** If approved, or if the policy allows for silent fallback,
    the CLI will use an available fallback model for the current turn or the
    remainder of the session.

### Model selection precedence

The model used by Gemini CLI is determined by the following order of precedence:

1.  **`--model` command-line flag:** A model specified with the `--model` flag
    when launching the CLI will always be used.
2.  **`GEMINI_MODEL` environment variable:** If the `--model` flag is not used,
    the CLI will use the model specified in the `GEMINI_MODEL` environment
    variable.
3.  **`model.name` in `settings.json`:** If neither of the above are set, the
    model specified in the `model.name` property of your `settings.json` file
    will be used.
4.  **Default model:** If none of the above are set, the default model will be
    used. The default model is `auto`
