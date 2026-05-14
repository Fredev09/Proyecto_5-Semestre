-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-05-2026 a las 21:27:55
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
-- Estructura de tabla para la tabla `clientes_interesados`
--

DROP TABLE IF EXISTS `clientes_interesados`;
CREATE TABLE `clientes_interesados` (
  `id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `servicio` varchar(100) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha_envio` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('Pendiente','Contactado','Prioridad Alta') DEFAULT 'Pendiente',
  `fecha_contacto` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

DROP TABLE IF EXISTS `compras`;
CREATE TABLE `compras` (
  `id` int(11) NOT NULL,
  `concepto` varchar(150) NOT NULL,
  `proveedor` varchar(100) DEFAULT NULL,
  `valor` decimal(15,2) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inmuebles`
--

DROP TABLE IF EXISTS `inmuebles`;
CREATE TABLE `inmuebles` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `ubicacion` varchar(150) NOT NULL,
  `precio` decimal(15,2) NOT NULL,
  `estado` varchar(30) NOT NULL DEFAULT 'Disponible',
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos_constructora`
--

DROP TABLE IF EXISTS `proyectos_constructora`;
CREATE TABLE `proyectos_constructora` (
  `id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `ubicacion` varchar(150) DEFAULT NULL,
  `estado` varchar(50) DEFAULT 'Activo',
  `presupuesto` decimal(15,2) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(28, 'FabianMuñoz', 'scrypt:32768:8:1$d7AAkUykHvQ8TClK$49fb10c48a8edb40f5dc975a7e09d6b3a3726f948b18bdd7045704d5edfedb123fefc394fe180d8891fcddb7790dfee129df2b350faba2957adc56d33028a882', 'fabianmunozpadilla2006@gmail.com', 'usuario', 1),
(29, 'CamiLopez', 'scrypt:32768:8:1$2z3mtqVLXXEgMwxo$c6541e6a515775bb1bda9baaf482df6047287afcee8e2c1aa425cc5ab21cc215e674894447bf3002c04beeeee01cb2793f7c0a98c4c4a0e1f2c1056e91bc1f49', 'camila2001super@gmail.com', 'admin', 1),
(31, 'EileenPeña', 'scrypt:32768:8:1$rpjYlxTb1dsHOu42$c946c47afa29414ca660923570d40805933e08b5cbff23d48d4939b3b3b3faaaf32dd88ecc78318b068a08621b05a6fbdfcf6caa95c5eaca7e26ec54390fc154', 'eileenandreap009@gmail.com', 'admin', 1),
(32, 'KarolinaGarcia', 'scrypt:32768:8:1$qoiqxCxpgqn00gAi$8d332882fb01cc5a22db6151334ae77a6534ddc4ac2975d22e533f20ec3e0622891b42611905d78cc4aaf2c903811b26ec92f6930115bcd0335fba44bcfd3b60', 'karolinaospina0311@gmail.com', 'usuario', 1),
(33, 'Ivan03', 'scrypt:32768:8:1$WLiSyTFHm6ZCvs3g$ba227778ee8d62cfdfe10c5eb3d2d2406217ac425bfad24b696979a0f407cb8ee27648c3dca1d831b205049a23a92a8e9c076faec4b8673ff93ed4d3c5a54e96', 'idaso2008@gmail.com', 'usuario', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

DROP TABLE IF EXISTS `ventas`;
CREATE TABLE `ventas` (
  `id` int(11) NOT NULL,
  `inmueble_id` int(11) NOT NULL,
  `cliente` varchar(100) NOT NULL,
  `documento` varchar(50) DEFAULT NULL,
  `valor_venta` decimal(15,2) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes_interesados`
--
ALTER TABLE `clientes_interesados`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inmuebles`
--
ALTER TABLE `inmuebles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `proyectos_constructora`
--
ALTER TABLE `proyectos_constructora`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inmueble_id` (`inmueble_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes_interesados`
--
ALTER TABLE `clientes_interesados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `compras`
--
ALTER TABLE `compras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inmuebles`
--
ALTER TABLE `inmuebles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyectos_constructora`
--
ALTER TABLE `proyectos_constructora`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
