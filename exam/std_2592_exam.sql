-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Июн 10 2024 г., 14:54
-- Версия сервера: 5.7.26-0ubuntu0.16.04.1
-- Версия PHP: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `std_2592_exam`
--

-- --------------------------------------------------------

--
-- Структура таблицы `book_category`
--

CREATE TABLE `book_category` (
  `book_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `book_category`
--

INSERT INTO `book_category` (`book_id`, `category_id`) VALUES
(101, 1),
(102, 1),
(103, 2),
(104, 2),
(105, 3),
(106, 3),
(107, 4),
(108, 4);

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`id`, `category_name`) VALUES
(2, 'Classics'),
(4, 'Drama'),
(3, 'Fantasy'),
(1, 'Fiction');

-- --------------------------------------------------------

--
-- Структура таблицы `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `comment` text NOT NULL,
  `date_posted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `feedback`
--

INSERT INTO `feedback` (`id`, `score`, `comment`, `date_posted`, `book_id`, `user_id`) VALUES
(1, 5, 'Amazing book!', '2024-06-18 10:00:00', 101, 1),
(2, 4, 'Very interesting.', '2024-06-18 10:30:00', 102, 2),
(3, 3, 'It was okay.', '2024-06-18 11:00:00', 103, 3),
(4, 5, 'Loved it!', '2024-06-18 11:30:00', 104, 1),
(5, 2, 'Not my type.', '2024-06-18 12:00:00', 105, 2),
(6, 4, 'Great read.', '2024-06-18 12:30:00', 106, 3),
(7, 5, 'Fantastic!', '2024-06-18 13:00:00', 107, 1),
(8, 3, 'Good, but long.', '2024-06-18 13:30:00', 108, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `files`
--

CREATE TABLE `files` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `hash` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `files`
--

INSERT INTO `files` (`id`, `file_name`, `mime_type`, `hash`) VALUES
('a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 'war_and_peace.jpg', 'image/jpeg', '1234567890abcdef1234567890abcdef'),
('a7b8c9d0-1e2f-3a4b-5c6d-7e8f9a0b1c2d', 'the_hobbit.jpg', 'image/jpeg', 'abcdef12345678907890abcdef12345678'),
('b2c3d4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 'moby_dick.jpg', 'image/jpeg', 'abcdef1234567890abcdef1234567890'),
('b8c9d0e1-2f3a-4b5c-6d7e-8f9a0b1c2d3e', 'crime_and_punishment.jpg', 'image/jpeg', '4567890abcdef123456abcdef12345678'),
('c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f', '1984.jpg', 'image/jpeg', '7890abcdef1234567890abcdef123456'),
('d4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a', 'great_gatsby.jpg', 'image/jpeg', '4567890abcdef1234567890abcdef1234'),
('e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b', 'mockingbird.jpg', 'image/jpeg', 'abcdef7890abcdef1234567890abcdef12'),
('f6a7b8c9-0d1e-2f3a-4b5c-6d7e8f9a0b1c', 'pride_and_prejudice.jpg', 'image/jpeg', '7890abcdef1234567890abcdefabcdef');

-- --------------------------------------------------------

--
-- Структура таблицы `new_books`
--

CREATE TABLE `new_books` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `publication_year` varchar(4) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `writer` varchar(100) NOT NULL,
  `pages` int(11) NOT NULL,
  `total_ratings` int(11) NOT NULL,
  `ratings_count` int(11) NOT NULL,
  `cover_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `new_books`
--

INSERT INTO `new_books` (`id`, `title`, `description`, `publication_year`, `publisher`, `writer`, `pages`, `total_ratings`, `ratings_count`, `cover_image`) VALUES
(101, 'War and Peace', 'A historical novel', '1869', 'ABC Publishing', 'Leo Tolstoy', 1225, 5, 1, 'a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d'),
(102, 'Moby Dick', 'The story of Captain Ahab', '1851', 'XYZ Publishers', 'Herman Melville', 635, 4, 1, 'b2c3d4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e'),
(103, '1984', 'A dystopian novel', '1949', 'QRS Books', 'George Orwell', 328, 3, 1, 'c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f'),
(104, 'The Great Gatsby', 'A novel set in the Jazz Age', '1925', 'LMN Publishers', 'F. Scott Fitzgerald', 218, 5, 1, 'd4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a'),
(105, 'To Kill a Mockingbird', 'A novel about racial injustice', '1960', 'TUV Books', 'Harper Lee', 281, 2, 1, 'e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b'),
(106, 'Pride and Prejudice', 'A romantic novel', '1813', 'DEF Publishers', 'Jane Austen', 432, 5, 1, 'f6a7b8c9-0d1e-2f3a-4b5c-6d7e8f9a0b1c'),
(107, 'The Hobbit', 'A fantasy novel', '1937', 'GHI Publishing', 'J.R.R. Tolkien', 310, 3, 1, 'a7b8c9d0-1e2f-3a4b-5c6d-7e8f9a0b1c2d'),
(108, 'Crime and Punishment', 'A novel about moral dilemmas', '1866', 'JKL Publishers', 'Fyodor Dostoevsky', 671, 5, 1, 'b8c9d0e1-2f3a-4b5c-6d7e-8f9a0b1c2d3e');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `given_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `surname`, `given_name`, `middle_name`, `username`, `password_hash`, `role_id`) VALUES
(1,'Smith','John','Edward','johnsmith',MD5('hash123'),1),
(2,'Doe','Jane','Ann','janedoe',MD5('hash456'),2),
(3,'Brown','Charlie','David','charliebrown',MD5('hash789'),3);

-- --------------------------------------------------------

--
-- Структура таблицы `user_roles`
--

CREATE TABLE `user_roles` (
  `id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `role_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `user_roles`
--

INSERT INTO `user_roles` (`id`, `role_name`, `role_description`) VALUES
(1, 'Admin', 'Has full access to the system, including creating and deleting books'),
(2, 'Moderator', 'Can edit book details and moderate reviews'),
(3, 'User', 'Can leave reviews');

-- --------------------------------------------------------

--
-- Структура таблицы `version_control`
--

CREATE TABLE `version_control` (
  `version` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `version_control`
--

INSERT INTO `version_control` (`version`) VALUES
('a12c34b56d78');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `book_category`
--
ALTER TABLE `book_category`
  ADD PRIMARY KEY (`book_id`,`category_id`),
  ADD KEY `fk_book_category_category_id_categories` (`category_id`);

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_categories_category_name` (`category_name`);

--
-- Индексы таблицы `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_feedback_book_id_new_books` (`book_id`),
  ADD KEY `fk_feedback_user_id_users` (`user_id`);

--
-- Индексы таблицы `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_files_hash` (`hash`);

--
-- Индексы таблицы `new_books`
--
ALTER TABLE `new_books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_new_books_cover_image_files` (`cover_image`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_users_username` (`username`),
  ADD KEY `fk_users_role_id_user_roles` (`role_id`);

--
-- Индексы таблицы `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `version_control`
--
ALTER TABLE `version_control`
  ADD PRIMARY KEY (`version`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

--
-- AUTO_INCREMENT для таблицы `new_books`
--
ALTER TABLE `new_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `book_category`
--
ALTER TABLE `book_category`
  ADD CONSTRAINT `fk_book_category_book_id_new_books` FOREIGN KEY (`book_id`) REFERENCES `new_books` (`id`),
  ADD CONSTRAINT `fk_book_category_category_id_categories` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Ограничения внешнего ключа таблицы `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `fk_feedback_book_id_new_books` FOREIGN KEY (`book_id`) REFERENCES `new_books` (`id`),
  ADD CONSTRAINT `fk_feedback_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `new_books`
--
ALTER TABLE `new_books`
  ADD CONSTRAINT `fk_new_books_cover_image_files` FOREIGN KEY (`cover_image`) REFERENCES `files` (`id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_role_id_user_roles` FOREIGN KEY (`role_id`) REFERENCES `user_roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
