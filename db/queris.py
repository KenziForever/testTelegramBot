CREATE_TABLE_PRODUCT = """
CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    category VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    product_id VARCHAR(255),
    photo TEXT
    )
"""

INSERT_PRODUCT_QUERY = """
    INSERT INTO product (name, category, size, price,product_id, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""