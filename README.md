# Gemini Extractor

A simple CLI tool that uses Google Gemini (via the `google-genai` SDK) to parse unstructured markdown product files and extract user-specified fields into a clean, human‑readable output.

---

## Features

* Reads from any markdown file containing product descriptions.
* Extracts one or more specified fields (e.g. `Name`, `Price`, `Overview`).
* Cleans up Gemini’s response (strips code fences) and outputs plain text or a JSON list.
* Configurable via environment variables for API keys.
* Lightweight CLI interface.

---

## Prerequisites

* **Python 3.8+** installed.
* A Google Cloud project with access to Gemini API and a valid API key.
* [uv](https://github.com/universa-io/uv) (Python package manager) installed globally.

---

## Installation

You can set up the project either with **uv** or with **pip**. Both workflows create an isolated Python environment.

### A) Using uv

1. Clone this repository:

   ```bash
   git clone https://github.com/your-org/gemini-extractor.git
   cd gemini-extractor
   ```
2. Initialize `uv` project (:

   ```bash
   uv init
   ```
3. Create a virtual environment using `uv` and activate it:

   ```bash
   uv venv
   ```

   Then activate:

   ```bash
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate   # Windows
   ```
4. Install dependencies with `uv`:

   ````bash
   uv add google-genai python-dotenv
   ````

### B) Using pip

1. Clone this repository:

   ```bash
   git clone https://github.com/your-org/gemini-extractor.git
   cd gemini-extractor
   ```
2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate   # Windows
   ```
3. Install dependencies via `pip`:

   ```bash
   pip install google-genai python-dotenv
   ```

### Common Step

4. Create a `.env` file in the project root and add your Gemini key:

   ````ini
   GEMINI_API_KEY=your_actual_api_key_here
   ````

Run the CLI tool to extract fields from a markdown file:

```bash
python main.py --file prod1info.md --keys Name Price Overview
```

* `--file` (or `-f`): Path to the markdown file (defaults to `prod1info.md`).
* `--keys` (or `-k`): One or more field names to extract (e.g. `Name`, `SKU`, `Price`).

### Output Behavior

* **Single key**: prints the raw value only (human‑readable).
* **Multiple keys**: prints each as `Field: value` on separate lines.

---

## Example

Given `prod1info.md`:

```md
# Product Details
**Name:** UltraWidget 3000
**Price:** $149.99
**Overview:** Wireless charging, waterproof, 24h battery
```

```bash
python .\main.py -k box style
```

```
box: 1 graphic printed oversized t-shirt
style: Graphic Print
```

---

## Configuration

* **`GEMINI_API_KEY`**: Your Gemini API key, loaded via `python-dotenv` from `.env`.
* **Model**: By default the script uses `gemini-2.0-flash`. To change it, edit the `model` parameter in `main.py`.
* **Prompt Instructions**: Tweak `system_instruction` in `extract_fields_from_file()` to refine extraction behavior.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
