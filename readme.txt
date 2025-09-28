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
