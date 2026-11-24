"""Transcripts as LangChain Documents, the text as page_content and the source's details as
metadata: ready for a splitter, an embedding model and a vector store.

    pip install apify-client langchain-core
    python langchain_documents.py
"""
import os
import sys

from apify_client import ApifyClient
from langchain_core.documents import Document

sys.stdout.reconfigure(encoding="utf-8")  # transcripts come in any script; a Windows console's code page fails on most
client = ApifyClient(os.environ["APIFY_TOKEN"])


def transcripts(actor: str, run_input: dict) -> list[Document]:
    run = client.actor(actor).call(run_input=run_input, logger=None)
    return [Document(page_content=item["text"], metadata={
                "source": item.get("url") or item.get("episodeUrl") or item.get("audioUrl"),
                "title": item.get("title") or item.get("episodeTitle") or item.get("description"),
                "language": item.get("language"), "durationSeconds": item.get("durationSeconds"),
                "publishedAt": item.get("publishedAt") or item.get("createdAt")})
            for item in client.dataset(run.default_dataset_id).iterate_items() if item.get("text")]


docs = transcripts("pikoulas/youtube-transcripts", {"searchQueries": ["retrieval augmented generation"], "maxVideosPerSource": 5})
docs += transcripts("pikoulas/podcast-transcripts", {"podcasts": ["Lex Fridman Podcast"], "maxEpisodes": 1, "maxMinutesPerEpisode": 10})
for d in docs:
    print(d.metadata["title"], len(d.page_content), "characters")
