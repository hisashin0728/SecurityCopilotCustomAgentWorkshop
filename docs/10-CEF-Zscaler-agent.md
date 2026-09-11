# Lab 10: CEF から Zscaler ZIA/ZPA の週次異常レポートエージェントを作る

**所要時間:** 45 分
**ゴール:** ローカル指示書を GitHub Copilot に読み込ませ、Microsoft Sentinel に取り込まれた CEF ログから Zscaler ZIA/ZPA の統計と異常傾向を分析し、日本語 HTML/CSS レポートを生成するカスタムエージェント一式を作成する

## こんなケースはありませんか

> 「ZIA と ZPA のログ量やブロック傾向を毎週確認しているが、製品ごとに列の使われ方が違い、異常の根拠をそろえて報告するのが難しい」——CEF の実スキーマと値を先に確認する指示書を用意すると、環境差を踏まえた再利用可能なレポートを作成できます。

この Lab では、要件をまとめたローカル Markdown ファイルを Builder に配置し、その内容を唯一の要件としてカスタムエージェントを生成します。生成された YAML、HTML、README が実環境の CEF マッピングと異常判定の根拠を正しく扱っているか、人が確認するところまでが演習です。

> [!IMPORTANT]
> この演習では Microsoft Sentinel の `CommonSecurityLog` を対象にします。CEF のカスタム列と ZIA/ZPA の識別値は設定やログ種別によって異なるため、列名や `DeviceProduct` の値を推測で確定しません。実データへの接続は読み取り専用とし、メール送信は講師指定のテスト環境で承認後にだけ実施してください。

## 10-1. ローカル指示書を作成する

1. VS Code で `Security Copilot custom plugins builder/Builder` フォルダーを開きます。
2. Explorer で **New File** を選び、Builder のルートに `WeeklyZscalerCEFReport.md` を新規作成します。
3. 作成したファイルへ、次の指示書を入力します。

```markdown
# 目的
- Microsoft Sentinel に取り込まれた Common Event Format (CEF) ログから Zscaler Internet Access (ZIA) と Zscaler Private Access (ZPA) を分析し、週次で SOC/CSIRT 向けの統計および異常傾向レポートを日本語の HTML/CSS で生成する Security Copilot Custom Agent を作成すること

# データソースと事前確認
- Microsoft Sentinel の CommonSecurityLog を読み取り専用で利用すること
- 生成前に Builder のワークフローと利用可能なツールを使い、CommonSecurityLog の実在、利用可能な列、直近のデータ有無を確認すること
- DeviceVendor、DeviceProduct、DeviceEventClassID、DeviceEventCategory、DeviceAction、および CEF カスタム列の Label と値を少量の集計結果で確認し、Zscaler、ZIA、ZPA を識別する条件を根拠とともに提示すること
- ZIA/ZPA の製品識別値、カスタム列の意味、分析対象ログ種別を推測しないこと。不明または複数候補がある場合は、生成前に利用者へ質問すること
- AdditionalExtensions や DeviceCustomString* などを使う場合は、対応する Label を確認し、環境で検証できたマッピングだけを採用すること

# 分析要件
- レポート対象期間は今週と直前の同じ長さの期間とし、期間境界とタイムゾーンをレポートに明記すること
- ZIA と ZPA を分けて、イベント数、許可・ブロック・失敗などのアクション、重要度、イベントカテゴリー、上位の送信元 IP、宛先 IP、宛先ホストまたはアプリケーションを集計すること
- ZIA では、取得できる範囲で Web 通信、脅威またはセキュリティカテゴリー、ブロック動作、宛先を分析すること
- ZPA では、取得できる範囲でプライベートアプリケーションアクセス、接続または認証の成功・失敗、アプリケーション、送信元を分析すること
- ログに存在しない項目は別の列から推測せず「データなし」または「未マッピング」と表示すること
- 今週と前週の件数および比率を比較し、急増、急減、新規出現、ブロック率または失敗率の上昇、重要度の高いイベント集中を異常候補として抽出すること
- 十分な履歴が利用できる場合は、少なくとも過去 28 日の時間単位または日単位の集計から KQL の時系列ベースラインを作成し、異常スコア、実測値、期待値を返すこと。履歴が不足する場合は時系列異常を断定せず「判定不能」とすること
- 異常の有無は「異常あり」「顕著な異常なし」「判定不能」のいずれかで示し、使用した期間、比較値、閾値または異常スコアを根拠として併記すること
- 異常候補は最大 5 件とし、各項目に製品、指標、観測値、比較値または期待値、判定理由を含めること
- 相関を因果関係として断定せず、取得データだけで確認できない内容を生成しないこと

# KQL とトークン制御
- 時間条件と Zscaler の識別条件をクエリの早い段階で適用すること
- 生ログを無制限に返さず、原則として summarize、bin、project、top または take を使って集計・列選択・件数制限を行うこと
- 上位項目は各分類 10 件以内、異常候補の詳細は 5 件以内に制限すること
- URL、メッセージ、AdditionalExtensions などの長い自由記述をそのまま LLM へ渡さないこと
- Security Copilot Custom Agent の LLM (gpt-4o) のトークン制限を考慮し、分析を複数の小さな集計スキルへ分割すること

# レポートイメージ
- レポート概要
  - 対象期間、タイムゾーン、データ最終受信時刻、ZIA/ZPA のデータ有無
  - 総合判定と判定根拠
- 週次サマリー
  - ZIA/ZPA 別イベント数と前週比
  - 許可・ブロック・失敗の件数と比率
- 日次トレンド
  - ZIA/ZPA 別の日次件数
  - 異常スコア、実測値、期待値
- 分布と上位項目
  - 重要度、イベントカテゴリー、アクション
  - 送信元 IP、宛先 IP、宛先ホストまたはアプリケーション
- 異常候補上位 5 件
  - 指標、観測値、比較値または期待値、根拠
- 分析サマリー
  - データに基づく自然言語分析 3〜5 項目
- 推奨対策方針
  - 即時確認すべき点
  - ZIA ポリシーまたは脅威カテゴリーの確認
  - ZPA アクセスポリシーまたは認証・接続経路の確認

# HTML/CSS と通知
- レポートは日本語で生成すること
- JavaScript、外部スクリプト、外部フォント、外部画像を使用しないこと
- フォントは Meiryo, メイリオ, sans-serif を指定すること
- Outlook のメール本文を想定し、最大幅を 600〜700 px として、単純な表とインライン CSS を優先すること
- 色だけに依存せず、異常判定をテキストでも表示すること
- 動的な文字列は HTML エスケープする前提とし、URL、ユーザー、IP などの機密性に配慮すること
- HTML の生成と Logic Apps によるメール送信の責務を分離すること
- メール送信は sendApproved=false を既定とし、人が本文と講師指定の固定宛先を確認した後だけ許可すること

# アウトプット
- Builder/output フォルダにエージェント名でフォルダを作成し、次を生成すること
  - カスタムエージェントの YAML ファイル
  - ダミーデータだけを使用したサンプル HTML
  - README
- README には、確認済みのテーブルと列、ZIA/ZPA の識別条件、CEF カスタム列のマッピング、異常判定方法と閾値、設定値、登録方法、テスト方法、制約、Logic Apps 通知手順を記載すること
- 環境固有 ID、接続情報、メールアドレス、シークレットを埋め込まず、未確定値は明示的なプレースホルダーにすること
```

4. ファイルを保存し、Explorer で次の配置になっていることを確認します。

```text
Builder/
├─ SKILL.md
├─ WeeklyZscalerCEFReport.md
├─ references/
└─ output/
```

5. `WeeklyZscalerCEFReport.md` を開き、目的、データソースと事前確認、分析要件、KQL とトークン制御、レポートイメージ、HTML/CSS と通知、アウトプットの7節があることを確認します。

CEF の標準フィールドは `CommonSecurityLog` の列へマッピングされますが、製品固有フィールドはカスタム列や `AdditionalExtensions` に入ることがあります。そのため、実在するユーザー、完全な URL、IP アドレス、シークレットを指示書へ追記せず、列の意味はサンプルと Label の組み合わせで確認します。

## 10-2. 指示書からエージェントを生成する

Copilot Chat を **Agent** モードにし、Microsoft Sentinel と Security Copilot Agent の Builder が利用するツールを有効にして、次を送ります。

```text
ローカルの WeeklyZscalerCEFReport.md を読み、その指示だけを要件として Security Copilot Custom Agent を作成してください。
Builder のワークフローに従って Microsoft Sentinel の CommonSecurityLog にある利用可能な列と少量の集計結果を確認し、Zscaler、ZIA、ZPA の識別条件および CEF カスタム列の Label と値の対応を確定してください。
製品の識別条件、分析対象ログ種別、期間境界、タイムゾーン、異常判定に必要な履歴または Logic Apps スキル設定が不明な場合は、生成前に質問してください。値や列を推測して補完しないでください。
生成物は指示書で指定された Builder/output 配下へ保存し、最後に検証結果、異常判定の根拠、未確定のプレースホルダーを一覧にしてください。
```

Copilot から質問された場合は、講師が用意した演習環境の値を答えます。特に `DeviceVendor`、`DeviceProduct`、CEF カスタム列の Label、対象タイムゾーンは、実環境の確認結果を優先します。ZIA または ZPA の一方しか取得できない場合は、存在しないデータを補わず、その製品を「データなし」として生成を続けるか講師へ確認します。

## 10-3. スキーマとデータを確認する

生成前の確認結果に、次の情報があることを確認します。

- `CommonSecurityLog` が存在し、直近のデータがある
- `DeviceVendor` と `DeviceProduct` の実際の値から Zscaler ログを識別している
- ZIA と ZPA を分ける値またはログ種別が確認できている
- 時刻、アクション、重要度、カテゴリー、送信元、宛先に使う列が実在する
- `DeviceCustomString*` などを使う場合、対応する `*Label` と値を組み合わせて意味を確認している
- 長い値や個人情報を表示せず、値の種類と件数を少量の集計で確認している

ZIA/ZPA の識別値が空、混在、または一意でない場合は、その状態のまま KQL を固定しません。講師へ対象ログ種別を確認するか、README に未確定のプレースホルダーとして残します。

## 10-4. 出力フォルダーを確認する

生成後、`Builder/output/<エージェント名>/` に次の3ファイルがあることを確認します。ファイル名は Builder の命名規則に従うため、完全一致でなくても構いません。

```text
Builder/output/<エージェント名>/
├─ <エージェント名>.yaml
├─ <エージェント名>-sample.html
└─ README.md
```

- YAML: Sentinel KQL スキル、ZIA/ZPA の集計と異常判定、レポート生成指示、Logic Apps 連携に必要な定義
- HTML: 予約済みの例示用 IP アドレスなど、ダミーデータだけを使った Outlook 向け表示サンプル
- README: スキーマ確認結果、CEF マッピング、異常判定方法、設定値、登録方法、テスト方法、制約、メール通知の手順

> [!CAUTION]
> サンプル HTML に実在するユーザー名、URL、IP アドレス、アプリケーション名、ログ本文を含めません。IP アドレスは `192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24` などの例示用範囲を使用します。

## 10-5. YAML と KQL をレビューする

| 観点 | 合格条件 |
|---|---|
| Data source | Microsoft Sentinel の `CommonSecurityLog` を対象にしている |
| Product filter | 実データで確認した値により Zscaler と ZIA/ZPA を識別している |
| CEF mapping | カスタム列を使う場合、Label と値の対応を確認し README に記録している |
| Time windows | 今週と前週を同じ長さで比較し、期間境界とタイムゾーンが明確である |
| Baseline | 履歴が十分な場合だけ時系列ベースラインを使い、履歴不足時は判定不能とする |
| Token control | 早期フィルター、集計、`project`、`top` / `take` で出力を絞っている |
| Report scope | ZIA/ZPA、アクション、重要度、カテゴリー、送信元/宛先、日次推移を扱う |
| Findings | 異常候補を最大5件とし、観測値、比較値または期待値、判定理由を示す |
| Grounding | データがない項目を捏造せず「データなし」「未マッピング」「判定不能」と示す |
| Safety | 読み取り専用で、秘密情報や環境固有値を埋め込まない |

KQL の `limit` だけに頼らず、先に時間範囲と製品を絞り、集計してから必要列だけを返していることを確認します。時系列異常検知に `series_decompose_anomalies()` などを使う場合は、入力系列の粒度、履歴期間、閾値、実測値、ベースライン、異常スコアがレビューできることを確認します。

## 10-6. サンプル HTML をレビューする

ブラウザーと Outlook のテストメールで次を確認します。

- 日本語で、`Meiryo, メイリオ, sans-serif` のフォント指定がある
- JavaScript、外部スクリプト、外部フォント、外部画像を使っていない
- メール本文向けに最大幅がおおむね 600〜700 px に収まる
- 総合判定が色だけでなくテキストでも読める
- ZIA/ZPA 別の前週比較、日次傾向、アクション、カテゴリー、送信元/宛先、異常候補、推奨対策を確認できる
- 異常候補ごとに観測値、比較値または期待値、判定理由がある
- データ欠損時に「0」と捏造せず「データなし」「判定不能」と表示できる
- 動的値を HTML として無条件に解釈せず、エスケープする前提が README に記載されている

> [!NOTE]
> メールクライアントは CSS 対応が異なります。チャートを JavaScript や外部画像で描画せず、表、数値、単純な横棒など、HTML と CSS だけで意味が伝わる表現を優先します。

## 10-7. 異常判定と Logic Apps 連携をテストする

次のケースを、実データまたは講師が用意したサニタイズ済みデータで確認します。

1. **通常:** 今週と前週に十分なデータがあり、比較値と判定根拠が表示される。
2. **急増:** ブロックまたは接続失敗が増加し、該当製品、指標、観測値、比較値が異常候補に表示される。
3. **データなし:** ZIA または ZPA が0件の場合に、もう一方の値で補完せず「データなし」と表示される。
4. **履歴不足:** ベースラインに必要な履歴がない場合に「判定不能」と表示される。
5. **欠損列:** 想定したカスタム列がない場合に、別の列を推測せず「未マッピング」と表示される。
6. **大量データ:** 生ログを返さず、上位件数と異常候補の上限が守られる。

Logic Apps 連携は [Lab 7](07-logic-apps.md) と同様に、最初は `sendApproved=false` でテストします。人が HTML 本文、異常判定の根拠、講師指定の固定宛先を確認した後だけ `sendApproved=true` とし、テスト用メールボックスへ送信します。

## チェックポイント

- [ ] Builder 直下に `WeeklyZscalerCEFReport.md` を作成し、指定された7節を記述した
- [ ] Copilot にローカル指示書をファイル名で参照させた
- [ ] `CommonSecurityLog` の実スキーマと少量の集計結果を生成前に確認した
- [ ] Zscaler、ZIA、ZPA の識別条件と CEF カスタム列の Label 対応を確認した
- [ ] `Builder/output/<エージェント名>/` に YAML、サンプル HTML、README を生成した
- [ ] 今週と前週の比較、および履歴が十分な場合の時系列ベースラインを確認した
- [ ] 異常の根拠と「異常あり」「顕著な異常なし」「判定不能」の区別を確認した
- [ ] KQL の時間範囲、列、集計結果、上位件数が制限されていることを確認した
- [ ] 日本語、メイリオ、JavaScript なし、メール向け幅を HTML で確認した
- [ ] Logic Apps のテスト送信を承認付き・固定宛先で確認した

## 参考資料

- [CEF and CommonSecurityLog field mapping](https://learn.microsoft.com/azure/sentinel/cef-name-mapping)
- [Ingest syslog and CEF messages to Microsoft Sentinel with the Azure Monitor Agent](https://learn.microsoft.com/azure/sentinel/connect-cef-syslog-ama)
- [CEF via AMA data connector - Configure specific appliance or device for Microsoft Sentinel data ingestion](https://learn.microsoft.com/azure/sentinel/unified-connector-cef-device)
- [KQL anomaly detection and forecasting](https://learn.microsoft.com/kusto/query/anomaly-detection)
- [`series_decompose_anomalies()`](https://learn.microsoft.com/kusto/query/series-decompose-anomalies-function)