------- Fragments data -------
CREATE TABLE IF NOT EXISTS users_fragments (
    id                      SERIAL PRIMARY KEY,
    user_id                 TEXT NOT NULL,
    user_username           TEXT NOT NULL,
    milestone_id            INT NOT NULL,
    fragment_id             INT NOT NULL,
    fragment_name           TEXT NOT NULL,
    fragment_description    TEXT NOT NULL,
    fragment_default_text   TEXT NOT NULL,
    fragment_hardness       FLOAT NOT NULL,
    text                    TEXT NOT NULL,
    UNIQUE (milestone_id, fragment_id)
);
