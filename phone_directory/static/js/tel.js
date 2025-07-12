document.addEventListener('DOMContentLoaded', function() {
  // Функция для создания уведомления
  function showNotification(message, type) {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const messageSpan = document.createElement('span');
    messageSpan.textContent = message;
    
    const closeBtn = document.createElement('span');
    closeBtn.className = 'notification-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = function() {
      notification.style.animation = 'fadeOut 0.3s ease-out forwards';
      setTimeout(() => notification.remove(), 300);
    };
    
    notification.appendChild(messageSpan);
    notification.appendChild(closeBtn);
    container.appendChild(notification);
    
    // Автоматическое закрытие через 5 секунд
    setTimeout(() => {
      notification.style.animation = 'fadeOut 0.3s ease-out forwards';
      setTimeout(() => notification.remove(), 300);
    }, 5000);
  }

  // Обработка сообщений Django
  {% if messages %}
    {% for message in messages %}
      showNotification("{{ message|escapejs }}", "{{ message.tags }}");
    {% endfor %}
  {% endif %}

  // Закрытие модальных окон при клике вне их или на крестик
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    modal.addEventListener('click', function(event) {
      if (event.target === this || event.target.classList.contains('close')) {
        this.style.display = 'none';
      }
    });
  });

  // Закрытие модальных окон по нажатию ESC
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      modals.forEach(modal => {
        if (modal.style.display === 'block') {
          modal.style.display = 'none';
        }
      });
    }
  });
});