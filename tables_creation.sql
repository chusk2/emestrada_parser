use exams_db ;

-- Create table subjects
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject varchar(100) UNIQUE
);

-- Create table years
CREATE TABLE IF NOT EXISTS years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT UNIQUE
);

-- Create table topics
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic varchar(255) UNIQUE
);

-- Create table exams
CREATE TABLE IF NOT EXISTS exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam VARCHAR(255) UNIQUE
);

-- Create table exercise_numbers
CREATE TABLE IF NOT EXISTS exercise_numbers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exercise_number varchar(255) UNIQUE
);