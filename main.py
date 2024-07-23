from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
from settings import secret_key, password
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['MYSQL_DB'] = "todoapp"
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)


@app.route('/index')
def index():
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('SELECT * FROM users WHERE id != 1 ORDER BY id ASC')
        users = conn.fetchall()
        return render_template('index.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'loggedin' in session:
        current_day = datetime.now().strftime("%Y-%m-%d")
        if request.method == "POST":
            title = request.form['title']
            message = request.form['message']
            status = request.form['status']
            assigned = request.form['assigned']
            level = request.form['level']
            author = session['fullname']
            creation_date = get_current_date()
            deadline = request.form['date']
            assigned_project = request.form['assigned_project']
            conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            conn.execute('INSERT INTO posts VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                         (title, message, status, assigned, level, author, creation_date, deadline, assigned_project))
            conn.connection.commit()
            return redirect(url_for('index'))
        conn2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn2.execute("SELECT * FROM users WHERE id != 1 ORDER BY id ASC")
        users = conn2.fetchall()

        conn3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn3.execute("SELECT title FROM projects")
        project_titles = conn3.fetchall()

        return render_template('create.html', users=users, current_day=current_day, project_titles=project_titles)
    else:
        return redirect(url_for('login'))


def get_current_date():
    return datetime.today()


@app.route('/personal_task_list/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if 'loggedin' in session:
        if request.method == "POST":
            message = request.form['message']
            author = session['fullname']
            creation_date = get_current_date()
            conn1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            conn1.execute(
                "INSERT INTO comments(id, message, author, creation_date, post_id) VALUES(NULL, %s, %s, %s, %s)",
                (message, author, creation_date, post_id))
            conn1.connection.commit()

        conn_comment = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn_comment.execute(
            "SELECT message, author, creation_date FROM comments WHERE post_id IN (SELECT id FROM posts WHERE id = %s)",
            (post_id,))
        comments = conn_comment.fetchall()

        conn_task_details = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn_task_details.execute(
            "SELECT id, title, message, status, assigned, level, author, creation_date, deadline FROM posts WHERE id = %s",
            (post_id,))
        detailed_post = conn_task_details.fetchone()
        return render_template("detailed_post.html", detailed_post=detailed_post, comments=comments)
    else:
        return redirect(url_for('login'))


@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT title, message, status, assigned, level, deadline, project FROM posts WHERE id = %s", (post_id,))
        old_data = conn.fetchone()

        if request.method == "POST":
            title = request.form['title']
            message = request.form['message']
            status = request.form['status']
            assigned = request.form['assigned']
            level = request.form['level']
            deadline = request.form['date']
            assigned_project = request.form['assigned_project']
            conn.execute(
                f"UPDATE posts SET title = %s, message = %s, status = %s, assigned = %s, level = %s, deadline = %s, project = %s WHERE id = {post_id}",
                (title, message, status, assigned, level, deadline, assigned_project))
            conn.connection.commit()
            conn.close()
            return redirect(url_for('index'))
        conn2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn2.execute("SELECT * FROM users WHERE id != 1")
        users = conn2.fetchall()

        conn3 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn3.execute("SELECT title FROM projects")
        project_titles = conn3.fetchall()
        return render_template("edit.html", old_data=old_data, users=users, project_titles=project_titles)
    else:
        return redirect(url_for('login'))


@app.route('/<int:post_id>/restore')
def post_restore(post_id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("UPDATE posts SET status = %s, assigned = %s  WHERE id= %s", ("In Progress", "unassigned", post_id))
    conn.connection.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:post_id>/delete')
def delete(post_id):
    if 'loggedin' in session:
        conn1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn1.execute("DELETE FROM comments WHERE post_id = %s", (post_id,))
        conn1.connection.commit()

        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        conn.connection.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/personal_task_list/<employee_name>')
def personal_task_list(employee_name):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM posts WHERE assigned = %s AND status != 'Archive'", (employee_name,))
        tasks = conn.fetchall()
        return render_template('personal_tasks.html', tasks=tasks)
    else:
        return redirect(url_for('login'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'loggedin' in session:
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            user_password = request.form['password']

            conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            conn.execute('INSERT INTO users VALUES(NULL, %s, %s, %s, %s)', (firstname, lastname, email, user_password))
            conn.connection.commit()
            return redirect(url_for('index'))
        return render_template('add_user.html')
    else:
        return redirect(url_for('login'))


@app.route('/member_list')
def member_list():
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('SELECT * FROM users WHERE id != 1 ORDER BY id ASC')
        users = conn.fetchall()

        headers = (
            "Member", "Action 1", "Action 2"
        )

        return render_template("member_list.html", users=users, headers=headers)
    else:
        return redirect(url_for('login'))


@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT firstname, lastname, email FROM users WHERE id = %s", (user_id,))
        old_data = conn.fetchone()

        if request.method == "POST":
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            conn.execute(
                f"UPDATE users SET firstname = %s, lastname = %s, email = %s WHERE id = {user_id}",
                (firstname, lastname, email))
            conn.connection.commit()
            conn.close()
            return redirect(url_for('index'))
        return render_template("edit_user.html", old_data=old_data)
    else:
        return redirect(url_for('login'))


@app.route('/user/<int:user_id>/delete')
def user_delete(user_id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.connection.commit()
        return redirect(url_for('member_list'))
    else:
        return redirect(url_for('login'))


@app.route('/archive')
def archive():
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM posts WHERE status = 'Archive'")
        archived_tasks = conn.fetchall()
        return render_template('archive.html', archived_tasks=archived_tasks)
    else:
        return redirect(url_for('login'))


@app.route('/archive/detailed_post/<int:post_id>')
def detailed_archive(post_id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM posts WHERE status = 'Archive' AND id = %s", (post_id,))
        archived_task = conn.fetchone()
        return render_template("detailed_archived_post.html", archived_task=archived_task)
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['password']
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM users WHERE email = %s AND password = %s", (user_email, user_password))
        account = conn.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['fullname'] = account['firstname'] + " " + account['lastname']
            session['email'] = account['email']
            return redirect(url_for('index'))
        else:
            return "<h1>Wrong Username/Password! Please try again!</h1>"
    return render_template('login.html')


@app.route('/unassigned_tasks')
def unassigned_tasks():
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM posts WHERE assigned = 'unassigned' AND status != 'Archive'")
        tasks = conn.fetchall()
        return render_template('unassigned_tasks.html', tasks=tasks)
    else:
        return "<h1>Wrong Username/Password! Please try again!</h1>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/projects')
def projects():
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM projects")
        projects_list = conn.fetchall()
        return render_template('projects.html', projects_list=projects_list)
    else:
        return "<h1>Wrong Username/Password! Please try again!</h1>"


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if 'loggedin' in session:
        current_day = datetime.now().strftime("%Y-%m-%d")
        if request.method == "POST":
            name = request.form['name']
            description = request.form['description']
            status = request.form['status']
            level = request.form['level']
            author = session['fullname']
            creation_date = get_current_date()
            deadline = request.form['enddate']

            conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            conn.execute("INSERT INTO projects VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)",
                         (name, description, status, level, author, creation_date, deadline))
            conn.connection.commit()
            conn.close()
            return redirect(url_for('projects'))
        return render_template('project_create.html', current_day=current_day)
    else:
        return "<h1>Wrong Username/Password! Please try again!</h1>"


@app.route('/project/id=<int:project_id>', methods=['GET', 'POST'])
def project_details(project_id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
        proj_details = conn.fetchone()

        conn1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn1.execute("SELECT * FROM posts WHERE project = %s", (proj_details['title'],))
        ticket_list = conn1.fetchall()

        conn2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s", (proj_details['title'],))
        total_project_tickets = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND status = %s",
                      (proj_details['title'], 'In Progress'))
        in_progress_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND status = %s",
                      (proj_details['title'], 'Waiting for Check'))
        not_checked_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND status = %s",
                      (proj_details['title'], 'Approved'))
        approved_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND status = %s",
                      (proj_details['title'], 'Archive'))
        finished_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND level = %s",
                      (proj_details['title'], 'Urgent'))
        urgent_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND level = %s",
                      (proj_details['title'], 'High'))
        high_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND level = %s",
                      (proj_details['title'], 'Medium'))
        medium_ticket = conn2.fetchone()
        conn2.execute("SELECT COUNT(*) FROM posts WHERE project = %s AND level = %s",
                      (proj_details['title'], 'Low'))
        low_ticket = conn2.fetchone()

        return render_template(
            'project_details.html',
            proj_details=proj_details,
            ticket_list=ticket_list,
            total_project_tickets=total_project_tickets,
            in_progress_ticket=in_progress_ticket,
            not_checked_ticket=not_checked_ticket,
            approved_ticket=approved_ticket,
            finished_ticket=finished_ticket,
            urgent_ticket=urgent_ticket,
            high_ticket=high_ticket,
            medium_ticket=medium_ticket,
            low_ticket=low_ticket
        )
    else:
        return "<h1>Wrong Username/Password! Please try again!</h1>"


@app.route('/project/<int:id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    if 'loggedin' in session:
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("SELECT * FROM projects WHERE id = %s", (id,))
        old_data = conn.fetchone()

        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']
            status = request.form['status']
            level = request.form['level']
            deadline = request.form['date']
            conn.execute(
                "UPDATE projects SET title = %s, description = %s, status = %s, level = %s, end_date = %s WHERE id= %s",
                (title, description, status, level, deadline, id)
            )
            conn.connection.commit()
            conn.close()
            return redirect(url_for('projects'))
    return render_template('project_edit.html', old_data=old_data)


@app.route('/project/<int:id>/delete')
def project_delete(id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("DELETE FROM projects WHERE id= %s", (id,))
    conn.connection.commit()
    return redirect(url_for('projects'))


@app.route('/user/<int:id>')
def user_page(id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = conn.fetchone()

    stat_conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    fullname = user['firstname'] + " " + user['lastname']
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s", (fullname,))
    total_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND status = 'Active'", (fullname,))
    total_active_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND status = 'In Progress'", (fullname,))
    total_inprogress_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND status = 'Waiting for Approval'", (fullname,))
    total_wa_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND status = 'Archive'", (fullname,))
    total_archived_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND level = 'Urgent'", (fullname,))
    total_urgent_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND level = 'High'", (fullname,))
    total_high_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND level = 'Medium'", (fullname,))
    total_medium_tkt_nr = stat_conn.fetchone()
    stat_conn.execute("SELECT COUNT(*) FROM posts WHERE assigned = %s AND level = 'Low'", (fullname,))
    total_low_tkt_nr = stat_conn.fetchone()

    return render_template("user_details.html",
                           user=user,
                           total_tkt_nr=total_tkt_nr,
                           total_active_tkt_nr=total_active_tkt_nr,
                           total_inprogress_tkt_nr=total_inprogress_tkt_nr,
                           total_wa_tkt_nr=total_wa_tkt_nr,
                           total_archived_tkt_nr=total_archived_tkt_nr,
                           total_urgent_tkt_nr=total_urgent_tkt_nr,
                           total_high_tkt_nr=total_high_tkt_nr,
                           total_medium_tkt_nr=total_medium_tkt_nr,
                           total_low_tkt_nr=total_low_tkt_nr
                           )


@app.route('/updates')
def updates():
    return "<h2>Test</h2>"


@app.route('/test')
def test_page():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True)
