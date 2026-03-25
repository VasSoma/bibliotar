CREATE TABLE users_home_address (
    user_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, address_id),
    CONSTRAINT fk_uha_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_uha_address
        FOREIGN KEY (address_id)
        REFERENCES home_address(address_id)
        ON DELETE CASCADE
);
