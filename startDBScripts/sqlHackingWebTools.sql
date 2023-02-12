CREATE DATABASE IF NOT EXISTS hacking_tools_web;
use hacking_tools_web;

#config
SET GLOBAL connect_timeout = 600;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL interactive_timeout = 6000;
SET GLOBAL wait_timeout = 1000;
drop table IF EXISTS TAGS_FROM_WEB_SCRAPPED CASCADE;
drop table IF EXISTS webs_scrapped CASCADE;
drop table IF EXISTS LOGS_WEBS_SCRAPPED CASCADE;


CREATE TABLE IF NOT EXISTS WebsScrapped
(
    scrapDate      datetime     NOT NULL,
    baseUrl        VARCHAR(255) NOT NULL,
    endpoint       VARCHAR(255) NOT NULL,
    isScrapFinished BOOLEAN,
    PRIMARY KEY (baseUrl, endpoint)
);

CREATE TABLE IF NOT EXISTS TagsFromWebsScrapped
(
    tag                   VARCHAR(50)  NOT NULL,
    tagInfo              VARCHAR(255) NOT NULL,
    webScrapped          VARCHAR(100) NOT NULL,
    endpointWebScrapped VARCHAR(255) NOT NULL,
    PRIMARY KEY (tag, tagInfo, webScrapped, endpointWebScrapped),
    foreign key (webScrapped, endpointWebScrapped) REFERENCES WebsScrapped (baseUrl, endpoint)
);

CREATE TABLE IF NOT EXISTS LogWebsScrapped
(
    logDate   datetime     NOT NULL,
    baseUrl  VARCHAR(255) NOT NULL,
    endpoint  VARCHAR(255) NOT NULL,
    logError VARCHAR(255) NOT NULL,
    PRIMARY KEY (baseUrl, endpoint, logError)
);

DROP TABLE IF EXISTS sniffedEndpoints;
CREATE TABLE IF NOT EXISTS sniffedEndpoints
(
    endpoint VARCHAR(255) NOT NULL,
    information longtext NOT NULL,
    PRIMARY KEY (endpoint)
);

INSERT INTO sniffedEndpoints VALUES ('https://free-nba.p.rapidapi.com/players', '{"https://free-nba.p.rapidapi.com/players": [
    {
        "id": 14,
        "first_name": "Ike",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Anigbogu",
        "position": "C",
        "team": {
            "id": 12,
            "abbreviation": "IND",
            "city": "Indiana",
            "conference": "East",
            "division": "Central",
            "full_name": "Indiana Pacers",
            "name": "Pacers"
        },
        "weight_pounds": 0
    },
    {
        "id": 25,
        "first_name": "Ron",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Baker",
        "position": "G",
        "team": {
            "id": 20,
            "abbreviation": "NYK",
            "city": "New York",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "New York Knicks",
            "name": "Knicks"
        },
        "weight_pounds": 0
    },
    {
        "id": 47,
        "first_name": "Jabari",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Bird",
        "position": "G",
        "team": {
            "id": 2,
            "abbreviation": "BOS",
            "city": "Boston",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "Boston Celtics",
            "name": "Celtics"
        },
        "weight_pounds": 0
    },
    {
        "id": 67,
        "first_name": "MarShon",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Brooks",
        "position": "G",
        "team": {
            "id": 15,
            "abbreviation": "MEM",
            "city": "Memphis",
            "conference": "West",
            "division": "Southwest",
            "full_name": "Memphis Grizzlies",
            "name": "Grizzlies"
        },
        "weight_pounds": 0
    },
    {
        "id": 71,
        "first_name": "Lorenzo",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Brown",
        "position": "G",
        "team": {
            "id": 28,
            "abbreviation": "TOR",
            "city": "Toronto",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "Toronto Raptors",
            "name": "Raptors"
        },
        "weight_pounds": 0
    },
    {
        "id": 90,
        "first_name": "Omri",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Casspi",
        "position": "F",
        "team": {
            "id": 15,
            "abbreviation": "MEM",
            "city": "Memphis",
            "conference": "West",
            "division": "Southwest",
            "full_name": "Memphis Grizzlies",
            "name": "Grizzlies"
        },
        "weight_pounds": 0
    },
    {
        "id": 1,
        "first_name": "Alex",
        "height_feet": 6,
        "height_inches": 6,
        "last_name": "Abrines",
        "position": "G",
        "team": {
            "id": 21,
            "abbreviation": "OKC",
            "city": "Oklahoma City",
            "conference": "West",
            "division": "Northwest",
            "full_name": "Oklahoma City Thunder",
            "name": "Thunder"
        },
        "weight_pounds": 200
    },
    {
        "id": 119,
        "first_name": "Tyler",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Davis",
        "position": "C",
        "team": {
            "id": 21,
            "abbreviation": "OKC",
            "city": "Oklahoma City",
            "conference": "West",
            "division": "Northwest",
            "full_name": "Oklahoma City Thunder",
            "name": "Thunder"
        },
        "weight_pounds": 0
    },
    {
        "id": 149,
        "first_name": "Keenan",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Evans",
        "position": "G",
        "team": {
            "id": 9,
            "abbreviation": "DET",
            "city": "Detroit",
            "conference": "East",
            "division": "Central",
            "full_name": "Detroit Pistons",
            "name": "Pistons"
        },
        "weight_pounds": 0
    },
    {
        "id": 179,
        "first_name": "Marcin",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Gortat",
        "position": "C",
        "team": {
            "id": 13,
            "abbreviation": "LAC",
            "city": "LA",
            "conference": "West",
            "division": "Pacific",
            "full_name": "LA Clippers",
            "name": "Clippers"
        },
        "weight_pounds": 0
    },
    {
        "id": 1593,
        "first_name": "Andrew",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Bogut",
        "position": "F",
        "team": {
            "id": 10,
            "abbreviation": "GSW",
            "city": "Golden State",
            "conference": "West",
            "division": "Pacific",
            "full_name": "Golden State Warriors",
            "name": "Warriors"
        },
        "weight_pounds": 0
    },
    {
        "id": 241,
        "first_name": "Amir",
        "height_feet": 6,
        "height_inches": 9,
        "last_name": "Johnson",
        "position": "C-F",
        "team": {
            "id": 23,
            "abbreviation": "PHI",
            "city": "Philadelphia",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "Philadelphia 76ers",
            "name": "76ers"
        },
        "weight_pounds": 240
    },
    {
        "id": 392,
        "first_name": "Malachi",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Richardson",
        "position": "G",
        "team": {
            "id": 29,
            "abbreviation": "UTA",
            "city": "Utah",
            "conference": "West",
            "division": "Northwest",
            "full_name": "Utah Jazz",
            "name": "Jazz"
        },
        "weight_pounds": 0
    },
    {
        "id": 281,
        "first_name": "Zach",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Lofton",
        "position": "G",
        "team": {
            "id": 9,
            "abbreviation": "DET",
            "city": "Detroit",
            "conference": "East",
            "division": "Central",
            "full_name": "Detroit Pistons",
            "name": "Pistons"
        },
        "weight_pounds": 0
    },
    {
        "id": 263,
        "first_name": "Kosta",
        "height_feet": 7,
        "height_inches": 0,
        "last_name": "Koufos",
        "position": "C",
        "team": {
            "id": 26,
            "abbreviation": "SAC",
            "city": "Sacramento",
            "conference": "West",
            "division": "Pacific",
            "full_name": "Sacramento Kings",
            "name": "Kings"
        },
        "weight_pounds": 245
    },
    {
        "id": 382,
        "first_name": "Billy",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Preston",
        "position": "F",
        "team": {
            "id": 6,
            "abbreviation": "CLE",
            "city": "Cleveland",
            "conference": "East",
            "division": "Central",
            "full_name": "Cleveland Cavaliers",
            "name": "Cavaliers"
        },
        "weight_pounds": 0
    },
    {
        "id": 384,
        "first_name": "Zhou",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Qi",
        "position": "F-C",
        "team": {
            "id": 11,
            "abbreviation": "HOU",
            "city": "Houston",
            "conference": "West",
            "division": "Southwest",
            "full_name": "Houston Rockets",
            "name": "Rockets"
        },
        "weight_pounds": 0
    },
    {
        "id": 388,
        "first_name": "Zach",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Randolph",
        "position": "F",
        "team": {
            "id": 26,
            "abbreviation": "SAC",
            "city": "Sacramento",
            "conference": "West",
            "division": "Pacific",
            "full_name": "Sacramento Kings",
            "name": "Kings"
        },
        "weight_pounds": 0
    },
    {
        "id": 430,
        "first_name": "DJ",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Stephens",
        "position": "G-F",
        "team": {
            "id": 15,
            "abbreviation": "MEM",
            "city": "Memphis",
            "conference": "West",
            "division": "Southwest",
            "full_name": "Memphis Grizzlies",
            "name": "Grizzlies"
        },
        "weight_pounds": 0
    },
    {
        "id": 437,
        "first_name": "Milos",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Teodosic",
        "position": "G",
        "team": {
            "id": 13,
            "abbreviation": "LAC",
            "city": "LA",
            "conference": "West",
            "division": "Pacific",
            "full_name": "LA Clippers",
            "name": "Clippers"
        },
        "weight_pounds": 0
    },
    {
        "id": 448,
        "first_name": "Gary",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Trent Jr.",
        "position": "G",
        "team": {
            "id": 25,
            "abbreviation": "POR",
            "city": "Portland",
            "conference": "West",
            "division": "Northwest",
            "full_name": "Portland Trail Blazers",
            "name": "Trail Blazers"
        },
        "weight_pounds": 0
    },
    {
        "id": 494,
        "first_name": "Michael",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Smith",
        "position": "",
        "team": {
            "id": 2,
            "abbreviation": "BOS",
            "city": "Boston",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "Boston Celtics",
            "name": "Celtics"
        },
        "weight_pounds": 0
    },
    {
        "id": 495,
        "first_name": "John",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Morton",
        "position": "",
        "team": {
            "id": 6,
            "abbreviation": "CLE",
            "city": "Cleveland",
            "conference": "East",
            "division": "Central",
            "full_name": "Cleveland Cavaliers",
            "name": "Cavaliers"
        },
        "weight_pounds": 0
    },
    {
        "id": 496,
        "first_name": "Howard",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Wright",
        "position": "",
        "team": {
            "id": 1,
            "abbreviation": "ATL",
            "city": "Atlanta",
            "conference": "East",
            "division": "Southeast",
            "full_name": "Atlanta Hawks",
            "name": "Hawks"
        },
        "weight_pounds": 0
    },
    {
        "id": 497,
        "first_name": "Michael",
        "height_feet": 0,
        "height_inches": 0,
        "last_name": "Ansley",
        "position": "",
        "team": {
            "id": 22,
            "abbreviation": "ORL",
            "city": "Orlando",
            "conference": "East",
            "division": "Southeast",
            "full_name": "Orlando Magic",
            "name": "Magic"
        },
        "weight_pounds": 0
    }
]}');

commit;