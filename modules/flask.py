from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, Blueprint, jsonify
import datetime, os, re, shutil
from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

from modules.thread import thread
from modules.password import PassGenerate
from modules.strings import Console,Mess, Objects, SaveLog
from modules.log import LOG
from modules.sql import SQL
from modules.tools import restart, RandomKey, GetTime, RemoveIP, CheckLetter, extract_number, CheckDateFormat, FLBD, GetRootProject, ScanDir, SortData
from modules.image import Scan,compress_image
from modules.config import Config

accounts = {}
usernames = []
perm = {}
ScanDirs = []
SQL.MakeOffline()
accounts = SQL.ReadAccounts()
usernames = SQL.ReadUsernames()
perm = SQL.ReadPerm()
pattern = re.compile(r"\((\d+)\)")
app = Flask(__name__, template_folder='../templates', static_folder='../dir')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'dir')
errors = Blueprint('errors', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 16 MB limi
BASE_DIR = app.config['UPLOAD_FOLDER']
ScanDirs = ScanDir(BASE_DIR)

if bool(Config.read()['core']['debug']) == True:
    app.secret_key = "123456789"
else:
    app.secret_key = RandomKey()

class SIL(FlaskForm):
    SU = SelectField(render_kw={"class": "form-select"})
    submit = SubmitField(label=Objects.Search.value, render_kw={'class': "btn"})
    StartDate = StringField(render_kw={"placeholder": Objects.StartDate.value})
    EndDate = StringField(render_kw={"placeholder": Objects.EndDate.value})

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": Objects.username.value, "class": "form-control", "id": "floatingInput", "type": "text"})
    password = StringField(render_kw={"placeholder": Objects.password.value, "class": "form-control","id": "floatingInput", "type": "password"})
    code = StringField(render_kw={"placeholder": "Code", "class": "captchatextbox", "autocomplete": "off", "inputmode": "numeric", "maxlength": "4"})
    login = SubmitField(label=Objects.login.value, render_kw={"class": "btn btn-primary w-100 py-2"})

class SearchForm(FlaskForm):
    searchtxt = StringField(render_kw={"placeHolder": Objects.SearchFiles.value, "class": "", "type": "text", "style": "text-align: left; font-family: tahoma;"})
    searchbtn = SubmitField(render_kw={"value": f"{Objects.Search.value}", "class": "btn"})

class dir(FlaskForm):
    # upluad files
    filesname = StringField(render_kw={"placeholder": Objects.FilesName.value, "class": "form-control", "type": "text"})
    image = FileField(Objects.ChooseFile.value, validators=[FileRequired(),FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], render_kw={"multiple": True, 'style': "color: #ffffff"})
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
    selectuser = SelectField("SelectUser", render_kw={"class": "form-select"}, validators=[DataRequired()])
    changepermission = SubmitField(label= Objects.submit.value, render_kw={"class": "btn"})
    # clear log
    clearlog = SubmitField(label= Objects.clear.value, render_kw={"class": "btn"})
    # delete user
    selectuserdelete = SelectField(render_kw={"class": "form-select"})
    deleteusername = SubmitField(render_kw={"class": "btn"}, label=Objects.delete.value)
    # restart core
    restartcore = SubmitField(render_kw={"class": "btn"}, label=Objects.restart.value)
    # change password
    changepassword = SubmitField(render_kw={"class": "btn"}, label=Objects.ChangePass.value)
    oldpassword = StringField(render_kw={"placeholder": Objects.OldPass.value, "class": "form-control", "type": "password"})
    newpassword = StringField(render_kw={"placeholder": Objects.NewPass.value, "class": "form-control", "type": "password"})
    renewpassword = StringField(render_kw={"placeholder": Objects.ReNewPass.value, "class": "form-control", "type": "password"})
    # Make thumbnail
    makeit = SubmitField(render_kw={"class": "btn"}, label=Objects.MakeIt.value)

def FlaskAPP():
    #session time
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        try:
            app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        except Exception as e:
            LOG.error(Console.SessionError.value.format(error=e))

    @app.route('/update_permissions', methods=['POST'])
    def update_permissions():
        data = request.get_json()
        user_id = data.get('user_id')
        permissions = data.get('permissions')
        SQL.Changepermission(user_id, permissions)
        return "done"

    # API
    @app.route("/get_options", methods=["GET"])
    def get_options():
        return jsonify(SQL.AfterReadPerm(), SQL.Readpermusers())

    # Blueprints
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value, image="404"), 404
    app.register_error_handler(404, page_not_found)

    @app.errorhandler(403)
    def page_not_found(error):
        return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value, image="404"), 403
    app.register_error_handler(403, page_not_found)

    @app.errorhandler(500)
    def page_not_found(error):
        return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.WarningDetail.value, image="404"), 500
    app.register_error_handler(500, page_not_found)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template('message.html', titlemsg=Mess.Heavy.value, detailmsg=Mess.FileToLarge.value, image="file-large"), 413
    app.register_error_handler(413, request_entity_too_large)
    
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
                if CheckLetter(username) == True:
                    if username not in accounts:
                        flash(Mess.WrongPasswordOrEmail.value, "alert-error")
                    else:
                        if not PassGenerate(username, password) == accounts[username]["password"]:
                            flash(Mess.WrongPasswordOrEmail.value)
                        else:
                            if int(accounts[username]['logedin']) == 0:
                                session['username'] = accounts[username]['username']
                                session['id'] = accounts[username]['id']
                                SQL.UpdateUserOnline(username, 1)
                                accounts[username]['logedin'] = 1
                                LOG.debug(Console.LoginSuccess.value.format(username=session["username"]))
                                SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.LI.value, SaveLog.LogIn.value)
                                return redirect(url_for('dir_listing'))
                            else:
                                flash(Mess.session.value)
                else:
                    flash(Mess.Keyboard.value)
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
        FS = []
        FM = []
        if "username" in session:
            URLREQ = request.base_url.replace(RemoveIP(), "")

            # Upload image
            if form.upload.data == True:
                count = 1
                NewFileName = form.filesname.data
                files = request.files.getlist(form.image.name)
                if not NewFileName:
                    flash(Mess.FileNameEmpty.value)
                    return redirect(url_for('dir_listing', req_path=req_path))
                else:
                    for count_loop, file in enumerate(files, start=1):
                        NFN = NewFileName + f"_({str(count_loop )})" + os.path.splitext(file.filename)[1]
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
                    LOG.info(Console.UploadImage.value.format(user=session['username'], count=count, dir=URLREQ))
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.FileUpload.value, str(len(files)))
                    flash(Mess.UploadSucc.value.format(count=len(files)))
            
            # MAKE NEW Folder
            if form.submitnewfoldername.data == True:
                newfoldername = form.newfoldername.data
                if newfoldername == "":
                    flash(Mess.EmptyFolder.value)
                else:
                    FullDestination = BASE_DIR + "\\" + URLREQ + "\\" + newfoldername
                    ScanDirs.append(URLREQ + "\\" + newfoldername)
                    if os.path.exists(FullDestination) == False:
                        try:
                            os.makedirs(FullDestination, exist_ok=True)
                            flash(Mess.FolderSucc.value)
                            LOG.info(Console.UserMakeFolder.value.format(username=session['username'], name=newfoldername))
                            SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.MakeNewFolder.value, newfoldername)
                        except:
                            LOG.error(Console.NewFolderError.value.format(username=session['username']))
                    else:
                        flash(Mess.FolderExist.value)

            # rename folder
            if form.submitname.data == True:
                if req_path == "":
                    flash(Mess.NotinDir.value)
                    return redirect(url_for('login'))
                else:
                    oldname = ""
                    Newname = form.getname.data
                    ReqDir = "/" + req_path
                    SelectFolder = req_path.split('/')[-1]
                    if "/" + req_path in ScanDirs:
                        OldDir = ScanDirs[ScanDirs.index(ReqDir)]
                        GetTargetIndex = ScanDirs.index(ReqDir)
                        FullOldDir = BASE_DIR + OldDir.replace("/", "\\")
                        FullNewDir = BASE_DIR + "\\" + req_path.replace(SelectFolder, Newname).replace("/", "\\")
                        if os.path.exists(FullNewDir):
                            flash(Mess.FolderExist.value)
                        else:
                            os.rename(FullOldDir, FullNewDir)
                            ScanDirs[GetTargetIndex] = "/" + req_path.replace(SelectFolder, Newname)
                            FullNewDir.replace(BASE_DIR, "").replace("/","\\")
                            flash(Mess.RenameSuccMSG.value)
                            return redirect(url_for('login'))
                        

                    #     if os.path.exists(FD[1]) == False:
                    #         #os.rename(FD[0], FD[1])
                    #         flash(Mess.RenameSucc.value.format(new=Newname, old=oldname))
                    #         LOG.info(Console.UsernameRenameFolder.value.format(username=session['username'], old=oldname, new=Newname))
                    #         SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.RenameFolder.value, SaveLog.RenameFolderDetail.value.format(old=oldname, new=Newname))
                    #     else:
                    #         flash(Mess.FolderExist.value)
                    # except:
                    #     LOG.error(Console.ErrorRenameFolder.value.format(username=session['username']))
                    # return redirect(url_for('login'))
                
            # sort files and folders
            abs_path = os.path.join(BASE_DIR, req_path)
            if not os.path.exists(abs_path):
                return render_template('message.html', titlemsg=Mess.PageNotFoundTitle.value, detailmsg=Mess.PageNotFoundDetail.value, image="exist")
            if os.path.isdir(abs_path):
                for item in os.listdir(abs_path):
                    item_path = os.path.join(abs_path, item)
                    if os.path.isfile(item_path):
                        FS.append(item)
                    elif os.path.isdir(item_path):
                        FM.append(item)
            return render_template('index.html',folders=SortData(FM), files=SortData(FS), current_path=req_path, form=form, perm=perm[accounts[session['username']]['id']])
        else:
            return redirect(url_for('login'))

    # Delete file
    @app.route('/delete', methods=['POST'])
    def delete_file():
        session.pop('_flashes', None)
        req_path = request.form.get('path', '')
        file_name = request.form.get('file_name')
        abs_path = str(os.path.join(app.config['UPLOAD_FOLDER'], req_path, file_name))
        abs_path_thumb = os.path.join(app.config['UPLOAD_FOLDER'], req_path, "thumb_" + file_name)
        if os.path.isfile(abs_path) or os.path.isdir(abs_path):
            SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.DeleteFile.value, file_name)
            try:
                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                    os.remove(abs_path_thumb)
                    LOG.info(Console.UserDeleteFile.value.format(username=session['username'], file=file_name))
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.DeleteFile.value, file_name)
                    flash(Mess.DeleteFile.value)
                elif os.path.isdir(abs_path):
                    ScanDirs.remove(abs_path.replace(GetRootProject() + "\\" + "dir", "").replace("\\", "/"))
                    shutil.rmtree(abs_path)
                    LOG.info(Console.UserDeleteFolder.value.format(username=session['username'], folder=req_path))
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.DeleteFolder.value, req_path)
                    flash(Mess.DeleteFolder.value)
            except Exception as e:
                flash(Mess.ErorrDeleteFOF.value.format(error=str(e)))
        else:
            flash(Mess.FOFNotFound.value)
        return redirect(url_for('dir_listing', req_path=req_path))
    
    # Search page
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        FindSearch = []
        session.pop('_flashes', None)
        form = SearchForm()
        if form.validate_on_submit():
            ForSearch = form.searchtxt.data
            if ForSearch == "":
                flash(Mess.SearchEmpty.value)
                return render_template('search.html', form=form)
            else:
                if CheckLetter(ForSearch) == True:
                    for address in ScanDirs:
                        if ForSearch in address.split("/")[-1]:
                            FindSearch.append(address)
                    LOG.info(Console.UserSearch.value.format(username=session['username'], search=ForSearch))
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.Search.value, ForSearch)
                    if not FindSearch:
                        flash(Mess.NotExist.value.format(search=ForSearch))
                        return render_template('search.html', form=form, perm=perm[accounts[session['username']]['id']])
                    else:
                        return render_template('search.html', search=True, form=form, folders=sorted(FindSearch, key=extract_number), perm=perm[accounts[session['username']]['id']])
                else:
                    flash(Mess.Keyboard.value)
                    return render_template('search.html', form=form, perm=perm[accounts[session['username']]['id']])
        else:
            if "username" in session:
                if int(perm[accounts[session['username']]['id']]['search']) == 0:
                    return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.NotPerm.value, image='not')
                else:
                    return render_template('search.html', form=form, perm=perm[accounts[session['username']]['id']])
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
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.ChangePassword.value, "****")
                    flash(Mess.ChangepasswordSuccess.value)
                else:
                    flash(Mess.WrongPasswordPre.value)
        # User Register
        if form.register.data == True:
            username = form.username.data
            password = form.password.data
            repassword = form.repassword.data
            if username in accounts:
                flash(Mess.UsernameExist.value)
            else:
                if username == "" or password == "" or repassword == "":
                    flash(Mess.EmptyFields.value)
                else:
                    if CheckLetter(username) == True:
                        if password == repassword:
                            SQL.Register(username, PassGenerate(username, password))
                            flash(Mess.RegisterSuccess.value)
                            LOG.info(Console.RegisterSuccess.value.format(admin=session['username'], username=username))
                            SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.UserRegister.value, username)
                            return redirect(url_for('panel'))
                        else:
                            flash(Mess.PasswordNotMatch.value)
                    else:
                        flash(Mess.Keyboard.value)
                        
        # Clear Log
        if form.clearlog.data == True:
            LOG.clearlogfile(session['username'])
            SQL.RemoveAllLogs()
            flash(Mess.ClearLog.value)
            return render_template('panel.html', form=form, perm=perm[accounts[session['username']]['id']])
        
        # delete username
        if form.deleteusername.data == True:
            selectusername = form.selectuserdelete.data
            if selectusername in accounts:
                if selectusername == "admin":
                    flash(Mess.DeleteAdmin.value)
                else:
                    SQL.DeleteUsername(selectusername)
                    flash(Mess.DeleteUsername.value.format(username=selectusername))
                    LOG.info(Console.DelUsername.value.format(admin=session['username'], username=selectusername))
                    SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.DeleteUser.value, selectusername)
                    return redirect(url_for('panel'))
            
        # Restart core
        if form.restartcore.data == True:
            SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.ReloadCore.value, "****")
            restart()

        # Make thumbnails
        if form.makeit.data == True:
            thread(Scan())
        
        # Check sessions
        if "username" in session:
            form.selectuserdelete.choices = SQL.ReadUsernames()
            return render_template('panel.html', form=form, perm=perm[accounts[session['username']]['id']])
        else:
            return redirect(url_for('login'))
         
    # Log page
    @app.route('/log', methods=['GET', 'POST'])
    def log():
        SLog = []
        form = SIL()
        SDate = []
        if form.submit.data == True:
            session.pop('_flashes', None)
            GetUser = form.SU.data
            start_date = form.StartDate.data
            end_date = form.EndDate.data
            if start_date == "" or end_date == "":
                flash(Mess.EmptyDate.value)
            else:
                if CheckDateFormat(start_date) == False or CheckDateFormat(end_date) == False:
                    flash(Mess.WrongDateFormat.value)
                else:
                    SLog = SQL.ReadLogs(GetUser)
                    SDate = FLBD(SLog, start_date.replace("-", ""), end_date.replace("-", ""))
        if "username" in session:
            if int(perm[accounts[session['username']]['id']]['log']) == 0:
                return render_template('message.html', titlemsg=Mess.Warningtitle.value, detailmsg=Mess.NotPerm.value, image="not")
            else:
                form.SU.choices = SQL.ReadUsernames()
                return render_template('log.html', logs=SDate, form=form)
        else:
            return redirect(url_for('login'))

    # user logout
    @app.route("/logout")
    def logout():
        try:
            SQL.UpdateUserOnline(session["username"], 0)
            accounts[session["username"]]['logedin'] = 0
            LOG.debug(Console.Logout.value.format(username=session["username"]))
            SQL.InsertLog(len(SQL.ReadLogs(username="1")) + 1, GetTime(), session['username'], SaveLog.LO.value ,SaveLog.LogOut.value)
            session.clear()
            return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))