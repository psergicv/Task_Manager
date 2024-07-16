<h1>Task Manager</h1>

Task Manager is a web application designed for small to medium-sized teams to manage their tasks and projects efficiently. It is built using the Flask framework, with HTML/CSS/JS for the front-end and MySQL as the database.


<h1>Features</h1>

- &nbsp; User authentication with a default admin user
- &nbsp; User profiles and task lists
- &nbsp; Task creation, editing, and management
- &nbsp; Project creation and management
- &nbsp; Member list and profile editing
- &nbsp; Task archive


<h1>Getting Started</h1>

<h3>Prerequisites</h3>

To run this project, you will need:

- Python 3.6 or higher
- MySQL

<h3>Installation</h3>

- &nbsp; Clone the repository: git clone https://github.com/psergicv/Task_Manager.git
- &nbsp; Install the required dependencies: pip install -r requirements.txt
- &nbsp; Create a MySQL database and configure the database settings in config.py.
- &nbsp; Run the following command to start the application: python app.py
- &nbsp; Open your browser and navigate to http://localhost:5000


<h1>Usage</h1>
<h3>Login</h3>
Users need to use their credentials to access the application. Initially, a default admin user is set up to create accounts for other users. Registration is not available; users can only be added by the admin.

![Screenshot login page](https://user-images.githubusercontent.com/64396685/227368194-3d8a22bd-3443-4b48-b169-a62752b6ea1a.png)

<h3>Main Page</h3>
After logging in, users are taken to the main page, which displays the profiles of all team members. Users can access the task list of any team member by clicking on their profile.

![Screenshot Main Page](https://user-images.githubusercontent.com/64396685/227368713-6aa00417-eec1-4ecb-ae98-d97200a17d96.png)

<h3>Task List</h3>
The personal task list of each user shows all assigned tasks. Users can access the task details by clicking on a specific task.

![Screenshot Personal Task List](https://user-images.githubusercontent.com/64396685/227368907-ded48a4f-d0ec-4735-8946-2fb05a16f418.png)

<h3>Task Details</h3>
The Task Details page provides comprehensive information about a task, including the ability to edit, close, or delete it. Additionally, users can leave comments for the person responsible for the task.

![Screenshot Task Details](https://user-images.githubusercontent.com/64396685/227369041-458680a2-f6aa-4301-a6c0-5070b78683bb.png)
![Screenshot Task Details Comment Section](https://user-images.githubusercontent.com/64396685/227369054-f2be533f-44a0-4e7a-917d-9f708655a42b.png)

<h3>Create Task</h3>
Users can create tasks by providing a title, description, status, deadline, assignee, priority, and project association. After creating a task, it will appear in the task list of the assigned user.

![Screenshot Create Task Page](https://user-images.githubusercontent.com/64396685/227369187-571f7004-dc9f-40e4-b660-02b1d6483002.png)

<h3>Member List</h3>
The Member List page displays all team members, and users can view the details of each member by clicking on their profile. Users can edit their profile details, and admins can edit any user's profile or delete users.

![Screenshot Member List Page](https://user-images.githubusercontent.com/64396685/227369426-f6dea220-ee09-4241-bd20-906346a05205.png)

<h3>Project List</h3>
The Project List page shows all active projects. Clicking on a project will open the Project Details page, which includes project information, stats, and a list of associated tasks.

![Screenshot Project List](https://user-images.githubusercontent.com/64396685/227369847-c1f368f2-4e88-4643-96da-0ae6e0d98877.png)
![Screenshot Project Details](https://user-images.githubusercontent.com/64396685/227369866-eede40f3-52c0-4bd8-8564-48ac6f2a5100.png)

<h3>Archive</h3>
The Archive page stores all completed tasks for future reference.

<h3>License</h3>
This project is licensed under the MIT License. See the LICENSE file for details.

