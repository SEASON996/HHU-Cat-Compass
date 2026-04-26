# 校园流浪猫管理小程序 - API 接口文档

## 基础信息

- **Base URL**: `https://api.campus-cat.com/v1`
- **认证方式**: Bearer Token（微信小程序登录后获取）
- **响应格式**: JSON
- **状态码规范**:

| 状态码 | 说明         |
| ------ | ------------ |
| 200    | 成功         |
| 201    | 创建成功     |
| 400    | 请求参数错误 |
| 401    | 未认证       |
| 403    | 无权限       |
| 404    | 资源不存在   |
| 500    | 服务器错误   |

## 通用响应结构

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1703512800000
}
```

**请求参数**:

json

```
{
  "code": "wx_authorization_code",
  "student_id": "202412340101"
}
```



**响应数据**:

json

```
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 7200,
  "user": {
    "id": 1,
    "student_id": "202412340101",
    "nickname": "猫君",
    "avatar_url": "https://...",
    "role": "user"
  }
}
```



### 1.2 获取当前用户信息

| 项目       | 内容       |
| :--------- | :--------- |
| **URL**    | `/auth/me` |
| **Method** | `GET`      |
| **Auth**   | ✅ 需要     |

------

## 模块二：猫咪管理

### 2.1 获取猫咪列表（地图标记点）

| 项目       | 内容    |
| :--------- | :------ |
| **URL**    | `/cats` |
| **Method** | `GET`   |

**请求参数**:

| 参数   | 类型    | 必填 | 说明                            |
| :----- | :------ | :--- | :------------------------------ |
| campus | string  | 是   | 校区：jiangning/xikanglu/jintan |
| status | string  | 否   | 状态筛选                        |
| limit  | integer | 否   | 每页数量，默认50                |
| offset | integer | 否   | 偏移量，默认0                   |

**响应数据**:

json

```
{
  "total": 25,
  "list": [
    {
      "id": 1,
      "cat_uuid": "CAT202412340001",
      "name": "橘座",
      "photo_url": "https://...",
      "latitude": 31.912345,
      "longitude": 118.765432,
      "status": "normal",
      "health_status": "neutered"
    }
  ]
}
```



### 2.2 获取猫咪详情

| 项目       | 内容               |
| :--------- | :----------------- |
| **URL**    | `/cats/{cat_uuid}` |
| **Method** | `GET`              |

**响应数据**:

json

```
{
  "id": 1,
  "cat_uuid": "CAT202412340001",
  "name": "橘座",
  "gender": "male",
  "age_type": "adult",
  "color": "橘色",
  "health_status": "neutered",
  "campus": "jiangning",
  "location_desc": "图书馆东侧草坪",
  "latitude": 31.912345,
  "longitude": 118.765432,
  "photo_url": "https://...",
  "status": "normal",
  "remark": "亲人，爱吃猫条",
  "created_by": {
    "student_id": "202412340101",
    "nickname": "救助君"
  },
  "created_at": "2024-12-15T10:30:00Z",
  "stats": {
    "feeding_count": 128,
    "comment_count": 15
  }
}
```



### 2.3 新增猫咪（管理员）

| 项目       | 内容               |
| :--------- | :----------------- |
| **URL**    | `/cats`            |
| **Method** | `POST`             |
| **Auth**   | ✅ 需要（仅管理员） |

**请求参数**:

json

```
{
  "name": "橘座",
  "gender": "male",
  "age_type": "adult",
  "color": "橘色",
  "health_status": "healthy",
  "campus": "jiangning",
  "location_desc": "图书馆东侧草坪",
  "latitude": 31.912345,
  "longitude": 118.765432,
  "photo_url": "https://...",
  "status": "normal",
  "remark": "亲人，爱吃猫条"
}
```



### 2.4 申请修改猫咪信息

| 项目       | 内容                              |
| :--------- | :-------------------------------- |
| **URL**    | `/cats/{cat_uuid}/modify-request` |
| **Method** | `POST`                            |
| **Auth**   | ✅ 需要                            |

**请求参数**:

json

```
{
  "field_name": "name",
  "new_value": "橘座大王"
}
```



### 2.5 审核修改申请（管理员）

| 项目       | 内容                         |
| :--------- | :--------------------------- |
| **URL**    | `/admin/reviews/{review_id}` |
| **Method** | `PUT`                        |
| **Auth**   | ✅ 需要（仅管理员）           |

**请求参数**:

json

```
{
  "status": "approved",
  "review_remark": "信息属实，已审核"
}
```



------

## 模块三：投喂打卡

### 3.1 添加投喂打卡

| 项目       | 内容        |
| :--------- | :---------- |
| **URL**    | `/feedings` |
| **Method** | `POST`      |
| **Auth**   | ✅ 需要      |

**请求参数**:

json

```
{
  "cat_id": 1,
  "feed_time": "2024-12-20T08:30:00Z",
  "food_type": "猫粮",
  "photo_url": "https://...",
  "remark": "小家伙胃口很好"
}
```



### 3.2 获取猫咪投喂记录

| 项目       | 内容                        |
| :--------- | :-------------------------- |
| **URL**    | `/cats/{cat_uuid}/feedings` |
| **Method** | `GET`                       |

**请求参数**:

| 参数      | 类型    | 必填 | 说明             |
| :-------- | :------ | :--- | :--------------- |
| page      | integer | 否   | 页码，默认1      |
| page_size | integer | 否   | 每页数量，默认20 |

------

## 模块四：救助管理

### 4.1 提交救助申请

| 项目       | 内容       |
| :--------- | :--------- |
| **URL**    | `/rescues` |
| **Method** | `POST`     |
| **Auth**   | ✅ 需要     |

**请求参数**:

json

```
{
  "cat_id": 1,
  "campus": "jiangning",
  "location_desc": "图书馆东侧草坪，猫咪左腿受伤",
  "photo_url": "https://...",
  "description": "发现橘座左腿似乎受伤，走路一瘸一拐，需要救助"
}
```



### 4.2 获取救助申请列表（管理员）

| 项目       | 内容               |
| :--------- | :----------------- |
| **URL**    | `/admin/rescues`   |
| **Method** | `GET`              |
| **Auth**   | ✅ 需要（仅管理员） |

**请求参数**:

| 参数   | 类型   | 必填 | 说明                                  |
| :----- | :----- | :--- | :------------------------------------ |
| status | string | 否   | pending/processing/completed/rejected |
| campus | string | 否   | 校区筛选                              |

### 4.3 更新救助进度（管理员）

| 项目       | 内容                          |
| :--------- | :---------------------------- |
| **URL**    | `/admin/rescues/{request_no}` |
| **Method** | `PUT`                         |
| **Auth**   | ✅ 需要（仅管理员）            |

**请求参数**:

json

```
{
  "status": "processing",
  "feedback": "已联系校园动物保护社团，正在跟进"
}
```



------

## 模块五：领养管理

### 5.1 申请领养

| 项目       | 内容         |
| :--------- | :----------- |
| **URL**    | `/adoptions` |
| **Method** | `POST`       |
| **Auth**   | ✅ 需要       |

**请求参数**:

json

```
{
  "cat_id": 1,
  "applicant_name": "张三",
  "applicant_phone": "13800000000",
  "applicant_address": "南京市鼓楼区XX小区",
  "reason": "非常喜欢猫咪，有养猫经验"
}
```



### 5.2 获取领养申请列表（管理员）

| 项目       | 内容               |
| :--------- | :----------------- |
| **URL**    | `/admin/adoptions` |
| **Method** | `GET`              |
| **Auth**   | ✅ 需要（仅管理员） |

------

## 模块六：留言互动

### 6.1 发布留言

| 项目       | 内容        |
| :--------- | :---------- |
| **URL**    | `/comments` |
| **Method** | `POST`      |
| **Auth**   | ✅ 需要      |

**请求参数**:

json

```
{
  "cat_id": 1,
  "content": "今天看到橘座了，好可爱！"
}
```



### 6.2 获取猫咪留言列表

| 项目       | 内容                        |
| :--------- | :-------------------------- |
| **URL**    | `/cats/{cat_uuid}/comments` |
| **Method** | `GET`                       |

**请求参数**:

| 参数      | 类型    | 必填 | 说明             |
| :-------- | :------ | :--- | :--------------- |
| page      | integer | 否   | 页码，默认1      |
| page_size | integer | 否   | 每页数量，默认20 |

### 6.3 点赞留言

| 项目       | 内容                          |
| :--------- | :---------------------------- |
| **URL**    | `/comments/{comment_id}/like` |
| **Method** | `POST`                        |
| **Auth**   | ✅ 需要                        |

------

## 模块七：校区与地图

### 7.1 获取校区列表

| 项目       | 内容        |
| :--------- | :---------- |
| **URL**    | `/campuses` |
| **Method** | `GET`       |

**响应数据**:

json

```
{
  "list": [
    {
      "code": "jiangning",
      "name": "江宁校区",
      "center": {"lat": 31.912345, "lng": 118.765432},
      "zoom": 15
    },
    {
      "code": "xikanglu",
      "name": "西康路校区",
      "center": {"lat": 32.054321, "lng": 118.765432},
      "zoom": 15
    },
    {
      "code": "jintan",
      "name": "金坛校区",
      "center": {"lat": 31.723456, "lng": 119.567890},
      "zoom": 15
    }
  ]
}
```



### 7.2 获取校区猫咪统计

| 项目       | 内容                            |
| :--------- | :------------------------------ |
| **URL**    | `/campuses/{campus_code}/stats` |
| **Method** | `GET`                           |

**响应数据**:

json

```
{
  "total_cats": 25,
  "need_help": 3,
  "adopted": 2,
  "missing": 1,
  "total_feeding": 1024,
  "total_comments": 89
}
```



------

## 接口汇总表

| 模块 | 方法 | URL                         | 说明         | 认证   |
| :--- | :--- | :-------------------------- | :----------- | :----- |
| 认证 | POST | /auth/login                 | 登录         | 否     |
| 认证 | GET  | /auth/me                    | 获取当前用户 | 是     |
| 猫咪 | GET  | /cats                       | 获取猫咪列表 | 否     |
| 猫咪 | GET  | /cats/{uuid}                | 获取猫咪详情 | 否     |
| 猫咪 | POST | /cats                       | 新增猫咪     | 管理员 |
| 猫咪 | POST | /cats/{uuid}/modify-request | 申请修改     | 是     |
| 审核 | PUT  | /admin/reviews/{id}         | 审核修改     | 管理员 |
| 投喂 | POST | /feedings                   | 添加打卡     | 是     |
| 投喂 | GET  | /cats/{uuid}/feedings       | 打卡记录     | 是     |
| 救助 | POST | /rescues                    | 提交申请     | 是     |
| 救助 | GET  | /admin/rescues              | 申请列表     | 管理员 |
| 救助 | PUT  | /admin/rescues/{no}         | 更新进度     | 管理员 |
| 领养 | POST | /adoptions                  | 申请领养     | 是     |
| 领养 | GET  | /admin/adoptions            | 领养列表     | 管理员 |
| 留言 | POST | /comments                   | 发布留言     | 是     |
| 留言 | GET  | /cats/{uuid}/comments       | 留言列表     | 否     |
| 留言 | POST | /comments/{id}/like         | 点赞         | 是     |
| 地图 | GET  | /campuses                   | 校区列表     | 否     |
| 地图 | GET  | /campuses/{code}/stats      | 校区统计     | 否     |