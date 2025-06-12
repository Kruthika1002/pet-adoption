USE petadoption;
DROP TABLE pets;
CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    category VARCHAR(255),  -- Replacing role with category
    age INT ,
    rescue_date DATE NOT NULL,
    adoption_status VARCHAR(10)NOT NULL);
    
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

    INSERT INTO users (username, password) VALUES ('admin', 'admin123');
    
    SHOW TABLES;