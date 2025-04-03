CREATE TABLE IF NOT EXISTS profiles (
    profile_id bigint,
    created timestamp,
    hair_style text,
    hair_color text,
    eye_color text,
    height_cm integer,
    weight_kg numeric,
    playable_age_min_years numeric,
    playable_age_max_years numeric,
    gender_appearance_list text,
    ethnic_appearance_list text
);

CREATE TABLE IF NOT EXISTS submissions (
    submission_id bigint,
    submission_status text, 
    created timestamp,
    profile_id bigint,
    project_id bigint,
    project_name text, 
    role_id bigint,
    role_name text, 
    submission_media_counts text
);

COPY profiles FROM '/docker-entrypoint-initdb.d/profiles.csv' DELIMITER ',' CSV HEADER;
COPY submissions FROM '/docker-entrypoint-initdb.d/submissions.csv' DELIMITER ',' CSV HEADER; 
