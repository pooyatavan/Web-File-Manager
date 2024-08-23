from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, Blueprint
import datetime, os, re
from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from modules.password import PassGenerate
from modules.strings import Console,Mess, Objects, SelectUser, SaveLog
from modules.log import LOG
from modules.sql import SQL
from modules.tools import restart, GetDirServer, GetRootProject, GetTime
from modules.image import compress_image
from modules.config import Config

accounts = {}
usernames = []
accounts, usernames = SQL.ReadAccounts()
pattern = re.compile(r"\((\d+)\)")
app = Flask(__name__, template_folder='../templates', static_folder='../dir')
#app.secret_key = Random()
app.secret_key = "123456789"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'dir')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
errors = Blueprint('errors', __name__)

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": Objects.username.value, "class": "form-control", "id": "floatingInput", "type": "text"})
    password = StringField(render_kw={"placeholder": Objects.password.value, "class": "form-control","id": "floatingInput", "type": "password"})
    code = StringField(render_kw={"placeholder": "Code", "class": "captchatextbox", "autocomplete": "off", "inputmode": "numeric", "maxlength": "4"})
    login = SubmitField(label=Objects.login.value, render_kw={"class": "btn btn-primary w-100 py-2"})

class SearchForm(FlaskForm):
    searchtxt = StringField(render_kw={"placeHolder": Objects.SearchFiles.value, "class": "form-control mr-2", "type": "text", "style": "text-align: right;"})
    searchbtn = SubmitField(render_kw={"value": f"{Objects.Search.value}", "class": "btn btn-info"})

class dir(FlaskForm):
    file = FileField(render_kw={"class": "file"}, validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    uploadfile = SubmitField(label=Objects.upload.value, render_kw={'class': "btn btn-primary"})

class ChangeFolderName(FlaskForm):
    getname = StringField(render_kw={"placeholder": Objects.ChangeName.value, "class": "form-control"})
    submitname = SubmitField(label=Objects.SubmitChangeName.value, render_kw={"class": "btn btn-primary", "style": "float: right"})

class PanelForm(FlaskForm):
    username = StringField(render_kw={"placeholder": Objects.username.value, "class": "form-control", "id": "floatingInput", "type": "text"})
    password = StringField(render_kw={"placeholder": Objects.password.value, "class": "form-control","id": "floatingInput", "type": "password"})
    repassword = StringField(render_kw={"placeholder": Objects.repassword.value, "class": "form-control","id": "floatingInput", "type": "password"})
    register = SubmitField(label= Objects.register.value, render_kw={"class": "btn btn-primary w-100 py-2"})
    selectuser = SelectField(render_kw={"class": "form-select"}, choices=usernames)
    selectpermission = SelectField(render_kw={"class": "form-select"}, choices=[(0, SelectUser.choose.value), (1, SelectUser.Guest.value), (2, SelectUser.user.value), (3, SelectUser.admin.value)])
    changepermission = SubmitField(label= Objects.submit.value, render_kw={"class": "btn btn-primary w-100 py-2"})
    regselectpermission = SelectField(render_kw={"class": "form-select"}, choices=[(0, SelectUser.choose.value), (1, SelectUser.Guest.value), (2, SelectUser.user.value), (3, SelectUser.admin.value)])
    clearlog = SubmitField(label= Objects.clear.value, render_kw={"class": "btn btn-primary w-100 py-2"})
    selectuserdelete = SelectField(render_kw={"class": "form-select"}, choices=usernames)
    deleteusername = SubmitField(render_kw={"class": "btn btn-primary w-100 py-2"}, label=Objects.delete.value)
    restartcore = SubmitField(render_kw={"class": "btn btn-primary w-100 py-2"}, label=Objects.restart.value)

    changepassword = SubmitField(render_kw={"class": "btn btn-primary w-100 py-2"}, label=Objects.ChangePass.value)
    oldpassword = StringField(render_kw={"placeholder": Objects.OldPass.value, "class": "form-control","id": "floatingInput", "type": "password"})
    newpassword = StringField(render_kw={"placeholder": Objects.NewPass.value, "class": "form-control","id": "floatingInput", "type": "password"})
    renewpassword = StringField(render_kw={"placeholder": Objects.ReNewPass.value, "class": "form-control","id": "floatingInput", "type": "password"})

def FlaskAPP():
    # Blueprints
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value, image="blueprint/403"), 403
    app.register_error_handler(404, page_not_found)

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value, image="blueprint/403"), 403
    app.register_error_handler(403, page_not_found)

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.WarningDetail.value, image="blueprint/500"), 500
    app.register_error_handler(500, page_not_found)

    # Custom static folders
    @app.route('/static1/<path:filename>')
    def style(filename):
        return send_from_directory('../static', filename)
    
    @app.route("/login", methods=['POST', 'GET'])
    def login():
        form = LoginForm()
        if form.login.data == True:
            username = form.username.data
            password = form.password.data
            if username == "" or password == "":
                flash(Mess.EmptyFields.value, "alert-error")
            else:
                if username not in accounts:
                    flash(Mess.WrongPasswordOrEmail.value, "alert-error")
                else:
                    account = accounts[username]
                    if not PassGenerate(username, password) == account["password"]:
                        flash(Mess.WrongPasswordOrEmail.value)
                    else:
                        if account['permission'] == "lock":
                            return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.AccountLock.value)
                        else:
                            session['username'] = account['username']
                            session['permission'] = account['permission']
                            LOG.debug(Console.LoginSuccess.value.format(username=session["username"]))
                            return redirect(url_for('dir_listing'))
        else:
            if "username" in session:
                 return redirect(url_for('dir_listing'))
            else:
                return render_template('login.html', form=form)
        return render_template('login.html', form=form)

    @app.route('/', defaults={'req_path': ''}, methods=['POST', 'GET'])
    @app.route('/<path:req_path>', methods=['POST', 'GET'])
    def dir_listing(req_path):
        form = ChangeFolderName()
        if "username" in session:
            BASE_DIR = app.config['UPLOAD_FOLDER']
            if form.submitname.data == True:
                if req_path == "":
                    flash(Mess.NotinDir.value)
                    return redirect(url_for('login'))
                else:
                    Newname = form.getname.data
                    Renamelist = req_path.split('/')
                    Renamelist.pop()
                    Renamelist.append(Newname)
                    Fixname = ""
                    for name in Renamelist:
                        Fixname = Fixname + '\\' + name
                    os.rename(GetRootProject() + f"\\dir\\{req_path.replace('/', '\\')}", BASE_DIR + Fixname)
                    LOG.info(Console.UsernameRenameFolder.value.format(username=session['username'], old=Renamelist[0], new=Newname))
                    return redirect(url_for('login'))
            else:
                BASE_DIR = app.config['UPLOAD_FOLDER']
                abs_path = os.path.join(BASE_DIR, req_path)
                if not os.path.exists(abs_path):
                    return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value)
                if os.path.isfile(abs_path):
                    return f'Serving file: {abs_path}'
                files = os.listdir(abs_path)
                return render_template('index.html', files=files, current_path=req_path, form=form)
        else:
            return redirect(url_for('login'))
        
    @app.route('/upload', methods=['POST', 'GET'])
    def upload_file():
        count = 0
        req_path = request.form.get('path', '')
        abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)
        select_files = request.files.getlist('file')
        choose_filename = request.form.get('file_name')
        if choose_filename == "":
            flash(Mess.FileNameEmpty.value)
            return redirect(url_for('dir_listing', req_path=req_path))
        else:
            for count_loop, file in enumerate(select_files):
                NFN = choose_filename + f"_({count_loop})" + os.path.splitext(file.filename)[1]
                if not os.path.isfile(os.path.join(abs_path, NFN)):
                    file.save(os.path.join(abs_path, NFN))
                    compress_image(abs_path, NFN)
                else:
                    while True:
                        if count <= 10000:
                            new_file_name = choose_filename + f"_({count})" + os.path.splitext(file.filename)[1]
                            if not os.path.isfile(os.path.join(abs_path, new_file_name)):
                                file.save(os.path.join(abs_path, new_file_name))
                                compress_image(abs_path, new_file_name)
                                break
                            else:
                                count = count + 1
        SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.FileUpload.value, str(len(select_files)))
        flash(Mess.UploadSucc.value.format(count=len(select_files)))
        return redirect(url_for('dir_listing', req_path=req_path))

    @app.route('/new_folder', methods=['POST'])
    def new_folder():
        req_path = request.form.get('path', '')
        folder_name = request.form.get('folder_name')
        if folder_name:
            if os.path.exists(GetDirServer()[0] + "\\" + "dir" + "\\" + req_path + "\\" + folder_name) == False:
                abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path, folder_name)
                os.makedirs(abs_path, exist_ok=True)
                flash(Mess.FolderSucc.value)
                LOG.info(Console.UserMakeFolder.value.format(username=session['username'], name=folder_name))
                SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.MakeNewFolder.value, folder_name)
            else:
                flash(Mess.FolderExist.value)
        else:
            flash(Mess.EmptyFolder.value)
        return redirect(url_for('dir_listing', req_path=req_path))

    @app.route('/delete', methods=['POST'])
    def delete_file():
        session.pop('_flashes', None)
        req_path = request.form.get('path', '')
        file_name = request.form.get('file_name')
        abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path, file_name)
        abs_path_thumb = os.path.join(app.config['UPLOAD_FOLDER'], req_path, "thumb_" + file_name)
        if os.path.isfile(abs_path) or os.path.isdir(abs_path):
            SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.DeleteFile.value, file_name)
            try:
                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                    os.remove(abs_path_thumb)
                    LOG.info(Console.UserDeleteFile.value.format(username=session['username'], file=file_name))
                    SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.DeleteFile.value, file_name)
                    flash(Mess.DeleteFile.value)
                elif os.path.isdir(abs_path):
                    os.rmdir(abs_path)
                    LOG.info(Console.UserDeleteFolder.value.format(username=session['username'], folder=req_path))
                    SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.DeleteFolder.value, req_path)
                    flash(Mess.DeleteFolder.value)
            except Exception as e:
                flash(Mess.ErorrDeleteFOF.value.format(error=str(e)))
        else:
            flash(Mess.FOFNotFound.value)
        return redirect(url_for('dir_listing', req_path=req_path))

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        session.pop('_flashes', None)
        form = SearchForm()
        if form.validate_on_submit():
            ForSearch = form.searchtxt.data
            if ForSearch == "":
                flash(Mess.SearchEmpty.value)
                return render_template('search.html', form=form)
            else:
                search_results = []
                folder_Search = []
                FileLocation = ""
                for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
                    for file in files:
                        if "thumb_" not in file:
                            if ForSearch.lower() in file.lower():
                                relative_path = os.path.relpath(root, app.config['UPLOAD_FOLDER'])
                                FileLocation = "\\" + "dir" + "\\" + relative_path + "\\" + file
                                search_results.append(os.path.join(relative_path, file))
                    for dir in dirs:
                        if ForSearch.lower() in dir.lower():
                            folder_Search.append(os.path.join(root, dir).replace(GetRootProject(), "").replace("\\", "/").replace("/dir", ""))
                LOG.info(Console.UserSearch.value.format(username=session['username'], search=ForSearch))
                if not search_results and not folder_Search:
                    flash(Mess.NotExist.value.format(search=ForSearch))
                    return render_template('search.html', form=form)
                else:
                    return render_template('search.html', files=search_results, current_path=FileLocation, search=True, form=form, folders=folder_Search)
        else:
            if "username" in session:
                if session['permission'] == "lock":
                    return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.AccountLock.value)
                else:
                    return render_template('search.html', form=form)
            else:
                return redirect(url_for('login'))

    @app.route('/panel', methods=['GET', 'POST'])
    def panel():
        form = PanelForm()
        # Change Password
        if form.changepassword.data == True:
            oldpassword = form.oldpassword.data
            newpassword = form.newpassword.data
            renewpassword = form.renewpassword.data
            if oldpassword == "" or newpassword == "" or renewpassword == "":
                flash(Mess.EmptyFields.value)
            else:
                if PassGenerate(session['username'], oldpassword) == accounts[session['username']]['password']:
                    SQL.ChangePassword(session['username'], PassGenerate(session['username'], newpassword))
                    flash(Mess.ChangepasswordSuccess.value)
        # User Register
        if form.register.data == True:
            username = form.username.data
            password = form.password.data
            repassword = form.repassword.data
            regselectpermission = form.regselectpermission.data
            if username in accounts:
                flash(Mess.UsernameExist.value)
            else:
                if username == "" or password == "" or repassword == "":
                    flash(Mess.EmptyFields.value)
                else:
                    if int(regselectpermission) == 0:
                        flash(Mess.SelectPermiss.value)
                    else:
                        if password == repassword:
                            SQL.Register(username, PassGenerate(username, password), regselectpermission)
                            flash(Mess.RegisterSuccess.value)
                            LOG.info(Console.RegisterSuccess.value.format(admin=session['username'], username=username))
                            return redirect(url_for('panel'))
                        else:
                            flash(Mess.PasswordNotMatch.value)
            return render_template('panel.html', form=form)
        # change permission
        if form.changepermission.data == True:
            selectuser = form.selectuser.data
            selectpermission = form.selectpermission.data
            if int(selectpermission) == 0:
                flash(Mess.SelectPermiss.value)
            else:
                SQL.Changepermission(selectuser, selectpermission)
                flash(Mess.ChangePermission.value)
                LOG.info(Console.SetPermission.value.format(admin=session['username'], username=selectuser, permission=selectpermission))
        # Clear Log
        if form.clearlog.data == True:
            LOG.clearlogfile(session['username'])
            SQL.RemoveAllLogs()
            flash(Mess.ClearLog.value)
            return render_template('panel.html', form=form)
        # delete username
        if form.deleteusername.data == True:
            selectusername = form.selectuserdelete.data
            if selectusername in accounts:
                if selectusername == "admin":
                    flash(Mess.DeleteAdmin.value)
                    return render_template('panel.html', form=form)
                else:
                    SQL.DeleteUsername(selectusername)
                    flash(Mess.DeleteUsername.value.format(username=selectusername))
                    LOG.info(Console.DelUsername.value.format(admin=session['username'], username=selectusername))
                    return redirect(url_for('panel'))
            return render_template('panel.html', form=form)
        # Restart core
        if form.restartcore.data == True:
            restart()
        if "username" in session:
            return render_template('panel.html', form=form)
        else:
            return redirect(url_for('login'))

    # Log page
    @app.route('/log', methods=['GET', 'POST'])
    def log():
        return render_template('log.html', logs=SQL.ReadLogs())
    
    #session time
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=int(Config.read()['core']['session']))

    # user logout
    @app.route("/logout")
    def logout():
        try:
            LOG.debug(Console.Logout.value.format(username=session["username"]))
            session.clear()
            return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))