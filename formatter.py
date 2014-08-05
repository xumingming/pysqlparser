def format_columns(ret, columns):
    cnt = 0
    for column in columns:
        ret.append("\t")
        ret.append(column.name)
        ret.append(" ")
        ret.append(column.type)
        if column.comment != None:
            ret.append(" COMMENT '")
            ret.append(column.comment)
            ret.append("'")

        if cnt < len(columns) - 1:
            ret.append(",")
        ret.append("\n")
        cnt += 1

def format_create(stmt):
    ret = []
    ret.append("CREATE TABLE")
    if stmt.if_not_exists:
        ret.append(" IF NOT EXISTS")

    ret.append(" ")
    ret.append(stmt.name)
    ret.append(" ")

    ret.append("(\n")
    format_columns(ret, stmt.columns)
    ret.append(")")

    if stmt.comment:
        ret.append(" COMMENT '")
        ret.append(stmt.comment)
        ret.append("'")

    if stmt.partition_columns and len(stmt.partition_columns) > 0:
        ret.append("\n  PARTITIONED BY (\n")
        format_columns(ret, stmt.partition_columns)
        ret.append(")")

    if stmt.lifecycle != None:
        ret.append("\n LIFECYCLE ")
        ret.append(stmt.lifecycle)
    print "".join(ret)

def format_select(stmt):
    ret = []
    ret.append("SELECT ")
    idx = 0
    for column in stmt.columns:
        if idx > 0:
            ret.append("        ")
        ret.append(column)
        if idx < len(stmt.columns) - 1:
            ret.append(",")

        ret.append("\n")
        idx += 1

    ret.append("FROM ")
    ret.append(stmt.table_name)

    print "".join(ret)

def format(stmt):
    if stmt.type == 'create':
        format_create(stmt)
    elif stmt.type == 'select':
        format_select(stmt)


