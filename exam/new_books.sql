-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Июн 10 2024 г., 23:27
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

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `new_books`
--
ALTER TABLE `new_books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_new_books_cover_image_files` (`cover_image`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `new_books`
--
ALTER TABLE `new_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `new_books`
--
ALTER TABLE `new_books`
  ADD CONSTRAINT `fk_new_books_cover_image_files` FOREIGN KEY (`cover_image`) REFERENCES `files` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
