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
    target_completion_months = db.Column(db.Integer, nullable=True)  # 目標完了月数
    preferred_learning_style = db.Column(db.String(100), nullable=True)  # 学習スタイル
    
    results = db.relationship('ExamResult', backref='user', lazy=True)
    roadmap_progress = db.relationship('RoadmapProgress', backref='user', lazy=True)

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
    
    # 解説と学習支援
    explanation = db.Column(db.Text, nullable=True)  # 解説
    additional_info = db.Column(db.Text, nullable=True)  # 周辺知識
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5の難易度
    
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

class RoadmapStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    step_order = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # foundation, web_dev, data_analysis, etc.
    estimated_hours = db.Column(db.Integer, nullable=False)
    required_for_goals = db.Column(db.String(500))  # カンマ区切りの目標リスト
    exam_ids = db.Column(db.String(200))  # 関連する試験ID（カンマ区切り）
    resources = db.Column(db.Text)  # 学習リソースのJSON

class RoadmapProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('roadmap_step.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='not_started')  # not_started, in_progress, completed
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    step = db.relationship('RoadmapStep', backref='progress_records')

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
    
    if not questions:
        flash('この試験には問題が設定されていません', 'warning')
        return redirect(url_for('dashboard'))
    
    # セッションに試験情報を保存
    session['current_exam'] = {
        'exam_id': exam_id,
        'question_ids': [q.id for q in questions],
        'current_question': 0,
        'answers': {},
        'correct_count': 0
    }
    
    return redirect(url_for('exam_question', question_number=1))

@app.route('/exam/question/<int:question_number>')
@login_required
def exam_question(question_number):
    if 'current_exam' not in session:
        flash('試験セッションが見つかりません', 'error')
        return redirect(url_for('dashboard'))
    
    exam_data = session['current_exam']
    total_questions = len(exam_data['question_ids'])
    
    if question_number > total_questions:
        return redirect(url_for('exam_complete'))
    
    question_id = exam_data['question_ids'][question_number - 1]
    question = Question.query.get_or_404(question_id)
    exam = Exam.query.get_or_404(exam_data['exam_id'])
    
    progress_percentage = ((question_number - 1) / total_questions) * 100
    
    return render_template('exam_question.html', 
                         exam=exam, 
                         question=question, 
                         question_number=question_number,
                         total_questions=total_questions,
                         progress_percentage=progress_percentage)

@app.route('/exam/answer', methods=['POST'])
@login_required
def submit_answer():
    if 'current_exam' not in session:
        return redirect(url_for('dashboard'))
    
    exam_data = session['current_exam']
    question_number = int(request.form.get('question_number'))
    user_answer = request.form.get('answer')
    question_id = exam_data['question_ids'][question_number - 1]
    
    question = Question.query.get_or_404(question_id)
    is_correct = user_answer == question.correct_answer
    
    # 答えを記録
    exam_data['answers'][question_id] = {
        'user_answer': user_answer,
        'correct_answer': question.correct_answer,
        'is_correct': is_correct
    }
    
    if is_correct:
        exam_data['correct_count'] += 1
    
    session['current_exam'] = exam_data
    
    return render_template('answer_feedback.html',
                         question=question,
                         user_answer=user_answer,
                         is_correct=is_correct,
                         question_number=question_number,
                         total_questions=len(exam_data['question_ids']))

@app.route('/exam/complete')
@login_required
def exam_complete():
    if 'current_exam' not in session:
        return redirect(url_for('dashboard'))
    
    exam_data = session['current_exam']
    exam = Exam.query.get_or_404(exam_data['exam_id'])
    
    # 結果を保存
    result = ExamResult(
        user_id=current_user.id,
        exam_id=exam_data['exam_id'],
        score=exam_data['correct_count'],
        total_questions=len(exam_data['question_ids'])
    )
    db.session.add(result)
    db.session.commit()
    
    # セッションをクリア
    session.pop('current_exam', None)
    
    flash(f'試験が完了しました！ {exam_data["correct_count"]}/{len(exam_data["question_ids"])} 問正解', 'success')
    return redirect(url_for('exam_result', result_id=result.id))

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
        current_user.target_completion_months = int(request.form.get('target_completion_months', 0)) if request.form.get('target_completion_months') else None
        current_user.preferred_learning_style = request.form.get('preferred_learning_style')
        
        db.session.commit()
        flash('プロフィールを更新しました！パーソナライズされたロードマップをご確認ください。', 'success')
        return redirect(url_for('roadmap'))
    
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

# データベース初期化を遅延実行
def init_db():
    """データベースを安全に初期化"""
    try:
        db.create_all()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

@app.route('/roadmap')
@login_required
def roadmap():
    """ユーザーのパーソナライズされた学習ロードマップを表示"""
    # ユーザーの設定に基づいてロードマップを生成
    roadmap_data = generate_personalized_roadmap(current_user)
    
    # ユーザーの進捗を取得
    progress_data = get_user_progress(current_user)
    
    return render_template('roadmap.html', 
                         roadmap=roadmap_data, 
                         progress=progress_data,
                         user_profile=current_user)

def generate_personalized_roadmap(user):
    """ユーザーのプロフィールに基づいてパーソナライズされたロードマップを生成"""
    roadmap = {
        'title': f'{user.username}さんの学習ロードマップ',
        'estimated_duration': calculate_estimated_duration(user),
        'steps': []
    }
    
    # 基本的なPythonスキル
    if user.experience_level == 'beginner':
        roadmap['steps'].extend([
            {
                'id': 1,
                'title': 'Python基礎',
                'description': 'Pythonの基本文法、変数、データ型',
                'category': 'foundation',
                'estimated_hours': 20,
                'skills': ['変数と代入', 'データ型', '基本演算'],
                'exams': ['Python基礎試験 - 初級'],
                'status': 'available'
            },
            {
                'id': 2,
                'title': '制御構造',
                'description': 'if文、ループ処理、条件分岐',
                'category': 'foundation',
                'estimated_hours': 15,
                'skills': ['if文', 'for/whileループ', '条件演算子'],
                'exams': ['Python基礎試験 - 初級'],
                'status': 'locked'
            },
            {
                'id': 3,
                'title': 'データ構造',
                'description': 'リスト、辞書、タプル、セット',
                'category': 'foundation',
                'estimated_hours': 18,
                'skills': ['リスト操作', '辞書の活用', 'タプルとセット'],
                'exams': ['Python基礎試験 - 中級'],
                'status': 'locked'
            }
        ])
    elif user.experience_level == 'intermediate':
        roadmap['steps'].extend([
            {
                'id': 1,
                'title': 'Python復習',
                'description': 'Pythonの特徴的な機能の理解',
                'category': 'foundation',
                'estimated_hours': 10,
                'skills': ['リスト内包表記', 'lambda関数', 'デコレータ'],
                'exams': ['Python基礎試験 - 中級'],
                'status': 'available'
            }
        ])
    
    # 学習目標に応じた専門スキル
    if user.learning_goal and 'Web' in user.learning_goal:
        roadmap['steps'].extend([
            {
                'id': 10,
                'title': 'Webフレームワーク基礎',
                'description': 'FlaskまたはDjangoの基本',
                'category': 'web_development',
                'estimated_hours': 25,
                'skills': ['HTTP理解', 'テンプレート', 'ルーティング'],
                'exams': ['Web開発実践試験'],
                'status': 'locked'
            },
            {
                'id': 11,
                'title': 'データベース連携',
                'description': 'SQLとORM',
                'category': 'web_development',
                'estimated_hours': 20,
                'skills': ['SQL基礎', 'ORM操作', 'マイグレーション'],
                'exams': ['データベース基礎試験'],
                'status': 'locked'
            }
        ])
    elif user.learning_goal and 'データ分析' in user.learning_goal:
        roadmap['steps'].extend([
            {
                'id': 20,
                'title': 'データ分析ライブラリ',
                'description': 'NumPy, Pandas, Matplotlib',
                'category': 'data_analysis',
                'estimated_hours': 30,
                'skills': ['NumPy配列', 'Pandas操作', '可視化'],
                'exams': ['データ分析基礎試験'],
                'status': 'locked'
            }
        ])
    elif user.learning_goal and '自動化' in user.learning_goal:
        roadmap['steps'].extend([
            {
                'id': 30,
                'title': 'スクリプト作成',
                'description': 'ファイル操作、API連携',
                'category': 'automation',
                'estimated_hours': 15,
                'skills': ['ファイル処理', 'API活用', 'スケジューリング'],
                'exams': ['自動化スクリプト試験'],
                'status': 'locked'
            }
        ])
    
    # 最終プロジェクト
    roadmap['steps'].append({
        'id': 99,
        'title': '実践プロジェクト',
        'description': f'{user.target_app or "選択したアプリケーション"}の開発',
        'category': 'project',
        'estimated_hours': 40,
        'skills': ['プロジェクト設計', '実装', 'デプロイ'],
        'exams': ['最終プロジェクト評価'],
        'status': 'locked'
    })
    
    return roadmap

def calculate_estimated_duration(user):
    """ユーザーの学習時間に基づいて推定期間を計算"""
    base_hours = 80  # 基本的な学習時間
    
    if user.experience_level == 'beginner':
        base_hours = 120
    elif user.experience_level == 'intermediate':
        base_hours = 80
    elif user.experience_level == 'advanced':
        base_hours = 50
    
    # 学習目標による追加時間
    if user.learning_goal:
        if 'Web' in user.learning_goal:
            base_hours += 50
        elif 'データ分析' in user.learning_goal:
            base_hours += 60
        elif '自動化' in user.learning_goal:
            base_hours += 30
    
    weekly_hours = user.study_time_per_week or 5
    estimated_weeks = base_hours / weekly_hours
    
    return {
        'total_hours': base_hours,
        'weeks': int(estimated_weeks),
        'weekly_hours': weekly_hours
    }

def get_user_progress(user):
    """ユーザーの学習進捗を取得"""
    # 実際のデータベースから進捗を取得（今回は簡単な例）
    completed_exams = ExamResult.query.filter_by(user_id=user.id).count()
    total_exams = Exam.query.count()
    
    return {
        'completed_exams': completed_exams,
        'total_exams': total_exams,
        'completion_percentage': (completed_exams / total_exams * 100) if total_exams > 0 else 0
    }

# Renderでの初回リクエスト時に初期化
@app.before_request
def ensure_db_exists():
    """リクエスト前にデータベースの存在を確認"""
    if not hasattr(app, '_db_initialized'):
        with app.app_context():
            init_db()
        app._db_initialized = True

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))