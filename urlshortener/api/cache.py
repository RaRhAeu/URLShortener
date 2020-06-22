from flask_caching import Cache

config = {'CACHE_TYPE': 'redis',
          'CACHE_REDIS_URL': 'redis://localhost:6379/0'
          }

cache = Cache(config=config)
