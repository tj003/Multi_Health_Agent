import asyncio
import logging
import json
from pathlib import Path
from src.pipelines.orchestrator import run_pipeline

logger = logging.getLogger(__name__)

async def main():
    logger.info(" Starting GOQii multi-agent pipeline...")

    # Run pipeline
    results = await run_pipeline()

    clean_results = []
    for r in results:
        if isinstance(r, dict):
            clean_results.append(r)
        else:
            try:
                parsed = json.loads(str(r))
                if isinstance(parsed, dict):
                    clean_results.append(parsed)
                elif isinstance(parsed, list):
                    clean_results.extend(parsed)
            except Exception:
                clean_results.append({"raw_output": str(r)})

    # Save as clean JSON
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    fp = output_dir / "health_news.json"
    fp.write_text(json.dumps(clean_results, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info(f"✅ Saved results to {fp}")

if __name__ == "__main__":
    asyncio.run(main())
