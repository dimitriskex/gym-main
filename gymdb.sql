-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 12 Φεβ 2024 στις 09:31:36
-- Έκδοση διακομιστή: 10.4.24-MariaDB
-- Έκδοση PHP: 8.1.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `gymdb`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `announcements`
--

CREATE TABLE `announcements` (
  `announcementid` int(11) NOT NULL,
  `announcementtext` varchar(500) DEFAULT NULL,
  `createdat` datetime DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `users_userid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `announcements`
--

INSERT INTO `announcements` (`announcementid`, `announcementtext`, `createdat`, `userid`, `users_userid`) VALUES
(1, 'Dear Members, we\'re excited to announce our new yoga classes starting next Monday! Join us for relaxing sessions every Monday and Wednesday at 6:00 PM. Don\'t miss out!', '2024-02-12 10:00:00', 1, NULL),
(2, 'Hey Fitness Enthusiasts, just a reminder that our gym will be closed this Friday for maintenance. We apologize for any inconvenience caused.', '2024-02-11 15:30:00', 2, NULL),
(3, 'Congratulations to John Smith for achieving his fitness goals and winning our latest transformation challenge! Keep up the great work, John!', '2024-02-10 08:45:00', 3, NULL),
(4, 'Attention Members, due to popular demand, we\'ve added new spinning classes on Saturdays at 9:00 AM. Book your bikes now!', '2024-02-09 18:20:00', 1, NULL),
(5, 'Get ready to sweat! Our boot camp session this Thursday will focus on high-intensity interval training (HIIT). Bring your A-game and let\'s crush those calories!', '2024-02-08 12:10:00', 2, NULL);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `gymservices`
--

CREATE TABLE `gymservices` (
  `serviceid` int(11) NOT NULL,
  `servicename` varchar(50) DEFAULT NULL,
  `trainers_trainerid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `gymservices`
--

INSERT INTO `gymservices` (`serviceid`, `servicename`, `trainers_trainerid`) VALUES
(1, 'Weight Training', 1),
(2, 'Yoga Classes', 2),
(3, 'Cardio Workout', 1);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `programs`
--

CREATE TABLE `programs` (
  `programid` int(11) NOT NULL,
  `programname` varchar(50) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `programtime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `programs`
--

INSERT INTO `programs` (`programid`, `programname`, `capacity`, `programtime`) VALUES
(1, 'Morning Yoga', 15, '2024-02-12 08:00:00'),
(2, 'Evening Cardio', 20, '2024-02-13 18:00:00'),
(3, 'Weekend Bootcamp', 10, '2024-02-15 10:00:00');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `reservations`
--

CREATE TABLE `reservations` (
  `reservationid` int(11) NOT NULL,
  `userid` int(11) DEFAULT NULL,
  `programid` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `gymservices_serviceid` int(11) DEFAULT NULL,
  `programs_programid` int(11) DEFAULT NULL,
  `users_userid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `reservations`
--

INSERT INTO `reservations` (`reservationid`, `userid`, `programid`, `status`, `gymservices_serviceid`, `programs_programid`, `users_userid`) VALUES
(1, 1, 1, 'confirmed', NULL, NULL, NULL),
(2, 2, 2, 'pending', NULL, NULL, NULL),
(3, 3, 3, 'confirmed', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `trainers`
--

CREATE TABLE `trainers` (
  `trainerid` int(11) NOT NULL,
  `trainername` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `trainers`
--

INSERT INTO `trainers` (`trainerid`, `trainername`) VALUES
(1, 'John Doe'),
(2, 'Charlie Davis');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Άδειασμα δεδομένων του πίνακα `users`
--

INSERT INTO `users` (`userid`, `firstname`, `lastname`, `country`, `city`, `address`, `email`, `username`, `password`, `role`, `status`) VALUES
(1, 'John', 'Doe', 'USA', 'New York', '123 Main St', 'john@example.com', 'johndoe', 'password123', 'Trainer', 'Confirmed'),
(2, 'Jane', 'Smith', 'USA', 'Los Angeles', '456 Elm St', 'jane@example.com', 'janesmith', 'pass123', 'User', 'Confirmed'),
(3, 'Alice', 'Johnson', 'UK', 'London', '789 Oak St', 'alice@example.com', 'alicej', 'test123', 'User', 'Confirmed'),
(4, 'Charlie', 'Davis', 'UK', 'London', '789 Elm St', 'charlie@email.com', 'charlie789', 'password3', 'Trainer', 'Confirmed');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `announcements`
--
ALTER TABLE `announcements`
  ADD PRIMARY KEY (`announcementid`),
  ADD KEY `announcements_users_fk` (`users_userid`);

--
-- Ευρετήρια για πίνακα `gymservices`
--
ALTER TABLE `gymservices`
  ADD PRIMARY KEY (`serviceid`),
  ADD KEY `gymservices_trainers_fk` (`trainers_trainerid`);

--
-- Ευρετήρια για πίνακα `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`programid`);

--
-- Ευρετήρια για πίνακα `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservationid`),
  ADD KEY `reservations_gymservices_fk` (`gymservices_serviceid`),
  ADD KEY `reservations_programs_fk` (`programs_programid`),
  ADD KEY `reservations_users_fk` (`users_userid`);

--
-- Ευρετήρια για πίνακα `trainers`
--
ALTER TABLE `trainers`
  ADD PRIMARY KEY (`trainerid`);

--
-- Ευρετήρια για πίνακα `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `reservations`
--
ALTER TABLE `reservations`
  MODIFY `reservationid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `announcements`
--
ALTER TABLE `announcements`
  ADD CONSTRAINT `announcements_users_fk` FOREIGN KEY (`users_userid`) REFERENCES `users` (`userid`);

--
-- Περιορισμοί για πίνακα `gymservices`
--
ALTER TABLE `gymservices`
  ADD CONSTRAINT `gymservices_trainers_fk` FOREIGN KEY (`trainers_trainerid`) REFERENCES `trainers` (`trainerid`);

--
-- Περιορισμοί για πίνακα `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_gymservices_fk` FOREIGN KEY (`gymservices_serviceid`) REFERENCES `gymservices` (`serviceid`),
  ADD CONSTRAINT `reservations_programs_fk` FOREIGN KEY (`programs_programid`) REFERENCES `programs` (`programid`),
  ADD CONSTRAINT `reservations_users_fk` FOREIGN KEY (`users_userid`) REFERENCES `users` (`userid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
