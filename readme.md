# view_permission



## 0.简介

​		View_Permission 简称 vp，这是一个轻量的Django权限管理插件，可以通过组，管理用户对视图请求的限制，不仅仅可以直接限制用户请求，还可以通过用户传入的参数选择性的限制。


## 1.初始化

### 导包

``` bash
pip install django
pip install djangorestframework
pip install pandas
pip install numpy
pip install streamlit
```

### Settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    'view_permission'
]
```

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'view_permission.permissions.permission_middleware.PermissionCountMiddleware',  # 访问次数限制中间件
    'view_permission.permissions.permission_middleware.PermissionParamMiddleware',  # 访问参数限制中间件
]
```

#### 初始化视图和基本权限
```bash
python manage.py vpinit
```



## 2.Management

```bash
python manage.py
```

```bash
[view_permission]
    vpbasepermissioninit    # 只初始化基本权限
    vpcreatevip # 创建VIP
    vpinit  # 初始化权限和视图
    vpremoveallvip  # 删除所有VIP
    vpremovevip # 删除VIP
    vprunserver # 开启参数可视化界面
```



## 3.VP_Settings

#### model_setting

``` python
GROUP_MODEL_NAME = "vp_groups"	# 存储分组的表名
PERMISSION_MODEL_NAME = "vp_permissions"	# 存储权限的表名
VIEW_MODEL_NAME = "vp_views"	# 存储视图的表名
USER_TO_GROUP_FIELD_NAME = "view_group"  # 用户表中的权限外键名
```



#### app_setting

```python
EXCLUDE_APP_NAMES = []	# 在执行 python manage.py vpinit 的时候
```



#### vip_setting

```python
VIP_DIR = []	# 在执行 python manage.py vpvipinit 的时候会扫描该文件中的vip类
```



#### view_setting

默认可以接受8种 http_method，然而你也可以在 settings.py 中设置你想要限制的 http_method

```python
HTTP_METHOD_NAMES = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
```



## 4.VP_GROUP 默认权限组

### NON_LOGIN 未登陆组

在未登录的情况下默认为这个组。



### BASE_USER 基础组

在已经登陆且无任何附属VIP的情况下的默认组



### SUPER_USER 超级用户组

当用户的 is_superuser 被置于 true 的情况下，无条件附属该组，该组无视任何权限限制，也不会通过 req_info 给 request 传输任何参数。





## 5.Permission 权限

​		这里开始是该项目的特点所在：**ParamLimit** 和 **ReqInfo**，这两个功能可以基于权限通过传参限制请求，以及向request传输参数。



### ParamLimit 参数限制

``` json
{"a__lte": 10, "b__gt": 100}
```



​		**ParamLimit** 是权限表中的一个字段，它是一个 **Json** 字符串，ParamLimit中的键（key）为**字符串类型**，每一个键值对除了键（key）和值（value），还有一个参数：运算符号（**symbol**)，常用的有：大于（gt），小于（lt），在json字符串的键值中**最后一个双下划线**（__)后的字符串标志着运算符号。详细的运算符号可以在后面详细讲解。

​		直接操作Json字段很容易出现兼容性错误，所以，我们可以在 vp_server 后台系统中具体操作。进入后台系统的方式如下：

```base
python manage.py vprunserver
```



### ReqInfo 权限传参信息

```json
{"sub_user_limit": "5"}
```

```base
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.2.118:8501

```



​		**Reqinfo** 是权限表中的一个字段，它是一个 **Json** 字符串，ReqInfo中的键值对都是**字符串类型**，该Json字符串在通过该权限后解析后传入作为参数传输给request，你可以通过**request.vp_info**来获取解析过的json数据。

##### view.py

```python
class TestView(APIView):
    def get(self, request: Request):
        return Response(data=[request.vp_info])
```



## 6.Symbol 运算符号

​		运算符号（symbol）一般用于对请求参数进行限制时所使用的，其源代码可以在 view_permission.permissions.symbol 中的 SymbolMap可以看到。

```python
SymbolMap = {
    "equal": Equal,
    "lt": Lt,
    "gt": Gt,
    "lte": Lte,
    "gte": Gte,
    "in": In,
    "allow": Allow
}
```

