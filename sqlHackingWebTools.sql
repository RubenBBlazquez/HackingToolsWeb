use hacking_tools_web;

drop table webs_scrapped cascade;

CREATE TABLE WEBS_SCRAPPED(
    SCRAP_DATE datetime NOT NULL,
    WEB_SCRAPPED VARCHAR(100) NOT NULL,
    SCRAP_FINISHED BOOLEAN,
    PRIMARY KEY (WEB_SCRAPPED)
);

CREATE TABLE TAGS_FROM_WEB_SCRAPPED(
	TAG VARCHAR(100),
    WEB_SCRAPPED VARCHAR(100),
	PRIMARY KEY (TAG,WEB_SCRAPPED),
    foreign key (WEB_SCRAPPED) REFERENCES WEBS_SCRAPPED(WEB_SCRAPPED));
    
insert into webs_scrapped values (now(),'buenas',false);
commit;