/* schema.sql => 테이블 관련 파일 */

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS clusters;
DROP TABLE IF EXISTS jasosuls;

/*USER 생성
ID, 사용자 이름, 비밀번호
*/
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(10) UNIQUE NOT NULL, /*TEXT, varchar(10)*/
    passwd varchar(20) NOT NULL,
    create_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

/* 자소서 생성
=> ID, 사용자_ID, 자소서제목, 회사명, 생성일
*/
CREATE TABLE clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    writer_id INTEGER NOT NULL, /*users의 id 필요 - foreign key*/
    title varchar(150) NOT NULL,
    company varchar(50) NOT NULL,
    create_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (writer_id) REFERENCES users (id) ON DELETE CASCADE
);

/* 한 자소서에 대한 질문-내용 생성
=> ID, 사용자_ID, 자소서질문, 자소서내용, 생성일, 클러스터id
*/
CREATE TABLE jasosuls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    writer_id INTEGER NOT NULL, /*users의 id 필요 - foreign key*/
    cluster_id INTEGER NOT NULL, /*clusters의 id 필요 - foreign key*/
    question varchar(200) NOT NULL, /*자소서 질문*/
    content varchar(1500) NOT NULL, /*자소서 내용*/
    create_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (writer_id) REFERENCES users (id) ON DELETE CASCADE, /*외부 키 */
    FOREIGN KEY (cluster_id) REFERENCES clusters (id) ON DELETE CASCADE/*외부 키 */
);