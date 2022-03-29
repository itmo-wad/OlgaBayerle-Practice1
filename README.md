Practice#1 -- Olga Bayerle

Required
1. Create a flask app which connects to MongoDB and runs at ‘http://localhost:5000’

2. Authentication

-User can sign up at ‘/signup’
-Login page at ‘/auth’ .If success, return a secret page to user. If not, give user a flash message about the error.
-Store username, password in database

3. Implement image upload feature
-Form to upload image at ‘/upload’
-Save uploaded image to folder ‘upload’ on server side, allow only specified extensions
-Redirect to ‘/uploaded/<filename>’ which shows the uploaded image
-Return user back to ‘upload’ with flash error message if there would be any error
