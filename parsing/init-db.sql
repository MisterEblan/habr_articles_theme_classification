CREATE DATABASE IF NOT EXISTS habr_data;

USE habr_data;

CREATE TABLE habr_dataset (
    id UInt64,
    title String,
    content String,
    hub LowCardinality(String)
) ENGINE = MergeTree()
ORDER BY id;
