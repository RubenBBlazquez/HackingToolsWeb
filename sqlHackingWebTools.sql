use hacking_tools_web;

#config
SHOW VARIABLES LIKE "%timeout";
SET GLOBAL connect_timeout = 600;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL interactive_timeout = 6000;

drop table IF EXISTS TAGS_FROM_WEB_SCRAPPED CASCADE;
drop table IF EXISTS webs_scrapped CASCADE;


CREATE TABLE IF NOT EXISTS WEBS_SCRAPPED
(
    SCRAP_DATE     datetime     NOT NULL,
    BASE_URL       VARCHAR(255) NOT NULL,
    ENDPOINT       VARCHAR(255) NOT NULL,
    SCRAP_FINISHED BOOLEAN,
    PRIMARY KEY (BASE_URL, ENDPOINT)
);

CREATE TABLE IF NOT EXISTS TAGS_FROM_WEB_SCRAPPED
(
    TAG                   VARCHAR(50)  NOT NULL,
    TAG_INFO              VARCHAR(255) NOT NULL,
    WEB_SCRAPPED          VARCHAR(100) NOT NULL,
    ENDPOINT_WEB_SCRAPPED VARCHAR(255) NOT NULL,
    PRIMARY KEY (TAG, TAG_INFO, WEB_SCRAPPED, ENDPOINT_WEB_SCRAPPED),
    foreign key (WEB_SCRAPPED, ENDPOINT_WEB_SCRAPPED) REFERENCES WEBS_SCRAPPED (BASE_URL, ENDPOINT)
);

CREATE TABLE IF NOT EXISTS LOGS_WEBS_SCRAPPED
(
    LOG_DATE  datetime     NOT NULL,
    BASE_URL  VARCHAR(255) NOT NULL,
    ENDPOINT  VARCHAR(255) NOT NULL,
    LOG_ERROR VARCHAR(255) NOT NULL,
    PRIMARY KEY (BASE_URL, ENDPOINT, LOG_ERROR)
);

SELECT *
FROM webs_scrapped;

SELECT *
FROM TAGS_FROM_WEB_SCRAPPED
WHERE WEB_SCRAPPED LIKE
      'http://riberadeltajo.es/nuevaweb/index.php/component/mailto/?tmpl=component&template=pjo_consultingco&link=617ad3b40305e5422d22938efcc053c0b6976ee1';

SELECT DISTINCT COUNT(*)
FROM TAGS_FROM_WEB_SCRAPPED;

SELECT *
FROM TAGS_FROM_WEB_SCRAPPED;

SELECT * FROM logs_webs_scrapped;

commit;