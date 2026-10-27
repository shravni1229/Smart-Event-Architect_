-- ==========================================================
-- Smart Event Architect & Recommendation System
-- MySQL Workbench Compatible Database Script
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `smart_event_architect`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `smart_event_architect`;

-- 1. Users Table
DROP TABLE IF EXISTS `event_plans`;
DROP TABLE IF EXISTS `recommendation_logs`;
DROP TABLE IF EXISTS `event_requests`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `phone` VARCHAR(20),
    `password_hash` VARCHAR(255) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'user',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Event Requests Table
CREATE TABLE `event_requests` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `event_title` VARCHAR(150) NOT NULL,
    `event_type` VARCHAR(100) NOT NULL,
    `event_date` VARCHAR(50) NOT NULL,
    `guest_count` INT NOT NULL,
    `budget` DECIMAL(12, 2) NOT NULL,
    `location` VARCHAR(150) NOT NULL,
    `special_notes` TEXT,
    `status` VARCHAR(50) NOT NULL DEFAULT 'Pending',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_requests_user` FOREIGN KEY (`user_id`) 
        REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Event Plans Table
CREATE TABLE `event_plans` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `request_id` INT NOT NULL UNIQUE,
    `admin_id` INT NOT NULL,
    `plan_title` VARCHAR(150) NOT NULL,
    `description` TEXT NOT NULL,
    `services_included` TEXT NOT NULL,
    `cost_breakdown` TEXT NOT NULL,
    `total_estimated_cost` DECIMAL(12, 2) NOT NULL,
    `venue_suggestion` VARCHAR(200),
    `decor_theme` VARCHAR(150),
    `timeline_summary` TEXT,
    `admin_notes` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_plans_request` FOREIGN KEY (`request_id`) 
        REFERENCES `event_requests` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_plans_admin` FOREIGN KEY (`admin_id`) 
        REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Recommendation Logs Table
CREATE TABLE `recommendation_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `request_id` INT NULL,
    `event_type` VARCHAR(100) NOT NULL,
    `budget` DECIMAL(12, 2) NOT NULL,
    `guest_count` INT NOT NULL,
    `budget_tier` VARCHAR(50) NOT NULL,
    `recommended_services_json` TEXT NOT NULL,
    `generated_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_logs_request` FOREIGN KEY (`request_id`) 
        REFERENCES `event_requests` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample Admin User (password is 'admin123' hashed with werkzeug scrypt)
-- Note: Python init_db.py also sets this up automatically in SQLite!
INSERT INTO `users` (`id`, `full_name`, `email`, `phone`, `password_hash`, `role`) VALUES
(1, 'System Administrator', 'admin@eventarchitect.com', '+91 9876543210', 'scrypt:32768:8:1$E6O0zS9YlO9YQ7pZ$9cf5bb4dae5b38f8cf625eb9ad34b35ef584061a9ba460012750e3ad6a86e969d714d59a72d3f7493a15f013d81fa4d76fba0ce9944a1da2cf37bf7c53d4ebc5', 'admin'),
(2, 'Rohit Sharma', 'rohit@example.com', '+91 9123456789', 'scrypt:32768:8:1$E6O0zS9YlO9YQ7pZ$9cf5bb4dae5b38f8cf625eb9ad34b35ef584061a9ba460012750e3ad6a86e969d714d59a72d3f7493a15f013d81fa4d76fba0ce9944a1da2cf37bf7c53d4ebc5', 'user');

-- Sample Event Request
INSERT INTO `event_requests` (`id`, `user_id`, `event_title`, `event_type`, `event_date`, `guest_count`, `budget`, `location`, `special_notes`, `status`) VALUES
(1, 2, 'Grand Silver Jubilee Wedding', 'Wedding Ceremony & Reception', '2026-12-15', 250, 450000.00, 'Pune, Maharashtra', 'Prefer royal purple and blush pink decor with acoustic music during dinner.', 'Plan Created');

-- Sample Plan
INSERT INTO `event_plans` (`id`, `request_id`, `admin_id`, `plan_title`, `description`, `services_included`, `cost_breakdown`, `total_estimated_cost`, `venue_suggestion`, `decor_theme`, `timeline_summary`, `admin_notes`) VALUES
(1, 1, 1, 'Royal Orchid Silver Jubilee Package', 'Comprehensive bespoke plan including multi-cuisine buffet, live floral stage, cinematic drone video, and DJ dance floor.', '["Catering & Buffet Banquet", "Royal Floral Stage & Decor", "Cinematic Photography & Drone", "Sound, DJ & Intelligent Lights", "Event Anchor / Emcee", "Dedicated Event Coordinator"]', '{"Catering & Buffet Banquet": 220000, "Royal Floral Stage & Decor": 85000, "Cinematic Photography & Drone": 60000, "Sound, DJ & Intelligent Lights": 35000, "Event Anchor / Emcee": 15000, "Dedicated Event Coordinator": 20000}', 435000.00, 'The Corinthians Resort / Orchid Grand Lawn, Pune', 'Royal Purple & Soft Pink Orchid with Warm Fairy Lights', '04:00 PM - Guest Arrival & Welcome Drinks\n05:30 PM - Ring Ceremony & Stage Photos\n07:30 PM - Live Music & Sangeet Performance\n08:30 PM - Royal Buffet Dinner Opening\n10:30 PM - Cake Cutting & Vote of Thanks', 'Advance vendor lock-in recommended 3 weeks before event date.');
