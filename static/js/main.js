(function () {
  const FIELDS = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
  ];

  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(el => el.remove());
  }

  function showError(el, message) {
    const err = document.createElement('span');
    err.className = 'field-error';
    err.textContent = message;
    el.parentNode.appendChild(err);
  }

  function validate() {
    clearErrors();
    let valid = true;

    FIELDS.forEach(function (name) {
      const el = document.querySelector('[name="' + name + '"]');
      if (!el) return;

      const val = el.value.trim();

      if (val === '' || val === null) {
        showError(el, 'This field is required.');
        valid = false;
      } else if (el.tagName === 'INPUT' && isNaN(Number(val))) {
        showError(el, 'Please enter a numeric value.');
        valid = false;
      }
    });

    return valid;
  }

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predict-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      if (!validate()) {
        e.preventDefault();
        // Scroll to first error
        const firstErr = document.querySelector('.field-error');
        if (firstErr) firstErr.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      const btnText = document.getElementById('btn-text');
      const spinner = document.getElementById('spinner');
      const btn = document.getElementById('submit-btn');
      if (btnText) btnText.classList.add('hidden');
      if (spinner) spinner.classList.remove('hidden');
      if (btn) btn.disabled = true;
    });
  });
}());
