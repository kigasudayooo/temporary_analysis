# uvを使用したPython環境構築マニュアル

## 1. uvとは
uvは高速なPythonパッケージインストーラーで、pipの代替として使用できるツールです。Rustで書かれており、従来のpipと比べて大幅なパフォーマンス向上が期待できます。

## 2. システム要件
- Python 3.7以上
- Windows、macOS、またはLinux

## 3. uvのインストール

### pipを使用したインストール
```bash
pip install uv
```

### 動作確認
インストールが完了したら、以下のコマンドでuvのバージョンを確認できます：
```bash
uv --version
```

## 4. プロジェクトでの使用方法

### 4.1 仮想環境の作成

#### 新規仮想環境の作成（デフォルトのPythonバージョン）
```bash
uv venv
```
このコマンドで`.venv`ディレクトリに新しい仮想環境が作成されます。

#### 特定のPythonバージョンでの仮想環境作成
```bash
uv venv --python=3.10
# または
uv venv --python=/path/to/python3.10
```

#### 既存の仮想環境の反映
requirements.txtから既存の環境を再現する場合：
```bash
# 新しい仮想環境を作成
uv venv
# 仮想環境を有効化
source .venv/bin/activate  # Linux/macOS
# または
.venv\Scripts\activate     # Windows
# 既存の依存関係をインストール
uv pip install -r requirements.txt
```

既存のpip環境からuvに移行する場合：
```bash
# 現在の環境の依存関係を出力
pip freeze > requirements.txt
# uvで新しい仮想環境を作成
uv venv
# uvで依存関係をインストール
uv pip install -r requirements.txt
```

### 4.2 仮想環境の有効化
Windows:
```cmd
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 4.3 パッケージのインストール

#### requirements.txtからのインストール
```bash
uv pip install -r requirements.txt
```

#### 単一パッケージのインストール
```bash
uv pip install パッケージ名
```

#### 開発用パッケージのインストール
```bash
uv pip install -r requirements-dev.txt
```

## 5. よく使用するコマンド

### パッケージの一覧表示
```bash
uv pip freeze
```

### パッケージの更新
```bash
uv pip install --upgrade パッケージ名
```

### パッケージの削除
```bash
uv pip uninstall パッケージ名
```

## 6. uvの主な特徴

### 6.1 高速なインストール
- 並列ダウンロードとインストール
- キャッシュの最適化
- 依存関係の効率的な解決

### 6.2 互換性
- pipとの互換性維持
- requirements.txtの完全サポート
- pip.confの設定の尊重

## 7. トラブルシューティング

### 7.1 一般的な問題と解決方法

#### パッケージのインストールに失敗する場合
1. キャッシュのクリア
```bash
uv cache clean
```

2. 仮想環境の再作成
```bash
rm -rf .venv
uv venv
```

#### 依存関係の競合
requirements.txtの依存関係を確認し、必要に応じて更新してください。

### 7.2 エラーメッセージの確認
詳細なログを表示するには、-vオプションを使用します：
```bash
uv -v pip install パッケージ名
```

## 8. Pythonバージョン管理

### 8.1 システム上の複数Pythonバージョンの管理
uvは直接Pythonバージョンの管理を行いませんが、以下のツールと組み合わせて使用できます：

- pyenv (Linux/macOS)
- pyenv-win (Windows)
- asdf
- conda

#### pyenvとの併用例
```bash
# 特定のPythonバージョンをインストール
pyenv install 3.10.0

# そのバージョンを使用して仮想環境を作成
pyenv shell 3.10.0
uv venv
```

### 8.2 プロジェクトでのPythonバージョン固定
`.python-version`ファイルや`runtime.txt`を使用して、プロジェクトのPythonバージョンを明示的に指定することをお勧めします：

```bash
# .python-versionの例
3.10.0

# runtime.txtの例
python-3.10.0
```

## 9. ベストプラクティス

### 8.1 プロジェクト構成
```
プロジェクト/
├── .venv/
├── requirements.txt
├── requirements-dev.txt
└── src/
```

### 8.2 推奨設定
- プロジェクトごとに独立した仮想環境を使用
- requirements.txtの定期的な更新
- バージョン固定による再現性の確保

## 9. セキュリティ考慮事項
- 信頼できるソースからのパッケージのみをインストール
- 定期的なパッケージの更新
- 脆弱性チェックの実施

## 10. 補足情報
- プロジェクトのドキュメント: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- コミュニティサポート: GitHub Issues
- ライセンス: Apache-2.0/MIT