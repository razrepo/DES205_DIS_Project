CREATE DATABASE IF NOT EXISTS Designverse;

USE Designverse;

CREATE TABLE IF NOT EXISTS asset (
    asset_path VARCHAR(255) PRIMARY KEY,
    artist_name VARCHAR(100),
    artist_rollno INT,
    course_related VARCHAR(255),
    file_type VARCHAR(50),
    prof_of_course VARCHAR(100),
    asset_year INT,
    asset_description TEXT
);

INSERT INTO asset (asset_path, artist_name, artist_rollno, course_related, file_type, prof_of_course, asset_year, asset_description) VALUES
('/assets/1.jpg', 'Artist1', 123, 'Design Drawing & Visualization', 'image', 'Professor1', 2022, 'Description1'),
('/assets/2.jpg', 'Artist2', 234, 'Introduction to HCI', 'image', 'Professor2', 2023, 'Description2'),
('/assets/3.jpg', 'Artist3', 345, 'Prototyping Interactive Systems', 'image', 'Professor3', 2021, 'Description3'),
('/assets/4.jpg', 'Artist4', 456, 'Design Processes and Perspectives', 'image', 'Professor1', 2024, 'Description4'),
('/assets/5.jpg', 'Artist5', 567, 'Visual Design & Communication', 'image', 'Professor4', 2023, 'Description5');

CREATE TABLE IF NOT EXISTS comments (
    asset_path VARCHAR(255),
    comment TEXT,
    comment_by VARCHAR(100),
    comment_by_rollno INT,
    comment_date DATE,
    FOREIGN KEY (asset_path) REFERENCES asset(asset_path)
);

INSERT INTO comments(asset_path, comment, comment_by, comment_by_rollno, comment_date) VALUES
('/assets/1.jpg', 'Comment1', 'User1', 123, '2022-01-01'),
('/assets/1.jpg', 'Comment2', 'User2', 234, '2022-01-02'),
('/assets/1.jpg', 'Comment3', 'User3', 345, '2022-01-03'),
('/assets/1.jpg', 'Comment4', 'User4', 456, '2022-01-04'),
('/assets/1.jpg', 'Comment5', 'User5', 567, '2022-01-05'),
('/assets/1.jpg', 'Comment6', 'User6', 678, '2022-01-06'),
('/assets/2.jpg', 'Comment7', 'User7', 789, '2022-01-07'),
('/assets/2.jpg', 'Comment8', 'User8', 890, '2022-01-08'),
('/assets/2.jpg', 'Comment9', 'User9', 901, '2022-01-09'),
('/assets/2.jpg', 'Comment10', 'User10', 101, '2022-01-10'),
('/assets/2.jpg', 'Comment11', 'User11', 111, '2022-01-11'),
('/assets/2.jpg', 'Comment12', 'User12', 222, '2022-01-12'),
('/assets/3.jpg', 'Comment13', 'User13', 333, '2022-01-13'),
('/assets/3.jpg', 'Comment14', 'User14', 444, '2022-01-14'),
('/assets/3.jpg', 'Comment15', 'User15', 555, '2022-01-15'),
('/assets/3.jpg', 'Comment16', 'User16', 666, '2022-01-16'),
('/assets/3.jpg', 'Comment17', 'User17', 777, '2022-01-17'),
('/assets/3.jpg', 'Comment18', 'User18', 888, '2022-01-18'),
('/assets/4.jpg', 'Comment19', 'User19', 999, '2022-01-19'),
('/assets/4.jpg', 'Comment20', 'User20', 121, '2022-01-20'),
('/assets/4.jpg', 'Comment21', 'User21', 122, '2022-01-21'),
('/assets/4.jpg', 'Comment22', 'User22', 223, '2022-01-22'),
('/assets/4.jpg', 'Comment23', 'User23', 334, '2022-01-23'),
('/assets/4.jpg', 'Comment24', 'User24', 445, '2022-01-24'),
('/assets/5.jpg', 'Comment25', 'User25', 556, '2022-01-25'),
('/assets/5.jpg', 'Comment26', 'User26', 667, '2022-01-26'),
('/assets/5.jpg', 'Comment27', 'User27', 778, '2022-01-27'),
('/assets/5.jpg', 'Comment28', 'User28', 889, '2022-01-28');