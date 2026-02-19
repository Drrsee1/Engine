import sqlite3
import os
from datetime import datetime
from logger_config import get_logger

logger = get_logger()
DB_NAME = "signals.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            symbol TEXT NOT NULL,
            signal_type TEXT NOT NULL,
            rsi_5m REAL,
            rsi_15m REAL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            percent_move REAL,
            status TEXT DEFAULT 'OPEN'
        )
    ''')
    
    conn.commit()
    logger.info("Database initialized")
    return conn

def log_signal(symbol, signal_type, rsi_values, entry_price):
    """Log signal to database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # rsi_values is a list like [rsi_5m, rsi_15m]
        rsi_5m = rsi_values[0] if len(rsi_values) > 0 else None
        rsi_15m = rsi_values[1] if len(rsi_values) > 1 else None
        
        cursor.execute('''
            INSERT INTO signals (symbol, signal_type, rsi_5m, rsi_15m, entry_price, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (symbol, signal_type, rsi_5m, rsi_15m, entry_price, 'OPEN'))
        
        conn.commit()
        conn.close()
        logger.info(f"Signal logged: {symbol} {signal_type} RSI({rsi_5m:.2f}, {rsi_15m:.2f}) @ {entry_price:.4f}")
        
    except Exception as e:
        logger.error(f"Error logging signal: {e}")

def update_signal(symbol, exit_price):
    """Update signal with exit price and percent move"""
    try:
        if exit_price is None:
            logger.warning(f"Cannot update {symbol} - exit price is None")
            return
            
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Find the last open signal for this symbol
        cursor.execute('''
            SELECT id, entry_price FROM signals 
            WHERE symbol = ? AND status = 'OPEN'
            ORDER BY timestamp DESC LIMIT 1
        ''', (symbol,))
        
        result = cursor.fetchone()
        
        if result:
            signal_id, entry_price = result
            percent_move = ((exit_price - entry_price) / entry_price) * 100
            
            cursor.execute('''
                UPDATE signals 
                SET exit_price = ?, percent_move = ?, status = 'CLOSED'
                WHERE id = ?
            ''', (exit_price, percent_move, signal_id))
            
            conn.commit()
            logger.info(f"Signal updated: {symbol} exit @ {exit_price:.4f} ({percent_move:.2f}%)")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Error updating signal: {e}")

def get_performance_stats():
    """Get bot performance statistics"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_signals,
                SUM(CASE WHEN percent_move > 0 THEN 1 ELSE 0 END) as winning_signals,
                AVG(percent_move) as avg_percent_move,
                MAX(percent_move) as best_trade,
                MIN(percent_move) as worst_trade
            FROM signals WHERE status = 'CLOSED'
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_signals': result[0] or 0,
            'winning_signals': result[1] or 0,
            'avg_return': result[2] or 0,
            'best_trade': result[3] or 0,
            'worst_trade': result[4] or 0
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {}

# Initialize database on startup
if not os.path.exists(DB_NAME):
    init_db()
