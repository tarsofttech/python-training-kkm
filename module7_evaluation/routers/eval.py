"""
Evaluation Router - RAG Quality Assessment Endpoints

This router provides endpoints for running evaluations and retrieving reports.
"""

from fastapi import APIRouter, HTTPException, Request
from schemas import EvalRunResponse, EvalReportResponse
from evaluator import RAGEvaluator
import os
import json
from datetime import datetime

router = APIRouter(prefix="/api/v1/eval", tags=["evaluation"])


@router.post("/run", response_model=EvalRunResponse)
async def run_evaluation(request: Request):
    """
    Run a full evaluation suite on the RAG system.
    
    This endpoint:
    1. Loads evaluation questions from data/eval_questions.json
    2. Runs each question through the RAG system
    3. Evaluates faithfulness and relevancy
    4. Saves the report to disk
    5. Returns summary metrics
    
    Returns:
        EvalRunResponse: Evaluation summary and report path
    
    Raises:
        HTTPException 503: If RAG engine is not ready
        HTTPException 404: If eval questions file not found
        HTTPException 500: For unexpected errors
    """
    rag_engine = request.app.state.rag_engine
    
    if not rag_engine.is_ready():
        raise HTTPException(
            status_code=503,
            detail="RAG system not ready. Please ingest documents first."
        )
    
    questions_path = os.path.join("data", "eval_questions.json")
    
    if not os.path.exists(questions_path):
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation questions file not found: {questions_path}"
        )
    
    try:
        evaluator = RAGEvaluator(
            rag_engine=rag_engine,
            llm=rag_engine.llm
        )
        
        report = await evaluator.run_full_eval(questions_path)
        
        report_dir = os.getenv("EVAL_REPORT_PATH", "./data/eval_reports")
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_filename = f"eval_report_{timestamp}.json"
        report_path = os.path.join(report_dir, report_filename)
        
        evaluator.save_report(report, report_path)
        
        request.app.state.latest_report = report
        
        return EvalRunResponse(
            status="completed",
            total_questions=report["total_questions"],
            avg_faithfulness=report["metrics"]["avg_faithfulness"],
            avg_relevancy=report["metrics"]["avg_relevancy"],
            pass_rate=report["metrics"]["pass_rate"],
            report_path=report_path
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running evaluation: {str(e)}"
        )


@router.get("/report", response_model=EvalReportResponse)
async def get_latest_report(request: Request):
    """
    Get the latest evaluation report.
    
    Returns the most recently run evaluation report from memory.
    If no report exists in memory, attempts to load the latest from disk.
    
    Returns:
        EvalReportResponse: Latest evaluation report
    
    Raises:
        HTTPException 404: If no report is available
    """
    if hasattr(request.app.state, 'latest_report') and request.app.state.latest_report:
        report = request.app.state.latest_report
        return EvalReportResponse(**report)
    
    report_dir = os.getenv("EVAL_REPORT_PATH", "./data/eval_reports")
    
    if not os.path.exists(report_dir):
        raise HTTPException(
            status_code=404,
            detail="No evaluation reports found. Run an evaluation first."
        )
    
    report_files = [f for f in os.listdir(report_dir) if f.startswith("eval_report_") and f.endswith(".json")]
    
    if not report_files:
        raise HTTPException(
            status_code=404,
            detail="No evaluation reports found. Run an evaluation first."
        )
    
    latest_report_file = sorted(report_files)[-1]
    report_path = os.path.join(report_dir, latest_report_file)
    
    try:
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        return EvalReportResponse(**report)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading report: {str(e)}"
        )
