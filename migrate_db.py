"""
データベースマイグレーション用スクリプト
新しいユーザープロフィールカラムを追加
"""
import os
from app import app, db, User

def migrate_database():
    """データベースを最新のスキーマにマイグレーション"""
    with app.app_context():
        try:
            # 既存のテーブルを削除して再作成
            db.drop_all()
            db.create_all()
            
            print("✅ データベースマイグレーションが完了しました")
            print("🔄 新しいユーザープロフィール機能が利用可能です")
            
        except Exception as e:
            print(f"❌ マイグレーションエラー: {e}")
            raise

if __name__ == '__main__':
    migrate_database()