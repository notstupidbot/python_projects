from robots import  JsonConfig

cli_config_path="config/myconfig.json"
cli_config=JsonConfig(path=cli_config_path)

browser_cache_dir_setting_key,default_browser_cache_dir=["browser_cache_dir","storage/browser_cache"]
cookie_setting_key,default_cookie_path=["cookie_path","storage/cookies/cookies.json"]
db_setting_key,default_db_path=["db_path","storage/database/my.db"]

db_path = cli_config.get(db_setting_key)
cookie_path = cli_config.get(cookie_setting_key)
browser_cache_dir = cli_config.get(browser_cache_dir_setting_key)

if not browser_cache_dir:
    browser_cache_dir = default_browser_cache_dir
    cli_config.set(browser_cache_dir_setting_key, browser_cache_dir)
if not db_path:
    db_path = default_db_path
    cli_config.set(db_setting_key, db_path)
if not cookie_path:
    cookie_path = default_cookie_path
    cli_config.set(cookie_setting_key, cookie_path)
