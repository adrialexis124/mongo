#!/bin/bash

DELAY=25

mongosh <<EOF
var config = {
    "_id": "iabdrs",
    "version": 1,
    "members": [
        {
            "_id": 4,
            "host": "mongo4:27017",
            "priority": 2
        },
        {
            "_id": 5,
            "host": "mongo5:27017",
            "priority": 1
        },
        {
            "_id": 6,
            "host": "mongo6:27017",
            "priority": 1
        }
    ]
};
rs.initiate(config, { force: true });
EOF

echo "****** Esperando ${DELAY} segundos a que se apliquen la configuración del conjunto de réplicas ******"

sleep $DELAY

mongosh < /scripts/init.js
