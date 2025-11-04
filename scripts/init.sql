CREATE TABLE IF NOT EXISTS books (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  rating INT NOT NULL,
  comment TEXT
);

INSERT INTO books (title, author, description) VALUES
('The Pragmatic Programmer', 'Andrew Hunt; David Thomas', 'Classic software craftsmanship book'),
('Clean Code', 'Robert C. Martin', 'A Handbook of Agile Software Craftsmanship'),
('Designing Data-Intensive Applications', 'Martin Kleppmann', 'Big-picture data systems design')
ON CONFLICT DO NOTHING;
