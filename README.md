# GitHub Copilot で作る Microsoft Security Copilot カスタムエージェント

VS Code と GitHub Copilot を使って、Microsoft Sentinel のデータを確かめながら Microsoft Security Copilot のカスタムプラグインとエージェントを作ってみる、手動かし式のワークショップです。

## はじめての方へ

ようこそ！このワークショップは、**プログラミングがはじめての方でも進められる**ように作成しています。ワークショップは、「**やりたいことを日本語で AI に伝える** → **出てきた内容を一緒に確かめる**」の繰り返しを体験いただくコンテンツです。

> [!IMPORTANT]
> 本教材は 2026-08-18 時点の公開情報に基づきます。Microsoft Sentinel MCP サーバーの一部機能と Security Copilot のカスタムエージェント機能にはプレビュー機能が含まれます。講師は開催前に「公開前チェックリスト」で画面、権限、モデル名、制限を再確認してください。

## やさしい用語集

| 用語 | 説明 |
|---|---|
| **VS Code** | マイクロソフトの無料エディター（文章やコードを書くアプリ）。今回の作業場所です。 |
| **GitHub Copilot** | VS Code の中でチャットできる AI アシスタント。日本語でお願いできます。 |
| **Security Copilot** | セキュリティ向けの AI。今回はここに「道具（プラグイン）」を追加します。 |
| **Microsoft Sentinel** | セキュリティのログを集めて分析する仕組み。今回のデータの出どころです。 |
| **プラグイン / スキル / ツール** | Security Copilot に追加できる「道具」。例：ログを検索する道具、外部サービスに問い合わせる道具。 |
| **エージェント** | いくつかの道具を手順どおりに使って仕事をこなす「係」のようなもの。 |
| **MCP** | AI と道具をつなぐ共通の差し込み口。VS Code から Sentinel のデータを見るために使います。 |
| **KQL** | Sentinel/Defender のログを検索する問い合わせの言語（SQL に似たもの）。今回は AI が下書きしてくれます。 |
| **YAML** | 設定を書くファイル形式。プラグインの「仕様書」と思ってください。今回は AI が作ります。 |
| **API** | 他のサービスにネット経由で問い合わせる窓口。 |
| **Logic Apps** | Azure で自動処理を組む仕組み。今回はメール通知の例で使います。 |
| **トークン** | AI が一度に扱える文章の量の目安。多すぎると不安定になります。 |

## 困ったときは

- エラーメッセージが出たら、**その文面をそのまま GitHub Copilot に貼って「どうすればいい？」と聞いてみましょう**。ただし、パスワードや API キーなどの秘密は貼らないでください。
- 各 Lab の末尾にある「チェックポイント」で、できたことを確かめられます。
- うまくいかないときは、一つ前の Lab のチェックポイントに戻ると原因が見つかりやすいです。

## 到達目標

受講後、次のことができるようになります。

- VS Code と GitHub Copilot の開発環境を準備する
- Microsoft Sentinel MCP サーバーを VS Code に接続する
- MCP ツールで Sentinel/Defender のテーブルとスキーマを確認する
- KQL、API、GPT、対話型エージェントの YAML マニフェストを生成して検証する
- Security Copilot にカスタムプラグインまたはエージェントを登録してテストする
- Logic Apps に通知処理を分離し、トークン消費を抑える設計を説明する

## 対象者

- VS Code を初めて使う、または基本操作ができるセキュリティ担当者
- KQL と YAML の経験は不問
- Microsoft Sentinel、Defender XDR、Security Copilot の基礎用語を知っていると進めやすい

## 所要時間

| パート | 内容 | 目安 |
|---|---|---:|
| 事前準備 | アカウント、ロール、製品アクセスの確認 | 開催前 30 分 |
| Lab 0-1 | 環境構築と MCP 接続 | 45 分 |
| Lab 2-5 | 4 種類のプラグイン/エージェント作成 | 120 分 |
| Lab 6-7 | Logic Apps、チューニング、制約 | 45 分 |
| まとめ | 成果確認とクリーンアップ | 15 分 |

合計は約 3 時間 45 分です。API キーの発行や Azure リソースの準備時間は含みません。

## 必要なもの

- Windows または macOS の端末
- 最新の Visual Studio Code
- GitHub Copilot Enterprise が割り当てられた GitHub アカウント
- VS Code の GitHub Copilot 拡張機能
- Microsoft Security Copilot へのアクセスとプロビジョニング済み容量
- 演習用 Microsoft Sentinel/Defender 環境への読み取りアクセス
- カスタムプラグインを追加できる Security Copilot の権限
- API 演習を行う場合のみ VirusTotal API キー
- 応用演習を行う場合のみ Azure Logic Apps を作成できる権限

> [!NOTE]
> GitHub Copilot Enterprise は契約プランです。VS Code に「Enterprise 版」を別途インストールするのではなく、組織からライセンスを割り当てられたアカウントで GitHub Copilot 拡張機能へサインインします。

## 進め方

各 Lab は次の同じ流れで進みます。

1. ゴールと前提条件を確認する
2. GitHub Copilot に日本語の要求を渡す
3. 生成された YAML/KQL/OpenAPI を人がレビューする
4. 機密情報、対象テーブル、件数制限を確認する
5. Security Copilot に登録し、正常系と異常系をテストする
6. チェックポイントを満たしたら次の Lab に進む

## カリキュラム

1. [Lab 0: 事前準備](docs/00-prerequisites.md)
2. [Lab 1: 開発環境](docs/01-environment.md)
3. [Lab 2: Microsoft Sentinel MCP](docs/02-mcp.md)
4. [Lab 3: Defender サインイン失敗 KQL プラグイン](docs/03-kql-plugin.md)
5. [Lab 4: VirusTotal API プラグイン](docs/04-api-plugin.md)
6. [Lab 5: インシデント調査の対話型エージェント](docs/05-interactive-agent.md)
7. [Lab 6: KQL + GPT インシデント調査ツールキット](docs/06-mixed-plugin.md)
8. [Lab 7: Logic Apps HTML/CSS レポート通知](docs/07-logic-apps.md)
9. [Lab 8: チューニングと制約](docs/08-tuning-limitations.md)

講師は [講師ガイド](instructor-guide.md)、公開前の根拠確認には [参考資料](references.md)、撮影担当者は [画面ショット管理](assets/README.md) を使用してください。

## 安全上のルール

- API キー、トークン、パスワードをチャット、YAML、Git、画面ショットへ貼り付けない
- 演習は読み取り専用から開始し、最小権限のアカウントを使う
- AI の生成物をそのまま本番公開せず、クエリ対象、時間範囲、出力件数、認証方式をレビューする
- 実在する個人情報や機密インシデントを公開リポジトリへ含めない
- 外部 API への送信前に、組織のデータ取扱規程と API 提供元の利用条件を確認する

## 教材の状態

このワークショップでは [Security Copilot custom plugins builder](https://github.com/mariocuomo/Experimenting-With-Security-Copilot/tree/main/Security%20Copilot%20custom%20plugins%20builder)（[紹介記事](https://www.linkedin.com/pulse/security-copilot-custom-plugins-builder-mario-cuomo-tyjef/)）を活用します。これは VS Code の GitHub Copilot 向け AI スキルで、要件を言葉で伝えるだけで Security Copilot のプラグイン/エージェント用 YAML マニフェストの作成・スキーマ確認・検証までを案内します。YAML スキーマや KQL/OpenAPI の細部を覚えていなくてもレビュー可能な下書きが得られる点が利点です。詳しくは [Lab 1](docs/01-environment.md#security-copilot-custom-plugins-builder-とは) を参照してください。

このリポジトリで参照するコミュニティ製の custom plugins builder は Microsoft の公式製品ではありません。公式仕様は Microsoft Learn を正とし、生成結果は必ず Security Copilot 上で検証してください。
