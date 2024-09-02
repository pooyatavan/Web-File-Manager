from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, Blueprint
import datetime, os, re
from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

from modules.password import PassGenerate
from modules.strings import Console,Mess, Objects, SelectUser, SaveLog
from modules.log import LOG
from modules.sql import SQL
from modules.tools import restart, RandomKey, GetRootProject, GetTime, RemoveIP
from modules.image import compress_image
from modules.config import Config

accounts = {}
usernames = []
accounts, usernames = SQL.ReadAccounts()
pattern = re.compile(r"\((\d+)\)")
app = Flask(__name__, template_folder='../templates', static_folder='../dir')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'dir')
errors = Blueprint('errors', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if bool(Config.read()['core']['debug']) == True:
    app.secret_key = "123456789"
else:
    app.secret_key = RandomKey()

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": Objects.username.value, "class": "form-control", "id": "floatingInput", "type": "text"})
    password = StringField(render_kw={"placeholder": Objects.password.value, "class": "form-control","id": "floatingInput", "type": "password"})
    code = StringField(render_kw={"placeholder": "Code", "class": "captchatextbox", "autocomplete": "off", "inputmode": "numeric", "maxlength": "4"})
    login = SubmitField(label=Objects.login.value, render_kw={"class": "btn btn-primary w-100 py-2"})

class SearchForm(FlaskForm):
    searchtxt = StringField(render_kw={"placeHolder": Objects.SearchFiles.value, "class": "form-control mr-2", "type": "text", "style": "text-align: right;"})
    searchbtn = SubmitField(render_kw={"value": f"{Objects.Search.value}", "class": "btn"})

class dir(FlaskForm):
    # upluad files
    filesname = StringField(render_kw={"placeholder": Objects.FilesName.value, "class": "form-control", "type": "text"})
    image = FileField(Objects.ChooseFile.value, validators=[FileRequired(),FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], render_kw={"multiple": True, "class": "file-selector"})
    upload = SubmitField(label=Objects.upload.value, render_kw={'class': "btn"})
    # rename folder
    getname = StringField(render_kw={"placeholder": Objects.FolderName.value, "class": "form-control"})
    submitname = SubmitField(label=Objects.SubmitChangeName.value, render_kw={"class": "btn", "style": "float: right"})
    # make new folder
    newfoldername = StringField(render_kw={"placeholder": Objects.FolderName.value, "class": "form-control"})
    submitnewfoldername = SubmitField(label=Objects.NewFolder.value, render_kw={"class": "btn", "style": "float: right"})

class PanelForm(FlaskForm):
    # register user
    username = StringField(render_kw={"placeholder": Objects.username.value, "class": "form-control", "type": "text"})
    password = StringField(render_kw={"placeholder": Objects.password.value, "class": "form-control", "type": "password"})
    repassword = StringField(render_kw={"placeholder": Objects.repassword.value, "class": "form-control", "type": "password"})
    register = SubmitField(label= Objects.register.value, render_kw={"class": "btn"})
    # change permission
    selectuser = SelectField(render_kw={"class": "form-select"}, choices=usernames)
    selectpermission = SelectField(render_kw={"class": "form-select"}, choices=[(0, SelectUser.choose.value), (1, SelectUser.Guest.value), (2, SelectUser.user.value), (3, SelectUser.admin.value)])
    changepermission = SubmitField(label= Objects.submit.value, render_kw={"class": "btn"})
    regselectpermission = SelectField(render_kw={"class": "form-select"}, choices=[(0, SelectUser.choose.value), (1, SelectUser.Guest.value), (2, SelectUser.user.value), (3, SelectUser.admin.value), (4, SelectUser.Lock.value)])
    # clear log
    clearlog = SubmitField(label= Objects.clear.value, render_kw={"class": "btn"})
    # delete user
    selectuserdelete = SelectField(render_kw={"class": "form-select"}, choices=usernames)
    deleteusername = SubmitField(render_kw={"class": "btn"}, label=Objects.delete.value)
    # restart core
    restartcore = SubmitField(render_kw={"class": "btn"}, label=Objects.restart.value)
    # change password
    changepassword = SubmitField(render_kw={"class": "btn"}, label=Objects.ChangePass.value)
    oldpassword = StringField(render_kw={"placeholder": Objects.OldPass.value, "class": "form-control", "type": "password"})
    newpassword = StringField(render_kw={"placeholder": Objects.NewPass.value, "class": "form-control", "type": "password"})
    renewpassword = StringField(render_kw={"placeholder": Objects.ReNewPass.value, "class": "form-control", "type": "password"})

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
    
    # Login page
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

    # Main page
    @app.route('/', defaults={'req_path': ''}, methods=['POST', 'GET'])
    @app.route('/<path:req_path>', methods=['POST', 'GET'])
    def dir_listing(req_path):
        form = dir()
        if "username" in session:
            if int(session['permission']) == 4:
                 return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.AccountLock.value)
            else:
                BASE_DIR = app.config['UPLOAD_FOLDER']
                URLREQ = request.base_url.replace(RemoveIP(), "")

                # Upload image
                if form.upload.data == True:
                    count = 0
                    NewFileName = form.filesname.data
                    files = request.files.getlist(form.image.name)
                    if not NewFileName:
                        flash(Mess.FileNameEmpty.value)
                        return redirect(url_for('dir_listing', req_path=req_path))
                    else:
                        for count_loop, file in enumerate(files):
                            NFN = NewFileName + f"_({str(count_loop)})" + os.path.splitext(file.filename)[1]
                            if not URLREQ:
                                FA = BASE_DIR + "\\" + NFN
                                FP = BASE_DIR
                            else:
                                FA = BASE_DIR + "\\" + URLREQ + "\\" + NFN
                                FP = BASE_DIR + "\\" + URLREQ
                            if not os.path.isfile(FA):
                                file.save(FA)
                                compress_image(FP, NFN)
                            else:
                                while True:
                                    if count <= 10000:
                                        new_file_name = NewFileName + f"_({count})" + os.path.splitext(file.filename)[1]
                                        if not os.path.isfile(os.path.join(FP, new_file_name)):
                                            file.save(os.path.join(FP, new_file_name))
                                            compress_image(FP, new_file_name)
                                            break
                                        else:
                                            count = count + 1
                        SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.FileUpload.value, str(len(files)))
                        flash(Mess.UploadSucc.value.format(count=len(files)))

                # MAKE NEW Folder
                if form.submitnewfoldername.data == True:
                    newfoldername = form.newfoldername.data
                    if newfoldername == "":
                        flash(Mess.EmptyFolder.value)
                    else:
                        FullDestination = BASE_DIR + "\\" + URLREQ + "\\" + newfoldername
                        if os.path.exists(FullDestination) == False:
                            try:
                                os.makedirs(FullDestination, exist_ok=True)
                                flash(Mess.FolderSucc.value)
                                LOG.info(Console.UserMakeFolder.value.format(username=session['username'], name=newfoldername))
                                SQL.InsertLog(len(SQL.ReadLogs()) + 1, GetTime(), session['username'], SaveLog.MakeNewFolder.value, newfoldername)
                            except:
                                pass
                        else:
                            flash(Mess.FolderExist.value)

                # rename folder
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
                        try:
                            os.rename(GetRootProject() + f"\\dir\\{req_path.replace('/', '\\')}", BASE_DIR + Fixname)
                        except:
                            pass
                        LOG.info(Console.UsernameRenameFolder.value.format(username=session['username'], old=Renamelist[0], new=Newname))
                        return redirect(url_for('login'))
                
                abs_path = os.path.join(BASE_DIR, req_path)
                if not os.path.exists(abs_path):
                    return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value)
                if os.path.isfile(abs_path):
                    return f'Serving file: {abs_path}'
                dir_files = os.listdir(abs_path)
                return render_template('index.html', files=dir_files, current_path=req_path, form=form)
        else:
            return redirect(url_for('login'))

    # Delete file
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
    
    # Search page
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        BASE_DIR = app.config['UPLOAD_FOLDER']
        session.pop('_flashes', None)
        form = SearchForm()
        if form.validate_on_submit():
            ForSearch = form.searchtxt.data
            if ForSearch == "":
                flash(Mess.SearchEmpty.value)
                return render_template('search.html', form=form)
            else:
                file_search = []
                folder_Search = []
                FileLocation = ""
                for root, dirs, files in os.walk(BASE_DIR):
                    for file in files:
                        if "thumb_" not in file:
                            if ForSearch.lower() in file.lower():
                                relative_path = os.path.relpath(root, BASE_DIR)
                                FileLocation = "\\" + "dir" + "\\" + relative_path + "\\" + file
                                file_search.append(os.path.join(relative_path, file))
                    for dir in dirs:
                        if ForSearch.lower() in dir.lower():
                            folder_Search.append(root.replace(BASE_DIR, "").replace("\\", "/") + "/" + dir)
                LOG.info(Console.UserSearch.value.format(username=session['username'], search=ForSearch))
                if not file_search and not folder_Search:
                    flash(Mess.NotExist.value.format(search=ForSearch))
                    return render_template('search.html', form=form)
                else:
                    return render_template('search.html', files=file_search, current_path=FileLocation, search=True, form=form, folders=folder_Search)
        else:
            if "username" in session:
                if int(session['permission']) == 4:
                    return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.AccountLock.value)
                else:
                    return render_template('search.html', form=form)
            else:
                return redirect(url_for('login'))

    # User panel
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
        if "username" in session:
            if int(session['permission']) == 4:
                return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.AccountLock.value)
            else:
                return render_template('log.html', logs=SQL.ReadLogs())
        else:
            return redirect(url_for('login'))
    
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