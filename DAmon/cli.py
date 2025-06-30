import click
from loguru import logger
import os
from dotenv import load_dotenv

from .core import process_documents
from . import __version__

# Load environment variables from .env file
load_dotenv()

@click.group()
@click.version_option(version=__version__)
def cli():
    """
    DAmon: Data Arrangement/Annotation via simon tool.
    """
    # Default logging setup for non-verbose commands
    logger.remove() # Remove default handler
    logger.add(lambda msg: click.echo(msg, err=True), level="INFO", format="{message}")


@cli.command()
@click.option('--input', 'input_path', required=True, type=click.Path(exists=True),
              help='Path to a single file or a directory to scan.')
@click.option('--format', 'input_format', type=click.Choice(['auto', 'csv', 'pdf', 'doc', 'ppt']), default='auto',
              help='Specify input file format. "auto" attempts to detect.')
@click.option('--model', 'litellm_model_name', required=True, type=str,
              help='The litellm model name to use for Q&A extraction (e.g., "gpt-4", "claude-3-opus-20240229").')
@click.option('--output', 'output_path', required=True, type=click.Path(),
              help='Path to the output file or directory.')
@click.option('--export', 'export_format', type=click.Choice(['jsonl', 'csv', 'parquet']), default='jsonl',
              help='Output dataset format.')
@click.option('--num-qa', 'num_qa_pairs', type=int, default=None,
              help='Number of Q&A pairs to extract. LLM will be prompted to extract this many, and output will be truncated if more are returned.')
@click.option('--verbose', is_flag=True, help='Enable verbose logging for this command.')
def process(input_path, input_format, litellm_model_name, output_path, export_format, num_qa_pairs, verbose):
    """
    Process documents to extract Q&A content.
    """
    logger.remove() # Remove default handler
    if verbose:
        logger.add("file.log", rotation="10 MB", level="DEBUG")
        logger.enable("DataArragimon")
        logger.debug("Verbose logging enabled for process command.")
    else:
        logger.add(lambda msg: click.echo(msg, err=True), level="INFO", format="{message}")
        logger.enable("DataArragimon")

    logger.info(f"Starting document processing for: {input_path}")
    logger.info(f"Using model: {litellm_model_name}")
    logger.info(f"Exporting to: {output_path} in {export_format} format")

    try:
        process_documents(
            input_path=input_path,
            input_format=input_format,
            litellm_model_name=litellm_model_name,
            output_path=output_path,
            export_format=export_format,
            num_qa_pairs=num_qa_pairs
        )
        logger.info("Document processing completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")
        exit(1)

@cli.command()
@click.option('--input-file', 'input_file_path', required=True, type=click.Path(exists=True),
              help='Path to the data file to push (CSV, JSONL, or Parquet).')
@click.option('--repo-id', 'repo_id', required=True, type=str,
              help='The Hugging Face Hub repository ID (e.g., "your-username/your-dataset").')
@click.option('--split', 'split_name', type=click.Choice(['train', 'validation', 'test']), default='train',
              help='The name of the dataset split (e.g., "train", "validation", "test"). Defaults to "train".')
@click.option('--verbose', is_flag=True, help='Enable verbose logging for this command.')
def push_to_hf(input_file_path, repo_id, split_name, verbose):
    """
    Push extracted data to a Hugging Face Datasets repository, specifying a split.
    """
    logger.remove() # Remove default handler
    if verbose:
        logger.add("file.log", rotation="10 MB", level="DEBUG")
        logger.enable("DAmon")
        logger.debug("Verbose logging enabled for push-to-hf command.")
    else:
        logger.add(lambda msg: click.echo(msg, err=True), level="INFO", format="{message}")
        logger.enable("DAmon")

    logger.info(f"Attempting to push {input_file_path} as split '{split_name}' to Hugging Face Hub repository: {repo_id}")
    try:
        from .core import push_to_hub
        from datasets import Dataset, DatasetDict
        import pandas as pd
        import os

        file_ext = os.path.splitext(input_file_path)[1].lower()
        df = None
        if file_ext == '.jsonl':
            df = pd.read_json(input_file_path, lines=True)
        elif file_ext == '.csv':
            df = pd.read_csv(input_file_path)
        elif file_ext == '.parquet':
            df = pd.read_parquet(input_file_path)
        else:
            logger.error(f"Unsupported file format for pushing to Hugging Face Hub: {file_ext}")
            exit(1)
        
        if df is not None:
            dataset = Dataset.from_pandas(df)
            dataset_dict = DatasetDict({split_name: dataset})
            push_to_hub(dataset_dict, repo_id)
        else:
            logger.error("Failed to load data into DataFrame.")
            exit(1)

        logger.info("Data push to Hugging Face Hub completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during data push to Hugging Face Hub: {e}")
        exit(1)

if __name__ == '__main__':
    cli()
