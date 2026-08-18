CREATE TABLE `blog_posts` (
	`id` text PRIMARY KEY NOT NULL,
	`slug` text NOT NULL,
	`titulo` text NOT NULL,
	`autor` text DEFAULT 'Manu Jungle Forever',
	`fecha` text NOT NULL,
	`categoria` text,
	`extracto` text,
	`contenido` text NOT NULL,
	`imagen_hero` text,
	`estado` text DEFAULT 'publicado' NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `blog_posts_slug_unique` ON `blog_posts` (`slug`);--> statement-breakpoint
CREATE TABLE `departures` (
	`id` text PRIMARY KEY NOT NULL,
	`tour_id` text,
	`tour_nombre` text NOT NULL,
	`fecha_salida` text NOT NULL,
	`fecha_retorno` text,
	`cupos_totales` integer DEFAULT 8 NOT NULL,
	`precio` real NOT NULL,
	`moneda` text DEFAULT 'USD' NOT NULL,
	`guia_asignado` text,
	`estado` text DEFAULT 'confirmada' NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text,
	FOREIGN KEY (`tour_id`) REFERENCES `tours`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `passengers` (
	`id` text PRIMARY KEY NOT NULL,
	`departure_id` text NOT NULL,
	`nombre_completo` text NOT NULL,
	`nacionalidad` text,
	`fecha_nacimiento` text,
	`pasaporte` text,
	`whatsapp` text,
	`email` text,
	`restricciones_dieteticas` text,
	`condiciones_medicas` text,
	`costo` real DEFAULT 0,
	`monto_pagado` real DEFAULT 0,
	`saldo_pendiente` real DEFAULT 0,
	`estado_pago` text DEFAULT 'pendiente' NOT NULL,
	`foto` text,
	`created_at` text NOT NULL,
	`updated_at` text,
	FOREIGN KEY (`departure_id`) REFERENCES `departures`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `reclamos` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`codigo_reclamo` text NOT NULL,
	`fecha` text NOT NULL,
	`nombres` text NOT NULL,
	`documento` text NOT NULL,
	`domicilio` text NOT NULL,
	`telefono` text NOT NULL,
	`correo` text NOT NULL,
	`apoderado` text,
	`bien_tipo` text,
	`bien_monto` text,
	`bien_descripcion` text,
	`tipo` text NOT NULL,
	`detalle` text NOT NULL,
	`pedido` text NOT NULL,
	`estado` text DEFAULT 'Pendiente',
	`detalle_respuesta` text,
	`fecha_respuesta` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `reclamos_codigo_reclamo_unique` ON `reclamos` (`codigo_reclamo`);--> statement-breakpoint
CREATE TABLE `testimonials` (
	`id` text PRIMARY KEY NOT NULL,
	`nombre` text NOT NULL,
	`pais` text,
	`tour_nombre` text,
	`rating` integer DEFAULT 5,
	`comentario` text NOT NULL,
	`foto` text,
	`fecha` text NOT NULL,
	`estado` text DEFAULT 'publicado' NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `tours` (
	`id` text PRIMARY KEY NOT NULL,
	`slug` text NOT NULL,
	`nombre` text NOT NULL,
	`categoria` text NOT NULL,
	`estado` text DEFAULT 'activo' NOT NULL,
	`duracion_dias` integer NOT NULL,
	`duracion_noches` integer NOT NULL,
	`precio_desde` real NOT NULL,
	`moneda` text DEFAULT 'USD' NOT NULL,
	`capacidad_min` integer DEFAULT 1,
	`capacidad_max` integer DEFAULT 8,
	`dificultad` text,
	`temporada` text,
	`descripcion_corta` text,
	`descripcion_larga` text,
	`imagen_hero` text,
	`imagen_alt` text,
	`galeria_json` text,
	`itinerario_json` text,
	`transporte_json` text,
	`created_at` text NOT NULL,
	`updated_at` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `tours_slug_unique` ON `tours` (`slug`);--> statement-breakpoint
CREATE TABLE `users` (
	`id` text PRIMARY KEY NOT NULL,
	`email` text NOT NULL,
	`password_hash` text NOT NULL,
	`name` text NOT NULL,
	`role` text DEFAULT 'admin' NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `users_email_unique` ON `users` (`email`);