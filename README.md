# SKI AI Agent

SKI is a simple AI agent I built while learning from Boot.dev. It’s a lightweight project focused on understanding how agents work under the hood rather than building something overly complex.

The agent can read files, inspect directories, write files, and execute Python scripts based on a user’s prompt.

---

## What it does

* Accepts a natural language prompt
* Uses Gemini (`gemini-2.5-flash`) for reasoning
* Calls tools when needed
* Iterates until it reaches a final answer

At its core, this is a basic implementation of an LLM-powered agent loop.

---

## How it works

1. The user provides a prompt
2. The model analyzes the request
3. If needed, it calls a function (tool)
4. The function result is sent back to the model
5. The process repeats until no more tool calls are needed

---

## Available Tools

* `get_files_info` — list files in a directory
* `get_file_content` — read file contents
* `write_file` — write content to a file
* `run_python_file` — execute Python files with optional arguments

---

## Setup

```bash
git clone <your-repo>
cd ai-agent
uv venv
uv pip install -r requirements.txt
```

Set your Gemini API key:

```bash
export GOOGLE_API_KEY=your_api_key
```

---

## Usage

```bash
uv run main.py "how does the calculator render results to the console"
```

Verbose mode:

```bash
uv run main.py "your prompt" --verbose
```

---

## Notes

* This is a learning project, not production-ready
* Python execution is not sandboxed
* Limited to 10 iterations per run
* Error handling is minimal

---

## What I learned

* How LLM tool calling works
* Structuring messages using Content and Part
* Building an agent loop
* Handling function calls and responses
* Debugging schema and API errors

---

## Future Improvements

* Streaming responses
* Better error handling
* Sandboxed execution
* Persistent memory
* Improved tool selection

---

## Credits

Built while learning from Boot.dev.
