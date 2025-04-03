INSERT INTO users (user_id, user_name, email, phone_number, age) 
VALUES 
    (1, 'test_user', 'test@example.com', '+1234567890', 25),
    (2, 'john_doe', 'john@example.com', '+1234567891', 30),
    (3, 'jane_smith', 'jane@example.com', '+1234567892', 28),
    (4, 'alice_wonder', 'alice@example.com', '+1234567893', 35)
ON CONFLICT (user_id) DO UPDATE 
SET user_name = EXCLUDED.user_name,
    email = EXCLUDED.email,
    phone_number = EXCLUDED.phone_number,
    age = EXCLUDED.age;
