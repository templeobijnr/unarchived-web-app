import traceback
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from knowledge_base.models import KnowledgeChunk
from projects.models import ProjectContextEngine, ProjectUpload
from agentcore.tools import file_parser_tool_base64, dpg_summary_tool


def trigger_ai_analysis(project_file):
    try:
        # 1. Parse the file to extract text
        file_obj = project_file.file
        content = file_obj.read()
        file_obj.seek(0)  # Reset pointer
        result = file_parser_tool_base64.func(
            content=content.decode('utf-8', errors='ignore'),
            filename=project_file.original_filename,
            content_type=project_file.file_type
        )
        text = result.get("extracted_text", "")

        if not text:
            return

        # 2. Split and embed chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)
        model = settings.OPENAI_MODEL
        api_key = settings.OPENAI_API_KEY
        embedder = OpenAIEmbeddings(model=model, openai_api_key=api_key)
        vectors = embedder.embed_documents(chunks)

        # 3. Store in KnowledgeBase and ProjectUpload
        uploads = []
        for content, vector in zip(chunks, vectors):
            KnowledgeChunk.objects.create(
                content=content,
                embedding=vector,
                domain="projects",
                entity_name=project_file.project.title,
                source_document=project_file.original_filename,
                source_type="project_file"
            )
            uploads.append(ProjectUpload(
                project=project_file.project,
                file=project_file,
                extracted_text=content,
                embedding=vector
            ))
        ProjectUpload.objects.bulk_create(uploads)

        # 4. Update project context engine
        summaries = [c[:500] for c in chunks[:3]]
        summary = dpg_summary_tool.func({"description": "\n".join(summaries)})
        ProjectContextEngine.objects.update_or_create(
            project=project_file.project,
            defaults={"ai_summary": summary}
        )
    except Exception as e:
        traceback.print_exc()
