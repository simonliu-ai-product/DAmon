# DAmon

[![PyPI - Version](https://img.shields.io/pypi/v/DAmon/0.1.0)](https://pypi.org/project/DAmon/0.1.0/)

Data Arrangement/Annotation via Simon's tool.

A CLI tool to extract structured Q&A from documents using Large Language Models (LLMs). 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Extracting Q&A](#extracting-qa)
  - [Pushing to Hugging Face Hub](#pushing-to-hugging-face-hub)
- [Supported Document Types](#supported-document-types)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Document Parsing**: Automatically parses content from various document formats (PDF, CSV, DOCX, PPTX).
- **LLM-powered Q&A Extraction**: Utilizes Litellm to interact with different LLMs (e.g., gemini/gemini-2.5-flash) to extract question-answer pairs and the AI's thought process.
- **Flexible Output**: Exports extracted Q&A into `JSONL`, `CSV`, or `Parquet` formats.
- **Batch Processing**: Processes single files or entire directories of documents.
- **Hugging Face Hub Integration**: Easily push your extracted datasets to the Hugging Face Hub.

## Installation

Install the package from PyPI:

```bash
pip install DAmon
```

## Configuration

This tool uses `litellm` to interact with various LLM providers. You'll need to set up your API keys and specify the model.

Create a `.env` file in the root directory of the project and add your Litellm model and API key. For example, if you are using OpenAI:

```dotenv
GEMINI_API_KEY=<gemini-api-key>
```

Refer to the [Litellm documentation](https://litellm.ai/docs/providers) for details on configuring different LLM providers and their respective environment variables.

## Usage

The main command-line interface is `damon`.

### Processing Documents

Use the `process` command to process documents and extract Q&A pairs.

```bash
damon process <INPUT_PATH> [OPTIONS]
```

-   `<INPUT_PATH>`: Path to the input document (file or directory).

**Options:**

-   `--input-format [pdf|csv|docx|pptx|auto]`: Format of the input document(s). Use `"auto"` to detect based on file extension. Default: `auto`.
-   `--model TEXT`: Litellm model name to use for Q&A extraction. 
-   `--output-path PATH`: Path to save the extracted Q&A. Can be a file or a directory. If a directory, a timestamped file will be created. Default: `results/output.jsonl`.
-   `--export-format [jsonl|csv|parquet]`: Format for exporting the extracted Q&A. Default: `jsonl`.
-   `--num-qa INTEGER`: Number of Q&A pairs to extract per document. If not specified, extracts as many as possible.

**Examples:**

1.  **Process a single PDF file, output to CSV:**

    ```bash
    damon process --input data/test.pdf --model gemini/gemini-2.5-flash --output results/cyber_output --export csv --num-qa 5
    ```

2.  **Process all documents in a directory, auto-detect format, output to JSONL:**

    ```bash
    damon extract data/ --input-format auto --output-path results/ --export-format jsonl
    ```

3.  **Process a specific number of Q&A pairs from a DOCX file:**

    ```bash
    damon process documents/report.docx --input-format docx --num-qa 5 --output-path results/report_qa.jsonl
    ```

### Pushing to Hugging Face Hub

Use the `push-to-hf` command to upload your extracted dataset files to the Hugging Face Hub.

```bash
damon push-to-hf --input-file <FILE_PATH> --repo-id <REPO_ID> [--split <SPLIT_NAME>]
```

-   `--input-file <FILE_PATH>`: Path to the data file to push (e.g., `results/output.jsonl`).
-   `--repo-id <REPO_ID>`: Hugging Face Hub repository ID (e.g., `your-username/your-dataset-repo`).
-   `--split <SPLIT_NAME>`: Optional. The name of the dataset split (e.g., `train`, `validation`, `test`). Defaults to `train`.

**Prerequisites for pushing:**

-   You need to have the `datasets` and `huggingface_hub` libraries installed (`pip install datasets huggingface_hub`).
-   You must be logged in to Hugging Face. Run `huggingface-cli login` in your terminal and follow the prompts.

**Example:**

```bash
damon push-to-hf --input-file results/output_20250630_140154.csv --repo-id your-username/my-extracted-qa-dataset --split train
```

## Supported Document Types

-   `.pdf` (Portable Document Format)
-   `.csv` (Comma Separated Values)
-   `.docx` (Microsoft Word Document)
-   `.pptx` (Microsoft PowerPoint Presentation)

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. (Note: A `LICENSE` file is not included in the provided context, but it's good practice to include one.)

## Author
Simon Liu

A technology enthusiast in the field of artificial intelligence solutions, he focuses on helping companies to introduce generative artificial intelligence, MLOps and large language model (LLM) technologies to promote digital transformation and technology implementation. ​

Currently, he is also a Google GenAI developer expert (GDE), actively participating in the technical community, promoting the application and development of AI technology through technical articles, speeches and practical experience sharing. Currently, he has published more than 100 technical articles on the Medium platform, covering topics such as generative AI, RAG and AI Agent, and has served as a speaker in technical seminars many times to share the practical application of AI and generative AI. ​

My Linkedin: https://www.linkedin.com/in/simonliuyuwei/