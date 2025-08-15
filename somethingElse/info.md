# 博客系统数据库结构与关系

## 1. 数据表结构

### `user` 表
来源：`User(SQLAlchemyBaseUserTableUUID, Base, CRUDMixin)`
- **PK**: `id` (UUID)
- 其它字段来自 FastAPI Users（email、hashed_password、is_active、is_superuser、is_verified 等）

---

### `category` 表
- **PK**: `id` (int)
- **name** (str, 唯一)

关系：
- **一对多** → `article.category_id`（一个分类下多篇文章）

---

### `article` 表
- **PK**: `id` (int)
- **title** (str)
- **content** (text)
- **created_at** (datetime)
- **updated_at** (datetime)
- **FK**: `author_id` → `user.id` (UUID)
- **FK**: `category_id` → `category.id` (int, 可空)

关系：
- 多对一 → `user`（文章作者）
- 多对一 → `category`（分类）
- 多对多 → `tag`（通过 `article_tag`）
- 多对多 → `user`（点赞用户，通过 `article_like`）
- 一对多 → `comment`（文章评论）

---

### `tag` 表
- **PK**: `id` (int)
- **name** (str, 唯一)

关系：
- 多对多 → `article`（通过 `article_tag`）

---

### `comment` 表
- **PK**: `id` (int)
- **content** (text)
- **created_at** (datetime)
- **FK**: `author_id` → `user.id` (UUID)
- **FK**: `article_id` → `article.id` (int)

关系：
- 多对一 → `user`（评论作者）
- 多对一 → `article`（所属文章）

---

### `article_tag` 表（多对多中间表）
- **PK**: `article_id` (int)
- **PK**: `tag_id` (int)

关系：
- 多对多 → `article` ↔ `tag`

---

### `article_like` 表（多对多中间表）
- **PK**: `article_id` (int)
- **PK**: `user_id` (UUID)

关系：
- 多对多 → `article` ↔ `user`（点赞功能）

---

## 2. 关系总览（ER 概要图）

### user (UUID PK)
| relation              | detail|
|-|-|
| ├──< article.author_id || 
| │ | ├──< comment.article_id >── user (评论作者)|
| │ | ├──< article_tag.article_id >── tag|
| │ | └──< article_like.article_id >── user (点赞用户)|
| │ ||
| └──< comment.author_id ||


## 3. 关系类型总结

| 关系类型 | 表之间              | 中间表        | 说明 |
|----------|--------------------|--------------|------|
| 多对一   | article → user     | 无           | 每篇文章只有一个作者 |
| 多对一   | comment → user     | 无           | 每条评论只有一个作者 |
| 多对一   | article → category | 无           | 文章归属于一个分类 |
| 多对一   | comment → article  | 无           | 评论属于某篇文章 |
| 多对多   | article ↔ tag      | article_tag  | 一篇文章可有多个标签 |
| 多对多   | article ↔ user     | article_like | 用户可点赞多篇文章 |

