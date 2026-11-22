# AIサイト選び v1.0 — 0円AIアフィリエイト実験

2026-11-22 時点で確認できた公式情報から作った静的な比較サイトです。
ロリポップ！AIホームページ、Wix、Jimdoの条件を紹介します。
**実際の広告成果、アクセス、収益はまだありません。**

## この配布版でできること
- 7つの日本語HTMLページ（トップ／比較／ガイド／無料と有料の違い／運営／個人情報／404）
- 30秒の用途別ツール候補表示（JavaScript、追跡なし）
- 5つの公式情報ページの週1回の変更監視（GitHub Actions）
- 必要ならGemini APIの無料枠で記事の「未検証の下書き」を週1回だけ作成（GitHub Actions artifact保存）
- Cloudflare Pagesの無料プランで公開可能な静的サイト一式
- 内部リンクや未承認の広告URLをチェックするテスト
- `SITE_URL`が設定されればサイトマップ、canonical、robots.txtを生成

## 0円のための重要ルール
- 有料API・有料プラン・独自ドメインは**契約しない**。Cloudflareの`*.pages.dev`を使う。
- Geminiを使う場合、**有料課金を紐付けない無料枠のAI Studio APIキー**のみを使う。キー未設定なら処理を停止。
- AI記事は未検証のまま**自動公開しない**。新記事の生成は公開の保証ではない。
- 未承認広告の計測URLを勝手に作らない。利用中の広告リンクはA8.net発行済みの素材ID001のみ。
- サイト上の一部にA8.netの提携済み広告リンクを掲載。広告リンクは「PR・広告」を明示し、通常の公式リンクと区別している。
- 記事内容・運営者問い合わせ先は一般公開前に最終確認が必要。

## GitHub／Cloudflare Pagesで公開する手順

### 1. GitHubで新しい空の「Public」リポジトリを作る
1. https://github.com/new にアクセス。
2. Repository name に `ai-site-erabi`、Visibility を `Public` にする。
3. 新しいリポジトリを作成（初期README、.gitignoreなどは作成しなくてよい）。
4. **このフォルダの中身**をGitHubにアップロード。`index.html`ではなく、ルートの`site/`, `scripts/`, `data/`, `.github/`などを含める。
5. Actionsを有効化。リポジトリの`Settings > Actions > General`で必要な権限を確認。

※ChatGPT上でこのリポジトリが作成・アクセス可能になれば、以降のファイル登録はGitHub連携で実行できる場合があります。

### 2. Cloudflare Pagesの無料公開先を作る
1. https://dash.cloudflare.com/ で無料アカウントにログイン。
2. Workers & Pages から Pages を作成し、GitHub連携で `ai-site-erabi` を選ぶ。
3. Framework preset は `None`。
4. Build command は `python scripts/build_site.py`。
5. Build output directory は `dist`。
6. 初回デプロイで `https://＜プロジェクト名＞.pages.dev` の公開URLが発行される。
7. Pagesの設定で環境変数 `SITE_URL` にその**公開URL全体**を設定し、再デプロイする（サイトマップ生成）。
8. Pagesの環境変数 `CONTACT_URL` に、GitHubリポジトリのIssuesなど自分が管理する問い合わせ窓口の`https://` URLを設定し、再デプロイする。
9. 実際のサイトを開き、スマートフォン表示とすべてのリンクを確認。

Cloudflare Pagesは無料枠・ビルド上限の範囲で運用。枠を超えそうなら無料運用を停止して見直す。

### 3. GitHub Actionsを有効にする
- `Test static site` はpush時に自動でHTML・リンクを検査する。
- `Weekly official-source monitor` は毎週月曜06:41（日本時間）に公式ページ変更を確認し、`data/last-check.md` と `data/source-state.json` を更新する。
- `Optional weekly AI editorial draft` は毎週水曜07:31（日本時間）に記事の**下書き**を作る（キー未設定の場合は自動スキップ）。
- GitHubの仕様上、公開リポジトリで活動が60日間ないとスケジュールワークフローが無効化される場合がある。

### 4. Geminiの無料APIキーを使う場合（任意）
1. https://aistudio.google.com/ で無料利用可能なプロジェクト・モデルを確認。
2. 課金先を有効にしない。`gemini-3.5-flash-lite` の無料枠が利用可能なことを確認。
3. GitHub repo `Settings > Secrets and variables > Actions` に `GEMINI_API_KEY` を新規登録。
4. 毎週1件の下書きだけ生成。本文はGitHub ActionsのArtifactとして**14日間**保存する。
5. 自動で公開はされず、公式情報で事実を確認してからページへ反映する。

**ChatGPTにAPIキーを貼り付けない。** Geminiの無料枠・対応モデルは変わることがある。

### 5. ASP広告を設置する場合
1. 無料のA8.net（https://www.a8.net/）に本人名義で登録。
2. ロリポップ！AIホームページの案件を探して提携を申請。
3. 審査が承認されてから、A8.netが正式に発行するリンクをサイト内の通常リンクと差し替える。
4. 該当ページの冒頭、広告リンクの近くに**広告・PR**を明示し、`rel="sponsored noopener noreferrer"`を設定する。
5. ASPの広告主条件、自己申込の禁止事項、商標への広告出稿禁止を確認する。
6. ASPの管理画面で成果を確認。APIなどで確実に取得できない売上をシステムが推計して実績扱いしない。

### 6. 正式公開前の必須チェック
- 環境変数 `CONTACT_URL` に運営者の連絡窓口を設定すること。
- 運営方針・プライバシー・広告表示を、自分の公開・計測実態に合わせて更新すること。
- 料金・特典を各サービスの公式ページで再確認すること。
- 正式に提携した案件以外の広告URLを載せないこと。

## ローカルでのテスト
```
python scripts/render_pages.py
python -m unittest discover -s tests -v
python scripts/build_site.py
python -m http.server 8000 --directory dist
```
開いたら http://localhost:8000/ で確認できます。

## 仕組みの制約
- GitHubのリポジトリ新規作成／Cloudflareへのログインと連携／ASP本人確認は、外部アカウント側の操作が必要。
- source monitorはHTML文字列の変化を検出するだけ。変化が料金変更かどうかは**人間の判断**が必要。
- 提携審査や収益発生は保証されない。アクセス0・報酬0の可能性もある。
- すべてのサイト運用・AI生成を無人で行いながら、情報の正確性も保証することはできない。

## 参考リンク
- https://lolipop.jp/ai/homepage/
- https://lolipop.jp/ai/homepage/affiliate/
- https://ja.wix.com/blog/2026/09/how-to-use-wix-ai-website-builder
- https://www.jimdo.com/jp/
- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows
- https://ai.google.dev/gemini-api/docs/pricing