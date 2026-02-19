from flask import Flask, jsonify
from logger_config import get_logger
import threading
import time

logger = get_logger()
app = Flask(__name__)

# Track bot status
bot_status = {
    'running': True,
    'last_scan': None,
    'signals_sent': 0,
    'start_time': time.time()
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'RSI Extreme Engine is running',
            'running': bot_status['running'],
            'uptime_seconds': int(time.time() - bot_status['start_time'])
        }), 200
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get bot performance stats"""
    try:
        from signal_logger import get_performance_stats
        stats = get_performance_stats()
        return jsonify({
            'status': 'success',
            'data': stats,
            'uptime_seconds': int(time.time() - bot_status['start_time'])
        }), 200
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def run_server(port=5000):
    """Run Flask server in background"""
    try:
        logger.info(f"Running health check server on port {port}")
        # Suppress Flask logging
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Error running server: {e}")

def start_health_check_server(port=5000):
    """Start health check server in background thread"""
    try:
        server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
        server_thread.start()
        logger.info(f"Health check server started on port {port}")
    except Exception as e:
        logger.error(f"Error starting health check server: {e}")
