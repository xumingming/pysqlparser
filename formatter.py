def format(stmt):
    ret = []
    ret.append("CREATE TABLE")
    if stmt.ifNotExists:
        ret.append(" IF NOT EXISTS")

    ret.append(" ")
    ret.append(stmt.name)
    ret.append(" ")

    ret.append("(\n")
    cnt = 0
    for column in stmt.columns:
        ret.append("\t")
        ret.append(column.name)
        ret.append(" ")
        ret.append(column.type)
        if column.comment != None:
            ret.append(" COMMENT '")
            ret.append(column.comment)
            ret.append("'")

        if cnt < len(stmt.columns) - 1:
            ret.append(",")
        ret.append("\n")
        cnt += 1

    ret.append(")")
    
    print "".join(ret)
