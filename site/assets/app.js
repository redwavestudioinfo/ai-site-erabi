(function () {
  'use strict';
  const purpose = document.getElementById('purpose');
  const budget = document.getElementById('budget');
  const result = document.getElementById('picker-result');
  if (!purpose || !budget || !result) return;
  const candidates = {
    free: { title: 'まずはWixかJimdoの無料プランから', text: '無料公開を優先するなら、Wix・Jimdoの公式サイトで制限を確認してください。独自ドメインには有料プランが必要です。' },
    simple: { title: 'ロリポップ！AIホームページを確認', text: 'AIとの会話でサイトを作成する候補。10日間のお試しがあります。継続利用は有料で、契約期間ごとの支払額を必ず確認してください。' },
    design: { title: 'Wixを先に確認', text: 'AIで土台を作り、ドラッグ＆ドロップで細かく編集したい人向けの候補です。' },
    quick: { title: 'Jimdoを先に確認', text: '質問への回答をもとにサイトの土台を作れるAIビルダーが候補です。' }
  };
  function render() {
    const selected = budget.value === 'free' ? candidates.free : (candidates[purpose.value] || candidates.simple);
    result.replaceChildren();
    const strong = document.createElement('strong'); strong.textContent = selected.title;
    const text = document.createElement('span'); text.textContent = selected.text;
    result.append(strong, text);
  }
  purpose.addEventListener('change', render);
  budget.addEventListener('change', render);
  render();
})();
