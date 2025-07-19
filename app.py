from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# データベース設定 - Render用に調整
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    # Render PostgreSQLのURL修正
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///python_study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# セキュリティ設定
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24時間

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # プロフィール情報
    learning_goal = db.Column(db.String(200), nullable=True)  # 学習目標
    target_app = db.Column(db.String(100), nullable=True)  # 作りたいアプリケーション
    experience_level = db.Column(db.String(50), nullable=True, default='beginner')  # 経験レベル
    study_time_per_week = db.Column(db.Integer, nullable=True)  # 週の学習時間
    
    results = db.relationship('ExamResult', backref='user', lazy=True)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    exam_type = db.Column(db.String(50), nullable=False)  # basic, practical, data_analysis, practical_data_analysis
    questions = db.relationship('Question', backref='exam', lazy=True)
    results = db.relationship('ExamResult', backref='exam', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False, default='multiple_choice')  # multiple_choice or coding

    # For multiple choice
    option_a = db.Column(db.String(200), nullable=True)
    option_b = db.Column(db.String(200), nullable=True)
    option_c = db.Column(db.String(200), nullable=True)
    option_d = db.Column(db.String(200), nullable=True)
    correct_answer = db.Column(db.String(1), nullable=True)  # A, B, C, or D
    
    # For coding questions
    solution_template = db.Column(db.Text, nullable=True)
    test_code = db.Column(db.Text, nullable=True)

    explanation = db.Column(db.Text, nullable=True)

class ExamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # バリデーション
        if not username or len(username) < 3:
            flash('ユーザー名は3文字以上で入力してください', 'error')
            return redirect(url_for('register'))
        
        if not email or '@' not in email:
            flash('有効なメールアドレスを入力してください', 'error')
            return redirect(url_for('register'))
        
        if not password or len(password) < 6:
            flash('パスワードは6文字以上で入力してください', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('そのユーザー名は既に使用されています', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('そのメールアドレスは既に使用されています', 'error')
            return redirect(url_for('register'))
        
        try:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                experience_level='beginner'  # デフォルト値を明示的に設定
            )
            db.session.add(user)
            db.session.commit()
            
            flash('アカウントが作成されました！ログインしてください', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {e}")  # ログ出力
            flash('アカウント作成中にエラーが発生しました。しばらく時間をおいて再度お試しください。', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('ユーザー名とパスワードを入力してください', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'ようこそ、{user.username}さん！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('ユーザー名またはパスワードが正しくありません', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # データベースクエリを最適化
    exams = Exam.query.order_by(Exam.difficulty, Exam.exam_type).all()
    recent_results = ExamResult.query.filter_by(user_id=current_user.id).order_by(ExamResult.completed_at.desc()).limit(5).all()
    
    # パーソナライズされた推奨試験
    recommended_exams = get_recommended_exams(current_user)
    
    return render_template('dashboard.html', exams=exams, recent_results=recent_results, recommended_exams=recommended_exams)

@app.route('/exam/<int:exam_id>')
@login_required
def take_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    return render_template('exam.html', exam=exam, questions=questions)

@app.route('/submit_exam', methods=['POST'])
@login_required
def submit_exam():
    exam_id = request.form['exam_id']
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    
    score = 0
    total_questions = len(questions)
    
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        
        if question.question_type == 'multiple_choice':
            if user_answer == question.correct_answer:
                score += 1
        elif question.question_type == 'coding':
            # This is a simplified check. For a real application, 
            # you would run the user's code in a sandboxed environment 
            # against the test_code.
            # For now, we'll just check if the answer is not empty.
            if user_answer and user_answer.strip() != '':
                # A more robust check would involve executing the code.
                # This is a placeholder for that logic.
                # For example, you could try to run the code with test cases.
                # We will assume correctness if code is submitted.
                score += 1

    result = ExamResult(
        user_id=current_user.id,
        exam_id=exam_id,
        score=score,
        total_questions=total_questions
    )
    db.session.add(result)
    db.session.commit()
    
    return redirect(url_for('exam_result', result_id=result.id))

@app.route('/result/<int:result_id>')
@login_required
def exam_result(result_id):
    result = ExamResult.query.get_or_404(result_id)
    if result.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('dashboard'))
    return render_template('result.html', result=result)

@app.route('/progress')
@login_required
def progress():
    results = ExamResult.query.filter_by(user_id=current_user.id).order_by(ExamResult.completed_at.desc()).all()
    return render_template('progress.html', results=results)

@app.route('/profile')
@login_required
def profile():
    results = ExamResult.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', results=results)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.learning_goal = request.form.get('learning_goal')
        current_user.target_app = request.form.get('target_app')
        current_user.experience_level = request.form.get('experience_level')
        current_user.study_time_per_week = int(request.form.get('study_time_per_week', 0))
        
        db.session.commit()
        flash('プロフィールを更新しました！', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

def get_recommended_exams(user):
    """ユーザーの学習目標と経験レベルに基づいて推奨試験を取得"""
    recommendations = []
    
    # 経験レベルに基づく推奨
    if user.experience_level == 'beginner':
        recommendations.append({
            'reason': '初心者向け：基礎から始めましょう',
            'exams': Exam.query.filter_by(difficulty='beginner').all()
        })
    elif user.experience_level == 'intermediate':
        recommendations.append({
            'reason': '中級者向け：応用力を身につけましょう',
            'exams': Exam.query.filter_by(difficulty='intermediate').all()
        })
    elif user.experience_level == 'advanced':
        recommendations.append({
            'reason': '上級者向け：高度なスキルを磨きましょう',
            'exams': Exam.query.filter_by(difficulty='advanced').all()
        })
    
    # 学習目標に基づく推奨
    if user.learning_goal == 'Webアプリケーションを作りたい':
        recommendations.append({
            'reason': 'Webアプリ開発向け：実践的なスキルを身につけましょう',
            'exams': Exam.query.filter_by(exam_type='practical').all()
        })
    elif user.learning_goal == 'データ分析・AI/MLを学びたい':
        recommendations.append({
            'reason': 'データ分析向け：データ処理のスキルを身につけましょう',
            'exams': Exam.query.filter_by(exam_type='data_analysis').all()
        })
    
    # 作りたいアプリケーションに基づく推奨
    if user.target_app in ['ECサイト・ショッピングサイト', 'SNS・コミュニティサイト', '業務管理システム']:
        recommendations.append({
            'reason': 'システム開発向け：実践的なプログラミングスキルを身につけましょう',
            'exams': Exam.query.filter_by(exam_type='practical').all()
        })
    elif user.target_app == 'データ分析ツール':
        recommendations.append({
            'reason': 'データ分析向け：データ処理と分析のスキルを身につけましょう',
            'exams': Exam.query.filter_by(exam_type='practical_data_analysis').all()
        })
    
    return recommendations

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# データベース初期化
def init_db():
    """データベースを安全に初期化"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        # エラーが発生してもアプリケーションは継続
        pass

# アプリケーション起動時に初期化
init_db()

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))