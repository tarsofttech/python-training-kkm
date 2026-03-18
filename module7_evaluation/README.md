# Module 7: RAG Evaluation

Evaluate RAG system quality using LlamaIndex evaluators. This module measures faithfulness and relevancy of RAG responses, helping you understand and improve system performance.

---

## What You'll Learn

- Evaluating RAG responses with LlamaIndex evaluators
- Measuring faithfulness (answer aligns with context)
- Measuring relevancy (answer addresses the question)
- Creating test question sets
- Running automated evaluation suites
- Generating evaluation reports

---

## Prerequisites

1. **Ollama installed and running**
2. **Required models pulled** (llama3.1, nomic-embed-text)
3. **Completed Module 5** (Full RAG Pipeline)

---

## Setup

1. **Install dependencies**
   ```bash
   pip install -e .
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```

3. **Build the index** (ingest documents first)

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

---

## API Endpoints

### POST /api/v1/eval/run
Run full evaluation suite.

**Response:**
```json
{
  "status": "completed",
  "total_questions": 10,
  "avg_faithfulness": 0.85,
  "avg_relevancy": 0.92,
  "pass_rate": 0.80,
  "report_path": "./data/eval_reports/eval_report_20240312_103045.json"
}
```

### GET /api/v1/eval/report
Get latest evaluation report.

**Response:**
```json
{
  "timestamp": "2024-03-12T10:30:45",
  "total_questions": 10,
  "metrics": {
    "avg_faithfulness": 0.85,
    "avg_relevancy": 0.92,
    "pass_rate": 0.80,
    "passed": 8,
    "failed": 2
  },
  "results": [...]
}
```

---

## Evaluation Metrics

### Faithfulness
Measures whether the answer is grounded in the retrieved context.
- **1.0**: Answer fully supported by context
- **0.0**: Answer contradicts or unsupported by context

### Relevancy
Measures whether the answer addresses the question.
- **1.0**: Highly relevant answer
- **0.0**: Irrelevant answer

### Pass Rate
Percentage of questions that pass both faithfulness and relevancy checks.

---

## Running Evaluations

```bash
# Run evaluation
curl -X POST http://localhost:8000/api/v1/eval/run

# Get latest report
curl http://localhost:8000/api/v1/eval/report
```

---

## Next Steps

After completing this module, proceed to **Module 8: Docker Deployment** to containerize the complete application.

---

## Experimentation Ideas

- Add more evaluation questions
- Implement custom evaluators
- Track evaluation metrics over time
- A/B test different chunking strategies
- Compare different LLM models
