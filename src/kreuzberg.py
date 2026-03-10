import asyncio
from kreuzberg import extract_file, ExtractionConfig

async def main():
    config: ExtractionConfig = ExtractionConfig()
    result = await extract_file("./assets/samples/cv1.docx", config=config)


    with open("result.txt", "w") as f:
        f.write(str(result.content))

    content: str = result.content
    table_count: int = len(result.tables)
    metadata: dict = result.metadata

    print(f"Content length: {len(content)} characters")
    print(f"Tables: {table_count}")
    print(f"Metadata keys: {list(metadata.keys())}")

if __name__ == "__main__":
    asyncio.run(main())