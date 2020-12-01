-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-10-04 21:29:55
-- 服务器版本： 5.7.26
-- PHP 版本： 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `gon_detecter`
--

-- --------------------------------------------------------

--
-- 表的结构 `article`
--

CREATE TABLE `article` (
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `writer` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `intro` varchar(1000) COLLATE utf8_unicode_ci NOT NULL,
  `picture` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `uptime` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `comment_num` int(11) NOT NULL DEFAULT '0',
  `row_number` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `comment`
--

CREATE TABLE `comment` (
  `commenter` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `comment` varchar(5000) COLLATE utf8_unicode_ci NOT NULL,
  `uptime` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `row_number` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `eye_picture`
--

CREATE TABLE `eye_picture` (
  `uploader` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `picture` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `uptime` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `prob` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vcdr` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hcdr` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `row_number` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `userinfo`
--

CREATE TABLE `userinfo` (
  `username` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `mail` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `sex` char(2) COLLATE utf8_unicode_ci NOT NULL,
  `birth` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `place` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `userphoto` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `article` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `historypicture` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `row_number` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
