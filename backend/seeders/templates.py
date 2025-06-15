from models.prompt_template import PromptTemplate
from database import SessionLocal
import uuid
from sqlalchemy.exc import IntegrityError

def seed_prompt_templates():
    db = SessionLocal()

    prompts = [
        {
            "name": "Summarization",
            "category": "summary",
            "prompt_text": "Summarize the following document:\n\n{document_content}",
            "variables": [{"name": "document_content", "required": True}],
            "description": "Generates a concise summary of the document."
        },
        {
            "name": "Key Points Extraction",
            "category": "analysis",
            "prompt_text": "List the key points in the following document:\n\n{document_content}",
            "variables": [{"name": "document_content", "required": True}],
            "description": "Extracts major bullet points or facts."
        },
        {
            "name": "Sentiment Analysis",
            "category": "analysis",
            "prompt_text": "Analyze the sentiment (positive, negative, or neutral) of the following document:\n\n{document_content}",
            "variables": [{"name": "document_content", "required": True}],
            "description": "Classifies the tone of the document."
        },
        {
            "name": "Entity Extraction",
            "category": "extraction",
            "prompt_text": "Extract all people, dates, and monetary amounts mentioned in the document:\n\n{document_content}",
            "variables": [{"name": "document_content", "required": True}],
            "description": "Identifies named entities in the document."
        },
        {
            "name": "Custom Question Answering",
            "category": "custom",
            "prompt_text": "Answer the following question based on the document:\n\nDocument: {document_content}\n\nQuestion: {question}",
            "variables": [
                {"name": "document_content", "required": True},
                {"name": "question", "required": True}
            ],
            "description": "Lets user ask custom questions about the document."
        }
    ]

    for prompt in prompts:
        try:
            db.add(PromptTemplate(
                id=uuid.uuid4(),
                name=prompt["name"],
                description=prompt["description"],
                prompt_text=prompt["prompt_text"],
                category=prompt["category"],
                variables=prompt["variables"]
            ))
        except IntegrityError:
            db.rollback()
            continue

    db.commit()
    db.close()
    print("✅ Prompt templates seeded.")
