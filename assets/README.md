# 画面ショット管理

教材中の `SS-xx` を実画像へ差し替えるための台帳です。画像は `assets/screenshots/ss-xx-short-name.png` の形式で保存し、該当する差し替え枠を Markdown 画像リンクへ置換します。

現在、各 `SS-xx` には各製品 UI を模したサンプル画像（右上に「サンプル（ダミー）」バッジ付き）が入っています。本番では、同じファイル名のまま実際のキャプチャで上書きするだけで教材へ反映されます（本文の変更は不要です）。

## ダミー画像の生成

`assets/screenshots/` のダミー画像は次のコマンドで再生成できます。

```powershell
python assets/generate_placeholders.py
```

## 差し替え手順

1. 実際の画面をキャプチャする。
2. 撮影ルールに従ってマスクする。
3. `assets/screenshots/` の同じファイル名で上書き保存する。
4. 教材でダミーが実画像に変わったことを確認する。
5. この台帳の状態を「完了」にする。

## 撮影ルール

- 1600 x 900 以上の PNG を推奨
- UI 言語は教材本文と合わせる
- ユーザー名、メール、テナント ID、サブスクリプション ID、ワークスペース名をマスクする
- API キー、トークン、Cookie、実インシデントの内容を写さない
- 強調枠や番号は画像編集で追加し、本文の手順番号と一致させる

## 台帳

| ID | 対象 | ファイル名 | 状態 |
|---|---|---|---|
| SS-01 | VS Code About | ss-01-vscode-about.png | ダミー（差し替え待ち） |
| SS-02 | 必須拡張機能 | ss-02-extensions.png | ダミー（差し替え待ち） |
| SS-03 | Builder のフォルダー構成 | ss-03-builder-folder.png | ダミー（差し替え待ち） |
| SS-04 | MCP の HTTP 選択 | ss-04-mcp-http.png | ダミー（差し替え待ち） |
| SS-05 | MCP Running | ss-05-mcp-running.png | ダミー（差し替え待ち） |
| SS-06 | 2 コレクションのツール一覧 | ss-06-mcp-tools.png | ダミー（差し替え待ち） |
| SS-07 | Security Copilot へのプラグインアップロード | ss-07-upload-plugin.png | ダミー（差し替え待ち） |
| SS-08 | API キーのセットアップ（値は非表示） | ss-08-api-key-setup.png | ダミー（差し替え待ち） |
| SS-09 | 対話型エージェントのスタータープロンプト | ss-09-starter-prompts.png | ダミー（差し替え待ち） |
| SS-10 | Logic App の HTTP trigger と承認 Condition | ss-10-logicapp-trigger.png | ダミー（差し替え待ち） |
| SS-11 | Logic App の実行履歴（本文は非表示） | ss-11-logicapp-run.png | ダミー（差し替え待ち） |
