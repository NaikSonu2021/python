from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
from io import StringIO
import traceback
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'python-learning-platform-secret-key-2024')

# CORS configuration - allow all origins for development
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "OPTIONS"])

# Global sessions storage
execution_sessions = {}

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'message': 'Python Mastery Platform is running!'})

@app.route('/api/execute', methods=['POST', 'OPTIONS'])
def execute_code():
    """Execute Python code with input support and better error handling"""
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        code = data.get('code', '').strip()
        inputs = data.get('inputs', [])
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400
        
        # Security: Basic code validation
        dangerous_imports = ['os', 'subprocess', 'sys', 'eval', 'exec', '__import__']
        for danger in dangerous_imports:
            if danger in code.lower() and 'import' in code.lower():
                return jsonify({
                    'success': False,
                    'error': f'Security: {danger} operations are not allowed for safety reasons'
                }), 403
        
        # Create output capture
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_stdin = sys.stdin
        
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        # Create custom input function with better handling
        input_index = [0]
        
        def custom_input(prompt=''):
            """Custom input function that uses provided inputs"""
            if input_index[0] < len(inputs):
                value = str(inputs[input_index[0]])
                input_index[0] += 1
                # Display the prompt and input in output
                if prompt:
                    sys.stdout.write(f"{prompt}")
                sys.stdout.write(f"{value}\n")
                return value
            else:
                raise EOFError("No more inputs provided. Please provide all required inputs.")
        
        # Create safe execution environment
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'type': type,
            'isinstance': isinstance,
            'round': round,
            'pow': pow,
            'ord': ord,
            'chr': chr,
            'input': custom_input
        }
        
        execution_globals = {
            '__builtins__': safe_builtins,
            '__name__': '__main__'
        }
        
        try:
            # Execute the code
            exec(code, execution_globals)
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            
            # Clean up output
            if not output and not error:
                output = "Code executed successfully (no output)"
            
            return jsonify({
                'success': True,
                'output': output,
                'error': error if error else None,
                'session_id': session_id,
                'inputs_used': input_index[0]
            })
            
        except EOFError as e:
            return jsonify({
                'success': False,
                'output': sys.stdout.getvalue(),
                'error': f'Input Error: {str(e)}\n\nTip: Make sure you provide enough inputs for all input() calls in your code.',
                'session_id': session_id
            })
            
        except SyntaxError as e:
            error_msg = f"Syntax Error on line {e.lineno}: {e.msg}\n"
            error_msg += f"Check your code around: {e.text if e.text else 'that line'}"
            return jsonify({
                'success': False,
                'output': sys.stdout.getvalue(),
                'error': error_msg,
                'session_id': session_id
            })
            
        except ZeroDivisionError:
            return jsonify({
                'success': False,
                'output': sys.stdout.getvalue(),
                'error': 'Math Error: Division by zero\n\nTip: Check your calculations - you cannot divide by zero!',
                'session_id': session_id
            })
            
        except Exception as e:
            error_output = traceback.format_exc()
            # Make error more user-friendly
            error_lines = error_output.split('\n')
            friendly_error = f"Error: {type(e).__name__}\n"
            friendly_error += f"Message: {str(e)}\n\n"
            friendly_error += "Full traceback:\n" + error_output
            
            return jsonify({
                'success': False,
                'output': sys.stdout.getvalue(),
                'error': friendly_error,
                'session_id': session_id
            })
        
        finally:
            # Always restore original streams
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.stdin = old_stdin
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server Error: {str(e)}'
        }), 500

@app.route('/api/check_solution', methods=['POST', 'OPTIONS'])
def check_solution():
    """Check if user's solution passes test cases"""
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    
    try:
        data = request.json
        code = data.get('code', '').strip()
        test_cases = data.get('test_cases', [])
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400
        
        results = []
        
        for idx, test in enumerate(test_cases):
            try:
                # Prepare execution environment
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = StringIO()
                sys.stderr = StringIO()
                
                # Create custom input
                inputs = test.get('inputs', [])
                input_index = [0]
                
                def custom_input(prompt=''):
                    if input_index[0] < len(inputs):
                        value = str(inputs[input_index[0]])
                        input_index[0] += 1
                        return value
                    return ''
                
                # Safe execution environment
                safe_builtins = {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'input': custom_input
                }
                
                exec_globals = {
                    '__builtins__': safe_builtins,
                    '__name__': '__main__'
                }
                
                # Execute code
                exec(code, exec_globals)
                output = sys.stdout.getvalue().strip()
                expected = str(test.get('expected', '')).strip()
                
                # Compare output
                passed = output == expected
                
                results.append({
                    'passed': passed,
                    'test_number': idx + 1,
                    'input': inputs,
                    'expected': expected,
                    'got': output,
                    'description': test.get('description', f'Test case {idx + 1}')
                })
                
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
            except Exception as e:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                results.append({
                    'passed': False,
                    'test_number': idx + 1,
                    'error': str(e),
                    'description': test.get('description', f'Test case {idx + 1}')
                })
        
        all_passed = all(r.get('passed', False) for r in results)
        passed_count = sum(1 for r in results if r.get('passed', False))
        
        return jsonify({
            'success': True,
            'all_passed': all_passed,
            'results': results,
            'score': passed_count,
            'total': len(results),
            'percentage': (passed_count / len(results) * 100) if results else 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test execution error: {str(e)}'
        }), 500

@app.route('/api/save_progress', methods=['POST', 'OPTIONS'])
def save_progress():
    """Save user progress (placeholder for future database integration)"""
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    
    try:
        data = request.json
        # Future: Save to database
        # For now, just return success
        return jsonify({
            'success': True,
            'message': 'Progress saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test endpoint to verify API is working"""
    return jsonify({
        'success': True,
        'message': 'API is working!',
        'endpoints': {
            'execute': '/api/execute',
            'check_solution': '/api/check_solution',
            'save_progress': '/api/save_progress'
        }
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
