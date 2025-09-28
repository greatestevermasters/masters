myproject/
├── myproject/
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html           # Shared base template
│   ├── masters/            # Shared templates for masters
│   │   ├── content_list.html
│   │   ├── content_detail.html
│   └── partials/           # Navbars, footers, etc.
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── buddha/
│   ├── models.py           # Buddha-specific models (if needed)
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── osho/
│   └── ...
├── krishna/
│   └── ...
├── content/                # Shared content app
│   ├── models.py           # Teachings, Books, Videos, Blogs
│   ├── views.py
│   ├── urls.py
│   └── templates/content/  # List/detail templates
└── social/                 # Likes, comments, shares
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/social/
<<<<<<< HEAD

Single folder for CSS, JS, images. Shared across all apps.

                     ┌─────────────┐
                     │   masters   │
                     │  (project)  │
                     └─────┬──────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
     ┌─────────────┐                 ┌─────────────┐
     │  templates  │                 │   static    │
     │ (shared)    │                 │ (shared)    │
     │-------------│                 │-------------│
     │ base.html   │                 │ css/        │
     │ partials/   │                 │ js/         │
     │ content/    │                 │ images/     │
     │  ├─ content_list.html         │             │
     │  └─ content_detail.html       │             │
     └─────────────┘                 └─────────────┘
           │
           │
           ▼
  ┌─────────────────────┐
  │      content/       │  <-- Shared app for all content
  │---------------------│
  │ models.py           │
  │  - Content          │
  │    fields: title,   │
  │            type,    │
  │            master,  │
  │            body,... │
  │ views.py            │
  │  - content_list     │
  │  - content_detail   │
  │ urls.py             │
  └─────────┬───────────┘
            │
   ┌────────┴─────────┐
   │                  │
   ▼                  ▼
buddha/             osho/            krishna/
(optional)          (optional)       (optional)
- extra views       - extra views   - extra views
- specific models   - specific models - specific models

          ┌───────────────┐
          │    social/    │
          │---------------│
          │ models.py     │
          │ - Like        │
          │ - Comment     │
          │ - Share       │
          │ views.py      │
          │ urls.py       │
          └───────────────┘
                   ▲
                   │
           GenericForeignKey
                   │
           ┌───────┴─────────┐
           │ Content (any master/type) │
           └─────────────────────────┘


=======
>>>>>>> ec2e4328a35b9d5508a0e0d6c397784cb6347788
