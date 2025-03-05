CREATE DATABASE posts;
USE posts;

CREATE TABLE blog_posts (
    title VARCHAR(255),
    date DATE,
    story TEXT,
);

INSERT INTO blog_posts
  (title, date, story)
VALUES
  ('Fionas Birthday', '2025-17-02', 'We celebrated by going to the domes and to dinner in milwaukee'),
  ('TEST', '2020-02-02', 'TESTING');
