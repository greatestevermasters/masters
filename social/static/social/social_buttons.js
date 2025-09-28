document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".social-buttons").forEach(div => {
        const objectId = div.dataset.objectId;
        const appLabel = div.dataset.app;
        const modelName = div.dataset.model;
        const loginMsgDiv = div.querySelector(".login-msg");

        function safeQuery(selector) { return div.querySelector(selector); }

        // Like / Dislike buttons
        const likeBtn = safeQuery(".like-btn");
        const dislikeBtn = safeQuery(".dislike-btn");
        const shareBtn = safeQuery(".share-btn");
        const commentToggle = safeQuery(".comment-toggle");
        const commentForm = safeQuery(".comment-form");
        const commentList = safeQuery(".comment-list");
        const likeCountEl = safeQuery(".like-count");
        const dislikeCountEl = safeQuery(".dislike-count");

        // helper to request an endpoint (GET)
        function doGet(url, onSuccess) {
            fetch(url, {
                method: "GET",
                headers: {"X-Requested-With": "XMLHttpRequest"}
            }).then(r => r.json())
              .then(onSuccess)
              .catch(err => {
                  console.error("social ajax error", err);
              });
        }

        if (likeBtn) {
            likeBtn.addEventListener("click", function() {
                const val = this.dataset.value;
                const url = `/social/toggle_like/${appLabel}/${modelName}/${objectId}/${val}/`;
                doGet(url, data => {
                    if (data.success) {
                        if (likeCountEl) likeCountEl.textContent = data.like_count;
                        if (dislikeCountEl) dislikeCountEl.textContent = data.dislike_count;
                        if (loginMsgDiv) loginMsgDiv.textContent = "";
                    } else if (data.message && loginMsgDiv) {
                        loginMsgDiv.textContent = data.message;
                    }
                });
            });
        }

        if (dislikeBtn) {
            dislikeBtn.addEventListener("click", function() {
                const val = this.dataset.value;
                const url = `/social/toggle_like/${appLabel}/${modelName}/${objectId}/${val}/`;
                doGet(url, data => {
                    if (data.success) {
                        if (likeCountEl) likeCountEl.textContent = data.like_count;
                        if (dislikeCountEl) dislikeCountEl.textContent = data.dislike_count;
                        if (loginMsgDiv) loginMsgDiv.textContent = "";
                    } else if (data.message && loginMsgDiv) {
                        loginMsgDiv.textContent = data.message;
                    }
                });
            });
        }

        // Share button
        if (shareBtn) {
            shareBtn.addEventListener("click", function() {
                const platform = this.dataset.platform || "link";
                const url = `/social/share/${appLabel}/${modelName}/${objectId}/${platform}/`;
                doGet(url, data => {
                    if (data.success) {
                        // optionally display share_count somewhere if you add it
                        if (loginMsgDiv) loginMsgDiv.textContent = "";
                    } else if (data.message && loginMsgDiv) {
                        loginMsgDiv.textContent = data.message;
                    }
                });
            });
        }

        // Comment toggle & submit
        if (commentToggle && commentForm) {
            commentToggle.addEventListener("click", function() {
                commentForm.classList.toggle("show");
                commentForm.classList.toggle("hidden");
                if (commentForm.classList.contains("show")) {
                    const input = commentForm.querySelector('input[name="text"]');
                    if (input) input.focus();
                }
            });

            commentForm.addEventListener("submit", function(e) {
                e.preventDefault();
                const textInput = this.querySelector('input[name="text"]');
                const csrfInput = this.querySelector('input[name="csrfmiddlewaretoken"]');
                if (!textInput || !csrfInput) return;
                const csrfToken = csrfInput.value;
                fetch(`/social/add_comment/${appLabel}/${modelName}/${objectId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    body: new URLSearchParams({ text: textInput.value })
                }).then(r => r.json()).then(data => {
                    if (data.success) {
                        const li = document.createElement("li");
                        li.innerHTML = `<strong>${data.username}</strong>: ${data.text}`;
                        if (commentList) commentList.prepend(li);
                        textInput.value = "";
                        if (loginMsgDiv) loginMsgDiv.textContent = "";
                    } else if (data.message && loginMsgDiv) {
                        loginMsgDiv.textContent = data.message;
                    }
                }).catch(err => console.error(err));
            });
        }

        // Ajax nav (previous / next) - optional replacement of social-buttons block
        div.querySelectorAll(".ajax-nav").forEach(btn => {
            btn.addEventListener("click", function() {
                const url = this.dataset.url;
                if (!url || url === "#") return;
                fetch(url, { method: "GET", headers: {"X-Requested-With": "XMLHttpRequest"} })
                  .then(res => res.text())
                  .then(html => {
                      const parser = new DOMParser();
                      const doc = parser.parseFromString(html, "text/html");
                      const newDiv = doc.querySelector(".social-buttons");
                      if (newDiv) {
                          div.replaceWith(newDiv);
                          // re-run init for newly inserted block
                          document.dispatchEvent(new Event('DOMContentLoaded'));
                      }
                  }).catch(err => console.error(err));
            });
        });

    });
});
