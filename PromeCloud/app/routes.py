import os
import datetime
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from app import app
from app.models import db, Project


#Upload files only this exts.
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'pptx', 'mp4', 'dwg', '3ds', 'max', 'zip', 'rar',
    'png', 'jpg', 'jpeg', 'gif'
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#download or view
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/projects')
def api_projects():
    projects = Project.query.all()
    projects_list = [{
        'id': p.id,
        'title': p.title,
        'keywords': p.keywords,
        'filename': p.filename,
        'filetype': p.filetype,
        'created_at': p.created_at.isoformat()
    } for p in projects]
    return jsonify(projects_list)




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['project']
        keywords = request.form.get('keywords', '')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            project = Project(
                title=title,
                keywords=keywords,
                filename=filename,
                filetype=file.content_type,
                created_at=datetime.datetime.utcnow()
            )
            db.session.add(project)
            db.session.commit()

            file_url = url_for('uploaded_file', filename=filename)
            return f'''
                ✅ File "<b>{filename}</b>" uploaded under project "<b>{title}</b>" with keywords "<b>{keywords}</b>"<br><br>
                🔗 <a href="{file_url}" target="_blank">View File</a><br>
                🏠 <a href="/">Go Home</a>
            '''
        else:
            return '❌ Invalid file type or no file selected.'

    return render_template('uploads.html')


@app.route('/admin/projects')
def admin_projects():
    projects = Project.query.all()
    return render_template('admin_projects.html', projects=projects)


@app.route('/project/<title>')
def project_detail(title):
    project = Project.query.filter_by(title=title).first_or_404()
    return render_template('project_detail.html', project=project)

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Burada istersen DB sorgusu yapabilirsin, şimdilik hardcoded:
    if username == 'GODMIN' and password == '666':
        return jsonify({'success': True, 'token': 'totally-secure-token'}), 200
    else:
        return jsonify({'success': False, 'message': 'Hatalı giriş!'}), 401
