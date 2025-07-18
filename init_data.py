from app import app, db, Exam, Question

def init_sample_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Basic Exam - Beginner
        basic_beginner = Exam(
            title='Python基礎試験 - 初級',
            description='Pythonの基本的な文法と概念',
            difficulty='beginner',
            exam_type='basic'
        )
        db.session.add(basic_beginner)
        db.session.commit()
        
        # Basic Exam - Intermediate
        basic_intermediate = Exam(
            title='Python基礎試験 - 中級',
            description='Pythonの応用的な文法と概念',
            difficulty='intermediate',
            exam_type='basic'
        )
        db.session.add(basic_intermediate)
        db.session.commit()
        
        # Practical Exam - Beginner
        practical_beginner = Exam(
            title='Python実践試験 - 初級',
            description='実際のプログラミング問題（初級）',
            difficulty='beginner',
            exam_type='practical'
        )
        db.session.add(practical_beginner)
        db.session.commit()
        
        # Sample questions for Basic Beginner
        basic_beginner_questions = [
            {
                'question_text': 'Pythonで文字列を出力するための関数は何ですか？',
                'option_a': 'print()',
                'option_b': 'output()',
                'option_c': 'display()',
                'option_d': 'show()',
                'correct_answer': 'A',
                'explanation': 'print()関数は、Pythonで文字列や値を出力するための標準的な関数です。'
            },
            {
                'question_text': 'Pythonで変数に数値10を代入する正しい方法は？',
                'option_a': 'var = 10',
                'option_b': 'var := 10',
                'option_c': 'var == 10',
                'option_d': 'var -> 10',
                'correct_answer': 'A',
                'explanation': 'Pythonでは変数への代入に = 演算子を使用します。'
            },
            {
                'question_text': 'Pythonで文字列を表現する際に使用する記号は？',
                'option_a': '< >',
                'option_b': '[ ]',
                'option_c': '" " または \' \'',
                'option_d': '{ }',
                'correct_answer': 'C',
                'explanation': 'Pythonでは文字列をダブルクオート（"）またはシングルクオート（\'）で囲みます。'
            },
            {
                'question_text': 'Pythonでコメントを書く際に使用する記号は？',
                'option_a': '//',
                'option_b': '#',
                'option_c': '/*',
                'option_d': '--',
                'correct_answer': 'B',
                'explanation': 'Pythonでは # を使用して一行コメントを書きます。'
            },
            {
                'question_text': 'Pythonでリストを作成する際に使用する記号は？',
                'option_a': '{ }',
                'option_b': '( )',
                'option_c': '[ ]',
                'option_d': '< >',
                'correct_answer': 'C',
                'explanation': 'Pythonでは角括弧 [ ] を使用してリストを作成します。'
            },
            {
                'question_text': 'Pythonで条件分岐を行う際に使用するキーワードは？',
                'option_a': 'if',
                'option_b': 'when',
                'option_c': 'case',
                'option_d': 'switch',
                'correct_answer': 'A',
                'explanation': 'Pythonでは if キーワードを使用して条件分岐を行います。'
            },
            {
                'question_text': 'Pythonで繰り返し処理を行う際に使用するキーワードは？',
                'option_a': 'repeat',
                'option_b': 'loop',
                'option_c': 'for',
                'option_d': 'iterate',
                'correct_answer': 'C',
                'explanation': 'Pythonでは for キーワードを使用してループ処理を行います。'
            },
            {
                'question_text': 'Pythonで関数を定義する際に使用するキーワードは？',
                'option_a': 'function',
                'option_b': 'def',
                'option_c': 'method',
                'option_d': 'func',
                'correct_answer': 'B',
                'explanation': 'Pythonでは def キーワードを使用して関数を定義します。'
            },
            {
                'question_text': 'Pythonで辞書（dictionary）を作成する際に使用する記号は？',
                'option_a': '[ ]',
                'option_b': '( )',
                'option_c': '{ }',
                'option_d': '< >',
                'correct_answer': 'C',
                'explanation': 'Pythonでは波括弧 { } を使用して辞書を作成します。'
            },
            {
                'question_text': 'Pythonで文字列の長さを取得する関数は？',
                'option_a': 'length()',
                'option_b': 'size()',
                'option_c': 'count()',
                'option_d': 'len()',
                'correct_answer': 'D',
                'explanation': 'Pythonでは len() 関数を使用して文字列や他のオブジェクトの長さを取得します。'
            }
        ]
        
        for q_data in basic_beginner_questions:
            question = Question(
                exam_id=basic_beginner.id,
                question_text=q_data['question_text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
        
        # Sample questions for Basic Intermediate
        basic_intermediate_questions = [
            {
                'question_text': 'Pythonでクラスを定義する際に使用するキーワードは？',
                'option_a': 'class',
                'option_b': 'object',
                'option_c': 'struct',
                'option_d': 'type',
                'correct_answer': 'A',
                'explanation': 'Pythonでは class キーワードを使用してクラスを定義します。'
            },
            {
                'question_text': 'Pythonでモジュールをインポートする際に使用するキーワードは？',
                'option_a': 'include',
                'option_b': 'import',
                'option_c': 'require',
                'option_d': 'load',
                'correct_answer': 'B',
                'explanation': 'Pythonでは import キーワードを使用してモジュールをインポートします。'
            },
            {
                'question_text': 'Pythonでリスト内包表記の正しい書き方は？',
                'option_a': '{x for x in range(10)}',
                'option_b': '(x for x in range(10))',
                'option_c': '[x for x in range(10)]',
                'option_d': '<x for x in range(10)>',
                'correct_answer': 'C',
                'explanation': 'Pythonでは [expression for item in iterable] の形式でリスト内包表記を書きます。'
            },
            {
                'question_text': 'Pythonで例外処理を行う際に使用するキーワードは？',
                'option_a': 'try',
                'option_b': 'catch',
                'option_c': 'handle',
                'option_d': 'error',
                'correct_answer': 'A',
                'explanation': 'Pythonでは try-except 文を使用して例外処理を行います。'
            },
            {
                'question_text': 'Pythonでジェネレータを作成する際に使用するキーワードは？',
                'option_a': 'return',
                'option_b': 'yield',
                'option_c': 'generate',
                'option_d': 'create',
                'correct_answer': 'B',
                'explanation': 'Pythonでは yield キーワードを使用してジェネレータを作成します。'
            },
            {
                'question_text': 'Pythonでデコレータを定義する際に使用する記号は？',
                'option_a': '#',
                'option_b': '&',
                'option_c': '@',
                'option_d': '%',
                'correct_answer': 'C',
                'explanation': 'Pythonでは @ 記号を使用してデコレータを定義・適用します。'
            },
            {
                'question_text': 'Pythonでラムダ関数を定義する際に使用するキーワードは？',
                'option_a': 'lambda',
                'option_b': 'anonymous',
                'option_c': 'function',
                'option_d': 'arrow',
                'correct_answer': 'A',
                'explanation': 'Pythonでは lambda キーワードを使用して無名関数を定義します。'
            },
            {
                'question_text': 'Pythonでスライシングを行う際の正しい記法は？',
                'option_a': 'list(1:5)',
                'option_b': 'list[1:5]',
                'option_c': 'list{1:5}',
                'option_d': 'list<1:5>',
                'correct_answer': 'B',
                'explanation': 'Pythonでは角括弧内にコロンを使用してスライシングを行います。'
            },
            {
                'question_text': 'Pythonでwith文を使用する目的は？',
                'option_a': 'ループ処理',
                'option_b': '条件分岐',
                'option_c': 'リソース管理',
                'option_d': '関数定義',
                'correct_answer': 'C',
                'explanation': 'with文は、ファイルなどのリソースを自動的に管理するために使用されます。'
            },
            {
                'question_text': 'Pythonで*argsの目的は？',
                'option_a': '固定引数の受け取り',
                'option_b': '可変長引数の受け取り',
                'option_c': 'キーワード引数の受け取り',
                'option_d': 'デフォルト引数の設定',
                'correct_answer': 'B',
                'explanation': '*argsは可変長の位置引数を受け取るために使用されます。'
            }
        ]
        
        for q_data in basic_intermediate_questions:
            question = Question(
                exam_id=basic_intermediate.id,
                question_text=q_data['question_text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
        
        # Sample questions for Practical Beginner
        practical_beginner_questions = [
            {
                'question_text': '次のコードの出力は何ですか？\n\nfor i in range(3):\n    print(i)',
                'option_a': '1 2 3',
                'option_b': '0 1 2',
                'option_c': '3 2 1',
                'option_d': '0 1 2 3',
                'correct_answer': 'B',
                'explanation': 'range(3)は0, 1, 2の値を生成するため、出力は0 1 2となります。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\nnum = 5\nif num > 3:\n    print("大きい")\nelse:\n    print("小さい")',
                'option_a': '大きい',
                'option_b': '小さい',
                'option_c': 'エラー',
                'option_d': '何も出力されない',
                'correct_answer': 'A',
                'explanation': 'numの値5は3より大きいので、"大きい"が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\nlist1 = [1, 2, 3]\nlist1.append(4)\nprint(len(list1))',
                'option_a': '3',
                'option_b': '4',
                'option_c': '5',
                'option_d': 'エラー',
                'correct_answer': 'B',
                'explanation': 'append()で要素を追加後、リストの長さは4になります。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\ndef greet(name):\n    return "Hello, " + name\n\nprint(greet("Python"))',
                'option_a': 'Hello, Python',
                'option_b': 'Hello, name',
                'option_c': 'greet("Python")',
                'option_d': 'エラー',
                'correct_answer': 'A',
                'explanation': '関数greet()は引数nameと"Hello, "を連結して返すため、"Hello, Python"が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\ndict1 = {"a": 1, "b": 2}\nprint(dict1["a"])',
                'option_a': '1',
                'option_b': '2',
                'option_c': 'a',
                'option_d': 'エラー',
                'correct_answer': 'A',
                'explanation': '辞書dict1のキー"a"に対応する値1が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\ntext = "python"\nprint(text.upper())',
                'option_a': 'python',
                'option_b': 'PYTHON',
                'option_c': 'Python',
                'option_d': 'エラー',
                'correct_answer': 'B',
                'explanation': 'upper()メソッドは文字列を大文字に変換するため、"PYTHON"が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\nnum = 10\nif num % 2 == 0:\n    print("偶数")\nelse:\n    print("奇数")',
                'option_a': '偶数',
                'option_b': '奇数',
                'option_c': '10',
                'option_d': 'エラー',
                'correct_answer': 'A',
                'explanation': '10を2で割った余りは0なので、"偶数"が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\nlist2 = [1, 2, 3, 4, 5]\nprint(list2[1:4])',
                'option_a': '[1, 2, 3]',
                'option_b': '[2, 3, 4]',
                'option_c': '[1, 2, 3, 4]',
                'option_d': '[2, 3, 4, 5]',
                'correct_answer': 'B',
                'explanation': 'スライシング[1:4]は、インデックス1から3までの要素を取得するため、[2, 3, 4]が出力されます。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\ncount = 0\nfor i in range(5):\n    count += 1\nprint(count)',
                'option_a': '4',
                'option_b': '5',
                'option_c': '6',
                'option_d': '0',
                'correct_answer': 'B',
                'explanation': 'range(5)は5回繰り返すため、countは5になります。'
            },
            {
                'question_text': '次のコードの実行結果は？\n\nnum = 7\nif num > 5 and num < 10:\n    print("範囲内")\nelse:\n    print("範囲外")',
                'option_a': '範囲内',
                'option_b': '範囲外',
                'option_c': '7',
                'option_d': 'エラー',
                'correct_answer': 'A',
                'explanation': '7は5より大きく10より小さいので、"範囲内"が出力されます。'
            }
        ]
        
        for q_data in practical_beginner_questions:
            question = Question(
                exam_id=practical_beginner.id,
                question_text=q_data['question_text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            db.session.add(question)

        # Practical Coding Exam - Beginner
        practical_coding_beginner = Exam(
            title='Pythonコーディング基礎',
            description='基本的なアルゴリズムをコーディングで実践',
            difficulty='beginner',
            exam_type='practical_coding'
        )
        db.session.add(practical_coding_beginner)
        db.session.commit()

        coding_questions = [
            {
                'question_text': '2つの整数 `a` と `b` を受け取り、その合計を返す `add` という名前の関数を書いてください。',
                'question_type': 'coding',
                'solution_template': 'def add(a, b):\n    # ここにコードを書いてください\n    return 0\n',
                'test_code': 'assert add(2, 3) == 5\nassert add(-1, 1) == 0',
                'explanation': '関数内で `return a + b` とすることで、2つの引数の合計を返すことができます。'
            },
            {
                'question_text': '整数のリスト `numbers` を受け取り、その中の偶数だけを新しいリストとして返す `filter_even` という名前の関数を書いてください。',
                'question_type': 'coding',
                'solution_template': 'def filter_even(numbers):\n    # ここにコードを書いてください\n    return []\n',
                'test_code': 'assert filter_even([1, 2, 3, 4, 5]) == [2, 4]\nassert filter_even([10, 15, 20]) == [10, 20]',
                'explanation': 'forループとif文を使ってリストの各要素をチェックし、偶数（`num % 2 == 0`）であれば新しいリストに追加します。'
            }
        ]

        for q_data in coding_questions:
            question = Question(
                exam_id=practical_coding_beginner.id,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                solution_template=q_data['solution_template'],
                test_code=q_data['test_code'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
        
        db.session.commit()
        print("サンプルデータが正常に作成されました！")

if __name__ == "__main__":
    init_sample_data()