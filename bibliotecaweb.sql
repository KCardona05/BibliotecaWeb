-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-04-2025 a las 22:58:58
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bibliotecaweb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `lib_titulo` varchar(100) DEFAULT NULL,
  `lib_autor` varchar(100) DEFAULT NULL,
  `lib_disponible` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `lib_titulo`, `lib_autor`, `lib_disponible`) VALUES
(1, 'prueba', 'yo', 0),
(2, 'preuba2', 'yo2', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id_prestamo` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `libro_id` int(11) DEFAULT NULL,
  `estado` enum('pendiente','aprobado','rechazado') DEFAULT 'pendiente',
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamos`
--

INSERT INTO `prestamos` (`id_prestamo`, `usuario_id`, `libro_id`, `estado`, `fecha`) VALUES
(10, 11, 1, 'pendiente', '2025-04-22 15:43:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usu_nombre` varchar(100) DEFAULT NULL,
  `usu_correo` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `usu_rol` varchar(255) DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usu_nombre`, `usu_correo`, `password`, `usu_rol`) VALUES
(5, 'fernando2', '123456', 'hhh@gmail.com', 'administrador'),
(6, 'fernando vargas', '123456@gmail.com', 'pbkdf2:sha256:1000000$n54oGcKNTc5R8t7i$2f771765dedb49bf9fdaca21d75d5cc69144961157e446e113d2d645079d85fc', 'administrador'),
(7, 'karen', 'karen@gmail.com', '123456', 'administrador'),
(10, 'brian fernando vargas tapias', 'PRUEBA1@GMAIL.COM', 'pbkdf2:sha256:1000000$tUzBlbg9ryLsLXzG$15e7fc1d4f0f6e33c8f34133c8b0c336be5f79d4a2d1fa3a83d9b32e8ae57468', 'administrador'),
(11, 'prueba usuario', 'usuarioprueba@gmail.com', 'pbkdf2:sha256:1000000$1g0hyIqb06GLsENN$401741473eacf7c34ea3058fa52ae8c92c398acdd8a2b28c309436435a1be184', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id_prestamo`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `libro_id` (`libro_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usu_correo` (`usu_correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id_prestamo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id_libro`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
