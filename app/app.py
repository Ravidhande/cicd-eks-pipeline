from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🚀 CI/CD Pipeline Live!</h1>
    <p>Deployed via Jenkins → Docker → AWS EKS</p>
    <p>Built by Ravi Dhande | Cloud Engineer</p>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '1.0'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)