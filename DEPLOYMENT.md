# Friendscars Deployment Guide

## Quick Setup for Hostinger or Other Hosting Platforms

### 1. Files to Upload
Upload all your project files to your hosting provider. Key files:
- `main.py` - Main application file
- `app.py` - Flask application setup
- `models.py` - Database models
- `routes.py` - Application routes
- `wsgi.py` - Production entry point
- `deployment_packages.txt` - Required packages
- `static/` folder - CSS, images, uploads
- `templates/` folder - HTML templates

### 2. Install Dependencies
On your hosting platform, install the required packages:
```bash
pip install -r deployment_packages.txt
```

### 3. Environment Setup
Create a `.env` file based on `.env.example`:
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
SESSION_SECRET=your-random-secret-key-here
FLASK_ENV=production
```

### 4. Database Setup
If using PostgreSQL (recommended):
1. Create a PostgreSQL database on your hosting platform
2. Update the `DATABASE_URL` in your `.env` file
3. Run database migration:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 5. Web Server Configuration

#### For Apache with mod_wsgi:
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /path/to/your/app
    WSGIDaemonProcess friendscars python-path=/path/to/your/app
    WSGIProcessGroup friendscars
    WSGIScriptAlias / /path/to/your/app/wsgi.py
    
    <Directory /path/to/your/app>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
    Alias /static /path/to/your/app/static
    <Directory /path/to/your/app/static>
        Require all granted
    </Directory>
</VirtualHost>
```

#### For Nginx with uWSGI:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/path/to/your/app/friendscars.sock;
    }
    
    location /static {
        alias /path/to/your/app/static;
    }
}
```

### 6. File Permissions
Ensure the upload directory is writable:
```bash
chmod 755 static/uploads
```

### 7. Admin Access
Default admin credentials:
- Username: `abc`
- Password: `123`

Access admin panel at: `https://yourdomain.com/secret-admin-access-2025`

### 8. Testing
1. Visit your domain to check if it loads
2. Test category selection and vehicle browsing
3. Test admin login and vehicle management
4. Check image uploads work properly

## Hostinger Specific Steps

1. **Upload files**: Use File Manager or FTP to upload all project files
2. **Python App**: Create a new Python app in your Hostinger control panel
3. **Set entry point**: Set `wsgi.py` as your application file
4. **Install packages**: Use Hostinger's package installer or SSH
5. **Database**: Use Hostinger's PostgreSQL service or external database
6. **Domain**: Point your domain to the Python app

## Troubleshooting

- **500 Error**: Check error logs, usually database connection or missing packages
- **Images not loading**: Check file permissions and static folder path
- **Admin can't login**: Verify database is set up and contains admin user
- **Categories not working**: Check session configuration and secret key

## Support
For issues, check the application logs and verify all environment variables are set correctly.