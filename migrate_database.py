"""
本番環境用データベースマイグレーションスクリプト
新しいフィールドを既存のUserテーブルに追加
"""
import os
from app import app, db, User
from sqlalchemy import text

def migrate_database():
    """本番環境でデータベースの新しいフィールドを追加"""
    with app.app_context():
        try:
            print("データベースマイグレーション開始...")
            
            # 新しいカラムを追加（存在しない場合のみ）
            try:
                # target_completion_months カラムを追加
                db.engine.execute(text(
                    "ALTER TABLE user ADD COLUMN target_completion_months INTEGER"
                ))
                print("✅ target_completion_months カラムを追加しました")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e).lower():
                    print("ℹ️ target_completion_months カラムは既に存在します")
                else:
                    print(f"⚠️ target_completion_months 追加エラー: {e}")
            
            try:
                # preferred_learning_style カラムを追加
                db.engine.execute(text(
                    "ALTER TABLE user ADD COLUMN preferred_learning_style VARCHAR(100)"
                ))
                print("✅ preferred_learning_style カラムを追加しました")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e).lower():
                    print("ℹ️ preferred_learning_style カラムは既に存在します")
                else:
                    print(f"⚠️ preferred_learning_style 追加エラー: {e}")
            
            # 既存ユーザーのデフォルト値を設定
            try:
                db.engine.execute(text(
                    "UPDATE user SET target_completion_months = NULL WHERE target_completion_months IS NULL"
                ))
                db.engine.execute(text(
                    "UPDATE user SET preferred_learning_style = NULL WHERE preferred_learning_style IS NULL"
                ))
                print("✅ 既存ユーザーのデフォルト値を設定しました")
            except Exception as e:
                print(f"⚠️ デフォルト値設定エラー: {e}")
            
            print("🎉 データベースマイグレーション完了！")
            return True
            
        except Exception as e:
            print(f"❌ マイグレーションエラー: {e}")
            return False

if __name__ == '__main__':
    migrate_database()