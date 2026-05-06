-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-04-2026 a las 18:16:44
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_final`
--
CREATE DATABASE IF NOT EXISTS `proyecto_final` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `proyecto_final`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'usuario',
  `email_confirmado` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password_hash`, `email`, `rol`, `email_confirmado`) VALUES
(1, 'camilopez', 'scrypt:32768:8:1$NfxDWPADlIzpXbs7$e297429ad38bfb7e0ee0f6f7ee3c2e511e8573de4bf752254714c1d40d8b413ffbc3710f96b4ee656dd05c976413e90a33912d127b250ab57181f2f415c6349d', 'camila2001super@gmail.com', 'usuario', 0),
(2, 'camilopez03', 'scrypt:32768:8:1$K8AMuI9AJIy0PlHf$7cd767de006398273d5a8071ae564df7446ced3b7f8db88e14ddd7b158df764316ef1fc56531ce853501a98d2ca5a588d73c430fa2e82b8d290074f35df3261e', 'ddelahozluna@gmail.com', 'usuario', 1),
(3, 'andrea03', 'scrypt:32768:8:1$K4Gl3jPbtC6rjh9J$ccc2069f484a102c845cdc5a9c12329b9a6a22133fafab6f6b41c16685df84d74e12867ca91cd5da7794843264151ecec8775717802c052341b08c1da85d27ca', 'camila@correo.com', 'usuario', 0),
(4, 'daniela01', 'scrypt:32768:8:1$vXdgSzGsnDNM8IFV$929d07df61307215b8dbc6fd8ab7b2b6704335c8e544b9280cac9649ad40dda31c1dfb7e1b7f14f54fe540c4c5eb3ea8e62c87d510da9f9f54fb11cf44e8f676', 'daniela@correo.com', 'usuario', 0),
(5, 'eileen01', 'scrypt:32768:8:1$OHsRKQpMgt6WSgr8$b7e514cc37f64ec6888d028d9b48bf723cf7774d9389046eeefc11ebe341a4e5ab1ce295f304871432866c6fbad06b2023c797b12ec4a31d97fda9a45730c365', 'eileen@correo.com', 'admin', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
