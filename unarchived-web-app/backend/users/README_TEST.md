🧪 Test Instructions



🚀 Quickstart
Start the Development Server

python manage.py runserver

Access the Test Interfaces
Once the server is running, open your browser and navigate to:

🔹 Main Test Interface
http://127.0.0.1:8000/api/users/mgt/

Available Test UIs:

Feature	Status	Notes
Authentication	✅ Complete	Registration & Login
Project Management	✅ Complete	Create, Update, Delete
Team Management	⚠️ Partial	View, Add, Delete, Update (Add from UI is WIP)

Note: Adding members from the UI is still WIP.
You can currently add members via the Admin Dashboard.

Create a Superuser (Optional)
To manage data and users from the admin panel:


python manage.py createsuperuser
Access the Admin Dashboard
http://127.0.0.1:8000/admin/
Login with the superuser credentials you created.

✅ UI Test Results
Test Case	Result
Authentication	✅ Successful
Project Creation	✅ Successful
Add Members (from UI)	⚠️ WIP
