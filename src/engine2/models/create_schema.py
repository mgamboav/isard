# ~ import asyncio
# ~ from asyncpgsa import pg

# ~ async def connect():
	# ~ await pg.init(
		# ~ host="isard-database",
		# ~ port=5432,
		# ~ database="engine",
		# ~ user="isardvdi",
		# ~ # loop=loop,
		# ~ password="isardvdi",
		# ~ min_size=5,
		# ~ max_size=10
	# ~ )

# ~ connect()
# ~ query="CREATE TABLE Persons (PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255)"
# ~ with pg.query(query) as cursor:
    # ~ async for row in cursor:
        # ~ a = row.col_name
