document.addEventListener('DOMContentLoaded', () => {
  const createForm = /** @type {HTMLFormElement | null} */ (document.getElementById('create-form'));
  const errorMsg = /** @type {HTMLDivElement | null} */ (document.getElementById('error-msg'));

  /**
   * エラーメッセージを表示する
   * @param {string} message
   */
  const showError = (message) => {
    if (errorMsg) errorMsg.textContent = message;
  };

  // チケット新規作成
  if (createForm) {
    createForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const titleInput = /** @type {HTMLInputElement} */ (document.getElementById('title'));
      const assigneeInput = /** @type {HTMLInputElement} */ (document.getElementById('assignee'));

      const res = await fetch('/api/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: titleInput.value,
          assignee: assigneeInput.value,
        }),
      });

      if (res.ok) {
        window.location.reload();
      } else {
        const err = await res.json();
        showError(err.detail?.[0]?.msg || err.detail || '登録に失敗しました');
      }
    });
  }

  // ステータス変更
  document.querySelectorAll('.status-select').forEach((select) => {
    select.addEventListener('change', async (e) => {
      const target = /** @type {HTMLSelectElement} */ (e.target);
      const ticketId = target.dataset.ticketId;

      const res = await fetch(`/api/tickets/${ticketId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: target.value }),
      });

      if (res.ok) {
        window.location.reload();
      } else {
        const err = await res.json();
        alert(err.detail || 'ステータス更新に失敗しました');
        window.location.reload();
      }
    });
  });

  // チケット削除
  document.querySelectorAll('.delete-btn').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      const target = /** @type {HTMLButtonElement} */ (e.target);
      const ticketId = target.dataset.ticketId;
      if (!confirm(`ID:${ticketId} を削除しますか？`)) return;

      const res = await fetch(`/api/tickets/${ticketId}`, { method: 'DELETE' });
      if (res.ok) {
        window.location.reload();
      } else {
        alert('削除に失敗しました');
      }
    });
  });
});