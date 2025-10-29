from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import sys
from io import StringIO
import traceback
import uuid
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'python-learning-platform-secret-key-2024'
CORS(app, supports_credentials=True)

# Global sessions storage
execution_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute Python code with input support"""
    try:
        data = request.json
        code = data.get('code', '')
        inputs = data.get('inputs', [])
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # Create output capture
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_stdin = sys.stdin
        
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        # Create custom input function
        input_index = [0]  # Use list to allow modification in nested function
        
        def custom_input(prompt=''):
            if input_index[0] < len(inputs):
                value = inputs[input_index[0]]
                input_index[0] += 1
                sys.stdout.write(f"{prompt}{value}\n")
                return value
            else:
                raise EOFError("No more inputs provided")
        
        # Execute code
        execution_globals = {
            '__builtins__': __builtins__,
            'input': custom_input
        }
        
        try:
            exec(code, execution_globals)
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            
            return jsonify({
                'success': True,
                'output': output,
                'error': error if error else None,
                'session_id': session_id
            })
            
        except Exception as e:
            error_output = traceback.format_exc()
            return jsonify({
                'success': False,
                'output': sys.stdout.getvalue(),
                'error': error_output,
                'session_id': session_id
            })
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.stdin = old_stdin
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check_solution', methods=['POST'])
def check_solution():
    """Check if user's solution passes test cases"""
    try:
        data = request.json
        code = data.get('code', '')
        test_cases = data.get('test_cases', [])
        
        results = []
        
        for test in test_cases:
            try:
                # Prepare execution environment
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                # Create custom input
                inputs = test.get('inputs', [])
                input_index = [0]
                
                def custom_input(prompt=''):
                    if input_index[0] < len(inputs):
                        value = inputs[input_index[0]]
                        input_index[0] += 1
                        return value
                    return ''
                
                exec_globals = {
                    '__builtins__': __builtins__,
                    'input': custom_input
                }
                
                # Execute code
                exec(code, exec_globals)
                output = sys.stdout.getvalue().strip()
                expected = test.get('expected', '').strip()
                
                passed = output == expected
                
                results.append({
                    'passed': passed,
                    'input': test.get('inputs', []),
                    'expected': expected,
                    'got': output,
                    'description': test.get('description', '')
                })
                
                sys.stdout = old_stdout
                
            except Exception as e:
                sys.stdout = old_stdout
                results.append({
                    'passed': False,
                    'error': str(e),
                    'description': test.get('description', '')
                })
        
        all_passed = all(r.get('passed', False) for r in results)
        
        return jsonify({
            'success': True,
            'all_passed': all_passed,
            'results': results,
            'score': sum(1 for r in results if r.get('passed', False)),
            'total': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """Save user progress"""
    try:
        data = request.json
        # In production, save to database
        # For now, just return success
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
