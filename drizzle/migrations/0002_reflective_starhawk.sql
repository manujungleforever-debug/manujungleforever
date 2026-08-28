ALTER TABLE `departures` ADD `cupos_minimos` integer DEFAULT 2;--> statement-breakpoint
ALTER TABLE `departures` ADD `cupos_disponibles` integer;--> statement-breakpoint
ALTER TABLE `departures` ADD `notas` text;--> statement-breakpoint
ALTER TABLE `testimonials` ADD `bandera` text;--> statement-breakpoint
ALTER TABLE `users` ADD `foto` text;