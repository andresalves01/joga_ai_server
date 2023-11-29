SELECT
    "court".id,
    "court".name,
    "court".player_qty,
    "court".description,
    "court".modality,
    "court".rating,
    "court".address_id,
    "address".id,
    "address".street,
    "address".number,
    "address".zipcode,
    "address".complement,
    "address".block,
    "address".city_district,
    "address".city,
    "address".state,
    "address".country,
    "address".latitude,
    "address".longitude,
    slots.id,
    slots.reservation_datetime,
    slots.price,
    slots.cancellation_datetime,
    slots.user_id,
    photos.id,
    photos.url,
    amenities.id,
    amenities.name,
    amenities.icon_url

FROM
    joga_ai."court"

INNER JOIN joga_ai.address ON court.address_id = address.id

INNER JOIN (
    SELECT
        "slot".court_id,
        string_agg("slot".reservation_datetime::text, ';') AS reservation_datetime,
        string_agg("slot".price::text, ';') AS price,
        string_agg("slot".cancellation_datetime::text, ';') AS cancellation_datetime,
        string_agg("slot".user_id::text, ';') AS user_id,
        string_agg("slot".id::text, ';') AS id
    FROM
        joga_ai."slot"
    WHERE
        slot.user_id IS NULL
        AND slot.cancellation_datetime IS NULL
    GROUP BY 
        court_id
) AS slots ON "court".id = slots.court_id

LEFT JOIN (
    SELECT
        "photo".court_id,
        string_agg("photo".url::text, ';') AS url,
        string_agg("photo".id::text, ';') AS id
    FROM
        joga_ai."photo"
    GROUP BY court_id
) AS photos ON "court".id = photos.court_id

LEFT JOIN (
    SELECT 
        "court_has_amenity".court_id,
        string_agg("amenity".id::text, ';') as id,
        string_agg("amenity".name::text, ';') as name,
        string_agg("amenity".icon_url::text, ';') as icon_url
    FROM
        joga_ai."court_has_amenity"
    INNER JOIN
        joga_ai."amenity" ON "court_has_amenity".amenity_id = "amenity".id
    GROUP BY
        "court_has_amenity".court_id
) AS amenities ON "court".id = amenities.court_id

WHERE
    court.address_id IS NOT NULL