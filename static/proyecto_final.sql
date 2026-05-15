-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-05-2026 a las 13:29:45
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
  `imagen` varchar(255) DEFAULT NULL,
  `tipo_negocio` varchar(20) DEFAULT 'Venta'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inmuebles`
--

INSERT INTO `inmuebles` (`id`, `titulo`, `tipo`, `ubicacion`, `precio`, `estado`, `descripcion`, `imagen`, `tipo_negocio`) VALUES
(4, 'Casa Amoblada en el recreo', 'Casa', 'Monteria', 580000000.00, 'Disponible', 'Hermosa casa ubicada en buen barrio de la ciudad de Monteria, con todas las comodidades!!!', 'inmueble_c026c05065b44660b960f4c698cebce4.jpg', 'Venta'),
(6, 'Apartamento Moderno Urbina', 'Apartamento', 'Sincelejo', 1800000.00, 'Disponible', 'Hermoso apartamento amueblado en buen barrio de la ciudad', 'inmueble_e69de415ccdc480c82830c8dc258ed21.jpg', 'Arriendo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inmueble_multimedia`
--

DROP TABLE IF EXISTS `inmueble_multimedia`;
CREATE TABLE `inmueble_multimedia` (
  `id` int(11) NOT NULL,
  `inmueble_id` int(11) NOT NULL,
  `archivo` varchar(255) NOT NULL,
  `tipo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inmueble_multimedia`
--

INSERT INTO `inmueble_multimedia` (`id`, `inmueble_id`, `archivo`, `tipo`) VALUES
(1, 4, 'inmueble_e1fe98271216475e82e7194228f4cd7c.jpg', 'imagen'),
(2, 4, 'inmueble_ab3743e02d8f49c1a97e4d2abfe651ab.jpg', 'imagen'),
(4, 4, 'inmueble_6b944988f61e4dcc8119cac07118f4b2.mp4', 'video'),
(6, 6, 'inmueble_cb0e450b8b344861a137604e5442d13d.jpg', 'imagen'),
(7, 6, 'inmueble_d25e63c794c440098f5cc109121b3b7f.jpg', 'imagen'),
(8, 6, 'inmueble_ef44668bbbe64850b2a16b20acae62e0.mp4', 'video');

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

--
-- Volcado de datos para la tabla `proyectos_constructora`
--

INSERT INTO `proyectos_constructora` (`id`, `nombre`, `ubicacion`, `estado`, `presupuesto`, `descripcion`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Pavimentacion', NULL, 'Activo', NULL, 'Por la calle', NULL, NULL);

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
(4, 'daniela01', 'scrypt:32768:8:1$vXdgSzGsnDNM8IFV$929d07df61307215b8dbc6fd8ab7b2b6704335c8e544b9280cac9649ad40dda31c1dfb7e1b7f14f54fe540c4c5eb3ea8e62c87d510da9f9f54fb11cf44e8f676', 'daniela@correo.com', 'usuario', 0),
(6, 'lorena02', 'scrypt:32768:8:1$DPcPDKjrgv9iJX8n$a1ef7b22b9a89da03a4a9ec5adad52c6bf5c5bea20d04dfb3571d934ef6898593c48cf7855b6ce05824e404ef7d7f781b045cec1e0b1f39aa30be8efb1e35484', 'lorena@gmail.com', 'usuario', 0),
(7, 'angel04', 'scrypt:32768:8:1$14zr4jVW2RrceOcN$de0261930507753f515bf9880e09cd351943df6b7515109f26d07bc6587f365020150dc8744354427e431af07ee5db0bf727239775e2439fdbf55a7597c613ae', 'angel@correo.com', 'usuario', 0),
(19, 'dinaluna', 'scrypt:32768:8:1$YJVqvRASxQLlrllc$90b977087b79b3977989c3d8059592230fcc666061e0ab8a14dbbc66eef9be15a9fd879f8a0f2e4a672039cb9279a9f2bc2d597d30971ac1d88fde4c93a03959', 'ddelahozluna@gmail.com', 'usuario', 1),
(20, 'Franklin01', 'scrypt:32768:8:1$tylaNYpBEaXXG1oh$67e89c62be992c30b2bff13b77704072a79b76ed2039c8fd1501c347f3ae06bf82724b381f2f57210130b482e13939e8efe44a1b3c27090ae46aa49c70b1d9ae', 'Frankilito06@gmail.com', 'usuario', 1),
(22, 'danielalopez', 'scrypt:32768:8:1$upAu5e6LTfDaZq18$fdb1c9c039b002e989903779798f608317a20f01888df6a09c8f80a86caa99a838c7f0d2939e42d2b1ed97bdc909fab12ab490e051b98bb1ff69f73aa735c972', 'lopezdelahozlaura@gmail.com', 'usuario', 1),
(27, 'Javierlopez', 'scrypt:32768:8:1$ow2HldvkrsWOhyVh$980029b1d0216c9453a2271b923f2d6fe71b07e295a3f26c55a3156e3f67810a3cd4dcbe61b0255fb8bd6dbbae74e9ac8980475af437bf9a52bfc2db8eab42a8', 'lopezvelandiajavier45@gmail.com', 'usuario', 1),
(28, 'FabianMuñoz', 'scrypt:32768:8:1$d7AAkUykHvQ8TClK$49fb10c48a8edb40f5dc975a7e09d6b3a3726f948b18bdd7045704d5edfedb123fefc394fe180d8891fcddb7790dfee129df2b350faba2957adc56d33028a882', 'fabianmunozpadilla2006@gmail.com', 'usuario', 1),
(29, 'CamiLopez', 'scrypt:32768:8:1$VrGhnb7yj7nmrhtR$37a5f27a144414262b2586cf65dc52f66bb60906cf265c68c50a139985da162c02f4851d2ce91e8ba6bb530f19d684ff51fbd51d0a184bde09038067473e92ca', 'camila2001super@gmail.com', 'admin', 1),
(31, 'EileenPeña', 'scrypt:32768:8:1$rpjYlxTb1dsHOu42$c946c47afa29414ca660923570d40805933e08b5cbff23d48d4939b3b3b3faaaf32dd88ecc78318b068a08621b05a6fbdfcf6caa95c5eaca7e26ec54390fc154', 'eileenandreap009@gmail.com', 'admin', 1);

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
-- Indices de la tabla `inmueble_multimedia`
--
ALTER TABLE `inmueble_multimedia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inmueble_id` (`inmueble_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `inmueble_multimedia`
--
ALTER TABLE `inmueble_multimedia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `proyectos_constructora`
--
ALTER TABLE `proyectos_constructora`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inmueble_multimedia`
--
ALTER TABLE `inmueble_multimedia`
  ADD CONSTRAINT `inmueble_multimedia_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
