# Lab 2: Microsoft Sentinel MCP サーバーへ接続する

**所要時間:** 20 分  
**ゴール:** データ探索と Security Copilot エージェント作成の MCP ツールを VS Code から利用する

## こんなケースはありませんか

> 「調査のたびにどのテーブルに目的のデータがあるのか思い出せず、ドキュメントや過去の KQL を探し回っている」——サイロのテーブルが多く、列名も環境ごとに違うため、ベテランでもスキーマ確認に時間を取られがちです。

本 Lab で MCP サーバーを接続すると、**自然言語で「サインイン失敗を調べたい」と伝えるだけで、AI が実在するテーブルと列を探してくれる**ようになります。テーブル名を暗記する必要はなく、同じ MCP ツールが後の Lab で作るカスタムエージェントの土台にもなります。

> [!NOTE]
> 「MCP」は、VS Code から Sentinel のデータにつなぐ「差し込み口」だと思ってください。この Lab では 2 つの差し込み口を登録します。一つは「データを見る用」、もう一つは「エージェントを作る用」です。どちらも後で使うので、今は両方を入れておきます。

> [!IMPORTANT]
> 次の 2 つは用途が異なる MCP コレクションです。この Lab では両方を現在のワークスペースへ追加します。

| Server ID の例 | 用途 | URL |
|---|---|---|
| `sentinel-data-exploration` | テーブル検索、データ取得、エンティティ分析 | `https://sentinel.microsoft.com/mcp/data-exploration` |
| `security-copilot-agent-creation` | エージェントの作成、ツール検索、デプロイ | `https://sentinel.microsoft.com/mcp/security-copilot-agent-creation` |

## 2-1. データ探索コレクションを追加する

1. `Ctrl+Shift+P` を押します。
2. **MCP: Add Server** を選択します。
3. **HTTP (HTTP or Server-Sent Events)** を選択します。
4. 次の URL を入力します。大文字と小文字を変えないでください。

```text
https://sentinel.microsoft.com/mcp/data-exploration
```

5. Server ID に `sentinel-data-exploration` と入力します。
6. **Workspace** を選びます。
7. 信頼を求められたら、URL が `https://sentinel.microsoft.com/` であることを確認して許可します。
8. 演習対象テナントのアカウントで認証します。

> [!TIP]
> **画面ショット差し替え枠 `SS-04`:** MCP: Add Server で HTTP を選択する画面。

![SS-04 差し替え用ダミー: MCP: Add Server で HTTP を選択](../assets/screenshots/ss-04-mcp-http.png)

> [!TIP]
> **画面ショット差し替え枠 `SS-05`:** Microsoft の認証後、MCP サーバーが Running になった画面。テナント名以外の個人情報はマスクします。

![SS-05 差し替え用ダミー: MCP サーバーが Running](../assets/screenshots/ss-05-mcp-running.png)

## 2-2. エージェント作成コレクションを追加する

同じ手順でもう 1 台追加し、次を指定します。

```text
URL: https://sentinel.microsoft.com/mcp/security-copilot-agent-creation
Server ID: security-copilot-agent-creation
Scope: Workspace
```

**期待結果:** ワークスペースの `.vscode/mcp.json` に 2 つのサーバーが表示され、どちらも起動できます。

> [!CAUTION]
> 生成された `mcp.json` にアクセストークンを追記しないでください。認証は VS Code の認証フローに任せます。

## 2-3. ツールを確認する

1. **View > Chat** を開きます。
2. モードを **Agent** にします。
3. プロンプト欄のツールアイコンを選択します。
4. `sentinel-data-exploration` のデータ探索ツールが見えることを確認します。
5. `security-copilot-agent-creation` にエージェント作成用ツールが見えることを確認します。

> [!TIP]
> **画面ショット差し替え枠 `SS-06`:** 2 コレクションと配下のツールが展開されたツール一覧。

![SS-06 差し替え用ダミー: 2 コレクションのツール一覧](../assets/screenshots/ss-06-mcp-tools.png)

## 2-4. テーブルを検索する

データ探索コレクションだけを有効にし、次を送ります。

```text
Microsoft Sentinel で過去 24 時間のサインイン失敗を調べるために、利用可能な関連テーブルを検索してください。
まだログ本体は取得せず、候補テーブル名、用途、主要な時刻列と結果列を表にしてください。
```

**期待結果:** MCP ツールが呼び出され、テナントで利用可能なテーブル候補が返ります。候補は環境によって異なります。

次に、候補の 1 つを指定して少量だけ確認します。

```text
先ほど見つけた最適なテーブルを使い、過去 24 時間のサインイン失敗を最大 10 件だけ取得してください。
返す列は時刻、ユーザー、結果コード、IP アドレスに限定してください。使用した KQL も示してください。
```

**確認ポイント:** 時間条件、`project`、`take` または `top` が入り、不要な列や大量データを返していないこと。

## 2-5. 接続トラブルを切り分ける

| 症状 | 確認すること |
|---|---|
| 401/403 | 対象テナント、Security Reader、Security Copilot/データソース権限 |
| サーバーが起動しない | URL の綴り、VS Code の更新、組織のプロキシ設定 |
| ツールが表示されない | Agent モード、対象 MCP サーバーの起動、ツールの有効化 |
| テーブルが見つからない | Sentinel data lake のオンボード、データコネクタ、対象期間 |
| Builder がスキーマを取得しない | 必要な MCP コレクションが有効か、Builder の `allowed-tools` と実際のツール名が一致するか |

## チェックポイント

- [ ] 2 つの MCP コレクションを用途別に説明できる
- [ ] 両方のサーバーが VS Code で起動する
- [ ] テナントで利用可能なテーブルを MCP 経由で検索できる
- [ ] 最大 10 件、必要列のみのログ検索を実行できる
