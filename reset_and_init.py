"""
データベースをリセットして新しい構造でサンプルデータを作成
"""
from app import app, db
from init_data import init_sample_data

def reset_and_initialize():
    """データベースをリセットして初期化"""
    with app.app_context():
        try:
            print("データベースをリセット中...")
            db.drop_all()
            db.create_all()
            print("データベース構造を更新しました")
            
            print("サンプルデータを作成中...")
            init_sample_data()
            print("完了！アプリケーションの準備ができました")
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            raise

if __name__ == '__main__':
    reset_and_initialize()