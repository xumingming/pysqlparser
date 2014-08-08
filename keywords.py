from token1 import *

keywords = {}
keywords["ADD"] = ADD
keywords["ALL"] = ALL
keywords["ALTER"] = ALTER
keywords["AND"] = AND
keywords["AS"] = AS
keywords["ASC"] = ASC
keywords["BETWEEN"] = BETWEEN
keywords["BIGINT"] = BIGINT
keywords["BOOLEAN"] = BOOLEAN
keywords["BY"] = BY
keywords["CASE"] = CASE
keywords["CAST"] = CAST
keywords["COLUMN"] = COLUMN
keywords["COMMENT"] = COMMENT
keywords["CREATE"] = CREATE
keywords["DATETIME"] = DATETIME
keywords["DESC"] = DESC
keywords["DISTINCT"] = DISTINCT
keywords["DISTRIBUTE"] = DISTRIBUTE
keywords["DOUBLE"] = DOUBLE
keywords["DROP"] = DROP
keywords["ELSE"] = ELSE
keywords["EXISTS"] = EXISTS
keywords["FALSE"] = FALSE
keywords["FROM"] = FROM
keywords["FULL"] = FULL
keywords["GROUP"] = GROUP
keywords["HAVING"] = HAVING
keywords["IF"] = IF
keywords["IN"] = IN
keywords["INT"] = INT
keywords["INNER"] = INNER
keywords["INSERT"] = INSERT
keywords["INTO"] = INTO
keywords["IS"] = IS
keywords["JOIN"] = JOIN
keywords["LEFT"] = LEFT
keywords["LIFECYCLE"] = LIFECYCLE
keywords["LIKE"] = LIKE
keywords["LIMIT"] = LIMIT
keywords["MAPJOIN"] = MAPJOIN
keywords["NOT"] = NOT
keywords["NULL"] = NULL
keywords["ON"] = ON
keywords["OR"] = OR
keywords["ORDER"] = ORDER
keywords["OUTER"] = OUTER
keywords["OVERWRITE"] = OVERWRITE
keywords["PARTITION"] = PARTITION
keywords["PARTITIONED"] = PARTITIONED
keywords["RENAME"] = RENAME
keywords["REPLACE"] = REPLACE
keywords["RIGHT"] = RIGHT
keywords["RLIKE"] = RLIKE
keywords["SELECT"] = SELECT
keywords["SORT"] = SORT
keywords["STRING"] = STRING
keywords["TABLE"] = TABLE
keywords["THEN"] = THEN
keywords["TOUCH"] = TOUCH
keywords["TRUE"] = TRUE
keywords["UNION"] = UNION
keywords["WHEN"] = WHEN
keywords["WHERE"] = WHERE


def get_keyword(keyword):
    """
    """
    return keywords.get(keyword)
    
def is_keyword(keyword):
    return get_keyword(keyword)