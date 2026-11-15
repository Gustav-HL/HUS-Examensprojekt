BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Chunks" (
	"chunk_id"	TEXT,
	"doc_id"	TEXT,
	"chunk_index"	INTEGER,
	"text_content"	TEXT,
	PRIMARY KEY("chunk_id"),
	FOREIGN KEY("doc_id") REFERENCES "Documents"("doc_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Documents" (
	"doc_id"	TEXT,
	"title"	TEXT,
	"file_path"	TEXT,
	"sharepoint_url"	TEXT,
	"content_hash"	TEXT,
	"last_modified"	TEXT,
	"last_analyzed"	TEXT,
	"file_type"	TEXT,
	"keywords"	TEXT,
	"metadata"	TEXT,
	"entities"	TEXT,
	PRIMARY KEY("doc_id")
);
CREATE TABLE IF NOT EXISTS "Vectors" (
	"chunk_id"	TEXT,
	"vector"	BLOB,
	"dimensions"	INTEGER,
	PRIMARY KEY("chunk_id"),
	FOREIGN KEY("chunk_id") REFERENCES "Chunks"("chunk_id") ON DELETE CASCADE
);
COMMIT;
