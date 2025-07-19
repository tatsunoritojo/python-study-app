"""
サンプル問題データの追加
詳細な解説と周辺知識付きの問題を作成
"""
from app import app, db, Exam, Question

def add_sample_questions():
    """サンプル問題を追加"""
    with app.app_context():
        # 基礎試験の問題を追加
        basic_exam = Exam.query.filter_by(exam_type='basic', difficulty='beginner').first()
        if not basic_exam:
            basic_exam = Exam(
                title='Python基礎（初級）',
                description='Pythonの基本的な文法と概念を学習します',
                difficulty='beginner',
                exam_type='basic'
            )
            db.session.add(basic_exam)
            db.session.commit()

        # サンプル問題1: 変数とデータ型
        question1 = Question(
            exam_id=basic_exam.id,
            question_text='Pythonで文字列を表現する際に使用する正しい記号はどれですか？',
            question_type='multiple_choice',
            option_a='シングルクォート（\'）またはダブルクォート（"）',
            option_b='角括弧（[]）',
            option_c='波括弧（{}）',
            option_d='丸括弧（()）',
            correct_answer='A',
            explanation='Pythonでは文字列を表現するために、シングルクォート（\'）またはダブルクォート（"）を使用します。どちらを使用しても同じ結果が得られますが、一貫性を保つことが重要です。',
            additional_info='文字列の中にクォートを含める場合は、エスケープ文字（\\）を使用するか、異なる種類のクォートを使用できます。また、複数行の文字列には三重クォート（\'\'\'または"""）を使用します。トリプルクォートは文書化文字列（docstring）でも使用されます。',
            difficulty_level=1
        )

        # サンプル問題2: リストの操作
        question2 = Question(
            exam_id=basic_exam.id,
            question_text='リスト [1, 2, 3] の末尾に要素 4 を追加するための正しいメソッドはどれですか？',
            question_type='multiple_choice',
            option_a='append(4)',
            option_b='add(4)',
            option_c='insert(4)',
            option_d='push(4)',
            correct_answer='A',
            explanation='リストの末尾に要素を追加するには append() メソッドを使用します。append() は引数として渡された要素をリストの最後に追加します。',
            additional_info='リストの操作には他にも多くのメソッドがあります：insert(index, item)で指定位置に挿入、remove(item)で最初に見つかった要素を削除、pop()で最後の要素を削除して返す、extend()で別のリストの要素をすべて追加、などがあります。これらのメソッドを適切に使い分けることで効率的なプログラムが書けます。',
            difficulty_level=2
        )

        # サンプル問題3: 条件分岐
        question3 = Question(
            exam_id=basic_exam.id,
            question_text='Pythonのif文で「xが10以上かつ20以下」を判定する正しい条件式はどれですか？',
            question_type='multiple_choice',
            option_a='10 <= x <= 20',
            option_b='x >= 10 and x <= 20',
            option_c='10 <= x and x <= 20',
            option_d='上記すべて正しい',
            correct_answer='D',
            explanation='Pythonでは「10 <= x <= 20」のような連鎖比較が可能です。また、「x >= 10 and x <= 20」や「10 <= x and x <= 20」のように and 演算子を使用しても同じ結果が得られます。',
            additional_info='Pythonの連鎖比較は数学的な記法に近く、直感的で読みやすいコードが書けます。他の多くの言語では and 演算子を使う必要がありますが、Pythonの連鎖比較は言語の特徴の一つです。条件分岐では or, and, not 演算子も重要で、複雑な条件を組み合わせる際に使用します。',
            difficulty_level=2
        )

        # サンプル問題4: 関数
        question4 = Question(
            exam_id=basic_exam.id,
            question_text='Pythonで関数を定義するキーワードはどれですか？',
            question_type='multiple_choice',
            option_a='def',
            option_b='function',
            option_c='func',
            option_d='define',
            correct_answer='A',
            explanation='Pythonでは関数を定義するために def キーワードを使用します。def の後に関数名、括弧内に引数、コロン（:）の後にインデントされたブロックで関数の処理を記述します。',
            additional_info='関数は再利用可能なコードブロックを作成する重要な機能です。引数にはデフォルト値を設定でき、可変長引数（*args, **kwargs）も使用できます。return文で値を返すことができ、return文がない場合は None が返されます。関数の先頭にdocstringを書くことで、関数の説明を記述できます。',
            difficulty_level=2
        )

        # サンプル問題5: データ型の判定
        question5 = Question(
            exam_id=basic_exam.id,
            question_text='変数の型を調べるために使用する組み込み関数はどれですか？',
            question_type='multiple_choice',
            option_a='type()',
            option_b='typeof()',
            option_c='gettype()',
            option_d='datatype()',
            correct_answer='A',
            explanation='Pythonでは type() 関数を使用して変数の型を調べることができます。type(variable) とすると、その変数の型が返されます。',
            additional_info='型の確認には type() 以外に isinstance() 関数もあります。isinstance(obj, class) は obj が class のインスタンスかどうかを True/False で返します。isinstance() は継承関係も考慮するため、より柔軟な型チェックが可能です。動的型付け言語であるPythonでは、実行時に型を確認することが重要な場面があります。',
            difficulty_level=1
        )

        # データベースに追加
        questions = [question1, question2, question3, question4, question5]
        for question in questions:
            existing = Question.query.filter_by(
                exam_id=question.exam_id,
                question_text=question.question_text
            ).first()
            if not existing:
                db.session.add(question)

        db.session.commit()
        print("✅ サンプル問題が追加されました")

if __name__ == '__main__':
    add_sample_questions()