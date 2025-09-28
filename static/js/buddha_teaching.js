// ------------------ Toolbar Actions ------------------

// Like / Dislike AJAX toggle
// ------------------ Toolbar Actions ------------------

// Like / Dislike AJAX toggle
function toggleReaction(app_label, model_name, object_id, type, btn) {
  fetch(`/toggle_like/${app_label}/${model_name}/${object_id}/${type}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Accept': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const span = btn.querySelector("span") || document.createElement("span");
      if (!btn.contains(span)) btn.appendChild(span);
      span.textContent = data.count; // update count dynamically
    } else {
      alert("Error: " + (data.error || "Could not update."));
    }
  })
  .catch(err => console.error("Error in toggleReaction:", err));
}

// Share - copy current page URL
function share(item) {
  const link = window.location.href;
  navigator.clipboard.writeText(link)
    .then(() => {
      const msg = `Link for "${item}" copied!`;
      console.log(msg);
      alert(msg); // optionally replace with a toast notification
    })
    .catch(err => console.error("Copy failed:", err));
}

// Comment - simple prompt (could be integrated with backend)
function comment(item, btn) {
  const text = prompt("Write your comment for " + item + ":");
  if (text) {
    // Optionally send comment via AJAX to server
    console.log(`Comment for ${item}: ${text}`);
    const commentCard = document.createElement("div");
    commentCard.className = "comment-card";
    commentCard.textContent = text;
    btn.closest(".card")?.querySelector(".section-body")?.appendChild(commentCard);
  }
}

// Navigation - Next / Back placeholder (integrate carousel)
function nextItem(item) {
  console.log("Next:", item);
  // Replace with carousel/slider logic
}
function backItem(item) {
  console.log("Back:", item);
  // Replace with carousel/slider logic
}

// ------------------ Dropdown Menus ------------------
function toggleDropdown(id) {
  const el = document.getElementById(id + "-dropdown");
  document.querySelectorAll('.dropdown-content').forEach(d => {
    if (d !== el) d.style.display = 'none';
  });
  el.style.display = (el.style.display === 'block') ? 'none' : 'block';
}

window.addEventListener('click', function(e) {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-content').forEach(d => d.style.display = 'none');
  }
});

// ------------------ CSRF Token Helper ------------------
function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return decodeURIComponent(value);
  }
  return '';
}

// ------------------ Event Delegation ------------------
document.addEventListener("click", function(e) {
  const btn = e.target.closest(".like-btn, .dislike-btn, .share-btn, .comment-btn, .tool");
  if (!btn) return;

  const app_label = btn.dataset.appLabel;
  const model_name = btn.dataset.modelName;
  const object_id = btn.dataset.objectId;

  if (btn.classList.contains('like-btn')) toggleReaction(app_label, model_name, object_id, 'like', btn);
  if (btn.classList.contains('dislike-btn')) toggleReaction(app_label, model_name, object_id, 'dislike', btn);
  if (btn.classList.contains('share-btn')) share(btn.dataset.item || "Item");
  if (btn.classList.contains('comment-btn')) comment(btn.dataset.item || "Item", btn);
  if (btn.classList.contains('tool')) {
    if (btn.dataset.action === 'next') nextItem(btn.dataset.item || "Item");
    if (btn.dataset.action === 'back') backItem(btn.dataset.item || "Item");
  }
});

function toggleReaction(app_label, model_name, object_id, type, btn) {
  fetch(`/toggle_like/${app_label}/${model_name}/${object_id}/${type}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Accept': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const span = btn.querySelector("span.small") || btn.querySelector("span");
        if (span) span.textContent = data.count; // update count dynamically
      } else {
        alert("Error: " + (data.error || "Could not update."));
      }
    })
    .catch(err => console.error("Error in toggleReaction:", err));
}

// Share - Copy link or open social media
function share(item) {
  const link = prompt("Share link for " + item + ":", window.location.href);
  if (link) navigator.clipboard.writeText(link).then(() => alert("Copied to clipboard!"));
}

// Comment - simple prompt
function comment(item) {
  const text = prompt("Write your comment for " + item + ":");
  if (text) alert("Your comment on " + item + ": " + text);
}

// Navigation - Next / Back placeholder
function nextItem(item) {
  console.log("Next:", item);
  // Add carousel/slider logic if needed
}
function backItem(item) {
  console.log("Back:", item);
  // Add carousel/slider logic if needed
}

// ------------------ Dropdown Menus ------------------
function toggleDropdown(id) {
  const el = document.getElementById(id + "-dropdown");
  document.querySelectorAll('.dropdown-content').forEach(d => {
    if (d !== el) d.style.display = 'none';
  });
  el.style.display = (el.style.display === 'block') ? 'none' : 'block';
}
window.addEventListener('click', function(e) {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-content').forEach(d => d.style.display = 'none');
  }
});

// ------------------ Copy Share Link ------------------
function copyLink(inputId="shareLink") {
  const copyText = document.getElementById(inputId);
  if (!copyText) return;
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value)
    .then(() => alert("Link copied: " + copyText.value))
    .catch(err => console.error("Copy failed:", err));
}

// ------------------ CSRF Token Helper ------------------
function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return decodeURIComponent(value);
  }
  return '';
}

// ------------------ Event Delegation (dynamic content) ------------------
document.addEventListener("click", function(e) {
  // Like / Dislike buttons
  if (e.target.closest(".like-btn") || e.target.closest(".dislike-btn")) {
    const btn = e.target.closest(".like-btn") || e.target.closest(".dislike-btn");
    const app_label = btn.dataset.appLabel;
    const model_name = btn.dataset.modelName;
    const object_id = btn.dataset.objectId;
    const type = btn.classList.contains('like-btn') ? 'like' : 'dislike';
    toggleReaction(app_label, model_name, object_id, type, btn);
  }

  // Toolbar icon buttons (Back / Next / Share / Comment)
  if (e.target.closest(".tool")) {
    const btn = e.target.closest(".tool");
    const action = btn.dataset.action;
    const item = btn.dataset.item || '';
    switch (action) {
      case 'back': backItem(item); break;
      case 'next': nextItem(item); break;
      case 'share': share(item); break;
      case 'comment': comment(item); break;
    }
  }
});

