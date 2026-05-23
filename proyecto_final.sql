
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `proyecto_final` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `proyecto_final`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `ventas`;
DROP TABLE IF EXISTS `reservas`;
DROP TABLE IF EXISTS `inmueble_multimedia`;
DROP TABLE IF EXISTS `inmuebles`;
DROP TABLE IF EXISTS `cliente_proyecto`;
DROP TABLE IF EXISTS `clientes_constructora`;
DROP TABLE IF EXISTS `clientes_inmobiliaria`;
DROP TABLE IF EXISTS `clientes_interesados`;
DROP TABLE IF EXISTS `proyectos_constructora`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `compras`;

SET FOREIGN_KEY_CHECKS = 1;

-- --------------------------------------------------------
-- Tabla clientes_constructora
-- --------------------------------------------------------

CREATE TABLE `clientes_constructora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `tipo` enum('Entidad pública','Empresa privada','Cliente particular') NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(120) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `clientes_constructora` (`id`, `nombre`, `tipo`, `telefono`, `correo`, `direccion`, `fecha_registro`) VALUES
(1, 'Alcaldía Municipal de San Juan', 'Entidad pública', '3001234567', 'infraestructura@sanjuan.gov', 'Centro administrativo San Juan', '2026-05-15 04:57:06'),
(2, 'Constructora Delta S.A.', 'Empresa privada', '3109876543', 'contacto@deltasa.com', 'Zona industrial Bogotá', '2026-05-15 04:57:06'),
(3, 'Inversiones Rivera', 'Cliente particular', '3204567890', 'rivera@email.com', 'Villa Campestre', '2026-05-15 04:57:06');

ALTER TABLE `clientes_constructora` AUTO_INCREMENT = 7;

-- --------------------------------------------------------
-- Tabla clientes_inmobiliaria
-- --------------------------------------------------------

CREATE TABLE `clientes_inmobiliaria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `documento` varchar(30) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `tipo_interes` varchar(50) DEFAULT NULL,
  `observacion` text DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `clientes_inmobiliaria` (`id`, `nombre`, `documento`, `telefono`, `email`, `direccion`, `tipo_interes`, `observacion`, `fecha_registro`) VALUES
(1, 'Lorena Calle', '1066280317', '3205178088', 'lorena2001@gmail.com', 'Monteria, cordoba', 'Arriendo', 'Interesado en arriendo urbina', '2026-05-15 03:36:42');

ALTER TABLE `clientes_inmobiliaria` AUTO_INCREMENT = 2;

-- --------------------------------------------------------
-- Tabla clientes_interesados
-- --------------------------------------------------------

CREATE TABLE `clientes_interesados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `servicio` varchar(100) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha_envio` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` enum('Pendiente','Contactado','Prioridad Alta') DEFAULT 'Pendiente',
  `fecha_contacto` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `clientes_interesados` (`id`, `nombre`, `telefono`, `correo`, `servicio`, `mensaje`, `fecha_envio`, `estado`, `fecha_contacto`) VALUES
(1, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Diseño estructural', 'wgfhjoksjhgyugvbjnkm,dcygvhghf', '2026-05-19 08:51:36', 'Contactado', '2026-05-19 09:04:33'),
(2, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'fewfuogefiogbañogbo', '2026-05-19 08:53:05', 'Contactado', '2026-05-19 09:17:19'),
(3, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Consultoría', 'dgiyfgiyvwefgogfwiuegfwiyefiyg', '2026-05-19 08:59:08', 'Pendiente', NULL),
(4, 'Eileen', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'gdbuowagbfyie', '2026-05-19 09:04:23', 'Contactado', '2026-05-19 09:14:21'),
(5, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'njrfuwufwbvwulfvlewbvrjl', '2026-05-19 09:14:02', 'Pendiente', NULL),
(6, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Diseño estructural', 'aqsetiyuoggdyurddtfiyliñ', '2026-05-19 09:17:00', 'Pendiente', NULL),
(7, 'Camila', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'eiyeevsiulboevsboesebo', '2026-05-19 09:18:56', 'Pendiente', NULL),
(8, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Consultoría', 'wgyhuyerfiuliobfwi', '2026-05-19 09:27:11', 'Pendiente', NULL),
(9, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Construcción de obras', 'tdiyuiyg', '2026-05-19 09:30:01', 'Pendiente', NULL),
(10, 'Sarith', '3345204163', 'eileenandreap009@gmail.com', 'Interventoría', 'bireeruñoerr', '2026-05-19 09:37:13', 'Pendiente', NULL),
(11, 'Camila', '3005059348', 'eileenandreap009@gmail.com', 'Construcción de obras', 'biuoaricbiewuoebwj', '2026-05-19 09:40:27', 'Pendiente', NULL),
(12, 'Camila', '3005059348', 'eileenandreap009@gmail.com', 'Diseño estructural', 'vusjnoeeburbieebih', '2026-05-19 09:41:35', 'Pendiente', NULL);

ALTER TABLE `clientes_interesados` AUTO_INCREMENT = 13;

-- --------------------------------------------------------
-- Tabla proyectos_constructora
-- --------------------------------------------------------

CREATE TABLE `proyectos_constructora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `tipo_trabajo` varchar(150) NOT NULL,
  `ubicacion` varchar(150) DEFAULT NULL,
  `estado` varchar(50) DEFAULT 'Activo',
  `presupuesto` decimal(15,2) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `proyectos_constructora` (`id`, `nombre`, `tipo_trabajo`, `ubicacion`, `estado`, `presupuesto`, `descripcion`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Primer proyecto', 'Obras civiles', NULL, 'Activo', NULL, 'Descripcion del primer proyecto', NULL, NULL),
(2, 'Pavimentación Calle principal', 'Espacio público', NULL, 'Finalizado', NULL, 'Se pavimentó la calle principal del municipio de San Juan.', NULL, NULL),
(3, 'Proyecto 2', 'Obras civiles', NULL, 'Pendiente', NULL, 'Este es el proyecto 2', NULL, NULL);

ALTER TABLE `proyectos_constructora` AUTO_INCREMENT = 4;

-- --------------------------------------------------------
-- Tabla cliente_proyecto
-- --------------------------------------------------------

CREATE TABLE `cliente_proyecto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `fecha_asignacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `proyecto_id` (`proyecto_id`),
  CONSTRAINT `cliente_proyecto_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_constructora` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cliente_proyecto_ibfk_2` FOREIGN KEY (`proyecto_id`) REFERENCES `proyectos_constructora` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `cliente_proyecto` (`id`, `cliente_id`, `proyecto_id`, `fecha_asignacion`) VALUES
(11, 1, 2, '2026-05-15 05:18:22'),
(12, 3, 3, '2026-05-15 05:29:02');

ALTER TABLE `cliente_proyecto` AUTO_INCREMENT = 13;

-- --------------------------------------------------------
-- Tabla inmuebles
-- --------------------------------------------------------

CREATE TABLE `inmuebles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `ubicacion` varchar(150) NOT NULL,
  `precio` decimal(15,2) NOT NULL,
  `estado` varchar(30) NOT NULL DEFAULT 'Disponible',
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `tipo_negocio` varchar(20) DEFAULT 'Venta',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `inmuebles` (`id`, `titulo`, `tipo`, `ubicacion`, `precio`, `estado`, `descripcion`, `imagen`, `tipo_negocio`) VALUES
(4, 'Casa Amoblada en el recreo', 'Casa', 'Monteria', 580000000.00, 'Disponible', 'Hermosa casa ubicada en buen barrio de la ciudad de Monteria, con todas las comodidades!!!', 'inmueble_c026c05065b44660b960f4c698cebce4.jpg', 'Venta'),
(6, 'Apartamento Moderno Urbina', 'Apartamento', 'Sincelejo', 1800000.00, 'Disponible', 'Hermoso apartamento amueblado en buen barrio de la ciudad', 'inmueble_e69de415ccdc480c82830c8dc258ed21.jpg', 'Arriendo');

ALTER TABLE `inmuebles` AUTO_INCREMENT = 7;

-- --------------------------------------------------------
-- Tabla inmueble_multimedia
-- --------------------------------------------------------

CREATE TABLE `inmueble_multimedia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inmueble_id` int(11) NOT NULL,
  `archivo` varchar(255) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inmueble_id` (`inmueble_id`),
  CONSTRAINT `inmueble_multimedia_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `inmueble_multimedia` (`id`, `inmueble_id`, `archivo`, `tipo`) VALUES
(1, 4, 'inmueble_e1fe98271216475e82e7194228f4cd7c.jpg', 'imagen'),
(2, 4, 'inmueble_ab3743e02d8f49c1a97e4d2abfe651ab.jpg', 'imagen'),
(4, 4, 'inmueble_6b944988f61e4dcc8119cac07118f4b2.mp4', 'video'),
(6, 6, 'inmueble_cb0e450b8b344861a137604e5442d13d.jpg', 'imagen'),
(7, 6, 'inmueble_d25e63c794c440098f5cc109121b3b7f.jpg', 'imagen'),
(8, 6, 'inmueble_ef44668bbbe64850b2a16b20acae62e0.mp4', 'video');

ALTER TABLE `inmueble_multimedia` AUTO_INCREMENT = 9;

-- --------------------------------------------------------
-- Tabla reservas
-- --------------------------------------------------------

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inmueble_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `fecha_reserva` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_limite` date NOT NULL,
  `valor_reserva` decimal(15,2) NOT NULL DEFAULT 0.00,
  `estado` enum('Activa','Cancelada','Finalizada') NOT NULL DEFAULT 'Activa',
  `observacion` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `inmueble_id` (`inmueble_id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`),
  CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_inmobiliaria` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `reservas` AUTO_INCREMENT = 1;

-- --------------------------------------------------------
-- Tabla usuarios
-- --------------------------------------------------------

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'usuario',
  `email_confirmado` tinyint(4) DEFAULT 0,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usuarios` (`id`, `username`, `password_hash`, `email`, `rol`, `email_confirmado`, `activo`) VALUES
(6, 'Jpipe', 'scrypt:32768:8:1$c5QdQ50ldi7lv36U$e54dbde025e054f1b5f7018c34ec922158c3961375150c6ba274c1b2946793e2e97b103dc281d5382155f0672902ac7bdb9703dcb057771d8518777984598786', 'juanfelipearbu7@gmail.com', 'usuario', 1, 1),
(19, 'sarith.10', 'scrypt:32768:8:1$RkBzBzVi5ZWExUq8$4d7314f1d09da6cb3a89be3ed3a294eff3eaed596d46bb5ea31dab1fcf639130f747d40f36fa801eb8f8ff7683fdddbf271bfe3748db272221aa53eb7e12fbf4', 'callessarith@gmail.com', 'usuario', 1, 1),
(20, 'KarolinaGarcia', 'scrypt:32768:8:1$jAZBI6bRXlgtZ8l5$25c1a719ce5b5a27c50d599ba2bd5755bf7b0c3e256a19823cfad68141e5a33d1d373b3761f542567350fc1080db66a35abcbc310c4bfd8a58c2777231437ef3', 'karolinaospina0311@gmail.com', 'usuario', 1, 1),
(28, 'FabianMuñoz', 'scrypt:32768:8:1$d7AAkUykHvQ8TClK$49fb10c48a8edb40f5dc975a7e09d6b3a3726f948b18bdd7045704d5edfedb123fefc394fe180d8891fcddb7790dfee129df2b350faba2957adc56d33028a882', 'fabianmunozpadilla2006@gmail.com', 'usuario', 1, 1),
(29, 'CamiLopez', 'scrypt:32768:8:1$VrGhnb7yj7nmrhtR$37a5f27a144414262b2586cf65dc52f66bb60906cf265c68c50a139985da162c02f4851d2ce91e8ba6bb530f19d684ff51fbd51d0a184bde09038067473e92ca', 'camila2001super@gmail.com', 'admin', 1, 1),
(31, 'EileenPeña', 'scrypt:32768:8:1$rpjYlxTb1dsHOu42$c946c47afa29414ca660923570d40805933e08b5cbff23d48d4939b3b3b3faaaf32dd88ecc78318b068a08621b05a6fbdfcf6caa95c5eaca7e26ec54390fc154', 'eileenandreap009@gmail.com', 'admin', 1, 1);

ALTER TABLE `usuarios` AUTO_INCREMENT = 32;

-- --------------------------------------------------------
-- Tabla compras
-- --------------------------------------------------------

CREATE TABLE `compras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concepto` varchar(150) NOT NULL,
  `proveedor` varchar(100) DEFAULT NULL,
  `valor` decimal(15,2) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- Tabla ventas
-- --------------------------------------------------------

CREATE TABLE `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inmueble_id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `valor_venta` decimal(15,2) NOT NULL,
  `fecha` date NOT NULL,
  `observacion` text DEFAULT NULL,
  `metodo_pago` varchar(100) DEFAULT NULL,
  `porcentaje_anticipo` int(11) DEFAULT 0,
  `anticipo` decimal(15,2) DEFAULT 0.00,
  `saldo` decimal(15,2) DEFAULT 0.00,
  `estado_pago` varchar(50) DEFAULT 'Pendiente',
  PRIMARY KEY (`id`),
  KEY `inmueble_id` (`inmueble_id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`inmueble_id`) REFERENCES `inmuebles` (`id`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_inmobiliaria` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `ventas` (`id`, `inmueble_id`, `cliente_id`, `valor_venta`, `fecha`, `observacion`, `metodo_pago`, `porcentaje_anticipo`, `anticipo`, `saldo`, `estado_pago`) VALUES
(1, 4, 1, 580000000.00, '2026-05-02', 'Registrado con pago incial y proceso de venta ', NULL, 100, 580000000.00, 0.00, 'Pagado');

ALTER TABLE `ventas` AUTO_INCREMENT = 2;

COMMIT;