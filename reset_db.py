"""
Renderでのデータベースリセット用スクリプト
"""
import os
from app import app, db

def reset_database():
    """データベースを完全にリセット"""
    with app.app_context():
        try:
            # 全テーブルを削除
            db.drop_all()
            print("✅ All tables dropped")
            
            # 全テーブルを再作成
            db.create_all()
            print("✅ All tables created")
            
            print("🎉 Database reset completed successfully")
            
        except Exception as e:
            print(f"❌ Database reset error: {e}")
            raise

if __name__ == '__main__':
    reset_database()