# Portfolio WebApp

A bold and creative portfolio web application built with Django and Bootstrap, featuring dynamic theming, smooth animations, and comprehensive content management.

## 🚀 Project Overview

This portfolio webapp showcases a modern, mobile-first design with:
- **Bold Creative Design**: 4 dynamic color palettes with seamless light/dark mode switching
- **Professional Animations**: Subtle, performance-optimized animations using Animate.css and AOS
- **Responsive Layout**: Bootstrap 5.3 with mobile-first approach
- **Content Management**: Fully manageable through Django Admin
- **Interactive Features**: Project filtering, hidden easter eggs, and smooth transitions

## 🛠️ Tech Stack

- **Backend**: Django 4.2+ (Python 3.11+)
- **Frontend**: Bootstrap 5.3, Animate.css, AOS
- **Database**: PostgreSQL (External)
- **Containerization**: Docker & Docker Compose
- **Styling**: Custom CSS with Bootstrap variables
- **Animation**: Animate.css, AOS, Bootstrap transitions

## 📋 Features

### Core Functionality
- **Dynamic Theming**: 4 color palettes (Electric Neon, Sunset Gradient, Ocean Deep, Forest Modern)
- **Content Management**: Django Admin for all content (projects, blog, testimonials, services)
- **Responsive Design**: Mobile-first Bootstrap implementation
- **Performance Optimized**: Lightweight animations and optimized asset loading

### Interactive Elements
- **Project Filtering**: Filter by technology, category, or year
- **Smooth Animations**: Scroll-triggered and hover animations
- **Contact Forms**: Validated contact forms with success/error feedback
- **Easter Egg**: Hidden interactive element for engagement

### Admin Features
- **Site Parameters**: Configure themes, navigation, and site settings
- **User Management**: Role-based access control
- **Content CRUD**: Full content management for all sections

## 🎨 Color Palettes

### 1. Electric Neon (Tech-Forward)
- **Light**: Primary `#6366f1`, Secondary `#8b5cf6`, Accent `#06b6d4`
- **Dark**: Primary `#818cf8`, Secondary `#a78bfa`, Accent `#67e8f9`

### 2. Sunset Gradient (Creative)
- **Light**: Primary `#f59e0b`, Secondary `#ef4444`, Accent `#ec4899`
- **Dark**: Primary `#fbbf24`, Secondary `#f87171`, Accent `#f472b6`

### 3. Ocean Deep (Professional)
- **Light**: Primary `#0ea5e9`, Secondary `#06b6d4`, Accent `#10b981`
- **Dark**: Primary `#38bdf8`, Secondary `#22d3ee`, Accent `#34d399`

### 4. Forest Modern (Eco-Friendly)
- **Light**: Primary `#059669`, Secondary `#7c3aed`, Accent `#f59e0b`
- **Dark**: Primary `#10b981`, Secondary `#a855f7`, Accent `#fbbf24`

## 🏗️ Project Structure

```
portfolio-project/
├── portfolio_project/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                      # Django applications
│   ├── user_management/       # User authentication & permissions
│   ├── parameters/            # Site settings & configuration
│   └── project_management/    # Projects, blog, testimonials
├── templates/                 # Django templates
│   ├── base.html
│   ├── components/           # Reusable template components
│   └── pages/               # Page-specific templates
├── static/                   # Static assets
│   ├── css/                 # Custom styles
│   ├── js/                  # JavaScript files
│   └── img/                 # Images and media
├── docker-compose.yml        # Multi-container setup
├── Dockerfile               # Django app container
├── requirements.txt         # Python dependencies
└── .env                    # Environment variables
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (External database)

### 1. Clone Repository
```bash
git clone <repository-url>
cd portfolio-project
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Docker Development
```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### 4. Local Development (Alternative)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_HOST=your-postgres-host
DB_NAME=portfolio_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_PORT=5432

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Color Palette Customization
Access Django Admin → Parameters → Site Settings to:
- Switch between 4 predefined color palettes
- Toggle light/dark mode default
- Customize navigation styles
- Configure animation settings

## 📱 Content Management

### Django Admin Access
1. Navigate to `/admin/`
2. Login with superuser credentials
3. Manage content through intuitive interfaces:

**Projects**: Add/edit portfolio projects with images, technologies, and links
**Blog**: Create and publish blog articles with categories and tags
**Testimonials**: Manage client testimonials and reviews
**Services**: Configure services and skills offered
**Site Parameters**: Customize themes, navigation, and global settings

## 🎭 Animation Configuration

### Available Animation Types
- **Hero Animations**: Fade in up with staggered delays
- **Scroll Animations**: AOS-triggered animations on scroll
- **Hover Effects**: Subtle transform and scale effects
- **Navigation**: Smooth slide transitions for mobile menu
- **Forms**: Focus animations with glow effects

### Performance Considerations
- Animations respect `prefers-reduced-motion`
- Lightweight libraries (total ~7KB)
- GPU-accelerated transforms
- Debounced scroll events

## 🐳 Docker Deployment

### Production Build
```bash
# Build production image
docker build -t portfolio-app .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Configuration
- **Development**: Uses Django development server
- **Production**: Configured for production deployment
- **Database**: External PostgreSQL (not containerized)
- **Static Files**: Served via whitenoise or external CDN

## 🔒 Security Features

- CSRF protection enabled
- Secure headers configured
- Input validation and sanitization
- Role-based access control
- Environment variable security

## 📊 Monitoring & Analytics

- Custom Django admin logs
- Error tracking and reporting
- Performance monitoring hooks
- User interaction analytics (optional)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `/docs/`
- Review Django and Bootstrap documentation

---

**Built with ❤️ using Django & Bootstrap**