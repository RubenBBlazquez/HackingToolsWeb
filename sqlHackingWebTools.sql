use hacking_tools_web;
SET GLOBAL interactive_timeout=60;

drop table TAGS_FROM_WEB_SCRAPPED;
drop table webs_scrapped;


CREATE TABLE WEBS_SCRAPPED(
    SCRAP_DATE datetime NOT NULL,
    WEB_SCRAPPED VARCHAR(100) NOT NULL,
    SCRAP_FINISHED BOOLEAN,
    PRIMARY KEY (WEB_SCRAPPED)
);

CREATE TABLE TAGS_FROM_WEB_SCRAPPED(
	TAG VARCHAR(255),
    TAG_INFO VARCHAR(255),
    WEB_SCRAPPED VARCHAR(255),
	PRIMARY KEY (TAG,TAG_INFO,WEB_SCRAPPED),
    foreign key (WEB_SCRAPPED) REFERENCES WEBS_SCRAPPED(WEB_SCRAPPED));

SELECT count(*) FROM tags_from_web_scrapped;
insert into webs_scrapped values (now(),'buenas',false);
commit;