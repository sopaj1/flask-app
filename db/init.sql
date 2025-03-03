CREATE DATABASE IF NOT EXISTS posts;
USE posts;

CREATE TABLE IF NOT EXISTS blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    story TEXT NOT NULL,
    image VARCHAR(255) NULL
);
