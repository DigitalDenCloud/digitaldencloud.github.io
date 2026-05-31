// Contact form handler for digitalden.cloud /about/
// Posts to the existing API Gateway endpoint that fronts the Lambda + SES pipeline.
// No jQuery, no page refresh on success.

(function () {
  'use strict';

  const ENDPOINT = 'https://2ceumb6wy0.execute-api.eu-west-2.amazonaws.com/prod/contact';

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const submit = document.getElementById('cf-submit');
    const status = document.getElementById('cf-status');
    const honeypot = form.querySelector('input[name="website"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Honeypot — if the hidden field has a value, it's a bot. Drop silently.
      if (honeypot && honeypot.value) {
        setStatus('Message sent.', 'success');
        form.reset();
        return;
      }

      const data = {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        message: form.message.value.trim()
      };

      if (!data.name || !data.email || !data.message) {
        setStatus('Please fill in all fields.', 'error');
        return;
      }
      if (!isValidEmail(data.email)) {
        setStatus('Please enter a valid email.', 'error');
        return;
      }

      submit.disabled = true;
      setStatus('Sending…', 'loading');

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error('Network response was not ok');
          return res.json();
        })
        .then(function () {
          setStatus('Message sent.', 'success');
          form.reset();
        })
        .catch(function (err) {
          console.error('Contact form error:', err);
          setStatus('Something went wrong. Please try again.', 'error');
        })
        .finally(function () {
          submit.disabled = false;
        });
    });

    function setStatus(text, className) {
      status.textContent = text;
      status.className = 'cf-status ' + className;
    }

    function isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
  });
})();