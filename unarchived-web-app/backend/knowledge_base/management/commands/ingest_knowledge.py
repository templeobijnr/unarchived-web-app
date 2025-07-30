import os
from django.core.management.base import BaseCommand
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models import KnowledgeChunk

class Command(BaseCommand):
    help = "Ingests knowledge base documents into pgvector"

    def handle(self, *args, **options):
        base_dir = "./knowledge_base"
        documents = []

        loader = DirectoryLoader(base_dir, loader_cls=TextLoader, glob="**/*.md", recursive=True)
        documents.extend(loader.load())

        pdf_loader = DirectoryLoader(base_dir, loader_cls=PyPDFLoader, glob="**/*.pdf", recursive=True)
        documents.extend(pdf_loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectors = embeddings.embed_documents([c.page_content for c in chunks])

        instances = []
        for i, chunk in enumerate(chunks):
            meta = chunk.metadata
            instances.append(KnowledgeChunk(
                content=chunk.page_content,
                embedding=vectors[i],
                domain=meta.get("domain", "unspecified"),
                subdomain=meta.get("subdomain", ""),
                entity_name=meta.get("entity_name", ""),
                source_document=meta.get("source", "unknown"),
                source_type="manual",
                confidence_score=1.0
            ))
        KnowledgeChunk.objects.bulk_create(instances)
        self.stdout.write(self.style.SUCCESS(f"Ingested {len(instances)} chunks"))
