# Lab 9: ローカル指示書から週次 Defender レポートエージェントを作る

**所要時間:** 45 分
**ゴール:** 要件をまとめたローカル Markdown ファイルを GitHub Copilot に読み込ませ、Defender の週次統計を日本語 HTML で作成するカスタムエージェント一式を生成する

## こんなケースはありませんか

> 「チャットへ長い要件を毎回貼ると、条件が抜けたり、受講者ごとに生成結果が変わったりする」——要件をローカルの指示書として管理すると、同じ条件を再利用しながら生成物と一緒にレビューできます。

この Lab では、用意された指示書を Builder のローカルファイルとして配置し、その内容を唯一の要件としてカスタムエージェントを作成します。生成された YAML、HTML、README が指示書を満たすか、人が確認するところまでが演習です。

> [!IMPORTANT]
> この演習では Microsoft Sentinel ではなく Microsoft Defender の KQL スキルを使います。実データへの接続は読み取り専用とし、メール送信は講師指定のテスト環境で承認後にだけ実施してください。

## 9-1. ローカル指示書を作成する

まず、エージェントに実現してほしい目的、処理、出力を Markdown の指示書として整理します。チャットへ直接入力するのではなくファイルにすることで、長い要件を繰り返し利用でき、変更点もレビューしやすくなります。

1. VS Code で `Security Copilot custom plugins builder/Builder` フォルダーを開きます。
2. Explorer で **New File** を選び、Builder のルートに `WeeklyDefenderIncidentReport.md` を新規作成します。
3. 作成したファイルへ、次の指示書を入力します。

```markdown
# 目的
- Microsoft Defender に接続して、週次で SOC/CSIRT 向けの統計レポートを日本語の HTML/CSS で生成するカスタムエージェントを作成すること

# 詳細
- Microsoft Defender に対して、インシデント統計の傾向を KQL で集計し、レポートを作成すること
- レポートは日本語で生成すること
- Microsoft Sentinel ではなく、Defender の KQL スキルを利用すること。週次の傾向（先週・今週）を比較し、インシデントの傾向を分析して通知すること
- MITRE 戦術を分析して、
- HTML CSS を用いて、視認性の良いレポートを生成すること
 - JavaScript は用いないこと
 - フォントはメイリオフォントを用いること
 - Outlook でメール閲覧することを想定し、メールで開ける HTML 幅であること
- HTML CSS はロジックアプリを経由してメール通知を行うこと
- Security Copilot Custom Agent の LLM (gpt-4o) のトークン制限を考慮してエージェントを作成すること
 - KQL は limit をかけてトークン量を下げること

# レポートイメージ
- 日次トレンドチャート
 - Severity 別統計＋先週比較
- カテゴリー別分布
 - MITRE 戦術カテゴリー
 - 製品毎比較
- 送信元 IP / 宛先 IP
- 週次傾向サマリー
 - 前週比の自然言語分析（3〜5項目）
 - 危険度上位5件の詳細
- 推奨対策方針
 - 即時対応すべき点
 - ユーザー啓発
 - アーキテクチャ改善

# アウトプット
- 今回の生成物は、Builder/output フォルダにエージェント名でフォルダを作成し、中に以下を生成すること
 - カスタムエージェントの YAML ファイル
 - サンプル HTML イメージ例
 - README
```

4. ファイルを保存し、Explorer で次の配置になっていることを確認します。

```text
Builder/
├─ SKILL.md
├─ WeeklyDefenderIncidentReport.md
├─ references/
└─ output/
```

5. `WeeklyDefenderIncidentReport.md` を開き、目的、詳細、レポートイメージ、アウトプットの4節があることを確認します。

ローカルファイルにすることで、チャットへ長い要件を貼り直さず、レビューや差分管理の対象にできます。環境 ID、メールアドレス、実インシデント情報、シークレットは指示書へ追記しません。

<img width="2496" height="1592" alt="image" src="https://github.com/user-attachments/assets/209b504b-e895-45c9-90a5-4be07bd1aa53" />

## 9-2. 指示書からエージェントを生成する

Copilot Chat を **Agent** モードにし、Defender と Security Copilot Agent の Builder が利用するツールを有効にして、次を送ります。

```text
ローカルの WeeklyDefenderIncidentReport.md を読み、その指示だけを要件として Security Copilot Custom Agent を作成してください。
Builder のワークフローに従って Defender の利用可能なテーブルと列を確認し、不明点は生成前に質問してください。
生成物は指示書で指定された Builder/output 配下へ保存し、最後に検証結果と未確定のプレースホルダーを一覧にしてください。
```

Copilot から対象テーブル、実行方式、Logic Apps スキルの設定などを質問された場合は、講師が用意した演習環境の値を答えます。列名やテーブル名を推測で確定させず、利用可能な Defender スキーマの確認結果を優先します。

<img width="2496" height="1592" alt="image" src="https://github.com/user-attachments/assets/9c5912d0-199c-485d-b984-252b2cb42e82" />

## 9-3. 出力フォルダーを確認する

生成後、`Builder/output/<エージェント名>/` に次の3ファイルがあることを確認します。ファイル名は Builder の命名規則に従うため、完全一致でなくても構いません。

```text
Builder/output/<エージェント名>/
├─ <エージェント名>.yaml
├─ <エージェント名>-sample.html
└─ README.md
```

- YAML: Defender KQL スキル、レポート生成指示、Logic Apps 連携に必要な定義
- HTML: ダミーデータだけを使った Outlook 向け表示サンプル
- README: 設定値、登録方法、テスト方法、制約、メール通知の手順

> [!CAUTION]
> サンプル HTML に実在するユーザー名、IP アドレス、インシデント本文を含めません。リポジトリへ登録する場合は、予約済みの例示用 IP アドレスなど明示的なダミーデータを使います。

## 9-4. YAML と KQL をレビューする

| 観点 | 合格条件 |
|---|---|
| Data source | Sentinel ではなく Defender を対象にしている |
| Time windows | 今週と先週を同じ長さの期間で比較できる |
| Token control | 生ログを無制限に返さず、集計、`project`、`top` / `take` で絞っている |
| Report scope | Severity、日次推移、MITRE 戦術、製品、送信元/宛先 IP を扱う |
| Findings | 前週比3〜5項目と危険度上位5件を、取得結果の範囲で生成する |
| Grounding | データがない項目を捏造せず「データなし」と示す |
| Safety | 読み取り専用で、秘密情報や環境固有値を埋め込まない |

KQL の `limit` だけに頼らず、先に集計して必要列だけを返しているか確認します。IP ランキングや危険度上位項目には明示的な上限を設け、自由記述の長文をそのまま LLM へ渡さないようにします。

## 9-5. サンプル HTML をレビューする

ブラウザーと Outlook のテストメールで次を確認します。

- 日本語で、`Meiryo, メイリオ, sans-serif` のフォント指定がある
- JavaScript、外部スクリプト、外部フォントを使っていない
- メール本文向けに最大幅がおおむね 600〜700 px に収まる
- 重要な数値と見出しが、画像や JavaScript がなくても読める
- Severity 別比較、日次傾向、カテゴリー分布、IP、要約、上位5件、推奨対策が確認できる
- 動的値を HTML として無条件に解釈せず、エスケープする前提が README に記載されている

> [!NOTE]
> メールクライアントは CSS 対応が異なります。サンプル HTML は見た目だけでなく、インライン CSS またはメールで利用可能な単純な CSS、固定的な本文幅、表形式の崩れにくさを優先します。

## 9-6. Logic Apps 連携とテストを確認する

1. README に必要な Logic Apps の設定値と同一テナント要件が記載されていることを確認します。
2. 分析結果から HTML を作る処理と、メールを送る処理の責務が分かれていることを確認します。
3. [Lab 7](07-logic-apps.md) と同様に、最初は送信無効または承認なしでテストします。
4. 人が宛先と本文を確認した後、講師指定のテスト用メールボックスだけへ送信します。
5. 0 件、大量データ、欠損列を含むケースでも、捏造や無制限出力がないことを確認します。

## チェックポイント

- [ ] Builder 直下にローカル指示書を新規作成し、目的、詳細、レポートイメージ、アウトプットを記述した
- [ ] Copilot にローカル指示書をファイル名で参照させた
- [ ] `Builder/output/<エージェント名>/` に YAML、サンプル HTML、README を生成した
- [ ] Defender の実スキーマを確認し、今週と先週を比較する KQL の件数と列を制限した
- [ ] 日本語、メイリオ、JavaScript なし、メール向け幅を HTML で確認した
- [ ] 週次サマリー、危険度上位5件、推奨対策が根拠の範囲内で生成されることを確認した
- [ ] Logic Apps のテスト送信を承認付き・固定宛先で確認した
