CREATE TABLE IF NOT EXISTS profile_attributes (
    profile_id bigint,
    created timestamp,
    hair_style text,
    hair_color text,
    eye_color text,
    height_cm integer,
    height_imperial text,
    weight_kg numeric,
    weight_lbs numeric,
    playable_age_min_years numeric,
    playable_age_max_years numeric,
    gender_appearance_list text,
    ethnic_appearance_list text,
    piercing_note text,
    tattoo text,
    skill_list text,
    willingness_list text,
    pet_list text
);

COPY profile_attributes FROM '/docker-entrypoint-initdb.d/data.csv' DELIMITER ',' CSV HEADER;





