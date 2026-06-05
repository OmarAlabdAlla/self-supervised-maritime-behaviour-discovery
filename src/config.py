YEARS = [2021]
MONTHS = range(1, 4)

TABLES = [
    f"trajectories_{y}_{m:02d}"
    for y in YEARS
    for m in MONTHS
]

MAX_WORKERS = 8

BASE_QUERY = """
SELECT
    t.ctid                              AS traj_id,
    t.mmsi,
    s.imo,
    s.ship_name,
    dp.path[1]                          AS point_index,
    ST_Y(dp.geom)                       AS lat,
    ST_X(dp.geom)                       AS lon,
    t.timestamps[dp.path[1]]            AS timestamp,
    t.speed_over_ground[dp.path[1]]     AS sog,
    t.navigational_status[dp.path[1]]   AS nav_status,
    t.course_over_ground[dp.path[1]]    AS cog,
    t.heading[dp.path[1]]               AS heading
FROM {table} t
JOIN public.ships s ON t.mmsi = s.mmsi
CROSS JOIN LATERAL ST_DumpPoints(t.coordinates) AS dp
WHERE s.type_of_ship_and_cargo BETWEEN 80 AND 89
"""