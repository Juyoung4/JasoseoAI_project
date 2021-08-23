/* schema.sql => 테이블 관련 파일 */

DROP TABLE IF EXISTS users;

/*USER 생성
ID, 사용자 이름, 비밀번호
*/
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(10) UNIQUE NOT NULL, /*TEXT, varchar(10)*/
    passwd varchar(20) NOT NULL,
    create_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* POST 생성
=> ID, 사용자_ID, 생성일, 제목, 내용
*/
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    writer_id INTEGER NOT NULL, /*users의 id 필요 - foreign key*/
    title varchar(30) NOT NULL,
    content varchar(800) NOT NULL,
    create_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (writer_id) REFERENCES users (id) /*외부 키 */
);