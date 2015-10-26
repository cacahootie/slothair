
import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect(dbname='slothair', user='slothair')
except psycopg2.OperationalError:
    time.sleep(3)
    conn = psycopg2.connect(dbname='slothair', user='slothair')

def routes(source):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT distinct(dest_iata), airports.* FROM ROUTES
            JOIN AIRPORTS
                ON routes.dest_id = airports.airport_id
            WHERE 
                source_id = (
                    SELECT airport_id FROM AIRPORTS
                    WHERE iata_faa_id = %(source_iata)s
                )
            ;""",
            {
                'source_iata': source
            }
        )
        destinations = [dict(r) for r in cur]
        return {
            'results':destinations,
            'source_id': source,
            'numresults': len(destinations)
        }

def airport(iata):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT * FROM AIRPORTS
            WHERE IATA_FAA_ID = %(iata)s
            ;""",
            {
                'iata': iata
            }
        )
        return [dict(r) for r in cur][0]

def sources():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT NUM_ROUTES, AIRPORTS.* FROM ROUTES_PER_AIRPORT
            JOIN AIRPORTS
                ON ROUTES_PER_AIRPORT.source_id = AIRPORTS.airport_id
            WHERE NUM_ROUTES > 5
            ;"""
        )
        sources = [dict(r) for r in cur]
        return {
            'results':sources,
            'numresults': len(sources)
        }

def sourcelist():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT AIRPORTS.iata_faa_id FROM ROUTES_PER_AIRPORT
            JOIN AIRPORTS
                ON ROUTES_PER_AIRPORT.source_id = AIRPORTS.airport_id
            WHERE NUM_ROUTES > 5
            ;"""
        )
        return {
            "results":sorted(r[0] for r in cur)
        }

def origin_routes(origin):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT 
                DEST_IATA
            FROM ROUTES 
            WHERE SOURCE_IATA = %s 
            GROUP BY DEST_IATA 
            ORDER BY COUNT(DEST_IATA) DESC
            LIMIT 10
            ;""", (origin,)
        )
        return {
            "results":[r[0] for r in cur]
        }
