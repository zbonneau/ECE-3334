# Communication system

## Connection sequence
1. server listens for connection
2. server accepts connection
3. Server sends connection message
4. Client sends ID
5. Server connects client object with house ID
6. If client has been configured, send config values
7. If client has been configured, server gets config values
   1. Server updates HouseConfig Table with config values
8. Else, client requests config values
   1. Server gets config values from house table, sends to client
   2. Client accepts or rejects configs

## loop
9. If server receives data, update data Table
10. If server receives config Request, send config values
11. If User sets config values, update table, send to client
    1. If client rejects, inform user, cancel table update 

## Communication formats

### client: send_data
    send_data DATETIME: 2024-10-20 12:15, HOUSEID: 1, TEMP: 23.45, HUMIDITY: 34.23, MOISTURE: 24.54
    DATETIME: str
    HOUSEID: int
    TEMP: float
    HUMIDITY: float
    MOISTURE: float

### client: send_config
    send_config HOUSEID: 1, TEMPMIN: 12.0, TEMPMAX: 33.2, HUMDMIN: 30.5, HUMDMAX: 57.8, MOISTMIN: 14.5, MOISTMAX: 43.5
    HOUSEID: int
    TEMPMIN: float
    TEMPMAX: float
    HUMDMIN: float
    HUMDMAX: float
    MOISTMIN: float
    MOISTMAX: float

### client: accept_config
    accept_config HOUSEID: 1

### client: reject_config
    reject_config HOUSEID: 1

### server: get_ID
    get_ID

### client: send_ID
    send_ID HOUSEID: 1

### client: request_ID
    request_ID HOUSEID: 0

### client: request_config
    request_config HOUSEID: 1

### server: set_config
    set_config HOUSEID: 1, TEMPMIN: 12.0, TEMPMAX: 33.2, HUMDMIN: 30.5, HUMDMAX: 57.8, MOISTMIN: 14.5, MOISTMAX: 43.5
    HOUSEID: int
    TEMPMIN: float
    TEMPMAX: float
    HUMDMIN: float
    HUMDMAX: float
    MOISTMIN: float
    MOISTMAX: float