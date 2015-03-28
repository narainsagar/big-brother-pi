class Config(object):
    BASE_ADDR     = "http://localhost:9000"
    NODE_ADDR     = BASE_ADDR + "/api/records/all"
    LOG_ADDR      = BASE_ADDR + "/api/records/getlog"
    MAX_MSG_LEN   = ""
    SEND_DURATION = 3600