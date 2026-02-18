#!/usr/bin/env python3
"""
Flask web application for RAG Company Policies system.
Provides web UI and API endpoints for policy Q&A.
"""

import os
import time
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from src.rag import RAGSystem, QueryValidator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize RAG system
try:
    rag_system = RAGSystem()
    logger.info("RAG system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {e}")
    rag_system = None


@app.route('/')
def index():
    """Main chat interface."""
    return render_template('index.html')


@app.route('/policy/<path:filename>')
def serve_policy(filename):
    """Serve policy documents."""
    from flask import send_from_directory
    import os
    
    # Security: only allow files from policies directory
    policies_dir = os.path.join(os.getcwd(), 'policies')
    
    try:
        return send_from_directory(policies_dir, filename)
    except Exception as e:
        logger.error(f"Error serving policy file: {e}")
        return jsonify({'error': 'File not found'}), 404


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests and return AI responses."""
    try:
        # Check if RAG system is available
        if not rag_system:
            return jsonify({
                'error': 'RAG system not available. Please check configuration.',
                'answer': 'System temporarily unavailable.',
                'citations': [],
                'sources': []
            }), 500
        
        # Get question from request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'error': 'No question provided',
                'answer': 'Please provide a question.',
                'citations': [],
                'sources': []
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                'error': 'Empty question',
                'answer': 'Please ask a question about company policies.',
                'citations': [],
                'sources': []
            }), 400
        
        # Validate and preprocess question
        question = QueryValidator.preprocess_question(question)
        
        # Record start time for latency measurement
        start_time = time.time()
        
        # Process question with RAG system
        result = rag_system.query(question)
        
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)
        result['latency_ms'] = latency_ms
        
        logger.info(f"Processed query in {latency_ms}ms: {question[:50]}...")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({
            'error': 'Internal server error',
            'answer': 'I encountered an error processing your question. Please try again.',
            'citations': [],
            'sources': []
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        if not rag_system:
            return jsonify({
                'status': 'unhealthy',
                'error': 'RAG system not initialized'
            }), 503
        
        health_status = rag_system.health_check()
        
        if health_status['status'] == 'healthy':
            return jsonify(health_status)
        else:
            return jsonify(health_status), 503
            
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


@app.route('/api/stats')
def stats():
    """Get system statistics."""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not available'}), 503
        
        collection_count = rag_system.collection.count()
        
        return jsonify({
            'total_documents': collection_count,
            'collection_name': 'company_policies',
            'embedding_model': 'all-MiniLM-L6-v2',
            'llm_model': rag_system.llm_model
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if running in development mode
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    if rag_system:
        logger.info("RAG system ready for queries")
    else:
        logger.warning("RAG system not available - check configuration")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )