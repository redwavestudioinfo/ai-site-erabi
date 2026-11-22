/* AI SITE ERABI v2: client-only, privacy-conscious guided chooser. */
(function () {
  'use strict';
  const purpose = document.getElementById('purpose');
  const budget = document.getElementById('budget');
  const result = document.getElementById('picker-result');
  if (!purpose || !budget || !result) return;
  const options = {
    wix: {
      title: 'Wixから調べてみよう',
      text: 'AIで土台を作った後、画面上で細かく編集したい人向け。無料プランがありますが、広告表示と独自ドメインの条件は確認してください。',
      detail: '最初に確認：無料プランの機能制限・広告表示・ドメイン'
    },
    jimdo: {
      title: 'Jimdoから調べてみよう',
      text: '質問に答えながらサイトを作る方法が候補。無料プランから始められます。公開後の機能制限と独自ドメインの条件を確認しましょう。',
      detail: '最初に確認：無料プランの機能制限・独自ドメイン'
    },
    lolipop: {
      title: 'ロリポップ！AIホームページを調べてみよう',
      text: 'AIとの会話で作成・修正を進めたい人向け。10日間のお試し後は有料です。月額換算の表示だけでなく、契約期間の支払総額を確認してください。',
      detail: '最初に確認：試用終了後の料金・契約期間・支払総額'
    },
    free: {
      title: 'WixとJimdoの無料プランを比べよう',
      text: '「ずっと無料で公開したい」が最優先なら、無料プランのある2つが検討候補。ロリポップ！AIホームページは無料体験の後、継続利用に料金がかかります。',
      detail: '最初に確認：広告表示・機能制限・独自ドメイン'
    }
  };
  function choose() {
    if (budget.value === 'free') {
      if (purpose.value === 'design') return options.wix;
      if (purpose.value === 'quick') return options.jimdo;
      return options.free;
    }
    if (purpose.value === 'design') return options.wix;
    if (purpose.value === 'quick') return options.jimdo;
    return options.lolipop;
  }
  function render() {
    const item = choose();
    const icon = document.createElement('span');
    icon.className = 'result-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = '✦';
    const title = document.createElement('strong');
    title.textContent = item.title;
    const description = document.createElement('p');
    description.textContent = item.text;
    const detail = document.createElement('p');
    detail.className = 'result-detail';
    detail.textContent = item.detail;
    result.replaceChildren(icon, title, description, detail);
  }
  purpose.addEventListener('change', render);
  budget.addEventListener('change', render);
  render();
})();
