CREATE TABLE user (
	id CHAR(36) NOT NULL, 
	email VARCHAR(320) NOT NULL, 
	hashed_password VARCHAR(1024) NOT NULL, 
	is_active BOOL NOT NULL, 
	is_superuser BOOL NOT NULL, 
	is_verified BOOL NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	is_deleted BOOL NOT NULL, 
	CONSTRAINT pk_user PRIMARY KEY (id)
)

CREATE TABLE category (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	is_deleted BOOL NOT NULL, 
	CONSTRAINT pk_category PRIMARY KEY (id), 
	CONSTRAINT uq_category_name UNIQUE (name)
)

CREATE TABLE tag (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	is_deleted BOOL NOT NULL, 
	CONSTRAINT pk_tag PRIMARY KEY (id), 
	CONSTRAINT uq_tag_name UNIQUE (name)
)

CREATE TABLE article (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	title VARCHAR(200) NOT NULL, 
	content TEXT NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	author_id CHAR(36) NOT NULL, 
	category_id INTEGER, 
	is_deleted BOOL NOT NULL, 
	CONSTRAINT pk_article PRIMARY KEY (id), 
	CONSTRAINT fk_article_author_id_user FOREIGN KEY(author_id) REFERENCES user (id) ON DELETE CASCADE, 
	CONSTRAINT fk_article_category_id_category FOREIGN KEY(category_id) REFERENCES category (id) ON DELETE SET NULL
)

CREATE TABLE article_tag (
	article_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	CONSTRAINT pk_article_tag PRIMARY KEY (article_id, tag_id), 
	CONSTRAINT fk_article_tag_article_id_article FOREIGN KEY(article_id) REFERENCES article (id) ON DELETE CASCADE, 
	CONSTRAINT fk_article_tag_tag_id_tag FOREIGN KEY(tag_id) REFERENCES tag (id) ON DELETE CASCADE
)


CREATE TABLE article_like (
	article_id INTEGER NOT NULL, 
	user_id CHAR(36) NOT NULL, 
	CONSTRAINT pk_article_like PRIMARY KEY (article_id, user_id), 
	CONSTRAINT fk_article_like_article_id_article FOREIGN KEY(article_id) REFERENCES article (id) ON DELETE CASCADE, 
	CONSTRAINT fk_article_like_user_id_user FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
)

CREATE TABLE comment (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	content TEXT NOT NULL, 
	created_at DATETIME NOT NULL, 
	author_id CHAR(36) NOT NULL, 
	article_id INTEGER NOT NULL, 
	updated_at DATETIME NOT NULL, 
	is_deleted BOOL NOT NULL, 
	CONSTRAINT pk_comment PRIMARY KEY (id), 
	CONSTRAINT fk_comment_author_id_user FOREIGN KEY(author_id) REFERENCES user (id) ON DELETE CASCADE, 
	CONSTRAINT fk_comment_article_id_article FOREIGN KEY(article_id) REFERENCES article (id) ON DELETE CASCADE
)