[
  {
    "essential": true,
    "name": "rent-container",
    "memory": 256,
    "cpu": 128,
    "image": "${image}",
    "environment": [
      { "name": "DB_CONNECTION_URL", "value": "${db_connection_url}" },
      { "name": "LINE_TOKEN", "value": "${line_token}" },
      { "name": "YU_LINE_TOKEN", "value": "${yu_line_token}" }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${awslogs_group}",
        "awslogs-region": "${awslogs_region}",
        "awslogs-stream-prefix": "${awslogs_prefix}"
      }
    }
  }
]