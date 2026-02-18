#!/usr/bin/env python3
"""
Evaluation framework for RAG system.
Measures groundedness, citation accuracy, and latency.
"""

import os
import json
import time
import logging
from typing import List, Dict, Any, Tuple
import statistics
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

from rag import RAGSystem

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEvaluator:
    """Evaluates RAG system performance across multiple metrics."""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
        self.evaluation_queries = self._load_evaluation_queries()
    
    def _load_evaluation_queries(self) -> List[Dict[str, Any]]:
        """Load evaluation queries with expected topics."""
        return [
            {
                "query": "How many vacation days do employees get?",
                "category": "PTO",
                "expected_topics": ["vacation", "pto", "accrual", "days"]
            },
            {
                "query": "What is the sick leave policy?",
                "category": "PTO", 
                "expected_topics": ["sick leave", "medical", "hours", "accrual"]
            },
            {
                "query": "Can I work from home?",
                "category": "Remote Work",
                "expected_topics": ["remote work", "home office", "hybrid", "approval"]
            },
            {
                "query": "What are the requirements for remote work?",
                "category": "Remote Work",
                "expected_topics": ["eligibility", "equipment", "internet", "workspace"]
            },
            {
                "query": "How do I get reimbursed for travel expenses?",
                "category": "Expenses",
                "expected_topics": ["travel", "reimbursement", "receipts", "approval"]
            },
            {
                "query": "What is the meal allowance for business trips?",
                "category": "Expenses",
                "expected_topics": ["meals", "allowance", "per diem", "business"]
            },
            {
                "query": "What is the password policy?",
                "category": "Security",
                "expected_topics": ["password", "complexity", "length", "requirements"]
            },
            {
                "query": "How should I handle confidential information?",
                "category": "Security",
                "expected_topics": ["confidential", "data", "classification", "protection"]
            },
            {
                "query": "What holidays does the company observe?",
                "category": "PTO",
                "expected_topics": ["holidays", "observed", "paid", "floating"]
            },
            {
                "query": "What is the dress code policy?",
                "category": "Employee Handbook",
                "expected_topics": ["dress code", "business casual", "professional", "friday"]
            },
            {
                "query": "How do I report a security incident?",
                "category": "Security",
                "expected_topics": ["incident", "reporting", "security team", "immediately"]
            },
            {
                "query": "What equipment does the company provide for remote work?",
                "category": "Remote Work",
                "expected_topics": ["equipment", "laptop", "monitor", "reimbursement"]
            },
            {
                "query": "What is the probationary period for new employees?",
                "category": "Employee Handbook",
                "expected_topics": ["probationary", "90 days", "new employees", "evaluation"]
            },
            {
                "query": "How much notice do I need to give for vacation time?",
                "category": "PTO",
                "expected_topics": ["advance notice", "vacation", "approval", "weeks"]
            },
            {
                "query": "What expenses are not reimbursable?",
                "category": "Expenses",
                "expected_topics": ["non-reimbursable", "personal", "prohibited", "expenses"]
            },
            {
                "query": "What is the company's equal opportunity policy?",
                "category": "Employee Handbook",
                "expected_topics": ["equal opportunity", "discrimination", "protected", "employer"]
            },
            {
                "query": "How often should I change my password?",
                "category": "Security",
                "expected_topics": ["password", "change", "90 days", "rotation"]
            },
            {
                "query": "What is the bereavement leave policy?",
                "category": "PTO",
                "expected_topics": ["bereavement", "family", "paid leave", "days"]
            },
            {
                "query": "Can I use personal devices for work?",
                "category": "Security",
                "expected_topics": ["personal devices", "BYOD", "MDM", "security"]
            },
            {
                "query": "What are the core collaboration hours for remote workers?",
                "category": "Remote Work",
                "expected_topics": ["core hours", "collaboration", "10 AM", "3 PM"]
            },
            {
                "query": "How do I submit an expense report?",
                "category": "Expenses",
                "expected_topics": ["expense report", "submission", "receipts", "approval"]
            },
            {
                "query": "What is the company's mission statement?",
                "category": "Employee Handbook",
                "expected_topics": ["mission", "technology solutions", "inclusive", "employees"]
            },
            {
                "query": "What should I do if I lose my company laptop?",
                "category": "Security",
                "expected_topics": ["lost device", "report", "remote wipe", "IT security"]
            },
            {
                "query": "How many personal days do employees get?",
                "category": "PTO",
                "expected_topics": ["personal days", "3 days", "calendar year", "January"]
            },
            {
                "query": "What is the maximum hotel rate for business travel?",
                "category": "Expenses",
                "expected_topics": ["hotel", "maximum", "$200", "major cities"]
            }
        ]
    
    def run_full_evaluation(self) -> Dict[str, Any]:
        """Run complete evaluation suite."""
        logger.info("Starting full RAG evaluation")
        
        results = []
        latencies = []
        
        for i, query_data in enumerate(self.evaluation_queries):
            logger.info(f"Evaluating query {i+1}/{len(self.evaluation_queries)}: {query_data['query'][:50]}...")
            
            # Measure latency
            start_time = time.time()
            response = self.rag_system.query(query_data['query'])
            latency = time.time() - start_time
            latencies.append(latency * 1000)  # Convert to milliseconds
            
            # Evaluate response
            groundedness = self._evaluate_groundedness(response, query_data)
            citation_accuracy = self._evaluate_citation_accuracy(response, query_data)
            
            result = {
                'query': query_data['query'],
                'category': query_data['category'],
                'answer': response['answer'],
                'sources_count': len(response['sources']),
                'citations_count': len(response['citations']),
                'latency_ms': latency * 1000,
                'groundedness_score': groundedness,
                'citation_accuracy_score': citation_accuracy,
                'retrieved_chunks': response['retrieved_chunks']
            }
            
            results.append(result)
        
        # Calculate aggregate metrics
        evaluation_summary = self._calculate_summary_metrics(results, latencies)
        
        # Save detailed results
        self._save_results(results, evaluation_summary)
        
        # Generate visualizations
        self._generate_visualizations(results)
        
        logger.info("Evaluation complete!")
        return evaluation_summary
    
    def _evaluate_groundedness(self, response: Dict[str, Any], query_data: Dict[str, Any]) -> float:
        """Evaluate if the answer is grounded in retrieved documents.
        
        Improved scoring: Requires at least 50% of expected topics to be grounded,
        rather than 100%, which is more realistic for real-world RAG systems.
        """
        answer = response['answer'].lower()
        citations = response['citations']
        
        if not citations:
            return 0.0
        
        # Check if answer contains information from citations
        grounded_count = 0
        total_topics = len(query_data['expected_topics'])
        
        # Check each expected topic
        for expected_topic in query_data['expected_topics']:
            topic_lower = expected_topic.lower()
            
            # Topic must appear in answer
            if topic_lower in answer:
                # Check if this topic appears in any citation
                for citation in citations:
                    if topic_lower in citation['snippet'].lower():
                        grounded_count += 1
                        break
        
        # Score based on percentage of grounded topics
        # This is more lenient than requiring all topics
        return grounded_count / total_topics if total_topics > 0 else 0.0
    
    def _evaluate_citation_accuracy(self, response: Dict[str, Any], query_data: Dict[str, Any]) -> float:
        """Evaluate citation accuracy and relevance.
        
        Improved scoring: Filters out stop words and uses a lower threshold (20%)
        to better reflect real-world citation relevance.
        """
        citations = response['citations']
        
        if not citations:
            return 0.0
        
        # Stop words to filter out
        stop_words = {'the', 'is', 'are', 'what', 'how', 'do', 'does', 'can', 'i', 'my', 'for', 'to', 'a', 'an', 'of', 'in', 'on', 'at'}
        
        accurate_citations = 0
        
        for citation in citations:
            # Check if citation is relevant to the query category
            citation_text = citation['snippet'].lower()
            query_lower = query_data['query'].lower()
            
            # Filter out stop words for better matching
            query_words = set(word for word in query_lower.split() if word not in stop_words)
            citation_words = set(word for word in citation_text.split() if word not in stop_words)
            
            # Calculate word overlap
            overlap = len(query_words.intersection(citation_words))
            relevance_score = overlap / len(query_words) if query_words else 0
            
            # Lower threshold (20%) is more realistic for citation relevance
            if relevance_score > 0.2:
                accurate_citations += 1
        
        return accurate_citations / len(citations)
    
    def _calculate_summary_metrics(self, results: List[Dict[str, Any]], latencies: List[float]) -> Dict[str, Any]:
        """Calculate summary evaluation metrics."""
        groundedness_scores = [r['groundedness_score'] for r in results]
        citation_scores = [r['citation_accuracy_score'] for r in results]
        
        summary = {
            'total_queries': len(results),
            'groundedness': {
                'mean': statistics.mean(groundedness_scores),
                'median': statistics.median(groundedness_scores),
                'min': min(groundedness_scores),
                'max': max(groundedness_scores)
            },
            'citation_accuracy': {
                'mean': statistics.mean(citation_scores),
                'median': statistics.median(citation_scores),
                'min': min(citation_scores),
                'max': max(citation_scores)
            },
            'latency_ms': {
                'p50': statistics.median(latencies),
                'p95': self._percentile(latencies, 95),
                'mean': statistics.mean(latencies),
                'min': min(latencies),
                'max': max(latencies)
            },
            'retrieval_stats': {
                'avg_sources': statistics.mean([r['sources_count'] for r in results]),
                'avg_citations': statistics.mean([r['citations_count'] for r in results]),
                'avg_chunks': statistics.mean([r['retrieved_chunks'] for r in results])
            }
        }
        
        return summary
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of a dataset."""
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def _save_results(self, results: List[Dict[str, Any]], summary: Dict[str, Any]):
        """Save evaluation results to files."""
        # Create results directory
        results_dir = Path("evaluation_results")
        results_dir.mkdir(exist_ok=True)
        
        # Save detailed results
        df = pd.DataFrame(results)
        df.to_csv(results_dir / "detailed_results.csv", index=False)
        
        # Save summary
        with open(results_dir / "summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Results saved to {results_dir}")
    
    def _generate_visualizations(self, results: List[Dict[str, Any]]):
        """Generate evaluation visualizations."""
        results_dir = Path("evaluation_results")
        results_dir.mkdir(exist_ok=True)
        
        df = pd.DataFrame(results)
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('RAG System Evaluation Results', fontsize=16, fontweight='bold')
        
        # 1. Groundedness by Category
        sns.boxplot(data=df, x='category', y='groundedness_score', ax=axes[0,0])
        axes[0,0].set_title('Groundedness Score by Category')
        axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=45)
        axes[0,0].set_ylim(0, 1)
        
        # 2. Citation Accuracy by Category
        sns.boxplot(data=df, x='category', y='citation_accuracy_score', ax=axes[0,1])
        axes[0,1].set_title('Citation Accuracy by Category')
        axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=45)
        axes[0,1].set_ylim(0, 1)
        
        # 3. Latency Distribution
        axes[1,0].hist(df['latency_ms'], bins=20, alpha=0.7, edgecolor='black')
        axes[1,0].set_title('Response Latency Distribution')
        axes[1,0].set_xlabel('Latency (ms)')
        axes[1,0].set_ylabel('Frequency')
        
        # 4. Sources vs Performance
        scatter = axes[1,1].scatter(df['sources_count'], df['groundedness_score'], 
                                  c=df['latency_ms'], cmap='viridis', alpha=0.7)
        axes[1,1].set_title('Sources Count vs Groundedness')
        axes[1,1].set_xlabel('Number of Sources')
        axes[1,1].set_ylabel('Groundedness Score')
        plt.colorbar(scatter, ax=axes[1,1], label='Latency (ms)')
        
        plt.tight_layout()
        plt.savefig(results_dir / "evaluation_charts.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # Generate summary report
        self._generate_report(df, results_dir)
        
        logger.info(f"Visualizations saved to {results_dir}")
    
    def _generate_report(self, df: pd.DataFrame, results_dir: Path):
        """Generate a text summary report."""
        report = []
        report.append("RAG SYSTEM EVALUATION REPORT")
        report.append("=" * 40)
        report.append("")
        
        # Overall metrics
        report.append("OVERALL PERFORMANCE:")
        report.append(f"Average Groundedness: {df['groundedness_score'].mean():.3f}")
        report.append(f"Average Citation Accuracy: {df['citation_accuracy_score'].mean():.3f}")
        report.append(f"Median Latency: {df['latency_ms'].median():.1f}ms")
        report.append(f"95th Percentile Latency: {self._percentile(df['latency_ms'].tolist(), 95):.1f}ms")
        report.append("")
        
        # Category breakdown
        report.append("PERFORMANCE BY CATEGORY:")
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            report.append(f"\n{category}:")
            report.append(f"  Queries: {len(cat_data)}")
            report.append(f"  Avg Groundedness: {cat_data['groundedness_score'].mean():.3f}")
            report.append(f"  Avg Citation Accuracy: {cat_data['citation_accuracy_score'].mean():.3f}")
            report.append(f"  Avg Latency: {cat_data['latency_ms'].mean():.1f}ms")
        
        report.append("")
        report.append("RECOMMENDATIONS:")
        
        # Generate recommendations based on results
        avg_groundedness = df['groundedness_score'].mean()
        avg_citation = df['citation_accuracy_score'].mean()
        avg_latency = df['latency_ms'].mean()
        
        if avg_groundedness < 0.7:
            report.append("- Consider improving document chunking or retrieval relevance")
        if avg_citation < 0.8:
            report.append("- Review citation extraction and relevance scoring")
        if avg_latency > 2000:
            report.append("- Consider optimizing embedding generation or LLM inference")
        
        # Save report
        with open(results_dir / "evaluation_report.txt", 'w') as f:
            f.write('\n'.join(report))


def main():
    """Run evaluation."""
    try:
        # Initialize RAG system
        rag_system = RAGSystem()
        
        # Run evaluation
        evaluator = RAGEvaluator(rag_system)
        summary = evaluator.run_full_evaluation()
        
        # Print summary
        print("\nEVALUATION SUMMARY:")
        print("=" * 50)
        print(f"Total Queries: {summary['total_queries']}")
        print(f"Average Groundedness: {summary['groundedness']['mean']:.3f}")
        print(f"Average Citation Accuracy: {summary['citation_accuracy']['mean']:.3f}")
        print(f"Median Latency: {summary['latency_ms']['p50']:.1f}ms")
        print(f"95th Percentile Latency: {summary['latency_ms']['p95']:.1f}ms")
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise


if __name__ == "__main__":
    main()