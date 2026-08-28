-- Migration: add foto column to users table
ALTER TABLE `users` ADD COLUMN `foto` text;
