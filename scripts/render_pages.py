"""Render checked editorial pages. No external dependencies or AI hallucinated copy."""
from pathlib import Path
from datetime import date
from html import escape

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
DATE='2026年11月22日'

NAV=[('index.html','ホーム'),('compare.html','サービス比較'),('guide.html','作り方ガイド'),('about.html','運営方針')]

def page(title, description, body, *, active='', article=False):
    links=''.join(f'<a href="/{p}"'+(' aria-current="page"' if p==active else '')+f'>{label}</a>' for p,label in NAV)
    return f'''<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{escape(description,quote=True)}">
<title>{escape(title)}</title>
<meta name="robots" content="index,follow"><meta name="theme-color" content="#123044">
<link rel="stylesheet" href="/assets/styles.css">
<meta name="google-site-verification" content="gdwm3uodac9SUT8E0ySPk1PbU5tpjHOP52BWKDZ4WbQ" />
</head><body><a class="skip" href="#main">本文へ移動</a>
<header class="masthead"><div class="wrap header-inner"><a class="logo" href="/">AIサイト<span>選び</span></a><nav class="nav" aria-label="メインナビゲーション">{links}</nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="footer-links"><a href="/compare.html">サービス比較</a><a href="/guide.html">作り方ガイド</a><a href="/about.html">運営方針</a><a href="/privacy.html">プライバシーポリシー</a></div><small>© 2026 AIサイト選び｜公式情報から条件を整理する独立メディア。広告リンクは「PR・広告」と明示しています。</small></div></footer>
<script src="/assets/app.js" defer></script></body></html>'''

def heading(kicker,title,desc):
    return f'<section class="pagehead"><div class="wrap"><div class="kicker">{kicker}</div><h1>{title}</h1><p>{desc}</p></div></section>'

def sources(items):
    return '<section class="subtle-box"><strong>参照した公式情報</strong><ul class="sources">'+''.join(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a></li>' for label,url in items)+'</ul><p class="aside">確認日：'+DATE+'。価格・機能は変更される場合があります。申込前に必ず各公式サイトでご確認ください。</p></section>'

SRC=[('ロリポップ！AIホームページ公式','https://lolipop.jp/ai/homepage/'),('Wix公式のAIサイト作成ガイド','https://ja.wix.com/blog/2026/09/how-to-use-wix-ai-website-builder'),('Jimdo日本語公式','https://www.jimdo.com/jp/'),('Jimdo公式料金表','https://www.jimdo.com/jp/pricing/')]

home=f'''
<section class="hero hero-v2"><div class="wrap hero-grid">
  <div class="hero-copy">
    <p class="eyebrow"><span class="eyebrow-dot" aria-hidden="true"></span> AI WEBSITE GUIDE <span class="eyebrow-year">2026</span></p>
    <h1>AIでホームページ。<br><span class="gradient-text">自分に合う作り方、<br>ここで見つけよう。</span></h1>
    <p class="hero-lead">「無料で公開したい」「とにかく簡単がいい」「デザインもこだわりたい」。<br>あなたの目的から、AIホームページ作成サービスの違いをわかりやすく整理します。</p>
    <div class="actions"><a href="#choose" class="btn btn-primary">30秒で候補を探す <span aria-hidden="true">→</span></a><a href="#services" class="btn btn-ghost">3つのサービスを見る</a></div>
    <p class="hero-proof"><span aria-hidden="true">✓</span> 公式情報に基づく比較　 <span aria-hidden="true">✓</span> 無料と有料の違いも説明</p>
  </div>
  <div class="hero-visual" aria-hidden="true">
    <div class="browser-preview">
      <div class="browser-toolbar"><span class="window-dots"><i></i><i></i><i></i></span><span class="browser-address">AI SITE ERABI / FINDER</span><span class="browser-menu">•••</span></div>
      <div class="browser-inner"><div class="browser-intro">WHAT MATTERS MOST?</div><div class="browser-title">あなたはどのタイプ？</div>
        <div class="browser-option"><span class="option-emoji">◈</span><span>できるだけ無料で</span><span class="option-check">✓</span></div>
        <div class="browser-option muted-option"><span class="option-emoji">✳</span><span>直感的に編集したい</span><span>↗</span></div>
        <div class="browser-option muted-option"><span class="option-emoji">✦</span><span>会話しながら作りたい</span><span>↗</span></div>
        <div class="browser-preview-bottom"><span class="progress-lines"><b></b><b></b><b></b></span><span>あなたに合う選び方へ →</span></div>
      </div>
    </div>
    <span class="float-chip float-a">無料プランを比較</span><span class="float-chip float-b">料金の落とし穴もチェック</span>
  </div>
</div></section>
<div class="trust-strip"><div class="wrap trust-strip-inner"><span>迷ったら、ここから。</span><span>01 <strong>無料・有料を整理</strong></span><span>02 <strong>用途別に候補を提案</strong></span><span>03 <strong>契約前の注意点を確認</strong></span></div></div>
<section class="section choose-section" id="choose"><div class="wrap">
  <div class="section-heading"><p class="kicker">01 / QUICK FINDER</p><h2>まずは、あなたの希望を教えて。</h2><p>質問は2つだけ。条件に合いそうなサービスの<strong>調べ始める候補</strong>を提案します。</p></div>
  <div class="picker picker-v2"><div class="picker-left">
      <div class="step-label">QUESTION 01 <span>なにを重視する？</span></div>
      <label class="select-label" for="purpose">ホームページの作り方<select id="purpose"><option value="simple">AIと会話して進めたい</option><option value="design">デザインを自分で調整したい</option><option value="quick">質問に答えて土台を作りたい</option></select></label>
      <div class="step-label step-label-second">QUESTION 02 <span>予算のイメージは？</span></div>
      <label class="select-label" for="budget">利用料金<select id="budget"><option value="free">ずっと無料で公開できる候補がいい</option><option value="paid">必要なら有料でもOK</option></select></label>
      <p class="aside picker-caveat">※診断結果は公式に公開された特徴を整理した参考情報であり、実際の使用感・品質の順位ではありません。</p>
    </div>
    <div class="picker-right"><span class="result-chip">YOUR STARTING POINT</span><div class="picker-result" id="picker-result" aria-live="polite" aria-atomic="true"><span class="result-icon" aria-hidden="true">✦</span><strong>あなた向けの候補</strong><p>条件を選ぶと、候補と確認ポイントが表示されます。</p></div><a class="result-more" href="/compare.html">3サービスの詳しい比較を見る <span aria-hidden="true">↗</span></a></div>
  </div>
</div></section>
<section class="section section-alt" id="services"><div class="wrap">
  <div class="section-heading split"><div><p class="kicker">02 / CHOOSE YOUR STYLE</p><h2>3つのサービス、<br>違いは「作り方」と「料金」。</h2><p>一番高いものが正解とは限りません。まずは自分の優先順位から選びましょう。</p></div><a class="section-text-link" href="/compare.html">すべての条件を比較する ↗</a></div>
  <div class="service-grid">
    <article class="service-card service-free"><div class="service-top"><span class="service-symbol symbol-wix">W</span><span class="service-label">無料で公開したい人</span></div><h3>Wix</h3><p class="service-subtitle">AIで土台を作って、自分で細かく編集</p><div class="service-highlight"><strong>無料プランあり</strong><span>独自ドメインは有料</span></div><ul><li>画面上で細かな編集が可能</li><li>無料プランには広告表示</li><li>デザインを自分で直したい人向け</li></ul><a class="service-link" href="https://ja.wix.com/" target="_blank" rel="noopener noreferrer">公式サイトで確認 <span aria-hidden="true">↗</span></a></article>
    <article class="service-card service-quick"><div class="service-top"><span class="service-symbol symbol-jimdo">J</span><span class="service-label">質問から手軽に始めたい人</span></div><h3>Jimdo</h3><p class="service-subtitle">質問に答えながらサイトの土台を作成</p><div class="service-highlight"><strong>無料プランあり</strong><span>独自ドメインは有料</span></div><ul><li>質問回答型の作成フロー</li><li>無料プランで試せる</li><li>公開後の機能制限は要確認</li></ul><a class="service-link" href="https://www.jimdo.com/jp/" target="_blank" rel="noopener noreferrer">公式サイトで確認 <span aria-hidden="true">↗</span></a></article>
    <article class="service-card service-chat"><div class="service-top"><span class="service-symbol symbol-loli">L</span><span class="service-label">会話しながら作りたい人</span></div><h3>ロリポップ！<br>AIホームページ</h3><p class="service-subtitle">AIとの会話で作成・修正を進める</p><div class="service-highlight"><strong>10日間お試し</strong><span>継続利用は有料</span></div><ul><li>AIとの対話で構成を作る</li><li>長期契約は一括払い</li><li>月額660円〜は36か月契約時</li></ul><a class="service-link" href="https://lolipop.jp/ai/homepage/" target="_blank" rel="noopener noreferrer">公式サイトで確認 <span aria-hidden="true">↗</span></a></article>
  </div>
  <div class="ad-inline"><span class="ad-inline-badge">PR・広告</span><div><strong>ロリポップ！AIホームページを詳しく見る</strong><p>A8.netの広告リンクです。申込前に契約期間・支払総額を確認してください。</p><a href="https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E" rel="nofollow">質問に答えるだけ！AIが最短10分でサイト完成【ロリポップ！AIホームページ】</a><img border="0" width="1" height="1" src="https://www19.a8.net/0.gif?a8mat=4BGR8X+DJM182+348+4SNX5E" alt=""></div></div>
  <p class="aside service-disclaimer">※サービスの利用体験に基づくランキングではありません。各サービスの詳しい条件は公式サイトをご確認ください。広告リンクと通常の公式リンクは別に表示しています。</p>
</div></section>
<section class="section" id="quick-compare"><div class="wrap">
  <div class="section-heading"><p class="kicker">03 / AT A GLANCE</p><h2>迷ったら、この4項目を比べよう。</h2><p>料金の安さだけでなく、公開後の使い方まで考えるのがポイント。</p></div>
  <div class="compare-preview"><div class="table-scroll"><table><caption class="aside">公式情報をもとに整理／2026年11月確認</caption><thead><tr><th scope="col">比較項目</th><th scope="col">Wix</th><th scope="col">Jimdo</th><th scope="col">ロリポップ！AI</th></tr></thead><tbody>
    <tr><th scope="row">無料公開</th><td><span class="table-positive">無料プランあり</span></td><td><span class="table-positive">無料プランあり</span></td><td>10日間の試用</td></tr>
    <tr><th scope="row">作り方</th><td>AI＋画面編集</td><td>質問に回答</td><td>AIと会話</td></tr>
    <tr><th scope="row">独自ドメイン</th><td>有料プラン</td><td>有料プラン</td><td>契約条件を確認</td></tr>
    <tr><th scope="row">料金の注意点</th><td>無料版は広告表示</td><td>無料版は機能制限</td><td>長期契約は一括払い</td></tr>
  </tbody></table></div><a href="/compare.html" class="compare-bottom-link">詳しい比較表・料金条件を見る <span aria-hidden="true">→</span></a></div>
</div></section>
<section class="section section-soft" id="how-to"><div class="wrap">
  <div class="section-heading"><p class="kicker">04 / BEFORE YOU DECIDE</p><h2>「無料」の前に、<br>知っておきたいこと。</h2><p>契約前に知っておけば、あとで困りにくくなる4つのチェック。</p></div>
  <div class="feature-tiles"><article><span>01</span><h3>無料体験と無料プランは別</h3><p>期間終了後に有料となるサービスと、制限付きで無料公開できるサービスは違います。</p></article><article><span>02</span><h3>月額表示と支払総額</h3><p>「月額○円〜」でも長期契約の一括払いになる場合があります。</p></article><article><span>03</span><h3>ドメインの更新費用</h3><p>初年度無料でも、次年度以降の維持費がかかる可能性があります。</p></article><article><span>04</span><h3>乗り換えやすさ</h3><p>HTML・画像・記事を別サービスへ移せるか、事前に確認しましょう。</p></article></div>
</div></section>
<section class="section" id="learn"><div class="wrap">
  <div class="section-heading"><p class="kicker">05 / LEARN MORE</p><h2>もう少し詳しく知りたい人へ。</h2></div>
  <div class="learn-grid"><a href="/articles/free-vs-trial.html"><span class="learn-icon">¥</span><span class="learn-caption">お金のはなし</span><strong>「無料」と「無料体験」は何が違う？</strong><span class="learn-arrow">続きを読む ↗</span></a><a href="/guide.html"><span class="learn-icon">✳</span><span class="learn-caption">初めての制作</span><strong>AIでホームページを作る7ステップ</strong><span class="learn-arrow">続きを読む ↗</span></a><a href="/compare.html"><span class="learn-icon">≡</span><span class="learn-caption">サービス比較</span><strong>Wix・Jimdo・ロリポップの違い</strong><span class="learn-arrow">続きを読む ↗</span></a></div>
</div></section>
<section class="section faq-section"><div class="wrap faq-layout"><div><p class="kicker">FAQ</p><h2>よくある疑問</h2><p class="muted">気になる点は、公式の契約条件もあわせて確認してください。</p></div><div class="faq"><details><summary>完全無料でホームページを公開できる？</summary><p>WixとJimdoには無料プランがあります。ただし広告表示や機能制限があります。独自ドメインを使うには有料プランが必要です。</p></details><details><summary>AIだけでホームページは完成する？</summary><p>AIで土台を作れますが、文章・画像の正確性、連絡先、法的な表示、料金条件などは公開前に確認しましょう。</p></details><details><summary>どのサービスが一番いいの？</summary><p>目的によって変わります。無料公開を続けたいか、編集自由度を重視するか、会話で作りたいかを基準に選んでください。未使用サービスに順位は付けていません。</p></details></div></div></section>
<section class="closing-section"><div class="wrap closing-inner"><div><p class="kicker">START HERE</p><h2>最初の一歩を、<br>もっとシンプルに。</h2><p>まずは条件を整理するだけでOK。契約するのは、そのあと。</p></div><a class="btn btn-primary" href="#choose">自分に合う候補を探す →</a></div></section>
<section class="wrap transparency-section"><h2>比較の方針と広告について</h2><p>このサイトは公式情報をもとに条件を整理する独立メディアです。サービスを実際に使用した体験レビューではありません。一部にA8.net経由の成果報酬型広告があり、「PR・広告」と明記しています。広告の有無は掲載順を決める基準ではありません。<a href="/about.html">運営方針を見る</a></p></section>
'''

(SITE/'index.html').write_text(page('AIホームページ作成ツール比較｜無料で作れる？3サービスの選び方｜AIサイト選び','AIでホームページを作りたい初心者へ。Wix・Jimdo・ロリポップ！AIホームページの無料プラン、料金、編集方法を比較。2問で候補を探せます。',home,active='index.html'),encoding='utf-8')

compare=heading('COMPARE','AIホームページ作成ツール比較','最初から「おすすめ順位」を決めず、公式情報で確認できた条件を横並びに整理しました。')+'''
<section class="wrap section"><p class="kicker">比較表</p><h2>無料でどこまで使える？</h2>
<p class="muted">まずは次の3つの違いから確認。自分にとって外せない条件を決めると、選びやすくなります。</p>
<div class="compare-highlights">
 <div><span class="mini-number">01</span><h3>無料で公開を続けたい</h3><p>Wix・Jimdoには無料プランあり。広告表示や制限を確認。</p></div>
 <div><span class="mini-number">02</span><h3>自分で細かく直したい</h3><p>WixはAIによる土台作りの後も、画面上で編集可能。</p></div>
 <div><span class="mini-number">03</span><h3>会話で作りたい</h3><p>ロリポップは10日間試用可能。継続は有料なので支払総額を確認。</p></div>
</div>
<p class="scroll-hint">↔ 表は横にもスクロールできます（スマートフォン）</p><div class="table-scroll"><table><caption class="aside">公式情報に基づく比較／2026年11月22日確認</caption><thead><tr><th>項目</th><th>ロリポップ！AIホームページ</th><th>Wix（Harmony）</th><th>Jimdo（AIビルダー）</th></tr></thead><tbody>
<tr><th scope="row">無料利用</th><td>10日間のお試し</td><td>無料プランあり</td><td>無料プランあり</td></tr>
<tr><th scope="row">AIでの作り方</th><td>AIと会話して制作・修正</td><td>AIで作成後に画面上で編集</td><td>質問に回答して土台を作成</td></tr>
<tr><th scope="row">独自ドメイン</th><td>長期契約向けの初年度特典あり（条件付き）</td><td>有料プランが必要</td><td>有料プランが必要</td></tr>
<tr><th scope="row">費用の注意点</th><td>月額660円〜は36か月契約の場合。長期契約は一括払い</td><td>無料プランには広告表示。独自ドメインには有料契約が必要</td><td>無料プランの制限、独自ドメイン利用条件を要確認</td></tr>
<tr><th scope="row">おすすめの検討場面</th><td>会話中心でサイトを作りたいとき</td><td>デザインを自分で細かく調整したいとき</td><td>質問に答える方式で進めたいとき</td></tr>
<tr><th scope="row">公式リンク</th><td><a href="https://lolipop.jp/ai/homepage/" target="_blank" rel="noopener noreferrer">ロリポップ！</a></td><td><a href="https://ja.wix.com/" target="_blank" rel="noopener noreferrer">Wix</a></td><td><a href="https://www.jimdo.com/jp/" target="_blank" rel="noopener noreferrer">Jimdo</a></td></tr>
</tbody></table></div><p class="aside">比較表の「おすすめの検討場面」は編集上の目安であり、使用感を試験した評価ではありません。</p><aside class="notice" aria-label="広告"><p><strong>PR・広告｜ロリポップ！AIホームページ</strong></p><p>以下はA8.net経由の広告リンクです。契約条件は申込先でご確認ください。</p><p><a href="https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E" rel="nofollow">質問に答えるだけ！AIが最短10分でサイト完成【ロリポップ！AIホームページ】</a></p>
<img border="0" width="1" height="1" src="https://www19.a8.net/0.gif?a8mat=4BGR8X+DJM182+348+4SNX5E" alt=""></aside>
<h2>「月額660円〜」でいくら払う？</h2><p>ロリポップ！AIホームページの月額660円は、公式の36か月契約の月額換算です。36か月分の料金の合計は <strong>660円 × 36か月 = 23,760円（税込）</strong>。表示上の月額だけで判断せず、契約時にいくら必要か確認しましょう。</p><p>12か月以上のプランには独自ドメイン初年度無料の対象条件がありますが、更新後の費用も考慮してください。</p>
<div class="notice">ここではサービスの料金比較を目的としています。どのサービスも、必要な機能・予算・移行条件によって適切さが変わります。</div>
<h2>比較するときの順番</h2><ol class="feature-steps"><li><strong>無料で公開する必要があるか</strong><p>必要なら無料プランが存在するサービスから確認。</p></li><li><strong>AIで作った後の編集方法を確認する</strong><p>会話、ドラッグ＆ドロップ、フォーム入力のどれが向いているか。</p></li><li><strong>独自ドメインと更新費用を見る</strong><p>サブドメインで十分か、本格運用に向けて独自ドメインが必要か。</p></li><li><strong>将来の乗り換えを想定する</strong><p>移行できる範囲はサービスによって異なり、実装状況も変化します。</p></li></ol>
'''+sources(SRC)+'</section>'
(SITE/'compare.html').write_text(page('AIホームページ比較表｜ロリポップ・Wix・Jimdo｜AIサイト選び','AIサイト作成サービスの無料枠、独自ドメイン、編集方法、支払い条件を比較します。',compare,active='compare.html'),encoding='utf-8')

guide=heading('BEGINNER GUIDE','AIでホームページを作る7ステップ','最初の操作よりも「公開後に困らないこと」を重視した手順です。')+'''
<section class="wrap section article"><h2>まずは何を作りたいか決める</h2><p>AIにホームページを作らせる前に、用途を1つに絞ってください。店舗の案内、プロフィール、問い合わせ窓口、イベント告知では必要なページが違います。</p><ol class="feature-steps"><li><strong>目的を1行で書く</strong><p>例：「個人レッスンの内容・料金・問い合わせ方法を伝える」</p></li><li><strong>最低限の情報を集める</strong><p>名前、サービス内容、実際の料金、営業時間・対応範囲、写真、連絡方法を用意。</p></li><li><strong>無料条件を確認してツールを選ぶ</strong><p>試用期間なのか、期限なく無料公開できるプランなのかを区別する。</p></li><li><strong>AIでページの土台を作る</strong><p>見出しと文章の初稿を生成させる。連絡先や価格など事実は自分で入力する。</p></li><li><strong>スマホ画面を確認する</strong><p>文字の大きさ、押しやすいボタン、フォームの動作、画像表示を確認する。</p></li><li><strong>規約・画像・個人情報の扱いを確認する</strong><p>使ってよい写真か、問い合わせで取得する個人情報をどう扱うか確認する。</p></li><li><strong>公開して更新する</strong><p>公開後に修正できる操作を理解してから、ドメインや有料プランを検討する。</p></li></ol>
<h2>AIに入力する指示文の例</h2><div class="subtle-box"><p>個人レッスンの紹介ページを作ってください。目的は初めて訪れた人が内容と料金を理解し、問い合わせしやすくすることです。ページには「サービス内容」「料金」「よくある質問」「問い合わせ」を入れてください。料金や資格などの事実は推測せず、未入力の場所を残してください。スマートフォンでも読みやすくしてください。</p></div><p class="aside">この指示文はサイト運営者が作った例文であり、特定ツールでの出力を保証するものではありません。</p>
<h2>公開前チェック</h2><ul><li>電話番号・メールアドレス・料金を正しく記載したか</li><li>自分が権利を持たない画像や文章を無断利用していないか</li><li>無料プランにサービス提供者の広告が表示されるか</li><li>独自ドメインを使う場合、毎年の更新費用を確認したか</li><li>スマートフォンから問い合わせできるか</li></ul>
'''+sources(SRC)+'</section>'
(SITE/'guide.html').write_text(page('AIでホームページを作る7ステップ｜初心者向け｜AIサイト選び','AIでホームページを作りたい初心者向け。作成前の準備から公開前の確認まで7つの手順を解説。',guide,active='guide.html'),encoding='utf-8')

free=heading('COST GUIDE','無料プランと無料体験の違い','サービス選びで迷いやすい「無料」の意味と、実際の支払額を整理します。')+'''
<section class="wrap section article"><h2>「ずっと無料」と「最初だけ無料」は違う</h2><p>無料プランとは、機能制限などがあるものの無料で使い続けられる利用形態です。無料体験は、一定期間だけ有料機能を試す仕組みです。サービスによって、公開機能や期限、広告表示、独自ドメイン接続が異なります。</p>
<div class="table-scroll"><table><thead><tr><th>確認項目</th><th>無料プラン</th><th>無料体験</th></tr></thead><tbody><tr><th scope="row">利用期間</th><td>提供条件が続く限り利用可能</td><td>期限が定められる</td></tr><tr><th scope="row">機能制限</th><td>機能・容量・広告表示等に制限の可能性</td><td>体験期間中は有料相当の機能が使える場合もある</td></tr><tr><th scope="row">期限後</th><td>無料の制限内で継続できる場合がある</td><td>課金・利用停止などの条件を確認する</td></tr></tbody></table></div>
<h2>具体例</h2><ul><li><strong>ロリポップ！AIホームページ：</strong> 10日間のお試し。継続利用は有料。月額660円〜は36か月契約時の月額換算で、36か月合計は23,760円（税込）。</li><li><strong>Wix：</strong> 無料プランで作成・公開できるが、Wixの広告が表示される。独自ドメイン接続には有料プランが必要。</li><li><strong>Jimdo：</strong> 無料プランから開始できる。独自ドメイン利用には有料プランの条件がある。</li></ul>
<h2>無料で始める前に確認しておくこと</h2><ol><li>独自ドメインの有無・更新料</li><li>登録時にクレジットカードが必要か</li><li>試用期間の終了後にどうなるか</li><li>バックアップや他サービスへの移行方法</li><li>問い合わせフォームや商用利用の条件</li></ol><div class="notice">有料プランへ変更する前に、申込画面に表示される初回支払額と更新時の条件を確認してください。</div>
'''+sources(SRC)+'</section>'
(SITE/'articles/free-vs-trial.html').write_text(page('無料プランと無料体験の違い｜AIホームページ作成｜AIサイト選び','AIホームページ作成サービスの無料プランと無料体験、独自ドメインの追加費用を解説。',free),encoding='utf-8')

about=heading('ABOUT','このサイトの運営方針','「AIで簡単に作れる」の先にある、運用・費用・移行条件まで整理することを目指します。')+'''
<section class="wrap section article"><h2>サイトについて</h2><p>AIサイト選びは、AIでホームページを作りたい初心者向けに、サービス選択に必要な条件を公式情報から整理する独立した情報サイトです。運営名義は「AIサイト選び編集部」（仮称）です。現在は試験公開中です。</p>
<h2>編集方針</h2><ul><li>公式サイトや公式ヘルプへの参照リンクを示します。</li><li>実際に使用していないサービスの体験レビューは掲載しません。</li><li>料金・機能の更新チェックを自動化し、確認できない項目は断定しません。</li><li>AIを使って文章案を作成する場合も、出典確認を通過した情報だけを公開します。</li><li>広告の有無をサービスの優劣の根拠にしません。</li></ul>
<h2>広告と利益相反</h2><p>提携が承認された広告リンクは該当ページで「PR・広告」と表示しています。対象リンク経由の契約が成果条件を満たした場合、運営者に成果報酬が発生することがあります。広告の有無は比較内容の評価基準に含めません。</p>
<h2>運営への連絡</h2><p>現在は試験公開中で、問い合わせ窓口を準備しています。個人情報を含む内容を公開コメントなどに投稿しないでください。</p><div class="notice">問い合わせ窓口の設置後、このページで案内します。</div>
</section>'''
(SITE/'about.html').write_text(page('運営方針・広告について｜AIサイト選び','サイトの運営・広告方針。公開情報の参照、AIによる下書き、アフィリエイト掲載の基準を説明。',about,active='about.html'),encoding='utf-8')

privacy=heading('PRIVACY','プライバシーポリシー','本サイトにおけるデータの取得と外部リンクの扱いについて。')+'''
<section class="wrap section article"><h2>閲覧時の情報</h2><p>現時点では独自のアクセス解析タグを設置していません。一部ページにはA8.netの成果報酬型広告リンクと計測用の1×1画像タグがあります。広告配信事業者やリンク先がCookie等の技術を利用する場合があります。また、配信事業者（ホスティングサービス）はセキュリティ・運用上必要なアクセスログを取得する場合があります。</p>
<h2>外部サイトへのリンク</h2><p>サービスの公式サイトまたは広告リンクに移動した場合、移動先および広告配信事業者が定めるプライバシーポリシーも適用されます。広告リンクは「PR・広告」と明示します。</p>
<h2>お問い合わせ</h2><p>現在、問い合わせ窓口を準備しています。このサイトには個人情報を入力するフォームはありません。</p>
<h2>改定について</h2><p>サイトの機能、解析・広告タグの利用状況が変わった場合は内容を見直します。最終更新：2026年11月22日。</p></section>'''
(SITE/'privacy.html').write_text(page('プライバシーポリシー｜AIサイト選び','AIサイト選びのプライバシーポリシー。データ取得と外部リンクの扱いを記載。',privacy),encoding='utf-8')

print('Generated',len(list(SITE.rglob('*.html'))),'HTML pages')
