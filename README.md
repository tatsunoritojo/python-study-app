# Python学習アプリ

Python基礎から実践まで学習できるWebアプリケーションです。

## 機能

- **ユーザー認証** - 安全なログイン・登録システム
- **4種類の試験** - 基礎、実践、データ分析、実践データ分析
- **3段階の難易度** - 初級、中級、上級
- **学習進捗管理** - 受験履歴と成績の可視化
- **レスポンシブデザイン** - PC・スマートフォン対応

## 技術スタック

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy + PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **認証**: Flask-Login
- **デプロイ**: Render

## ローカル開発

```bash
# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを実行
python app.py
```

## 本番環境

このアプリケーションはRenderで公開されています。
PostgreSQLデータベースを使用し、環境変数で設定を管理しています。

## 作者

フリーランス開発者 - tatsu  
AI駆動開発による高速なWebアプリケーション制作