"""
最小限のテスト用アプリケーション
起動問題を診断するための簡単なバージョン
"""
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'test-key')

@app.route('/')
def hello():
    return '''
    <h1>🎉 Python Study App - Test Version</h1>
    <p>✅ Flask application is running successfully!</p>
    <p>🚀 Environment: {}</p>
    <p>🗄️ Database URL: {}</p>
    '''.format(
        os.environ.get('FLASK_ENV', 'development'),
        '✅ Configured' if os.environ.get('DATABASE_URL') else '❌ Not configured'
    )

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Application is running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))