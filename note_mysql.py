## CREATE USER

CREATE USER 'username'@'host' IDENTIFIED BY 'password';
CREATE USER 'test_admin'@'localhost' IDENTIFIED BY 'admin@123_S';
CREATE USER 'test_admin2'@'%' IDENTIFIED BY '';

## PRIVILEGES

GRANT privileges ON databasename.tablename TO 'username'@'host';
GRANT SELECT ON test_db.* TO 'test_admin2'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;

flush privileges;

REVOKE privilege ON databasename.tablename FROM 'username'@'host';
REVOKE SELECT ON test_db.* FROM 'test_min'@'%';

## drop user

drop user 'username'@'host';

## SHOW GRANTS
SHOW GRANTS FOR 'username'@'host'
