# DAmon

[![PyPI - Version](https://img.shields.io/pypi/v/DAmon/0.1.2)](https://pypi.org/project/DAmon/0.1.2/)

Data Arrangement/Annotation via Simon's tool.

一個使用大型語言模型 (LLMs) 從文件中提取結構化問答的命令列工具 (CLI)。

## 目錄

- [功能](#功能)
- [安裝](#安裝)
- [設定](#設定)
- [使用方式](#使用方式)
  - [提取問答](#提取問答)
  - [推送到 Hugging Face Hub](#推送到-hugging-face-hub)
- [支援的文件類型](#支援的文件類型)
- [貢獻](#貢獻)
- [授權](#授權)

## 功能

- **文件解析**：自動解析各種文件格式（PDF、CSV、DOCX、PPTX）的內容。
- **LLM 驅動的問答提取**：利用 Litellm 與不同的 LLM（例如 gemini/gemini-2.5-flash）互動，以提取問答對和 AI 的思考過程。
- **彈性輸出**：將提取的問答匯出為 `JSONL`、`CSV` 或 `Parquet` 格式。
- **批次處理**：處理單一文件或整個文件目錄。
- **Hugging Face Hub 整合**：輕鬆將您提取的資料集推送到 Hugging Face Hub。

## 安裝

從 PyPI 安裝套件：

```bash
pip install DAmon
```

## 設定

此工具使用 `litellm` 與各種 LLM 提供商互動。您需要設定您的 API 金鑰並指定模型。

在專案的根目錄中建立一個 `.env` 檔案，並新增您的 Litellm 模型和 API 金鑰。例如，如果您使用 OpenAI：

```dotenv
GEMINI_API_KEY=<gemini-api-key>
```

請參閱 [Litellm 文件](https://litellm.ai/docs/providers) 以了解如何設定不同的 LLM 提供商及其各自的環境變數。

### 自訂提示範本

您可以自訂 LLM 的提示範本。`damon` 命令將在執行目錄中尋找名為 `DAMON_PROMPT.md` 的檔案。

- 如果 `DAMON_PROMPT.md` 存在，其內容將用作 `PROMPT_TEMPLATE`。
- 如果 `DAMON_PROMPT.md` 不存在，將使用 `DAmon/core.py` 中嵌入的預設提示範本。

專案根目錄中提供了一個範本檔案 `DAMON_PROMPT_template.md`。您可以複製並將此檔案重新命名為 `DAMON_PROMPT.md` 以開始自訂您的提示。

## 使用方式

主要的命令列介面是 `damon`。

### 處理文件

使用 `process` 命令處理文件並提取問答對。

```bash
damon process <INPUT_PATH> [OPTIONS]
```

-   `<INPUT_PATH>`：輸入文件（檔案或目錄）的路徑。

**選項**：

-   `--input-format [pdf|csv|docx|pptx|auto]`：輸入文件格式。使用 `"auto"` 根據檔案副檔名自動偵測。預設值：`auto`。
-   `--model TEXT`：用於問答提取的 Litellm 模型名稱。
-   `--output-path PATH`：儲存提取問答的路徑。可以是檔案或目錄。如果是目錄，將建立一個帶有時間戳記的檔案。預設值：`results/output.jsonl`。
-   `--export-format [jsonl|csv|parquet]`：匯出提取問答的格式。預設值：`jsonl`。
-   `--num-qa INTEGER`：每個文件要提取的問答對數量。如果未指定，則盡可能多地提取。

**範例**：

1.  **處理單一 PDF 檔案，輸出為 CSV**：

    ```bash
    damon process --input data/test.pdf --model gemini/gemini-2.5-flash --output results/cyber_output --export csv --num-qa 5
    ```

2.  **處理目錄中的所有文件，自動偵測格式，輸出為 JSONL**：

    ```bash
    damon process data/ --input-format auto --output-path results/ --export-format jsonl
    ```

3.  **從 DOCX 檔案處理特定數量的問答對**：

    ```bash
    damon process documents/report.docx --input-format docx --num-qa 5 --output-path results/report_qa.jsonl
    ```

### 推送到 Hugging Face Hub

使用 `push-to-hf` 命令將您提取的資料集檔案上傳到 Hugging Face Hub。

```bash
damon push-to-hf --input-file <FILE_PATH> --repo-id <REPO_ID> [--split <SPLIT_NAME>]
```

-   `--input-file <FILE_PATH>`: 要推送的資料檔案路徑（例如 `results/output.jsonl`）。
-   `--repo-id <REPO_ID>`: Hugging Face Hub 儲存庫 ID（例如 `your-username/your-dataset-repo`）。
-   `--split <SPLIT_NAME>`: 選項。資料集分割的名稱（例如 `train`、`validation`、`test`）。預設為 `train`。

**推送先決條件**：

-   您需要安裝 `datasets` 和 `huggingface_hub` 函式庫（`pip install datasets huggingface_hub`）。
-   您必須登入 Hugging Face。在您的終端機中執行 `huggingface-cli login` 並按照提示操作。

**範例**：

```bash
damon push-to-hf --input-file results/output_20250630_140154.csv --repo-id your-username/my-extracted-qa-dataset --split train
```

## 支援的文件類型

-   `.pdf` (可攜式文件格式)
-   `.csv` (逗號分隔值)
-   `.docx` (Microsoft Word 文件)
-   `.pptx` (Microsoft PowerPoint 簡報)

## 貢獻

歡迎貢獻！請隨時開啟議題或提交拉取請求。

## 授權

此專案根據 MIT 授權條款授權 - 有關詳細資訊，請參閱 `LICENSE` 檔案。（注意：提供的內容中不包含 `LICENSE` 檔案，但包含一個是很好的做法。）

## 特別感謝

特別感謝 Thomas Chong 為這個專案製作了 [DeepWiki 文件](https://deepwiki.com/simonliu-ai-product/DAmon/1-damon-overview)。

## 作者簡介
劉育維（Simon Liu）

為人工智慧解決方案領域的技術愛好者，專注於協助企業如何導入生成式人工智慧、MLOps 與大型語言模型（LLM）技術，推動數位轉型與技術落地如何實踐。​

目前也是 Google GenAI 領域開發者專家（GDE），積極參與技術社群，透過技術文章、演講與實務經驗分享，推廣 AI 技術的應用與發展，目前，在 Medium 平台上發表超過百篇技術文章，涵蓋生成式 AI、RAG 和 AI Agent 等主題，並多次擔任技術研討會中的講者，分享 AI 與生成式 AI 的實務應用。​

My Linkedin: https://www.linkedin.com/in/simonliuyuwei/