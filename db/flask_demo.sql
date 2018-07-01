-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 18, 2018 at 10:20 AM
-- Server version: 5.7.22-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_demo`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('af2942ff687e');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `logo` varchar(250) DEFAULT NULL,
  `logo_path` varchar(255) DEFAULT NULL,
  `status` enum('A','D') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `parent_id`, `logo`, `logo_path`, `status`, `created_at`, `updated_at`) VALUES
(1, 'watches', 0, NULL, NULL, 'A', '2018-06-13 02:20:50', NULL),
(2, 'bags', 1, NULL, NULL, 'A', '2018-06-13 06:22:40', NULL),
(3, 'dresses', 0, NULL, NULL, 'A', '2018-06-13 04:40:30', NULL),
(4, 'sunglasses', 0, NULL, NULL, 'A', '2018-06-13 05:29:15', NULL),
(5, 'footware', 0, NULL, NULL, 'A', '2018-06-13 16:18:29', NULL),
(6, 'subCat 2', 5, NULL, NULL, NULL, '2018-06-13 12:24:26', '2018-06-13 12:37:56'),
(7, 'abc', 5, NULL, NULL, 'A', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `colors`
--

CREATE TABLE `colors` (
  `id` int(11) NOT NULL,
  `color_code` varchar(255) DEFAULT NULL,
  `status` enum('A','D') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `colors`
--

INSERT INTO `colors` (`id`, `color_code`, `status`) VALUES
(1, '#4567889', 'D'),
(2, '#000000', 'A'),
(3, '#4a86e8', 'A'),
(4, '#00ff00', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `text` text,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `unread` tinyint(1) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`id`, `title`, `text`, `timestamp`, `unread`, `user_id`) VALUES
(1, 'test', 'sdnfsbdshjf bghdvdsh gvdsghf dsfg', '2018-06-07 11:29:58', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `sub_cat_id` int(11) NOT NULL DEFAULT '0',
  `size_id` int(11) NOT NULL DEFAULT '0',
  `color_id` int(11) NOT NULL DEFAULT '0',
  `p_name` varchar(250) DEFAULT NULL,
  `p_descriptions` text,
  `p_price` float NOT NULL DEFAULT '0',
  `p_discount_percent` float NOT NULL DEFAULT '0',
  `is_feature` enum('Y','N') NOT NULL DEFAULT 'N',
  `is_banner_appear` enum('Y','N') NOT NULL DEFAULT 'N',
  `banner_image` varchar(255) DEFAULT NULL,
  `banner_image_path` varchar(255) DEFAULT NULL,
  `default_image` varchar(255) DEFAULT NULL,
  `default_image_path` varchar(255) DEFAULT NULL,
  `created_by` int(11) NOT NULL DEFAULT '0',
  `status` enum('A','D') DEFAULT NULL,
  `total_review` int(11) NOT NULL DEFAULT '0',
  `total_rating` int(11) DEFAULT '0',
  `total_rating_points` float NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `cat_id`, `sub_cat_id`, `size_id`, `color_id`, `p_name`, `p_descriptions`, `p_price`, `p_discount_percent`, `is_feature`, `is_banner_appear`, `banner_image`, `banner_image_path`, `default_image`, `default_image_path`, `created_by`, `status`, `total_review`, `total_rating`, `total_rating_points`, `created_at`, `updated_at`) VALUES
(1, 3, 0, 0, 2, 'test 1', 'vfsaghdfsah dsghjsf dshjf dshjf bds', 10000, 10, 'Y', 'Y', 'f0af2892a2d84e86a828d50646ea67ba.jpg', 'uploads/f0af2892a2d84e86a828d50646ea67ba.jpg', 'b733903dcf9240bc89113c9b0c6b563f.jpeg', 'uploads/b733903dcf9240bc89113c9b0c6b563f.jpeg', 1, 'A', 0, 0, 0, '2018-06-13 06:48:20', NULL),
(2, 3, 0, 0, 0, 'test 2', 'gsdfxsa dg sadfsgad', 10001, 10, 'Y', 'Y', 'b47a4cf988504149b989034925a34a65.jpg', 'uploads/b47a4cf988504149b989034925a34a65.jpg', 'ab49c29f055e419db55aa473a0b182f0.jpg', 'uploads/ab49c29f055e419db55aa473a0b182f0.jpg', 1, 'A', 0, 0, 0, '2018-06-13 06:49:23', NULL),
(3, 3, 0, 0, 0, 'test 3', 'gfgdfgfdg dfgd', 10002, 10, 'N', 'Y', 'f61311638dec4ce08a0bd65b8cd6c5e8.jpg', 'uploads/f61311638dec4ce08a0bd65b8cd6c5e8.jpg', '8f968572264f417681f7e30836f705e6.jpg', 'uploads/8f968572264f417681f7e30836f705e6.jpg', 1, 'A', 0, 0, 0, '2018-06-13 06:50:19', '2018-06-13 07:23:35'),
(4, 1, 0, 0, 0, 'watch 1', 'dfgdg', 2000, 15, 'Y', 'Y', '973c8b79d6544efd8e802dce3d393bca.jpeg', 'uploads/973c8b79d6544efd8e802dce3d393bca.jpeg', 'a0554050c6e74bab8dd6749f63c582db.jpeg', 'uploads/a0554050c6e74bab8dd6749f63c582db.jpeg', 1, 'A', 0, 0, 0, '2018-06-13 06:56:19', NULL),
(5, 1, 0, 0, 0, 'watch 2', 'dsvfdsdg', 20001, 20, 'Y', 'Y', '8eae03a9e456467fa8a364dcfb7bf510.jpg', 'uploads/8eae03a9e456467fa8a364dcfb7bf510.jpg', 'fe3723b6416f4adfaeef6c022c891236.jpg', 'uploads/fe3723b6416f4adfaeef6c022c891236.jpg', 1, 'A', 0, 0, 0, '2018-06-13 06:57:13', NULL),
(6, 2, 0, 0, 0, 'watch 3', 'dfs dsf', 3000, 20, 'N', 'N', '0a3e5e7bf52c40bfa8891ddc0afe1cc3.jpg', 'uploads/0a3e5e7bf52c40bfa8891ddc0afe1cc3.jpg', '1d79c28c4964476aaf555e21f53792f6.jpg', 'uploads/1d79c28c4964476aaf555e21f53792f6.jpg', 1, 'A', 0, 0, 0, '2018-06-13 06:58:25', '2018-06-13 07:23:17'),
(7, 2, 0, 0, 0, 'bag 1', 'dfs', 1000, 10, 'Y', 'Y', '03a3c059bd254fe4bce9cb49cbabef00.jpg', 'uploads/03a3c059bd254fe4bce9cb49cbabef00.jpg', '362d1b0fed234fb8a7615b05e68ce461.jpg', 'uploads/362d1b0fed234fb8a7615b05e68ce461.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:13:09', NULL),
(8, 2, 0, 0, 0, 'bag 2', 'sdf', 2000, 20, 'Y', 'Y', '5b74d66b3fd04b2b90ebe59b0927ff4a.jpg', 'uploads/5b74d66b3fd04b2b90ebe59b0927ff4a.jpg', '53517ea9d499450bbfc9dc279818fdbd.jpg', 'uploads/53517ea9d499450bbfc9dc279818fdbd.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:14:12', NULL),
(9, 2, 0, 0, 0, 'bag 3', 'fsfgdg', 3000, 20, 'N', 'Y', '5f02e7bedb8a4ee29067f38882b41f3f.jpg', 'uploads/5f02e7bedb8a4ee29067f38882b41f3f.jpg', 'c963bd6d3bc0465aa4e3f77298724fac.jpg', 'uploads/c963bd6d3bc0465aa4e3f77298724fac.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:14:51', '2018-06-13 07:23:03'),
(10, 5, 0, 0, 0, 'foot ware 1', 'dfgdg', 1000, 10, 'Y', 'Y', '7c8765d750ae4e64a9672375dc2c2da6.jpg', 'uploads/7c8765d750ae4e64a9672375dc2c2da6.jpg', '0143e09aacc540f8898fad55df6c949d.jpg', 'uploads/0143e09aacc540f8898fad55df6c949d.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:16:40', NULL),
(11, 5, 0, 0, 0, 'foot ware 2', 'adsdsf', 2000, 20, 'Y', 'Y', '714f64885afb41b2ab16863f0f47af29.jpg', 'uploads/714f64885afb41b2ab16863f0f47af29.jpg', '37f8ba1ef1bd474cb01922cb152fc1d2.jpg', 'uploads/37f8ba1ef1bd474cb01922cb152fc1d2.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:17:12', NULL),
(12, 5, 0, 0, 0, 'foot ware 3', 'sdfds sdf', 3000, 20, 'N', 'N', '860d894615bc4dc982aea95a93d71b8d.jpg', 'uploads/860d894615bc4dc982aea95a93d71b8d.jpg', '5aa695ec29ff4740a26ee542e9264ecd.jpg', 'uploads/5aa695ec29ff4740a26ee542e9264ecd.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:18:04', '2018-06-13 07:22:47'),
(13, 4, 0, 0, 0, 'sunglasses 1', 'dsf', 1000, 10, 'Y', 'Y', '857bb4406cd446299d773d61f01cd6ef.jpg', 'uploads/857bb4406cd446299d773d61f01cd6ef.jpg', 'b8e89a1e723d40ae87e9e1aab6ebdd5c.jpg', 'uploads/b8e89a1e723d40ae87e9e1aab6ebdd5c.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:19:16', NULL),
(14, 4, 0, 0, 0, 'sunglasses 2', 'ssd', 2000, 20, 'Y', 'Y', 'b21b83e093cc4f1d8cff0ed4ebd71982.jpg', 'uploads/b21b83e093cc4f1d8cff0ed4ebd71982.jpg', '363858fbef684185969d26cd96b8467c.jpg', 'uploads/363858fbef684185969d26cd96b8467c.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:20:22', NULL),
(15, 4, 0, 0, 0, 'sunglasses 3', 'asd', 3000, 20, 'N', 'N', '2abe440e19a84b9c819012cbd5bc2fb7.jpg', 'uploads/2abe440e19a84b9c819012cbd5bc2fb7.jpg', '9dc8be0fa6be437fa086aaafef807fb5.jpg', 'uploads/9dc8be0fa6be437fa086aaafef807fb5.jpg', 1, 'A', 0, 0, 0, '2018-06-13 07:21:31', '2018-06-13 07:22:32'),
(16, 5, 6, 0, 3, 'sunglasses 4', 'dfsdsfsfdsf', 34, 0, 'Y', 'N', '106b859497174a5ea5e2f19193be8d69.jpg', 'uploads/106b859497174a5ea5e2f19193be8d69.jpg', 'bd3ac2c0a0d946d9bfcb73fd04d6333d.jpg', 'uploads/bd3ac2c0a0d946d9bfcb73fd04d6333d.jpg', 1, 'A', 0, 0, 0, '2018-06-14 11:46:56', '2018-06-14 12:22:13');

-- --------------------------------------------------------

--
-- Table structure for table `product_images`
--

CREATE TABLE `product_images` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL DEFAULT '0',
  `image` varchar(250) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `type` enum('D','O') NOT NULL DEFAULT 'D',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `product_ratings`
--

CREATE TABLE `product_ratings` (
  `id` int(11) NOT NULL,
  `p_id` int(11) DEFAULT '0',
  `rating_points` float NOT NULL DEFAULT '0',
  `created_by` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_ratings`
--

INSERT INTO `product_ratings` (`id`, `p_id`, `rating_points`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 16, 0, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `product_reviews`
--

CREATE TABLE `product_reviews` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL DEFAULT '0',
  `review` varchar(255) DEFAULT NULL,
  `status` enum('A','R') NOT NULL DEFAULT 'R',
  `created_by` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_reviews`
--

INSERT INTO `product_reviews` (`id`, `p_id`, `review`, `status`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 16, NULL, 'R', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sizes`
--

CREATE TABLE `sizes` (
  `id` int(11) NOT NULL,
  `size_name` varchar(255) DEFAULT NULL,
  `status` enum('A','D') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sizes`
--

INSERT INTO `sizes` (`id`, `size_name`, `status`) VALUES
(1, 'rrrrrrrrrrr', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pw_hash` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `pw_hash`) VALUES
(1, 'King Arthur', 'arthur@camelot.org', '$2a$12$LH65Euf4QpVrzFrypZbb/uzDCiLTE3hOuPquNDc9hKEvemu.P.bJu'),
(2, 'Sir Lancelot', 'lancelot@camelot.org', '$2a$12$KRP3Ap9dvE3xDfX0ZK9Gj.VFEDDirl2j9x0WR1gj9W98fSsJFOV3K'),
(3, 'Sir Robin', 'robinthebrave@camelot.org', '$2a$12$/bahjQepbBQ8d7l2fzgnNOJ5ZrNXLyCbrNPraM9TgZIofHZp.BCFu');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user_type` int(11) NOT NULL DEFAULT '0',
  `first_name` varchar(190) DEFAULT NULL,
  `last_name` varchar(190) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `username` varchar(250) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `gender` enum('M','F') DEFAULT NULL,
  `is_seller` enum('Y','N') DEFAULT NULL,
  `is_active` enum('A','D') DEFAULT NULL COMMENT '''A'' => Active | ''D'' => Delete | NULL => Inactive',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `user_type`, `first_name`, `last_name`, `email`, `username`, `password`, `phone`, `gender`, `is_seller`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 3, 'admin', 'member', 'admin@flask.com', 'admin', '$2a$12$LH65Euf4QpVrzFrypZbb/uzDCiLTE3hOuPquNDc9hKEvemu.P.bJu', '123456', 'M', 'Y', 'A', '2018-06-07 10:29:32', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_types`
--

CREATE TABLE `user_types` (
  `id` int(11) NOT NULL,
  `type` varchar(15) DEFAULT NULL,
  `type_name` varchar(190) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_types`
--

INSERT INTO `user_types` (`id`, `type`, `type_name`, `created_at`, `updated_at`) VALUES
(3, 'SADMIN', 'Super Admin', '2018-06-07 18:18:32', '2018-06-07 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL DEFAULT '0',
  `created_by` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `colors`
--
ALTER TABLE `colors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_message_title` (`title`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_images`
--
ALTER TABLE `product_images`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_ratings`
--
ALTER TABLE `product_ratings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_reviews`
--
ALTER TABLE `product_reviews`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sizes`
--
ALTER TABLE `sizes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_user_email` (`email`),
  ADD KEY `ix_user_pw_hash` (`pw_hash`),
  ADD KEY `ix_user_name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_types`
--
ALTER TABLE `user_types`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `colors`
--
ALTER TABLE `colors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `product_images`
--
ALTER TABLE `product_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `product_ratings`
--
ALTER TABLE `product_ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `product_reviews`
--
ALTER TABLE `product_reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `sizes`
--
ALTER TABLE `sizes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `user_types`
--
ALTER TABLE `user_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
