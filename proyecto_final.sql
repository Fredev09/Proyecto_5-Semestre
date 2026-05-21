-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-05-2026 a las 18:43:26
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
-- Estructura de tabla para la tabla `clientes_constructora`
--

DROP TABLE IF EXISTS `clientes_constructora`;
CREATE TABLE `clientes_constructora` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `tipo` enum('Entidad pública','Empresa privada','Cliente particular') NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(120) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes_constructora`
--

INSERT INTO `clientes_constructora` (`id`, `nombre`, `tipo`, `telefono`, `correo`, `direccion`, `fecha_registro`) VALUES
(1, 'Alcaldía Municipal de San Juan', 'Entidad pública', '3001234567', 'infraestructura@sanjuan.gov', 'Centro administrativo San Juan', '2026-05-15 04:57:06'),
(2, 'Constructora Delta S.A.', 'Empresa privada', '3109876543', 'contacto@deltasa.com', 'Zona industrial Bogotá', '2026-05-15 04:57:06'),
(3, 'Inversiones Rivera', 'Cliente particular', '3204567890', 'rivera@email.com', 'Villa Campestre', '2026-05-15 04:57:06'),
(7, 'Maria', 'Cliente particular', '3345204163', 'dttj@gmail.com', NULL, '2026-05-19 06:17:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes_inmobiliaria`
--

DROP TABLE IF EXISTS `clientes_inmobiliaria`;
CREATE TABLE `clientes_inmobiliaria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `documento` varchar(30) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `tipo_interes` varchar(50) DEFAULT NULL,
  `observacion` text DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes_inmobiliaria`
--

INSERT INTO `clientes_inmobiliaria` (`id`, `nombre`, `documento`, `telefono`, `email`, `direccion`, `tipo_interes`, `observacion`, `fecha_registro`) VALUES
(1, 'Lorena Calle', '1066280317', '3205178088', 'lorena2001@gmail.com', 'Monteria, cordoba', 'Arriendo', 'Interesado en arriendo urbina', '2026-05-15 03:36:42'),
(2, 'Camila', '', '3044025028', '', '', 'Compra', '', '2026-05-20 03:08:45'),
(4, 'Camila', '2564416316546', '3044025028', 'dttj@gmail.com', 'ihbuaowbefo', 'Compra', 'jbcfoawnefo', '2026-05-20 03:12:53'),
(5, 'Camila', '2564416316546', '3044025028', 'dttj@gmail.com', 'ihbuaowbefo', 'Reserva', 'knnnaefkñsc>', '2026-05-20 03:15:53');

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

--
-- Volcado de datos para la tabla `clientes_interesados`
--

INSERT INTO `clientes_interesados` (`id`, `nombre`, `telefono`, `correo`, `servicio`, `mensaje`, `fecha_envio`, `estado`, `fecha_contacto`) VALUES
(1, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Diseño estructural', 'wgfhjoksjhgyugvbjnkm,dcygvhghf', '2026-05-19 03:51:36', 'Contactado', '2026-05-19 04:04:33'),
(2, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'fewfuogefiogbañogbo', '2026-05-19 03:53:05', 'Contactado', '2026-05-19 04:17:19'),
(3, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Consultoría', 'dgiyfgiyvwefgogfwiuegfwiyefiyg', '2026-05-19 03:59:08', 'Prioridad Alta', NULL),
(4, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'gdbuowagbfyie', '2026-05-19 04:04:23', 'Contactado', '2026-05-19 04:14:21'),
(5, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'njrfuwufwbvwulfvlewbvrjl', '2026-05-19 04:14:02', 'Prioridad Alta', NULL),
(6, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Diseño estructural', 'aqsetiyuoggdyurddtfiyliñ', '2026-05-19 04:17:00', 'Prioridad Alta', NULL),
(7, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'eiyeevsiulboevsboesebo', '2026-05-19 04:18:56', 'Prioridad Alta', NULL),
(8, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Consultoría', 'wgyhuyerfiuliobfwi', '2026-05-19 04:27:11', 'Prioridad Alta', NULL),
(9, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'tdiyuiyg', '2026-05-19 04:30:01', 'Prioridad Alta', NULL),
(10, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'bireeruñoerr', '2026-05-19 04:37:13', 'Prioridad Alta', NULL),
(11, 'Camila', '3005059348', 'eileenandreap009@gmail.com', 'Construcción de obras', 'biuoaricbiewuoebwj', '2026-05-19 04:40:27', 'Prioridad Alta', NULL),
(12, 'Camila', '3005059348', 'eileenandreap009@gmail.com', 'Diseño estructural', 'vusjnoeeburbieebih', '2026-05-19 04:41:35', 'Prioridad Alta', NULL),
(13, 'Camila', '3044025028', 'eileenandreap009@gmail.com', 'Diseño estructural', 'brwioñevnjtvjl', '2026-05-19 19:52:00', 'Prioridad Alta', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente_proyecto`
--

DROP TABLE IF EXISTS `cliente_proyecto`;
CREATE TABLE `cliente_proyecto` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `fecha_asignacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente_proyecto`
--

INSERT INTO `cliente_proyecto` (`id`, `cliente_id`, `proyecto_id`, `fecha_asignacion`) VALUES
(11, 1, 2, '2026-05-15 05:18:22'),
(12, 3, 3, '2026-05-15 05:29:02');

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
(4, 'Casa Amoblada en el recreo', 'Casa', 'Monteria', 580000000.00, 'Disponible', 'Acogedora casa familiar con ambiente cálido y hogareño, perfecta para disfrutar momentos en tranquilidad. Sus espacios amplios y bien distribuidos brindan comodidad, con una sala iluminada, cocina funcional, habitaciones confortables y patio ideal para reuniones familiares. Ubicada en un sector residencial tranquilo, cerca de parques, tiendas y colegios, ofreciendo un entorno seguro y agradable para vivir.', 'inmueble_c026c05065b44660b960f4c698cebce4.jpg', 'Venta'),
(6, 'Apartamento Moderno Urbina', 'Apartamento', 'Sincelejo', 1800000.00, 'Disponible', 'Apartamento moderno y acogedor, ideal para familias o parejas que buscan comodidad y buena ubicación. Cuenta con sala-comedor amplia, cocina integral contemporánea, habitaciones ventiladas con excelente iluminación natural y balcón con vista agradable. El conjunto residencial ofrece seguridad, zonas verdes, parqueadero y fácil acceso a centros comerciales, transporte público y áreas recreativas.', 'inmueble_e69de415ccdc480c82830c8dc258ed21.jpg', 'Arriendo'),
(11, 'Casa en excelente recinto', 'Casa', 'Monteria', 470000000.00, 'Disponible', 'Hermosa casa moderna ubicada en una zona residencial tranquila y segura. Cuenta con amplios espacios iluminados naturalmente, sala y comedor independientes, cocina integral equipada, habitaciones cómodas con clósets y acabados de excelente calidad. Dispone de patio, zona de lavandería, parqueadero privado y áreas verdes ideales para compartir en familia. Perfecta para quienes buscan comodidad, elegancia y una excelente ubicación cerca de supermercados, colegios y vías principales.', 'inmueble_908cc19e7dff482588db5abe61fd5206.jpg', 'Venta'),
(12, 'Apartamento en zona urbana', 'Apartamento', 'Monteria', 250000000.00, 'Disponible', 'Elegante apartamento ubicado en una zona urbana de alta valorización, diseñado para brindar confort y estilo. Cuenta con espacios modernos, cocina integral abierta, sala-comedor amplia, habitaciones con excelente iluminación y acabados contemporáneos. Incluye balcón panorámico, zona de lavandería y acceso a áreas comunes como piscina, gimnasio y vigilancia privada las 24 horas. Ideal para quienes desean vivir con comodidad, seguridad y cercanía a centros comerciales, universidades y vías principales.', 'inmueble_a6aae8a18c404827869bc737c164b662.jpg', 'Venta'),
(13, 'Apartamento amoblado alquiler', 'Apartamento', 'Monteria', 900000.00, 'Reservado', 'Apartamento moderno y acogedor disponible para arriendo en excelente ubicación residencial. Cuenta con espacios amplios y bien iluminados, sala-comedor confortable, cocina integral equipada, habitaciones ventiladas con clósets modernos y balcón con vista agradable. El conjunto ofrece seguridad privada, zonas verdes, parqueadero y acceso cercano a supermercados, transporte público, universidades y centros comerciales. Ideal para quienes buscan comodidad, tranquilidad y una excelente calidad de vida.', 'inmueble_ec79ff43da954a0bba02073aef873e0b.jpg', 'Arriendo'),
(14, 'Casa residencial alquiler', 'Casa', 'Monteria', 1950000.00, 'Disponible', 'Hermosa casa familiar disponible para arriendo en un sector residencial tranquilo y seguro. La propiedad cuenta con amplios espacios interiores, sala y comedor independientes, cocina integral funcional, habitaciones cómodas con excelente iluminación natural y patio ideal para compartir en familia. Además, dispone de zona de lavandería, parqueadero privado y áreas verdes cercanas. Su ubicación estratégica permite fácil acceso a colegios, supermercados, parques y vías principales, brindando comodidad y bienestar para toda la familia.', 'inmueble_c0efc6a7d6f04cfca2b5a97afd5f717a.jpg', 'Arriendo');

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
(8, 6, 'inmueble_ef44668bbbe64850b2a16b20acae62e0.mp4', 'video'),
(10, 11, 'inmueble_6819513cda73483fb3cdc6cb8a14323f.jpg', 'imagen'),
(11, 11, 'inmueble_23230e477b794c46ae06f6b3c3e11f51.jpg', 'imagen'),
(12, 11, 'inmueble_8bc864d4a91347a39692ea072cc5b500.jpg', 'imagen'),
(13, 12, 'inmueble_31dd032df33e43f1b38da7e333604e10.jpg', 'imagen'),
(14, 12, 'inmueble_0c3fa66d82884e2699148996a27ad53c.jpg', 'imagen'),
(15, 12, 'inmueble_08ee6d28c0f545c985766e174b24fc6e.jpg', 'imagen'),
(16, 13, 'inmueble_c8c8b7a8d0574a9288ed0072032b3579.jpg', 'imagen'),
(17, 13, 'inmueble_e7a6ed8beb79413a91e171455b93ab90.jpg', 'imagen'),
(18, 13, 'inmueble_f3492ddbceb8478aa114bb24a7bf6ff3.jpg', 'imagen'),
(19, 14, 'inmueble_29869155c42547449ccc17301430af2c.jpg', 'imagen'),
(20, 14, 'inmueble_1cfe779ca2cd452193e510ba9b762a3b.jpg', 'imagen'),
(21, 14, 'inmueble_5c71c6c581c94599ab3f21d922a6bae2.jpg', 'imagen');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos_constructora`
--

DROP TABLE IF EXISTS `proyectos_constructora`;
CREATE TABLE `proyectos_constructora` (
  `id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `tipo_trabajo` varchar(150) NOT NULL,
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

INSERT INTO `proyectos_constructora` (`id`, `nombre`, `tipo_trabajo`, `ubicacion`, `estado`, `presupuesto`, `descripcion`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Primer proyecto', 'Obras civiles', NULL, 'Activo', NULL, 'Descripcion del primer proyecto', NULL, NULL),
(2, 'Pavimentación Calle principal', 'Espacio público', NULL, 'Finalizado', NULL, 'Se pavimentó la calle principal del municipio de San Juan.', NULL, NULL),
(3, 'Proyecto 2', 'Obras civiles', NULL, 'Pendiente', NULL, 'Este es el proyecto 2', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

DROP TABLE IF EXISTS `reservas`;
CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `inmueble_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `fecha_reserva` datetime DEFAULT current_timestamp(),
  `fecha_limite` date DEFAULT NULL,
  `valor_reserva` decimal(12,2) DEFAULT NULL,
  `estado` varchar(30) DEFAULT 'Activa',
  `observacion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `inmueble_id`, `cliente_id`, `fecha_reserva`, `fecha_limite`, `valor_reserva`, `estado`, `observacion`) VALUES
(0, 13, 4, '2026-05-20 20:19:37', '2026-05-18', 20000.00, 'Activa', 'interesada en una reserva');

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
  `email_confirmado` tinyint(4) DEFAULT 0,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password_hash`, `email`, `rol`, `email_confirmado`, `estado`) VALUES
(6, 'Jpipe', 'scrypt:32768:8:1$c5QdQ50ldi7lv36U$e54dbde025e054f1b5f7018c34ec922158c3961375150c6ba274c1b2946793e2e97b103dc281d5382155f0672902ac7bdb9703dcb057771d8518777984598786', 'juanfelipearbu7@gmail.com', 'usuario', 1, 'Activo'),
(19, 'sarith.10', 'scrypt:32768:8:1$RkBzBzVi5ZWExUq8$4d7314f1d09da6cb3a89be3ed3a294eff3eaed596d46bb5ea31dab1fcf639130f747d40f36fa801eb8f8ff7683fdddbf271bfe3748db272221aa53eb7e12fbf4', 'callessarith@gmail.com', 'usuario', 1, 'Activo'),
(20, 'KarolinaGarcia', 'scrypt:32768:8:1$jAZBI6bRXlgtZ8l5$25c1a719ce5b5a27c50d599ba2bd5755bf7b0c3e256a19823cfad68141e5a33d1d373b3761f542567350fc1080db66a35abcbc310c4bfd8a58c2777231437ef3', 'karolinaospina0311@gmail.com', 'usuario', 1, 'Activo'),
(28, 'FabianMuñoz', 'scrypt:32768:8:1$d7AAkUykHvQ8TClK$49fb10c48a8edb40f5dc975a7e09d6b3a3726f948b18bdd7045704d5edfedb123fefc394fe180d8891fcddb7790dfee129df2b350faba2957adc56d33028a882', 'fabianmunozpadilla2006@gmail.com', 'usuario', 1, 'Activo'),
(29, 'CamiLopez', 'scrypt:32768:8:1$VrGhnb7yj7nmrhtR$37a5f27a144414262b2586cf65dc52f66bb60906cf265c68c50a139985da162c02f4851d2ce91e8ba6bb530f19d684ff51fbd51d0a184bde09038067473e92ca', 'camila2001super@gmail.com', 'admin', 1, 'Activo'),
(31, 'EileenPeña', 'scrypt:32768:8:1$rpjYlxTb1dsHOu42$c946c47afa29414ca660923570d40805933e08b5cbff23d48d4939b3b3b3faaaf32dd88ecc78318b068a08621b05a6fbdfcf6caa95c5eaca7e26ec54390fc154', 'eileenandreap009@gmail.com', 'admin', 1, 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

DROP TABLE IF EXISTS `ventas`;
CREATE TABLE `ventas` (
  `id` int(11) NOT NULL,
  `inmueble_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `valor_venta` decimal(15,2) NOT NULL,
  `fecha` date NOT NULL,
  `observacion` text DEFAULT NULL,
  `metodo_pago` varchar(100) DEFAULT NULL,
  `anticipo` decimal(15,2) DEFAULT NULL,
  `saldo` decimal(15,2) DEFAULT NULL,
  `estado_pago` varchar(50) DEFAULT NULL,
  `porcentaje_anticipo` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id`, `inmueble_id`, `cliente_id`, `valor_venta`, `fecha`, `observacion`, `metodo_pago`, `anticipo`, `saldo`, `estado_pago`, `porcentaje_anticipo`) VALUES
(1, 11, 2, 470000000.00, '2026-05-18', 'venta', 'Transferencia', 470000000.00, 0.00, 'Pagado', 55);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes_constructora`
--
ALTER TABLE `clientes_constructora`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `clientes_inmobiliaria`
--
ALTER TABLE `clientes_inmobiliaria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `clientes_interesados`
--
ALTER TABLE `clientes_interesados`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cliente_proyecto`
--
ALTER TABLE `cliente_proyecto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `proyecto_id` (`proyecto_id`);

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
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inmueble_id` (`inmueble_id`),
  ADD KEY `cliente_id` (`cliente_id`);

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
  ADD KEY `inmueble_id` (`inmueble_id`),
  ADD KEY `cliente_id` (`cliente_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes_constructora`
--
ALTER TABLE `clientes_constructora`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `clientes_inmobiliaria`
--
ALTER TABLE `clientes_inmobiliaria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `clientes_interesados`
--
ALTER TABLE `clientes_interesados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `inmuebles`
--
ALTER TABLE `inmuebles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `inmueble_multimedia`
--
ALTER TABLE `inmueble_multimedia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
