import redis 

redis_client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True) #creating a connecting to your redis server

#port via redis listens default 6379

#db = 0 , it has 0-15 apps for keeping data separate 

#redis decoded converts evertytihing into bytes internally first 

redis_client.set("test","working")
print(redis_client.get("test"))


# store test value working with key test and print value for a key from the redis client using get