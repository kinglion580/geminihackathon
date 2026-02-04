# Setup Guide

## Prerequisites

1. Python 3.8 or higher
2. Google Gemini API key

## Installation

### 1. Install Dependencies

```bash
pip install google-genai rich
```

### 2. Configure API Key

The application requires a Gemini API key to function. **Never commit your API key to git**.

#### Option A: Environment Variable (Recommended)

```bash
export GEMINI_API_KEY="your-api-key-here"
```

To make it permanent, add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### Option B: .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your-actual-api-key
   ```

3. Load it before running scripts:
   ```bash
   source .env
   ```

### 3. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and configure it as shown above

## Usage

### Run the Interactive CLI

```bash
python ai_act_cli.py
```

### Query the AI Act

```bash
python query_ai_act.py "What are prohibited AI practices?"
```

### Setup File Search Store (First Time)

```bash
python setup_ai_act_store.py
```

## Security Notes

⚠️ **IMPORTANT**:
- Never commit your `.env` file to git
- Never hardcode API keys in source code
- The `.gitignore` file is configured to prevent accidental commits
- If you accidentally commit a key, revoke it immediately and generate a new one

## Troubleshooting

**Error: GEMINI_API_KEY environment variable not set**
- Make sure you've exported the environment variable or created a `.env` file
- Verify the key is set: `echo $GEMINI_API_KEY`

**Error: 'google-genai' package not found**
- Install dependencies: `pip install google-genai rich`
