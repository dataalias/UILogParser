CREATE TABLE IF NOT EXISTS UbiquitiRouterLogs (
    id bigint
    , host varchar(50)
    , ip varchar(16)
    , fac varchar(50)
    , prio  varchar(50)
    , llevel  varchar(50)
    , tag  varchar(50)
    , utcsec bigint
    , r_utcsec bigint
    , tzoffset varchar(10)
    , ldate varchar(10)
    , ltime varchar(10)
    , prog  varchar(50)
    , msg varchar(2000)
)