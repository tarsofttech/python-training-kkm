"""
RAG Evaluator - Quality Assessment for RAG Systems

This module provides an RAGEvaluator class that:
- Evaluates RAG responses against expected answers
- Calculates faithfulness and relevancy scores
- Runs full evaluation suites
- Generates evaluation reports
"""

from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator
from typing import List, Dict
import json
import os
from datetime import datetime


class RAGEvaluator:
    """
    Evaluates RAG system quality using LlamaIndex evaluators.
    
    This class assesses RAG responses for:
    - Faithfulness: Does the answer align with the retrieved context?
    - Relevancy: Is the answer relevant to the question?
    """
    
    def __init__(self, rag_engine, llm):
        """
        Initialize the RAG evaluator.
        
        Args:
            rag_engine: RAGEngine instance to evaluate
            llm: LLM instance for evaluation
        """
        self.rag_engine = rag_engine
        self.llm = llm
        
        self.faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
        self.relevancy_evaluator = RelevancyEvaluator(llm=llm)
        
        print("📊 RAG Evaluator initialized")
    
    async def evaluate_single(
        self,
        question: str,
        expected_answer: str
    ) -> dict:
        """
        Evaluate a single question-answer pair.
        
        Args:
            question: The question to evaluate
            expected_answer: The expected/reference answer
        
        Returns:
            dict: Evaluation results with scores and pass/fail status
        """
        print(f"\n🔍 Evaluating: {question}")
        
        result = await self.rag_engine.query(
            question=question,
            top_k=3,
            return_augmented_prompt=False
        )
        
        actual_answer = result["answer"]
        
        print(f"   Expected: {expected_answer[:100]}...")
        print(f"   Actual: {actual_answer[:100]}...")
        
        faithfulness_result = await self.faithfulness_evaluator.aevaluate(
            query=question,
            response=actual_answer
        )
        
        relevancy_result = await self.relevancy_evaluator.aevaluate(
            query=question,
            response=actual_answer
        )
        
        faithfulness_score = 1.0 if faithfulness_result.passing else 0.0
        relevancy_score = float(relevancy_result.score) if hasattr(relevancy_result, 'score') else (1.0 if relevancy_result.passing else 0.0)
        
        passed = faithfulness_result.passing and relevancy_result.passing
        
        print(f"   Faithfulness: {faithfulness_score:.2f}")
        print(f"   Relevancy: {relevancy_score:.2f}")
        print(f"   Status: {'✅ PASS' if passed else '❌ FAIL'}")
        
        return {
            "question": question,
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "faithfulness_score": faithfulness_score,
            "relevancy_score": relevancy_score,
            "passed": passed,
            "sources": result["sources"]
        }
    
    async def run_full_eval(self, questions_path: str) -> dict:
        """
        Run evaluation on all questions in a JSON file.
        
        Args:
            questions_path: Path to JSON file with evaluation questions
        
        Returns:
            dict: Complete evaluation report with metrics
        """
        if not os.path.exists(questions_path):
            raise FileNotFoundError(f"Questions file not found: {questions_path}")
        
        with open(questions_path, 'r') as f:
            questions = json.load(f)
        
        print("=" * 80)
        print(f"🧪 RUNNING FULL EVALUATION")
        print("=" * 80)
        print(f"Total questions: {len(questions)}")
        print()
        
        results = []
        
        for q in questions:
            try:
                eval_result = await self.evaluate_single(
                    question=q["question"],
                    expected_answer=q["expected_answer"]
                )
                eval_result["id"] = q["id"]
                eval_result["source_doc"] = q["source_doc"]
                results.append(eval_result)
            except Exception as e:
                print(f"❌ Error evaluating question {q['id']}: {e}")
                results.append({
                    "id": q["id"],
                    "question": q["question"],
                    "error": str(e),
                    "passed": False
                })
        
        avg_faithfulness = sum(
            r.get("faithfulness_score", 0) for r in results
        ) / len(results) if results else 0.0
        
        avg_relevancy = sum(
            r.get("relevancy_score", 0) for r in results
        ) / len(results) if results else 0.0
        
        pass_count = sum(1 for r in results if r.get("passed", False))
        pass_rate = pass_count / len(results) if results else 0.0
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_questions": len(questions),
            "results": results,
            "metrics": {
                "avg_faithfulness": round(avg_faithfulness, 3),
                "avg_relevancy": round(avg_relevancy, 3),
                "pass_rate": round(pass_rate, 3),
                "passed": pass_count,
                "failed": len(results) - pass_count
            }
        }
        
        print("\n" + "=" * 80)
        print("📊 EVALUATION SUMMARY")
        print("=" * 80)
        print(f"Average Faithfulness: {avg_faithfulness:.3f}")
        print(f"Average Relevancy: {avg_relevancy:.3f}")
        print(f"Pass Rate: {pass_rate:.1%} ({pass_count}/{len(results)})")
        print("=" * 80)
        
        return report
    
    def save_report(self, report: dict, output_path: str) -> None:
        """
        Save evaluation report to a JSON file.
        
        Args:
            report: Evaluation report dictionary
            output_path: Path to save the report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {output_path}")
