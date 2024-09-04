import enum

class Mess(enum.Enum):
    UploadSucc = '{count} فایل آپلود شد'
    FolderSucc = 'فولدر با موفقیت ساخته شد'
    DeleteFile = 'فایل با موفقیت پاک شد'
    DeleteFolder = 'پوشه با موفقیت پاک شد'
    ErorrDeleteFOF = 'فایل یا فلدر پاک نشد'
    FOFNotFound = 'فایل یا فلدر پیدا نشد'
    EmptyFields = 'فیلد خالی است'
    WrongPassword = 'رمز عبور اشتباه است'
    WrongPasswordOrEmail = 'نام کاربری یا رمز عبور اشتباه است'
    ChangepasswordError = 'تغییر رمز عبور انجام نشد'
    ChangepasswordSuccess = 'تغییر رمز عبور انجام شد'
    UserNotExist = 'نام کاربری موجود نیست'
    PageNotFoundTitle = '404'
    PageNotFoundDetail = 'صفحه ایی که دنبال آن هستید پیدا نشد'
    Warningtitle = 'اخطار'
    WarningDetail = 'در سرور خطا رخ داده است'
    RegisterSuccess = 'یوزر با موفقیت ثبت نام شد'
    UsernameExist = 'این نام کاربری قبلا ساخته شده است'
    SearchEmpty = 'فیلد جست و جو خالی است'
    FileNotFound = 'فایلی پیدا نشد'
    FolderExist = 'پوشه با این اسم ساخته شده است'
    NotExist = '{search} پیدا نشد '
    AccountLock = 'اکانت شما قفل شده است'
    PasswordNotMatch = 'پسورد ها مثل هم نیستند'
    ChangePermission= 'تغییر دسترسی انجام شد'
    DeleteUsername = '{username} با موفقیت پاک شد'
    DeleteAdmin = 'یوزر ادمین را نمی توانید پاک کنید'
    ClearLog = 'لاگ با موفقیت پاک شد'
    EmptyFolder = 'اسم پوشه را انتخاب کنید'
    SelectPermiss = 'لطفا سطح دسترسی را انتخاب کنید'
    NotinDir = 'اول وارد پوشه شوید سپس نام پوشه را تغییر دهید'
    FileNameEmpty = 'اسم فایل را انتخاب گنید'

class Console(enum.Enum):
    ServerRunning = 'Server is running on {ip}:{port}'
    ServerError = 'Server cannot run'
    Logout = 'Account {username} logout'
    LoginSuccess = 'Account {username} loged in'
    RegisterSuccess = 'Registeration successfuly for {username}'
    RegisterFailed = 'Registeration Failed'
    ConnSQLError = 'Error while connecting to MySQL {ip}'
    ConnSQLSuccess = 'Connected to MySQL Server {ip}'
    Vistors = 'Someone, visit with this ip address: {ip}'
    LogClrear = 'Log.txt file hase been cleaned by {username}'
    Load = 'Loaded {number} from {table} in {time} second(s)'
    Error = 'Somethings not working to get client ip'
    Admin = 'Admin authorized with {ip} to open admin page'
    DebugOff = 'Debug mode is Off'
    DebugOn = 'Debug mode is ON'
    RemoveAllCaptchas = 'Captcha iamge deleted Successfuly'
    NetworkInfo = 'Server local ip address is {ip}'
    SetPermission = '{admin} change permission for {username} to {permission}'
    DelF = 'User {username} delete FOF {FOF} from {from}'
    DelUsername = 'User {admin} delete {username}'
    UserSearch = 'User {username} search for word: {search}'
    UserDeleteFolder = 'User {username} delete folder: {folder}'
    UserDeleteFile = 'User {username} delete file: {file}'
    UserMakeFolder = 'User {username} make new folder: {name}'
    UsernameRenameFolder = 'User {username} rename folder from {old} to {new}'
    CompressError = 'Error while convert photo'
    DirFolder = 'name "dir" folder not exist in root'
    NewFolderError = 'error while making a new folder for user {username}'
    ScanForThumbnail = 'System generate thumbnail for {counter} image fle'
    ErrorRenameFolder = 'Error while rename folder for user {username}'

class Objects(enum.Enum):
    Search = 'جستجو'
    SearchFiles = 'جستجو فایل ها'
    username = 'نام کاربری'
    password = 'رمز عبور'
    repassword = 'تکرار رمز عبور'
    login = "ورود"
    register = 'ثبت نام'
    submit = "تایید"
    clear = 'پاک کردن لاگ'
    upload = 'آپلود'
    delete = "پاک کردن"
    restart = 'ری استارت'
    selectpermis = 'انتخاب سطح دسترسی'
    ChangePass = 'تغییر رمز عبور'
    OldPass = 'رمز عبور فعلی'
    NewPass = 'رمز عبور جدید'
    ReNewPass = 'تکرار رمز عبور جدید'
    FolderName = 'نام پوشه'
    SubmitChangeName = 'تغییر نام'
    NewFolder = 'پوشه جدید'
    ChooseFile = 'انتخاب فایل'
    FilesName = 'اسم فایل'

class SelectUser(enum.Enum):
    choose = 'انتخاب'
    admin = 'ادممین'
    user = 'عادی'
    Guest = 'مهمان'
    Lock = 'قفل'

class SaveLog(enum.Enum):
    MakeNewFolder = 'ساخت پوشه جدید'
    DeleteFile = 'حذف کردن فایل'
    DeleteFolder = 'حذف کردن پوشه'
    FileUpload = 'آپلود'
    RenameFolder = 'تغییر نام پوشه'
    RenameFolderDetail = 'از {old} به {new}'