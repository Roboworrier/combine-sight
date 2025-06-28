# Plant Union Landing Page

A professional corporate landing page built with Flask that provides a welcome interface with two clickable options leading to different applications.

## Features

- **Professional Corporate Design**: Modern gradient background with clean white cards
- **Personalized Welcome**: Users enter their name and get a personalized welcome message
- **Two Clickable Options**: Two images that redirect to different IP addresses
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Hover Effects**: Interactive animations and visual feedback
- **Easy Link Management**: Simple to change redirect URLs in the code

## Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:5000`
   - The application will be accessible on all network interfaces

## Configuration

### Changing Redirect URLs

To change the redirect URLs, edit the `app.py` file:

```python
@app.route('/redirect/<target>')
def redirect_to_target(target):
    if target == 'option1':
        return redirect('http://10.1.1.168:5000')  # Change this URL
    elif target == 'option2':
        return redirect('http://10.1.2.107')       # Change this URL
    else:
        return redirect(url_for('landing_page'))
```

### Changing Images

Replace the images in the `static/Images/` folder:
- `botsight-logo.png` - First option image
- `Screenshot 2025-06-28 094425.png` - Second option image

### Customizing Text

Edit the `templates/landing.html` file to change:
- Welcome messages
- Option titles and descriptions
- Company branding

## File Structure

```
plant_union/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── Images/
│       ├── botsight-logo.png
│       └── Screenshot 2025-06-28 094425.png
└── templates/
    └── landing.html      # Main landing page template
```

## Usage Flow

1. User visits the landing page
2. User enters their name in the form
3. User sees a personalized welcome message
4. User clicks on one of the two image options
5. User is redirected to the corresponding application

## Technical Details

- **Framework**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradients and animations
- **Responsive**: CSS Grid and Flexbox for mobile compatibility
- **Port**: 5000 (configurable in app.py)

## Deployment

The application is configured to run on all network interfaces (`0.0.0.0`) on port 5000. For production deployment, consider:

- Using a production WSGI server like Gunicorn
- Setting up a reverse proxy with Nginx
- Configuring SSL certificates
- Setting `debug=False` in production 

## SSO for Plant Head Role

This app supports SSO (single sign-on) for the plant_head role. When a user clicks the first option, a secure token is generated and the user is redirected to the BotSight app's /sso_login endpoint. The BotSight app must have a matching /sso_login endpoint and use the same secret key and salt for token validation.

### How it works
- Landing page generates a token for plant_head
- Redirects to http://10.1.1.168:5000/sso_login?token=XYZ
- BotSight app validates the token and logs in the user as plant_head

### Security
- The token expires in 60 seconds
- Only the plant_head role is supported
- Use a strong secret key in production 