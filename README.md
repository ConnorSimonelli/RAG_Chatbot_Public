Overview:
    Purpose: CLI RAG chatbot that crawls a website, embeds scraped pages into a FAISS vector store, and answers questions using LangChain + OpenAI.
    Flow: Crawl pages → save text in RAGData/ → embed to faissIndex/ → query via RetrievalQA.

Features:
    Web crawler using Playwright + BeautifulSoup, respects robots.txt.
    Embedding with OpenAI text-embedding-3-large into FAISS.
    RetrievalQA over embedded docs with gpt-4o-mini.
    Simple, interactive CLI workflow.

Project Structure:
    -app.py:1: CLI entry; orchestrates crawl, embedding, chat loop.
    -crawler.py:1: Playwright-based crawler, robots.txt checks, saves text to RAGData/.
    -defineModel.py:1: Builds LangChain RetrievalQA with ChatOpenAI.
    -embedding.py:1: Loads RAGData/, splits, embeds to FAISS, returns retriever.

Prerequisites:
    -Python 3.10+ recommended.
    -OpenAI API key with access to embeddings and chat models.
    -Chromium for Playwright.

Install:
    -Create venv and install dependencies:
    -python -m venv .venv && source .venv/bin/activate (Windows: .\.venv\Scripts\activate)
    -pip install -U pip
    -pip install langchain langchain-openai langchain-community faiss-cpu python-dotenv validators beautifulsoup4 playwright requests
    -python -m playwright install chromium
    -Create .env:
    -OPENAI_API_KEY=your_key_here

Usage:
    -Run: python app.py
    -When prompted:
    -Enter a valid URL to crawl (must allow crawling via robots.txt and format should be "https://example.com").
    -Choose number of pages (1–50).
    -Optionally add more sites.
    -Ask questions about the scraped content when prompted.
    -Type exit to quit.
    -On next run, you can choose to reuse or clear RAGData/.

How It Works:
    -Crawl: crawler.py uses Playwright to render pages and BeautifulSoup to extract text, saving .txt files into RAGData/.
    -Embed: embedding.py loads .txt files, splits, embeds with OpenAI, saves to faissIndex/, and returns a retriever.
    -QA: defineModel.py builds a RetrievalQA chain over the retriever using gpt-4o-mini.

Configuration:
    -Environment: .env must include OPENAI_API_KEY.
    -Models: Embeddings text-embedding-3-large, Chat gpt-4o-mini (see defineModel.py and embedding.py to adjust).

Troubleshooting:
    -No documents embedded: Ensure RAGData/ has .txt files (the crawler must have succeeded). Error appears in defineModel.generateQaChain().
    -Playwright errors: Ensure python -m playwright install chromium was run and network access is allowed.
    -URL rejected: The site may disallow crawling per robots.txt (checked in crawler.py).
    -Validators: If URL is rejected, ensure it’s a full valid URL (e.g., https://example.com).
    -Rate limiting/blocks: The crawler sleeps 3s between pages; still, sites may block automated scraping.

Ethics & Compliance:
    -Respects robots.txt, but you’re responsible for site terms and legal compliance.
    -Avoid overwhelming sites; adjust delays responsibly.

Known Limitations:
    -Interactive only: no CLI flags for non-interactive runs.
    -RAGData/ cleanup assumes only files live there (see app.py).
    -No persistence for conversation state beyond a single run.
    -Minimal error handling around network and scraping edge cases.